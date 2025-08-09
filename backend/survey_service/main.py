# main.py
# Entry point for running the survey_service Flask app

from flask import Flask
from app.config.config import Config
from flask_cors import CORS
from app.routes.generate import generate_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register the survey generation route
    app.register_blueprint(generate_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
