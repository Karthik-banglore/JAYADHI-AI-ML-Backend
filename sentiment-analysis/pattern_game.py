# sentiment-analysis/pattern_game.py

from flask import Blueprint, request, jsonify
import requests
import re

pattern_game = Blueprint('pattern_game', __name__)

PATTERN_MODEL = "google/gemini-2.0-flash-001"
PATTERN_API_KEY = "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"
PATTERN_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@pattern_game.route('/api/game/pattern-predictor', methods=['POST'])
def pattern_predictor():
    data = request.get_json()
    seq = data.get("sequence")
    if not seq or len(seq) != 3:
        return jsonify({"error": "Please provide a sequence of 3 numbers as a list."}), 400

    prompt = (
        f"Given the number sequence: {seq}, identify the next number in the pattern "
        "and explain the logic. Respond in this format:\n\n"
        "**Next Number**: <only number>\n**Reason**: <your explanation>"
    )

    headers = {
        "Authorization": f"Bearer {PATTERN_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": PATTERN_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    try:
        response = requests.post(PATTERN_API_URL, headers=headers, json=body, timeout=15)
        result = response.json()
        message = result['choices'][0]['message']['content'].strip()

        match = re.search(r"\*\*Next Number\*\*:\s*(\d+).*?\*\*Reason\*\*:\s*(.+)", message, re.DOTALL)
        if match:
            next_number = match.group(1).strip()
            reason = match.group(2).strip()
            return jsonify({"next_number": int(next_number), "reasoning": reason})
        else:
            return jsonify({"error": "Could not parse result properly.", "raw": message}), 500
    except Exception as e:
        return jsonify({"error": "API request failed.", "details": str(e)}), 500
