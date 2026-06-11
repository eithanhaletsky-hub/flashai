from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.cards import cards_bp
    from app.routes.study import study_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cards_bp, url_prefix="/cards")
    app.register_blueprint(study_bp, url_prefix="/study")

    with app.app_context():
        from app import models
        db.create_all()

    return app
