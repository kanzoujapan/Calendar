from datetime import datetime, timedelta, timezone
from flask import current_app, redirect, request, jsonify

from . import api_bp
from ..services.google_oauth import (
    build_auth_url,
    exchange_code_for_tokens,
    save_refresh_token,
    set_session_tokens,
)

# oauth同意画面にredirect redirectは同意画面のエンドポイントを返して同時にGETを発火させるイメージ
@api_bp.get("/auth")
def auth():
    return redirect(build_auth_url())

@api_bp.get("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "missing_code"}), 400

    access, refresh, expires_in, user_id = exchange_code_for_tokens(code, state)
    exp_utc = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    set_session_tokens(user_id, access, exp_utc)
    save_refresh_token(user_id, refresh, exp_utc)

    origin = current_app.config["FRONTEND_ORIGIN"]
    return redirect(f"{origin}/?isSignedIn=true")