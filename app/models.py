from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_premium = db.Column(db.Boolean, default=False)
    decks = db.relationship("Deck", backref="owner", cascade="all, delete-orphan", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def deck_count(self):
        return len(self.decks)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
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
