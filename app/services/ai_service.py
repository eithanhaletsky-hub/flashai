import json
from google import genai
from flask import current_app

MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]


def generate_flashcards(topic, num_cards=10, language="he"):
    api_key = current_app.config["GEMINI_API_KEY"]
    if not api_key or api_key == "your-api-key-here":
        raise ValueError("Missing Gemini API key. Add it to your .env file.")

    client = genai.Client(api_key=api_key)

    lang_name = "Hebrew" if language == "he" else "English"

    prompt = f"""Create exactly {num_cards} flashcards about the topic: "{topic}"

Rules:
- Write in {lang_name}
- Each flashcard has a "front" (question/term) and "back" (answer/definition)
- Keep answers concise but complete
- Make questions clear and specific
- Return ONLY valid JSON, no markdown, no explanation

Return this exact JSON format:
{{
  "cards": [
    {{"front": "question here", "back": "answer here"}},
    {{"front": "question here", "back": "answer here"}}
  ]
}}"""

    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            text = response.text.strip()

            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                text = text.rsplit("```", 1)[0]

            data = json.loads(text)
            current_app.logger.info(f"Generated cards using model: {model_name}")
            return data["cards"]
        except Exception as e:
            last_error = e
            current_app.logger.warning(f"Model {model_name} failed: {e}")
            continue

    raise ValueError(f"All models failed. Last error: {last_error}")
