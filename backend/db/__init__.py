#このファイルはappとdbの紐付けを行う　
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy() # SQLAlchemyはSQLとflaskのORMを果たしている

def init_db(app):
    uri = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST','127.0.0.1')}:{os.getenv('DB_PORT','3306')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)