from datetime import datetime, timedelta
from app import db
from app.models import CardReview


def review_card(card_review, quality):
    """SM-2 algorithm. quality: 0-5 (0=forgot completely, 5=perfect recall)"""
    if quality < 0 or quality > 5:
        raise ValueError("Quality must be between 0 and 5")

    if quality >= 3:
        if card_review.repetitions == 0:
            card_review.interval = 1
        elif card_review.repetitions == 1:
            card_review.interval = 6
        else:
            card_review.interval = round(card_review.interval * card_review.ease_factor)
        card_review.repetitions += 1
    else:
        card_review.repetitions = 0
        card_review.interval = 1

    card_review.ease_factor = max(
        1.3,
        card_review.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )

    now = datetime.utcnow()
    card_review.last_review = now
    card_review.next_review = now + timedelta(days=card_review.interval)

    db.session.commit()
    return card_review


def get_due_cards(deck):
    now = datetime.utcnow()
    due = []
    for card in deck.cards:
        if card.review and card.review.next_review <= now:
            due.append(card)
        elif not card.review:
            due.append(card)
    return due
