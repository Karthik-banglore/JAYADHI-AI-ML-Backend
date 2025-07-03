# sentiment-analysis/chatbot.py
import random
import requests
import json
import logging
from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine

# LLM API constants
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODEL = "google/gemini-2.0-flash-001"

AI_KEYWORDS = [
    'ai', 'artificial intelligence', 'machine learning', 'deep learning',
    'robot', 'neural network', 'chatbot', 'data', 'model', 'training', 'algorithm'
]

def is_ai_related(message):
    msg = message.lower()
    return any(word in msg for word in AI_KEYWORDS)

def ask_ai_question(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You're a friendly AI teacher for kids. Answer AI-related questions in simple, fun language with real-world examples a child would understand."
            },
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            return answer
        else:
            logging.error(f"LLM API error: {response.status_code} {response.text}")
            return "Sorry, I couldn't get an answer from my AI brain right now. Try again later!"
    except Exception as e:
        logging.error(f"Exception in ask_ai_question: {e}")
        return "Sorry, I ran into a technical problem. Try again later!"

class ChatBot:
    def __init__(self):
        self.sa = SentimentAnalyzer()
        self.pe = PersonalizationEngine()
        self.templates = {
            "negative": [
                "I’m sorry you’re feeling stuck. Let’s tackle it together—what part is most confusing?",
                "I know this can be challenging. Describe where you hit a roadblock, and I’ll help.",
                "It’s okay to struggle. Tell me exactly what’s holding you back."
            ],
            "positive": [
                "Fantastic enthusiasm! Ready to level up?",
                "Great to see your confidence—shall we try a tougher challenge?",
                "Your positivity is awesome! Let’s crank up the difficulty."
            ],
            "neutral": [
                "Let’s keep going—what part would you like more help with?",
                "I’m here to guide you. What would you like to understand better?",
                "Okay, let’s move forward. Which bit should we focus on first?"
            ]
        }

    def generate_reply(self, student_id: str, message: str, topic: str = "general", context: dict = None):
        # 1. If the message is an AI-related question, call the LLM API
        if is_ai_related(message):
            ai_answer = ask_ai_question(message)
            return {
                "student_id": student_id,
                "reply": ai_answer,
                "emotion_detected": "informative",
                "tone": "generative",
                "topic": topic
            }

        # 2. Otherwise, use the classic sentiment/template logic
        sentiment = self.sa.analyze(message)
        emotion = sentiment["emotion"]
        reply = random.choice(self.templates.get(emotion, self.templates["neutral"]))

        if emotion == "positive":
            self.pe.update_performance(student_id, 0.9)

        return {
            "student_id": student_id,
            "reply": reply,
            "emotion_detected": emotion,
            "tone": "empathetic" if emotion == "negative" else ("encouraging" if emotion == "positive" else "neutral"),
            "topic": topic
        }
