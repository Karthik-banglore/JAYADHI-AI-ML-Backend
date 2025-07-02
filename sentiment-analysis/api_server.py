# sentiment-analysis/api_server.py

# --- Core Flask & Helper Imports ---
import os
import json
import random
import numpy as np
import base64
import io
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- TensorFlow and Keras Imports ---
from tensorflow.keras.models import load_model # type: ignore

# --- Your Existing AI Component Imports ---
from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine
from chatbot import ChatBot
from image_classifier import ImageClassifier
import config

# --- App & CORS Initialization ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# === LOAD ALL AI COMPONENTS AT STARTUP ===

# --- Load Your Existing Components ---
sentiment_analyzer = SentimentAnalyzer()
personalization_engine = PersonalizationEngine()
chatbot = ChatBot()
print("✅ Sentiment, Personalization, and ChatBot components loaded.")

# --- Load NEW Fruit Classifier ---
project_root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_root, '..', 'data-curation', 'fruits-360-subset')
model_path = os.path.join(project_root, '..', 'fruit_model.h5')

image_classifier = ImageClassifier(data_dir=data_dir)

if os.path.exists(model_path):
    image_classifier.model = load_model(model_path)
    # We need to load class_indices separately if model exists
    # For now, we will retrain each time if the file doesn't exist.
    # A better approach would be to save/load class_indices with the model.
    print("✅ Fruit classifier model loaded.")
    # This is a simplification. In a real app, you'd save/load this with the model.
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical'
    )
    image_classifier.class_indices = train_generator.class_indices

else:
    print("Could not find fruit classifier model. Training a new one...")
    image_classifier.train()
    image_classifier.model.save(model_path)
    print("✅ New fruit classifier model trained and saved.")

fruit_class_names = {v: k for k, v in image_classifier.class_indices.items()}


# === YOUR ORIGINAL API ENDPOINTS (UNCHANGED) ===

@app.route('/')
def index():
    return "JAYADHI AI for ALL: Personalization & Sentiment Server is running."

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

# === NEW FRUIT CLASSIFIER GAME ENDPOINTS ===

@app.route('/api/game/fruit/classes', methods=['GET'])
def get_fruit_classes():
    if not fruit_class_names:
        return jsonify({"error": "Fruit classes not available"}), 500
    
    # This line runs, but the result is never sent back!
    display_names = sorted(list(set([name.replace('_', ' ').split(' ')[0] for name in fruit_class_names.values()]))) 
    return jsonify(display_names)

@app.route('/api/game/fruit/random', methods=['GET'])
def get_random_fruit_challenge():
    """Provides a random fruit image from the test set for a challenge."""
    if not fruit_class_names:
        return jsonify({"error": "Fruit game not available"}), 500

    internal_class_name = random.choice(list(fruit_class_names.values()))
    class_dir = os.path.join('data-curation/fruits-360-subset/test', internal_class_name)
    
    if not os.path.exists(class_dir) or not os.listdir(class_dir):
        return jsonify({"error": f"No test images found for class: {internal_class_name}"}), 404

    random_image_name = random.choice(os.listdir(class_dir))
    image_path = os.path.join(class_dir, random_image_name)
    
    # Create a "display_name" for the frontend to check against
    display_name = internal_class_name.split(' ')[0]
    
    # Read image and encode as base64 to send to the frontend
    with open(image_path, "rb") as image_file:
        image_data_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({
        "display_name": display_name,
        "image_data": f"image/jpeg;base64,{image_data_base64}"
    })

@app.route('/api/game/fruit/classify', methods=['POST'])
def classify_fruit_endpoint():
    """Classifies a fruit image from a base64 string and checks the user's guess."""
    data = request.get_json()
    if not data or 'image_data' not in data or 'guess' not in data:
        return jsonify({"error": "Request must contain 'image_data' and 'guess'"}), 400

    # Save the base64 image to a temporary file
    image_data = data['image_data']
    if "base64," in image_data:
        image_data = image_data.split("base64,")[1]
    
    try:
        image_bytes = base64.b64decode(image_data)
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(image_bytes)

        predicted_internal_label, confidence = image_classifier.predict(temp_image_path)
        os.remove(temp_image_path) # Clean up the temp file
    except Exception as e:
        logging.error(f"Error during image prediction: {e}")
        return jsonify({"error": "Failed to process image"}), 500

    user_guess = data.get("guess")
    is_correct = user_guess.lower() in predicted_internal_label.lower()
    
    predicted_display_label = predicted_internal_label.split(' ')[0]

    if is_correct:
        educational_message = f"Correct! It's a {predicted_display_label}. Did you know there are over 7,500 varieties of apples?"
    else:
        educational_message = f"Not quite! My prediction is {predicted_display_label}. Keep trying!"

    return jsonify({
        "predicted_label": predicted_display_label,
        "confidence": round(confidence, 4),
        "is_correct": is_correct,
        "educational_message": educational_message
    })


# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=5001, host='127.0.0.1')
