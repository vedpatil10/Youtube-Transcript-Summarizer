from flask import Flask


def create_app() -> Flask:
    """Application factory for the YouTube Transcript Summarizer app."""
    app = Flask(__name__)

    # Register routes blueprint
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app


