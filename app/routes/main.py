from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
from app.models import Deck

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    if current_user.is_authenticated:
        decks = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.created_at.desc()).all()
        return render_template("index.html", decks=decks)
    return render_template("landing.html")


@main_bp.route("/api/decks")
@login_required
def api_decks():
    decks = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.created_at.desc()).all()
    return jsonify([
        {"id": d.id, "name": d.name, "card_count": d.card_count}
        for d in decks
    ])
