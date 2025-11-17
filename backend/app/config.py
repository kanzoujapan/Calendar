# setting variable

import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-insecure")
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_DOMAIN = "localhost"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google OAuth2
    OAUTH_URL = os.getenv("OAUTH_URL")
    TOKEN_URL = os.getenv("TOKEN_URL")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_USER_INFO_URL = os.getenv("GOOGLE_USER_INFO_URL")
    SCOPE = os.getenv("SCOPE", "openid profile email")

    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

    # networking & token handling
    ACCESS_TOKEN_BUFFER = int(os.getenv("ACCESS_TOKEN_BUFFER", "30"))  # 秒
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))          # 秒