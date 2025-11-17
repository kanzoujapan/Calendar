from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict
import secrets


from flask import current_app, session
from db import db
from db.models import GoogleToken
from ..services.http_utils import fetch_json, send_json
from ..utils.timeutil import utc_now

SESSION_KEY_ACCESS = "google_access_token"
SESSION_KEY_ACCESS_EXP = "google_access_token_exp"
SESSION_KEY_USER = "google_user_id"
SESSION_KEY_STATE = "oauth_state"


def new_state() -> str:
    """CSRF 対策の state を生成・セッション格納"""
    state = secrets.token_urlsafe(32)
    session[SESSION_KEY_STATE] = state
    current_app.logger.debug("Generated state: %s", state)
    return state

def validate_state(state_from_query: Optional[str]) -> None:
    expected = session.pop(SESSION_KEY_STATE, None)
    current_app.logger.debug("Validating state. received=%s expected=%s", state_from_query, expected)
    if not expected or state_from_query != expected:
        raise RuntimeError("Invalid OAuth state.")

def build_auth_url() -> str:
    # oauth同意画面url作成　クライアントidを送る
    base = current_app.config["OAUTH_URL"]
    params = {
        "response_type": "code",
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "redirect_uri": current_app.config["GOOGLE_REDIRECT_URI"],
        "scope": current_app.config["SCOPE"],
        "access_type": "offline",
        "include_granted_scopes": "true",
        "state": new_state()
    }
    from urllib.parse import urlencode
    return f"{base}?{urlencode(params)}"

def exchange_code_for_tokens(code: str, state: Optional[str]) -> Tuple[str, Optional[str], int, str]:
    validate_state(state)

    payload = {
        "code": code,
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": current_app.config["GOOGLE_REDIRECT_URI"],
        "grant_type": "authorization_code",
    }
    response = send_json(current_app.config["TOKEN_URL"], payload)

    access = response.get("access_token")
    refresh = response.get("refresh_token")  
    expires_in = int(response.get("expires_in", 3600))

    if not access:
        raise RuntimeError("Token exchange failed: no access_token.")

    userinfo = fetch_json(
        current_app.config["GOOGLE_USER_INFO_URL"],
        {"Authorization": f"Bearer {access}"},
    )
    sub = userinfo.get("sub")
    if not sub:
        raise RuntimeError("Token exchange failed: userinfo missing 'sub'.")

    return access, refresh, expires_in, sub

def save_refresh_token(user_id: str, refresh_token: Optional[str], exp_utc: datetime) -> None:
    rec = db.session.get(GoogleToken, user_id)
    if rec is None:
        rec = GoogleToken(google_sub=user_id, refresh_token=refresh_token, expires_at=exp_utc)
        db.session.add(rec)
    else:
        if refresh_token:
            rec.refresh_token = refresh_token
        rec.expires_at = exp_utc
    db.session.commit()

def set_session_tokens(user_id: str, access_token: str, exp_utc: datetime) -> None:
    session[SESSION_KEY_USER] = user_id
    session[SESSION_KEY_ACCESS] = access_token
    session[SESSION_KEY_ACCESS_EXP] = exp_utc.isoformat()

def refresh_access_token() -> str:
    user_id = session.get(SESSION_KEY_USER)
    if not user_id:
        raise RuntimeError("Not authenticated.")

    rec = db.session.get(GoogleToken, user_id)
    if not rec or not rec.refresh_token:
        raise RuntimeError("No refresh_token. Re-consent required.")

    data = {
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
        "refresh_token": rec.refresh_token,
        "grant_type": "refresh_token",
    }
    response = send_json(current_app.config["TOKEN_URL"], data)

    access = response.get("access_token")
    expires_in = int(response.get("expires_in", 3600))
    if not access or not expires_in:
        raise RuntimeError("Failed to refresh access token.")

    exp_utc = utc_now() + timedelta(seconds=expires_in)
    set_session_tokens(user_id, access, exp_utc)
    rec.expires_at = exp_utc
    db.session.commit()
    return access

def get_valid_access_token() -> str:
    token: Optional[str] = session.get(SESSION_KEY_ACCESS)
    exp_iso: Optional[str] = session.get(SESSION_KEY_ACCESS_EXP)

    if token and exp_iso:
        try:
            exp_dt = datetime.fromisoformat(exp_iso)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        except Exception:
            exp_dt = utc_now() - timedelta(seconds=1)

        buffer = current_app.config["ACCESS_TOKEN_BUFFER"]
        if exp_dt > utc_now() + timedelta(seconds=buffer):
            return token

    return refresh_access_token()