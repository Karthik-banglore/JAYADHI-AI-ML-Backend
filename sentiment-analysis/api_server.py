from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import traceback
import atexit
import logging
import config

# Import all the AI components
from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine
from chatbot import ChatBot

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the core components
sentiment_analyzer = SentimentAnalyzer()
personalization_engine = PersonalizationEngine()
chatbot = ChatBot()

@app.route('/')
def index():
    return "JAYADHI AI for ALL: Personalization & Sentiment Server is running."

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    """
    Endpoint for Anoop (Chatbot).
    Receives a student message, analyzes sentiment, and logs it.
    """
    try:
        print("Received sentiment request")
        data = request.get_json()
        print(f"Request  {data}")
        
        if not data or 'student_id' not in data or 'message' not in data:
            return jsonify({"error": "Request must include 'student_id' and 'message'"}), 400
    except Exception as e:
        print(f"Error in Sentiment analysis: {e}")
        return jsonify({"error": str(e)}), 500
    
    student_id = data['student_id']
    message = data['message']
    analysis_result = sentiment_analyzer.analyze(message)
    
    # Log the sentiment to the student's permanent profile
    personalization_engine.log_sentiment(student_id, analysis_result)
    
    # Return a response to the chatbot to help it shape its reply
    response = {
        "emotion": analysis_result['emotion'],
        "scores": analysis_result['vader_scores'],
        "suggested_tone": "empathetic" if analysis_result['emotion'] == 'negative' else "encouraging"
    }
    return jsonify(response)

@app.route('/api/difficulty/<string:student_id>', methods=['GET'])
def get_student_difficulty(student_id):
    """Endpoint for Anangsha (Games) to fetch the current difficulty for a student."""
    profile = personalization_engine.get_profile_data(student_id)
    if "error" in profile:
        return jsonify(profile), 404

    return jsonify({"student_id": student_id, "difficulty_level": profile['current_difficulty']})

@app.route('/api/performance', methods=['POST'])
def update_student_performance():
    """Endpoint for Anangsha (Games) to submit a performance score."""
    try:
        data = request.get_json()
        if not data or 'student_id' not in data or 'score' not in data:
            return jsonify({"error": "Request must include 'student_id' and 'score'"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON in request body"}), 400

    student_id = data['student_id']
    performance_score = float(data['score']) / 100.0

    personalization_engine.update_performance(student_id, performance_score)
    profile = personalization_engine.get_profile_data(student_id)

    return jsonify({"message": "Performance updated successfully", "new_difficulty": profile['current_difficulty']})

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    try:
        data = request.get_json()
        if not data or 'student_id' not in data or 'message' not in data:
            return jsonify({"error": "Request must include 'student_id' and 'message'"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    
    student_id = data['student_id']
    message = data['message']
    topic = data.get('topic', 'general')
    
    response = chatbot.generate_reply(student_id, message, topic)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=5001, host='127.0.0.1')
