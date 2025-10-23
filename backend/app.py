from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import zoneinfo

app = Flask(__name__)
CORS(app)  # 開発では Vite proxy があるので必須ではないが、本番を見据えて許可

@app.post("/api/plan")
def plan():
    data = request.get_json(silent=True) or {}
    date = data.get("date")
    if not date:
        return jsonify({"message": "date is required"}), 400

    jst = zoneinfo.ZoneInfo("Asia/Tokyo")
    ts  = datetime.now(jst).strftime("%H:%M")
    return jsonify({"date": date, "timestamp": ts})

if __name__ == "__main__":
    app.run(port=3000, debug=True)