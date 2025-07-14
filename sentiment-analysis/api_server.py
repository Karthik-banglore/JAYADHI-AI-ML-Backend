# sentiment-analysis/api_server.py (Updated with Prompt & Pattern endpoints)
import os
import sys
import json
import random
import numpy as np
import base64
import io
import logging
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model  #type: ignore
import requests
import re

from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine
from chatbot import ChatBot
from image_classifier import ImageClassifier
import config
from teacher_dashboard import setup_teacher_dashboard_routes
from logger import ai_logger # Make sure you have your logger instance

# Load quiz questions at startup
try:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    quiz_path = os.path.join(project_root, 'quiz-data', 'ai_questions.json')
    with open(quiz_path, 'r') as f:
        quiz_questions = json.load(f)
    print("✅ AI quiz questions loaded successfully.")
except Exception as e:
    print(f"❌ Error loading quiz questions: {e}")
    quiz_questions = {"beginner": [], "intermediate": [], "advanced": []}

# Store active questions per student (in production, use Redis)
active_questions = {}


# --- Data Detective Import Hack for Hyphen Directory ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, "data-curation"))
from data_issues_config import DATA_ISSUES # type: ignore

# --- App & CORS Initialization ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# === LOAD ALL AI COMPONENTS AT STARTUP ===
sentiment_analyzer = SentimentAnalyzer()
personalization_engine = PersonalizationEngine()
chatbot = ChatBot()
print("✅ Sentiment, Personalization, and ChatBot components loaded.")

# === REGISTER TEACHER DASHBOARD ROUTES ===
setup_teacher_dashboard_routes(app, personalization_engine, ai_logger)
print("✅ Teacher Dashboard routes registered successfully.")


# --- Load or Train Fruit Classifier ---
project_root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_root, '..', 'data-curation', 'fruits-360-subset')
model_path = os.path.join(project_root, '..', 'fruit_model.h5')

image_classifier = ImageClassifier(data_dir=data_dir)

if os.path.exists(model_path):
    print(f"Loading existing model from: {model_path}")
    image_classifier.load_existing_model(model_path)
    print("✅ Fruit classifier model loaded successfully.")
else:
    print(f"Model not found at {model_path}. Training a new one...")
    image_classifier.train()
    image_classifier.model.save(model_path)
    print(f"✅ New model trained and saved to {model_path}")

fruit_class_names = {v: k for k, v in image_classifier.class_indices.items()}

# --- Data Detective Dataset Paths ---
DATA_DETECTIVE_DATASETS = {
    'easy':   {'file': 'data-curation/messy-datasets/easy_student_data.json',   'config': 'easy_student_data'},
    'medium': {'file': 'data-curation/messy-datasets/medium_employee_data.json','config': 'medium_employee_data'},
    'hard':   {'file': 'data-curation/messy-datasets/hard_product_data.json',  'config': 'hard_product_data'}
}


# === API ENDPOINTS ===

@app.route('/')
def index():
    return "JAYADHI AI for ALL: Personalization & Sentiment Server is running."

# --- Original Endpoints ---
@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    student_id = data['student_id']
    message = data['message']
    analysis_result = sentiment_analyzer.analyze(message)
    personalization_engine.log_sentiment(student_id, analysis_result)
    response = {
        "emotion": analysis_result['emotion'],
        "scores": analysis_result['vader_scores'],
        "suggested_tone": "empathetic" if analysis_result['emotion'] == 'negative' else "encouraging"
    }
    return jsonify(response)

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    student_id = data['student_id']
    message = data['message']
    topic = data.get('topic', 'general')
    response = chatbot.generate_reply(student_id, message, topic)
    return jsonify(response)
    
@app.route('/api/difficulty/<string:student_id>', methods=['GET'])
def get_student_difficulty(student_id):
    profile = personalization_engine.get_profile_data(student_id)
    if "error" in profile:
        return jsonify(profile), 404
    return jsonify({"student_id": student_id, "difficulty_level": profile['current_difficulty']})

@app.route('/api/performance', methods=['POST'])
def update_student_performance():
    data = request.get_json()
    student_id = data['student_id']
    performance_score = float(data['score']) / 100.0
    personalization_engine.update_performance(student_id, performance_score)
    profile = personalization_engine.get_profile_data(student_id)
    return jsonify({"message": "Performance updated successfully", "new_difficulty": profile['current_difficulty']})

# --- Fruit Classifier Endpoints ---
@app.route('/api/game/fruit/classes', methods=['GET'])
def get_fruit_classes():
    if not fruit_class_names:
        return jsonify({"error": "Fruit classes not available"}), 500
    display_names = sorted(list(set([name.replace('_', ' ').split(' ')[0] for name in fruit_class_names.values()])))
    return jsonify(display_names)

