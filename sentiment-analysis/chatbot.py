# sentiment-analysis/chatbot.py
import random
from sentiment_analyzer import SentimentAnalyzer
from personalization_engine import PersonalizationEngine

class ChatBot:
    def __init__(self):
        self.sa = SentimentAnalyzer()
        self.pe = PersonalizationEngine()

        # Reply templates by emotion
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

    def generate_reply(self, student_id: str, message: str, topic: str = "general"):
        sentiment = self.sa.analyze(message)
        emotion = sentiment["emotion"]
        # Pick a random template for this emotion
        reply = random.choice(self.templates.get(emotion, self.templates["neutral"]))

        # Optionally adjust performance for positive engagement
        if emotion == "positive":
            self.pe.update_performance(student_id, 0.9)

        return {
            "student_id": student_id,
            "reply": reply,
            "emotion_detected": emotion,
            "tone": "empathetic" if emotion == "negative" else ("encouraging" if emotion == "positive" else "neutral"),
            "topic": topic
        }
