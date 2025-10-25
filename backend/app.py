from flask import Flask
from flask_cors import CORS
from calendar_api import api_bp

app = Flask(__name__)
CORS(app)  # 開発では Vite proxy があるので必須ではないが、本番を見据えて許可
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(port=3000, debug=True)