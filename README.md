# FlashAI — AI-Powered Flashcard Generator

> Create smart flashcards instantly with AI. Study with 4 different modes and master any topic.

**Live Demo:** [eithan.pythonanywhere.com](https://eithan.pythonanywhere.com)

---

## Features

- **AI Flashcard Generation** — Type any topic, get up to 30 flashcards instantly (Hebrew & English)
- **4 Study Modes:**
  - Flashcards — Classic flip cards with spaced repetition (SM-2 algorithm)
  - Multiple Choice — Auto-generated quiz with scoring
  - Match — Race to match terms with definitions
  - Write — Type answers from memory
- **User Accounts** — Register, login, personal decks
- **Deck Management** — Create, edit, delete cards and decks
- **Spaced Repetition** — SM-2 algorithm tells you when to review each card
- **Responsive Design** — Works on desktop and mobile

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite, SQLAlchemy |
| AI | Google Gemini API |
| Auth | Flask-Login, Werkzeug |
| Frontend | HTML, Tailwind CSS, JavaScript |
| Hosting | PythonAnywhere |

## Setup

```bash
# Clone
git clone https://github.com/eithanhaletsky-hub/flashai.git
cd flashai

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your Gemini API key

# Run
python run.py
```

Open **http://127.0.0.1:5000** in your browser.

## Project Structure

```
flashai/
├── app/
│   ├── __init__.py          # App factory, Flask-Login setup
│   ├── models.py            # User, Deck, Card, CardReview models
│   ├── routes/
│   │   ├── auth.py          # Register, login, logout
│   │   ├── cards.py         # Generate, view, edit, delete cards
│   │   ├── main.py          # Landing page, dashboard
│   │   └── study.py         # 4 study modes
│   ├── services/
│   │   ├── ai_service.py    # Gemini API integration
│   │   └── spaced_repetition.py  # SM-2 algorithm
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS
├── config.py                # App configuration
├── run.py                   # Entry point
└── requirements.txt
```

## API Key

This project uses the [Google Gemini API](https://ai.google.dev/). Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey).

## License

MIT License — free to use, modify, and sell.
