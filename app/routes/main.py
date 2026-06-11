from flask import Blueprint, render_template, jsonify
from app.models import Deck

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    decks = Deck.query.order_by(Deck.created_at.desc()).all()
    return render_template("index.html", decks=decks)


@main_bp.route("/api/decks")
def api_decks():
    decks = Deck.query.order_by(Deck.created_at.desc()).all()
    return jsonify([
        {"id": d.id, "name": d.name, "card_count": d.card_count}
        for d in decks
    ])
