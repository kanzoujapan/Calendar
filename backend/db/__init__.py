from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    # 1) DATABASE_URL があれば優先（例: mysql+pymysql://...）
    uri = os.getenv("DATABASE_URL")
    if not uri:
        # 2) もしくは個別項目から組み立て（MySQL を使うなら PyMySQL が必要）
        if os.getenv("DB_USER"):
            uri = (
                f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST','127.0.0.1')}:{os.getenv('DB_PORT','3306')}/{os.getenv('DB_NAME')}"
            )
        else:
            # 3) 何もなければまず SQLite で動かす
            uri = "sqlite:///data.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)