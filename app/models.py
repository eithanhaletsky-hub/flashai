from datetime import datetime
from app import db


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cards = db.relationship("Card", backref="deck", cascade="all, delete-orphan", lazy=True)

    @property
    def card_count(self):
        return len(self.cards)

    @property
    def due_count(self):
        now = datetime.utcnow()
        return sum(1 for c in self.cards if c.review and c.review.next_review <= now)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"), nullable=False)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    review = db.relationship("CardReview", backref="card", uselist=False, cascade="all, delete-orphan")


class CardReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    ease_factor = db.Column(db.Float, default=2.5)
    interval = db.Column(db.Integer, default=0)
    repetitions = db.Column(db.Integer, default=0)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)
    last_review = db.Column(db.DateTime, nullable=True)