@app.route('/api/game/fruit/random', methods=['GET'])
def get_random_fruit_challenge():
    if not fruit_class_names:
        return jsonify({"error": "Fruit game not available"}), 500
    internal_class_name = random.choice(list(fruit_class_names.values()))
    class_dir = os.path.join(data_dir, 'test', internal_class_name)
    if not os.path.exists(class_dir) or not os.listdir(class_dir):
        return jsonify({"error": f"No test images found for class: {internal_class_name}"}), 404
    random_image_name = random.choice(os.listdir(class_dir))
    image_path = os.path.join(class_dir, random_image_name)
    display_name = internal_class_name.replace('_', ' ').split(' ')[0]
    with open(image_path, "rb") as image_file:
        image_data_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    return jsonify({"display_name": display_name, "image_data": f"image/jpeg;base64,{image_data_base64}"})

@app.route('/api/game/fruit/classify', methods=['POST'])
def classify_fruit_endpoint():
    data = request.get_json()
    if not data or 'image_data' not in data or 'guess' not in data :
        return jsonify({"error": "Request must contain 'image_data' and 'guess'"}), 400
    try:
        predicted_internal_label, confidence = image_classifier.predict_from_base64(data['image_data'])
    except Exception as e:
        logging.error(f"Error during image prediction: {e}")
        return jsonify({"error": "Failed to process image"}), 500
    user_guess = data.get("guess")
    is_correct = user_guess.lower() in predicted_internal_label.lower()
    predicted_display_label = predicted_internal_label.replace('_', ' ').split(' ')[0]
    if is_correct:
        educational_message = f"Correct! It's a {predicted_display_label}. Well done!"
    else:
        educational_message = f"Not quite! My prediction is {predicted_display_label}. Keep trying!"
    return jsonify({
        "predicted_label": predicted_display_label,
        "confidence": round(confidence, 4),
        "is_correct": is_correct,
        "educational_message": educational_message
    })
# --- Data Detective Endpoints ---
@app.route('/api/game/data-detective/dataset/<difficulty>', methods=['GET'])
def get_data_detective_dataset(difficulty):
    if difficulty not in DATA_DETECTIVE_DATASETS:
        return jsonify({"error": "Invalid difficulty level. Use 'easy', 'medium', or 'hard'."}), 400
    info = DATA_DETECTIVE_DATASETS[difficulty]
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(project_root, info['file'])
    try:
        df = pd.read_json(path)
    except Exception as e:
        return jsonify({"error": f"Failed to load dataset: {e}"}), 500
    return jsonify({
        "difficulty": difficulty,
        "dataset_name": info['config'],
        "total_rows": len(df),
        "columns": list(df.columns),
        "data": df.to_dict('records'),
        "instructions": f"Examine this {difficulty} dataset and identify data quality issues.",
        "expected_issues_count": DATA_ISSUES[info['config']]['total_issues']
    })

@app.route('/api/game/data-detective/validate', methods=['POST'])
def validate_data_detective_answers():
    data = request.get_json()
    diff = data.get('difficulty')
    identified = data.get('identified_issues', [])
    student_id = data.get('student_id', 'anonymous')
    if diff not in DATA_DETECTIVE_DATASETS or not isinstance(identified, list):
        return jsonify({"error": "Missing or invalid difficulty or identified_issues."}), 400
    cfg = DATA_DETECTIVE_DATASETS[diff]['config']
    expected = DATA_ISSUES[cfg]['issues']
    total = DATA_ISSUES[cfg]['total_issues']
    score = 0
    found, missed = [], []
    for exp in expected:
        match = any(i.get('type') == exp['type'] and i.get('column') == exp['column'] for i in identified)
        if match:
            score += 1
            found.append({'type': exp['type'], 'column': exp['column'], 'explanation': exp['explanation']})
        else:
            missed.append({'type': exp['type'], 'column': exp['column'], 'explanation': exp['explanation'], 'hint': exp['suggested_action']})
    pct = round((score / total) * 100, 1) if total else 0
    if pct >= 80:
        overall = "Excellent detective work! You identified most issues."
    elif pct >= 60:
        overall = "Good job! You caught several key issues."
    elif pct >= 40:
        overall = "You're on the right track! Look more carefully for subtle issues."
    else:
        overall = "Keep practicing! Data cleaning is like detective work."
    if student_id != 'anonymous':
        personalization_engine.update_performance(student_id, pct / 100.0)
    return jsonify({
        "score_percentage": pct,
        "issues_found": score,
        "total_issues": total,
        "found_issues": found,
        "missed_issues": missed,
        "overall_feedback": overall,
        "educational_tip": "Data cleaning is like detective work—search for clues that something looks off!",
        "difficulty": diff
    })

