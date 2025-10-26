from flask import jsonify, Blueprint, request, redirect
import urllib.parse
from datetime import datetime
import zoneinfo
import os 
from dotenv import load_dotenv

load_dotenv()

api_bp = Blueprint("api", __name__, url_prefix="/api")

# from front to GET /api/auth 
# redirect to Endpoint to initiate Google Oauth2 authentication
@api_bp.get("/auth")
def auth():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "https://www.googleapis.com/auth/calendar.readonly", #将来的には.eventsにしてイベントの書き込みなども可能にするかもしれない
        "access_type": "offline",
        "include_granted_scopes": "true",
        "state": "xyz123"  # 任意のCSRF対策用トークン
    }

    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@api_bp.get("/oauth2callback")
def authentication_callback():
    token_url = "https://oauth2.googleapis.com/token"
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


