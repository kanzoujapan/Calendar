# app factory 

from flask import Flask, jsonify
from dotenv import load_dotenv
from .config import Config
from db import db

def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config())
    

    db.init_app(app)

    # Blueprints
    with app.app_context():
        from .blueprints import api_bp
        app.register_blueprint(api_bp)

    
    @app.errorhandler(RuntimeError)
    def handle_runtime(e):
        return jsonify({"error": str(e)}), 400

    return app