@app.route('/api/game/data-detective/help', methods=['GET'])
def get_data_detective_help():
    return jsonify({
        "game_objective": "Learn to identify common data quality issues",
        "types_of_issues": [
            {"type": "missing_value", "description": "Empty or null fields"},
            {"type": "outlier", "description": "Values far outside the normal range"},
            {"type": "formatting", "description": "Inconsistent data formats"},
            {"type": "impossible_value", "description": "Values that cannot logically occur"},
            {"type": "case_inconsistency", "description": "Mixed uppercase/lowercase"}
        ],
        "tips": [
            "Check each column for unusual or missing values",
            "Look for values that don't make sense",
            "Ensure all entries follow the same format",
            "Pay attention to outliers and inconsistencies"
        ]
    })


# --- NEW: Prompt Evaluator Endpoint ---
# Prompt Evaluator Constants
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

@app.route('/api/game/prompt-evaluator', methods=['POST'])
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

# --- NEW: Pattern Predictor Endpoint ---
PATTERN_MODEL = PROMPT_MODEL
PATTERN_API_KEY = PROMPT_API_KEY
PATTERN_API_URL = PROMPT_BASE_URL

@app.route('/api/game/pattern-predictor', methods=['POST'])
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

        import re
        match = re.search(r"\*\*Next Number\*\*:\s*(\d+).*?\*\*Reason\*\*:\s*(.+)", message, re.DOTALL)
        if match:
            next_number = match.group(1).strip()
            reason = match.group(2).strip()
            return jsonify({"next_number": int(next_number), "reasoning": reason})
        else:
            return jsonify({"error": "Could not parse result properly.", "raw": message}), 500
    except Exception as e:
        return jsonify({"error": "API request failed.", "details": str(e)}), 500

# --- AI Quiz Game Endpoints ---

@app.route('/api/game/quiz/question/<difficulty>', methods=['GET'])
def get_ai_quiz_question(difficulty):
    """Get a random quiz question for the specified difficulty"""
    if difficulty not in quiz_questions:
        return jsonify({"error": "Invalid difficulty level. Use 'beginner', 'intermediate', or 'advanced'"}), 400
    
    questions = quiz_questions[difficulty]
    if not questions:
        return jsonify({"error": f"No questions available for {difficulty} difficulty"}), 404
    
    # Select a random question
    question = random.choice(questions)
    
    # Store the question for answer validation
    session_id = f"session_{random.randint(1000, 9999)}"
    active_questions[session_id] = question
    
    # Return question without correct answer
    response_question = {
        "session_id": session_id,
        "id": question["id"],
        "question": question["question"],
        "options": question["options"],
        "difficulty": difficulty,
        "hint_available": True
    }
    
    return jsonify(response_question)

@app.route('/api/game/quiz/answer', methods=['POST'])
def submit_ai_quiz_answer():
    """Submit quiz answer and get feedback with sentiment-aware responses"""
    data = request.get_json()
    
    if not data or 'session_id' not in data or 'selected_answer' not in data:
        return jsonify({"error": "Missing session_id or selected_answer"}), 400
    
    session_id = data['session_id']
    selected_answer = int(data['selected_answer'])
    student_id = data.get('student_id', 'anonymous')
    
    # Retrieve the stored question
    if session_id not in active_questions:
        return jsonify({"error": "Question session not found or expired"}), 404
    
    question = active_questions[session_id]
    is_correct = selected_answer == question['correct_answer']
    
    # Get student's recent sentiment for personalized feedback
    recent_sentiment = 'neutral'
    if student_id != 'anonymous':
        try:
            student_profile = personalization_engine.get_profile_data(student_id)
            if 'sentiment_history' in student_profile and student_profile['sentiment_history']:
                recent_sentiment = student_profile['sentiment_history'][-1].get('emotion', 'neutral')
        except:
            recent_sentiment = 'neutral'
    
    # Generate sentiment-aware feedback
    if is_correct:
        if recent_sentiment == 'positive':
            feedback = f"Fantastic! {question['explanation']} Your enthusiasm for learning AI is wonderful!"
        elif recent_sentiment == 'negative':
            feedback = f"Great job getting this right! {question['explanation']} See, you're better at this than you thought!"
        else:
            feedback = f"Correct! {question['explanation']}"
    else:
        if recent_sentiment == 'negative':
            feedback = f"Don't worry, learning takes time! {question['explanation']} You're making progress with each attempt!"
        else:
            feedback = f"Not quite, but good thinking! {question['explanation']}"
    
    # Update student performance
    if student_id != 'anonymous':
        score = 100 if is_correct else 0
        personalization_engine.update_performance(student_id, score / 100.0)
    
    # Clean up session
    del active_questions[session_id]
    
    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question['correct_answer'],
        "correct_option": question['options'][question['correct_answer']],
        "explanation": question['explanation'],
        "feedback": feedback,
        "educational_fact": question['educational_fact'],
        "difficulty": question['difficulty']
    })

