from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Deck, Card, CardReview
from app.services.ai_service import generate_flashcards
from app.translations import get_translations
from app import get_lang

cards_bp = Blueprint("cards", __name__)


def t():
    return get_translations(get_lang())


@cards_bp.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        deck_name = request.form.get("deck_name", "").strip() or topic
        num_cards = int(request.form.get("num_cards", 10))
        language = request.form.get("language", "he")

        if not topic:
            flash(t()["flash_enter_topic"], "error")
            return render_template("generate.html")

        num_cards = max(3, min(num_cards, 30))

        try:
            cards_data = generate_flashcards(topic, num_cards, language)
        except Exception as e:
            flash(t()["flash_ai_failed"].format(error=e), "error")
            return render_template("generate.html")

        deck = Deck(name=deck_name, description=f"Generated from: {topic}", user_id=current_user.id)
        db.session.add(deck)
        db.session.flush()

        for card_data in cards_data:
            card = Card(deck_id=deck.id, front=card_data["front"], back=card_data["back"])
            db.session.add(card)
            db.session.flush()
            review = CardReview(card_id=card.id)
            db.session.add(review)

        db.session.commit()
        flash(t()["flash_created"].format(count=len(cards_data)), "success")
        return redirect(url_for("cards.deck_view", deck_id=deck.id))

    return render_template("generate.html")


@cards_bp.route("/deck/<int:deck_id>")
@login_required
def deck_view(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        flash(t()["flash_access_denied"], "error")
        return redirect(url_for("main.landing"))
    return render_template("deck.html", deck=deck)


@cards_bp.route("/deck/<int:deck_id>/delete", methods=["POST"])
@login_required
def deck_delete(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        flash(t()["flash_access_denied"], "error")
        return redirect(url_for("main.landing"))
    db.session.delete(deck)
    db.session.commit()
    flash(t()["flash_deck_deleted"], "info")
    return redirect(url_for("main.landing"))


@cards_bp.route("/card/<int:card_id>/edit", methods=["POST"])
@login_required
def card_edit(card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403
    data = request.get_json()
    if "front" in data:
        card.front = data["front"]
    if "back" in data:
        card.back = data["back"]
    db.session.commit()
    return jsonify({"success": True})


@cards_bp.route("/card/<int:card_id>/delete", methods=["POST"])
@login_required
def card_delete(card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403
    deck_id = card.deck_id
    db.session.delete(card)
    db.session.commit()
    return jsonify({"success": True, "deck_id": deck_id})
