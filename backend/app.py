from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from db import init_db, db

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)  # 開発では Vite proxy があるので必須ではないが、本番を見据えて許可

init_db(app)

from calendar_api import api_bp
app.register_blueprint(api_bp)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=3000, debug=True)