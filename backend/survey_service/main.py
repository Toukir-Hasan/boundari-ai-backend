# main.py
from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.generate import generate_bp

def key_by_token_or_ip():
    """
    Identify the caller for rate limiting.
    Prefer the bearer token so each client gets its own bucket,
    otherwise fallback to the remote IP.
    """
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return get_remote_address()

def create_app():
    app = Flask(__name__)
    # Allow your local frontend during dev; tighten later
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

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

    app.register_blueprint(generate_bp)  # your existing routes
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
