from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.translations import get_translations
from app import get_lang

auth_bp = Blueprint("auth", __name__)


def t():
    return get_translations(get_lang())


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.landing"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not username or not email or not password:
            flash(t()["flash_all_fields"], "error")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash(t()["flash_password_min"], "error")
            return render_template("auth/register.html")

        if password != confirm:
            flash(t()["flash_password_match"], "error")
            return render_template("auth/register.html")

        from app.models import User
        if User.query.filter_by(username=username).first():
            flash(t()["flash_username_taken"], "error")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash(t()["flash_email_taken"], "error")
            return render_template("auth/register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(t()["flash_welcome"], "success")
        return redirect(url_for("main.landing"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.landing"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        from app.models import User
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash(t()["flash_invalid_login"], "error")
            return render_template("auth/login.html")

        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.landing"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(t()["flash_logged_out"], "info")
    return redirect(url_for("main.landing"))
