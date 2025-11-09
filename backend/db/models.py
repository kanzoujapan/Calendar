from . import db
from datetime import datetime

class GoogleToken(db.Model):
    __tablename__ = "google_tokens"

    # ここを主キーにする（get(user_id) が効くように）
    google_sub   = db.Column(db.String(255), primary_key=True)
    refresh_token = db.Column(db.String(2048))
    expires_at    = db.Column(db.DateTime)

    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)