@app.route('/api/game/quiz/topics', methods=['GET'])
def get_quiz_topics():
    """Get available quiz difficulties and topic counts"""
    topic_summary = {}
    
    for difficulty, questions in quiz_questions.items():
        topic_summary[difficulty] = {
            "question_count": len(questions),
            "topics": ["AI Fundamentals", "Machine Learning", "Computer Vision", "Natural Language Processing", "Neural Networks"]
        }
    
    return jsonify({
        "available_difficulties": list(quiz_questions.keys()),
        "topic_summary": topic_summary,
        "total_questions": sum(len(questions) for questions in quiz_questions.values())
    })

@app.route('/api/game/quiz/hint', methods=['POST'])
def get_quiz_hint():
    """Get an AI-generated hint for struggling students"""
    data = request.get_json()
    
    if not data or 'session_id' not in data:
        return jsonify({"error": "Missing session_id"}), 400
    
    session_id = data['session_id']
    student_message = data.get('student_message', '')
    
    if session_id not in active_questions:
        return jsonify({"error": "Question session not found or expired"}), 404
    
    question = active_questions[session_id]
    
    # Use chatbot for personalized hints if student is struggling
    if any(word in student_message.lower() for word in ['stuck', 'hard', 'difficult', 'help', 'confused']):
        try:
            hint_request = f"Give a gentle hint for this AI quiz question without revealing the answer: {question['question']}. Options: {', '.join(question['options'])}"
            bot_response = chatbot.generate_reply('quiz_student', hint_request, 'quiz_help')
            
            return jsonify({
                "hint": bot_response['reply'],
                "encouragement": "Take your time and think through each option carefully!",
                "tone": bot_response.get('tone', 'supportive')
            })
        except:
            pass
    
    # Fallback to a general encouraging message
    return jsonify({
        "hint": "Think about what you know about AI and try to eliminate options that don't make sense.",
        "encouragement": "You're doing great! Every question helps you learn more about AI.",
        "tone": "supportive"
    })

    # --- Leaderboard Endpoint ---
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get student XP rankings based on performance history"""
    all_profiles = []
    
    # Get all student profiles
    for student_id in personalization_engine.student_profiles:
        profile_data = personalization_engine.get_profile_data(student_id)
        if "error" not in profile_data:
            all_profiles.append(profile_data)
    
    if not all_profiles:
        return jsonify([])
    
    leaderboard = []
    for profile in all_profiles:
        # Calculate XP based on performance history
        performance_history = profile.get("performance_history", [])
        xp = int(sum(performance_history) * 100) if performance_history else 0
        
        leaderboard.append({
            "student_id": profile["student_id"],
            "name": profile.get("name", "Anonymous"),
            "xp": xp,
            "rank": 0  # Will be set after sorting
        })
    
    # Sort by XP (highest first) and assign ranks
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1
    
    return jsonify(leaderboard)

# --- Explainability Module Endpoint ---
@app.route('/api/explainability/<student_id>', methods=['GET'])
def explain_difficulty_adjustment(student_id):
    """Explain why the AI adjusted a student's difficulty level"""
    profile = personalization_engine.get_profile_data(student_id)
    
    if "error" in profile:
        return jsonify({"error": f"Student {student_id} not found"}), 404
    
    current_difficulty = profile.get("current_difficulty", 3)
    performance_history = profile.get("performance_history", [])
    
    # Generate explanation based on performance
    explanation = f"The student's difficulty is currently level {current_difficulty}. "
    
    if len(performance_history) > 0:
        avg_performance = sum(performance_history) / len(performance_history)
        
        if avg_performance > 0.8:
            explanation += "This is based on their excellent performance history, showing they can handle challenging content."
        elif avg_performance > 0.6:
            explanation += "This is based on their solid performance history, demonstrating consistent understanding of the material."
        elif avg_performance > 0.4:
            explanation += "This level reflects their moderate performance, allowing for steady progress without overwhelming them."
        else:
            explanation += "This easier level was chosen to help build their confidence based on recent struggles."
        
        # Add trend information
        if len(performance_history) >= 3:
            recent_trend = performance_history[-1] - performance_history[-3]
            if recent_trend > 0.1:
                explanation += " Recent improvement trends suggest they may be ready for increased challenges."
            elif recent_trend < -0.1:
                explanation += " Recent performance decline led to difficulty adjustment for better support."
    else:
        explanation += "This is the default starting level as no performance data is available yet."
    
    return jsonify({
        "student_id": student_id,
        "explanation": explanation,
        "current_difficulty": current_difficulty,
        "performance_data_points": len(performance_history)
    })



# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=5001, host='127.0.0.1')
