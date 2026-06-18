import random
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Deck, Card, CardReview
from app.services.spaced_repetition import review_card, get_due_cards
from app.translations import get_translations
from app import get_lang

study_bp = Blueprint("study", __name__)


def t():
    return get_translations(get_lang())


@study_bp.route("/deck/<int:deck_id>")
@login_required
def study_menu(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        flash(t()["flash_access_denied"], "error")
        return redirect(url_for("main.landing"))
    due_cards = get_due_cards(deck)
    return render_template("study_menu.html", deck=deck, due_count=len(due_cards))


@study_bp.route("/deck/<int:deck_id>/flashcards")
def study_flashcards(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    due_cards = get_due_cards(deck)
    return render_template("study.html", deck=deck, due_cards=due_cards)


@study_bp.route("/deck/<int:deck_id>/quiz")
def study_quiz(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = deck.cards
    if len(cards) < 4:
        return render_template("study_menu.html", deck=deck, due_count=0,
                               error="You need at least 4 cards for quiz mode.")
    quiz_data = []
    for card in cards:
        wrong_answers = [c.back for c in cards if c.id != card.id]
        random.shuffle(wrong_answers)
        options = wrong_answers[:3] + [card.back]
        random.shuffle(options)
        quiz_data.append({
            "id": card.id,
            "question": card.front,
            "correct": card.back,
            "options": options,
        })
    random.shuffle(quiz_data)
    return render_template("study_quiz.html", deck=deck, quiz_data=quiz_data)


@study_bp.route("/deck/<int:deck_id>/match")
def study_match(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = deck.cards[:8]
    if len(cards) < 4:
        return render_template("study_menu.html", deck=deck, due_count=0,
                               error="You need at least 4 cards for match mode.")
    pairs = [{"id": c.id, "front": c.front, "back": c.back} for c in cards]
    random.shuffle(pairs)
    return render_template("study_match.html", deck=deck, pairs=pairs)


@study_bp.route("/deck/<int:deck_id>/write")
def study_write(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = [{"id": c.id, "front": c.front, "back": c.back} for c in deck.cards]
    random.shuffle(cards)
    return render_template("study_write.html", deck=deck, cards=cards)


@study_bp.route("/review", methods=["POST"])
def submit_review():
    data = request.get_json()
    card_id = data.get("card_id")
    quality = data.get("quality")

    card = Card.query.get_or_404(card_id)
    if not card.review:
        card.review = CardReview(card_id=card.id)

    review_card(card.review, quality)

    return jsonify({
        "success": True,
        "next_review": card.review.next_review.strftime("%d/%m/%Y"),
        "interval": card.review.interval
    })
