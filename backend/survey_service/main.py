# main.py
from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.generate import generate_bp

def key_by_token_or_ip():
    """
        Build a **rate-limit key** for the current request.

    Priority:
      1) If the client sends an Authorization header with a Bearer token,
         use the token value so each client gets an independent bucket.
      2) Otherwise, fall back to the caller's remote IP address.

    Returns:
        str: The identifier used by Flask-Limiter to bucket requests.
    """
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return get_remote_address()

def create_app():
    
    """
   Application factory. Creates and configures a Flask instance.

    What it sets up:
        - CORS: Allows your local frontend during development.
        - Rate limiting: 3 requests/minute per token/IP (configurable).
        - Basic security headers: Sent on every response.
        - Blueprints: Registers API routes (e.g., /api/surveys/generate).

    Returns:
        Flask: A configured Flask application. 

   
    """
    
    
    app = Flask(__name__)
    # Allow your local frontend during dev; tighten later
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 20 requests per minute per token/IP
    Limiter(
        key_func=key_by_token_or_ip,
        default_limits=["3 per minute"],
        storage_uri="memory://",  # good enough for local;
        app=app,
    )

    # Optional: basic security headers
    @app.after_request
    def add_security_headers(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp
    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {"status": "healthy", "service": "boundari-backend"}, 200


    app.register_blueprint(generate_bp)  # your existing routes
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)

