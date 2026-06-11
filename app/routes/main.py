from flask import Blueprint, render_template
from app.models import Deck

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    decks = Deck.query.order_by(Deck.created_at.desc()).all()
    return render_template("index.html", decks=decks)
