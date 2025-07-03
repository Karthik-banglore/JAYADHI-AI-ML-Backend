# sentiment-analysis/prompt_game.py

from flask import Blueprint, request, jsonify
import requests

prompt_game = Blueprint('prompt_game', __name__)

PROMPT_MODEL = "google/gemini-2.0-flash-001"
PROMPT_API_KEY = "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"
PROMPT_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


easy = [
    "You wake up and can talk to animals. What do you say to your pet?",
    "Describe your dream treehouse. What does it look like?",
    "Write a story about a magic pencil that brings drawings to life."
     ]
moderate = [
    "You find a treasure map in your backyard. What happens next?",
    "You discover a secret door in your school. Where does it lead?",
    "Write about a day when everything in your house is upside down."
]
hard = [
     "You are the world’s youngest astronaut and get to fly to the moon. Describe your space trip.",
    "You invent a robot that does your homework. What goes wrong?",
    "Write a journal entry from the point of view of a time traveler who visits 100 years into the future."
]

def get_task(level, index):
    level_map = {"easy": easy, "moderate": moderate, "hard": hard}
    return level_map.get(level.lower(), [])[index % 3]

@prompt_game.route('/api/game/prompt-evaluator', methods=['POST'])
def prompt_evaluator():
    data = request.get_json()
    level = data.get("level")
    task_index = int(data.get("task_index", 0))
    user_prompt = data.get("user_prompt")

    scenario = get_task(level, task_index)
    if not scenario or not user_prompt:
        return jsonify({"error": "Missing or invalid level, task_index, or user_prompt."}), 400

    system_prompt = f"""You're a Prompt Quality Evaluator for kids. A student was asked to create a prompt to generate the following: "{scenario}".

Evaluate their prompt for clarity, creativity, and how well it achieves the task. 
Give result in this format exactly:

Result: <0%, 10%, 25%, 50%, 75%, 100%>
Feedback: <clear tips to improve>
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    headers = {
        "Authorization": f"Bearer {PROMPT_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": PROMPT_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(PROMPT_BASE_URL, headers=headers, json=body, timeout=15)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        lines = reply.split("\n")
        result_line = next((line for line in lines if line.lower().startswith("result:")), None)
        feedback_line = next((line for line in lines if line.lower().startswith("feedback:")), None)

        return jsonify({
            "task": scenario,
            "result": result_line.split(":", 1)[1].strip() if result_line else "Unknown",
            "feedback": feedback_line.split(":", 1)[1].strip() if feedback_line else "No feedback provided."
        })
    except Exception as e:
        return jsonify({"error": "API request failed.", "details": str(e)}), 500
