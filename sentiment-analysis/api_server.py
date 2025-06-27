from flask import Flask, request, jsonify
from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine
import config

app = Flask(__name__)

# Initialize the core components
sentiment_analyzer = SentimentAnalyzer()
personalization_engine = PersonalizationEngine()

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
        data = request.get_json()
        if not data or 'student_id' not in data or 'message' not in data:
            return jsonify({"error": "Request must include 'student_id' and 'message'"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    
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
        return jsonify(profile), 404 # Use 404 Not Found for missing students

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
    performance_score = float(data['score']) / 100.0 # Normalize score from 0-100 to 0-1

    personalization_engine.update_performance(student_id, performance_score)
    profile = personalization_engine.get_profile_data(student_id)

    return jsonify({"message": "Performance updated successfully", "new_difficulty": profile['current_difficulty']})

if __name__ == '__main__':
    # For production, use a proper WSGI server like Gunicorn.
    app.run(debug=config.DEBUG, port=config.PORT)