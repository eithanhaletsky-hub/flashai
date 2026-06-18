from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def get_lang():
    if current_user.is_authenticated and current_user.ui_lang:
        return current_user.ui_lang
    return session.get("lang", "he")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_translations():
        from app.translations import get_translations
        lang = get_lang()
        return dict(t=get_translations(lang), lang=lang)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.cards import cards_bp
    from app.routes.study import study_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cards_bp, url_prefix="/cards")
    app.register_blueprint(study_bp, url_prefix="/study")

    with app.app_context():
        from app import models
        db.create_all()

    return app
