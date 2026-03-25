import os
from flask import Flask
from .extensions import db

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    database_url = os.environ.get("DATABASE_URL", "sqlite:///firstrep.db")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.onboarding import onboarding_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(onboarding_bp)

    with app.app_context():
        db.create_all()

    return app