from flask import jsonify, Blueprint, request, redirect, session, current_app
import requests, urllib.parse, os
from datetime import datetime, timedelta, timezone
from db import db
from db.models import GoogleToken
import zoneinfo 
from dotenv import load_dotenv

load_dotenv()

api_bp = Blueprint("api", __name__, url_prefix="/api")




def refresh_access_token(user_id):
    token_url = os.getenv("TOKEN_URL")
    user_info = GoogleToken.query.get(user_id)
    if not user_info or not user_info.refresh_token:
        raise RuntimeError("No refresh_token. Re-consent needed.")

    refresh_token_data = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": user_info.refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data = refresh_token_data, timeout = 15)
    response.raise_for_status()
    payload = response.json()

    new_access_token = payload.get("access_token")
    expires_in = payload.get("expires_in", 3600)

    if not new_access_token or not expires_in:
        raise RuntimeError("Failed to refresh access token.")
    
    exp_utc = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    session["google_access_token"] = new_access_token
    session["google_access_token_exp"] = exp_utc.isoformat()


    user_info.expires_at = exp_utc
    db.session.commit()

    return new_access_token


def get_valid_access_token():
    user_id = session.get("google_user_id")
    if not user_id:
        raise RuntimeError("Not authenticated user.")
    
    token = session.get("google_access_token")
    exp_iso = session.get("google_access_token_exp")

    if token and exp_iso:
        try:
            exp_dt = datetime.fromisoformat(exp_iso)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        except Exception:
            exp_dt = datetime.now(timezone.utc) - timedelta(seconds=1)

        if exp_dt > datetime.now(timezone.utc) + timedelta(seconds=30):
            return token
        

    return refresh_access_token(user_id)


    

    






# from front to GET /api/auth 
# redirect to Endpoint to initiate Google Oauth2 authentication
@api_bp.get("/auth")
def auth():
    base_url = os.getenv("OAUTH_URL")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scope = os.getenv("SCOPE")
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope, #将来的には.eventsにしてイベントの書き込みなども可能にするかもしれない
        "access_type": "offline",
        "include_granted_scopes": "true",
        "state": "xyz123"  # 任意のCSRF対策用トークン
    }

    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@api_bp.get("/oauth2callback")
def authentication_callback():
    token_url = os.getenv("TOKEN_URL")
    code = request.args.get("code")
    state = request.args.get("state")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    sendData = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "state": state,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data = sendData)
    token_response_data = response.json()
    access_token = token_response_data.get("access_token")
    refresh_token = token_response_data.get("refresh_token")
    expires_in = token_response_data.get("expires_in", 3600)

    if not access_token:
        current_app.logger.error(f"No access_token in token response: {token_response_data}")
        return jsonify({"error": "token_exchange_failed"}), 400

    user_google_info_url = os.getenv("GOOGLE_USER_INFO_URL")
    user_google_info = requests.get(user_google_info_url, headers = {"Authorization": f"Bearer {access_token}"}   
    ).json()


    user_id = user_google_info.get("sub")

    if not user_id:
        current_app.logger.error(f"userinfo missing 'sub': {user_google_info}")
        return jsonify({"error": "missing_sub"}), 400

    exp_utc = datetime.now(timezone.utc) + timedelta(seconds= expires_in)
    session["google_access_token"] = access_token
    session["google_user_id"] = user_id
    session["google_access_token_exp"] = exp_utc.isoformat()

    user_info = db.session.get(GoogleToken, user_id)
    if user_info is None:
        user_info = GoogleToken(google_sub=user_id, refresh_token=refresh_token, expires_at=exp_utc)
        db.session.add(user_info)

    else:
        if refresh_token:
            user_info.refresh_token = refresh_token
        user_info.expires_at = exp_utc
    db.session.commit()

    # ...existing code...
    return redirect(os.getenv("FRONTEND_ORIGIN") + "/")


    
    

    

    

    





# from front to POST /api/plan
# receive date and return it with currrent timestamp in JST
# 受け取った日付をgoogle calendar api に問い合わせる、そしてその日のイベントを取得する
@api_bp.post("/plan")
def plan():
    data = request.get_json(silent=True) or {}
    date = data.get("date")
    if not date:
        return jsonify({"message": "date is required"}), 400

    jst = zoneinfo.ZoneInfo("Asia/Tokyo")
    ts  = datetime.now(jst).strftime("%H:%M")
    return jsonify({"date": date, "timestamp": ts})


