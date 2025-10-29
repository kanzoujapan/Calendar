from . import db
from sqlalchemy.sql import func

class GoogleToken(db.Model):
    __tablename__ = "google_tokens"

    user_id = db.Column(db.String(64), primary_key=True)
    google_sub = db.Column(db.String(64), unique=True, nullable=False)
    refresh_token = db.Column(db.Text, nullable=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    # MySQL の CURRENT_TIMESTAMP / ON UPDATE CURRENT_TIMESTAMP を優先
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )