from flask import jsonify, request # これは外部からのリクエストを受け取るためのオブジェクト
from . import api_bp
from ..utils.timeutil import jst_now

@api_bp.post("/plan")
def plan():
    data = request.get_json(silent=True) or {}
    date = data.get("date")
    if not date:
        return jsonify({"message": "date is required"}), 400

    ts = jst_now().strftime("%H:%M")
    return jsonify({"date": date, "timestamp": ts})