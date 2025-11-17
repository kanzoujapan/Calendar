from . import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class GoogleToken(db.Model):
    __tablename__ = "google_tokens"
    google_sub = db.Column(db.String(128), primary_key=True)
    refresh_token = db.Column(db.String(1024), nullable=True)
    expires_at = db.Column(TIMESTAMP(timezone=True), nullable=True)