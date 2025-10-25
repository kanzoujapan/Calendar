from flask import jsonify, Blueprint, request, redirect
import urllib.parse
from datetime import datetime
import zoneinfo
import os 
from dotenv import load_dotenv

load_dotenv()

api_bp = Blueprint("api", __name__, url_prefix="/api")

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

@api_bp.post("/plan")
def plan():
    data = request.get_json(silent=True) or {}
    date = data.get("date")
    if not date:
        return jsonify({"message": "date is required"}), 400

    jst = zoneinfo.ZoneInfo("Asia/Tokyo")
    ts  = datetime.now(jst).strftime("%H:%M")
    return jsonify({"date": date, "timestamp": ts})