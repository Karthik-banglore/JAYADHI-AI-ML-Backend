from typing import Dict, List
import json
from datetime import datetime
from database import db

class StudentProfile:
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.current_difficulty = 3
        self.performance_history: List[float] = []
        self.sentiment_history: List[Dict] = []
        self.learning_profile = "visual"  # visual/auditory/kinesthetic
        self.proficiency_level = "beginner"  # beginner/intermediate/expert
        self.stress_level = "low"  # low/medium/high
        self.engagement_level = "medium"  # low/medium/high

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "current_difficulty": self.current_difficulty,
            "performance_history": self.performance_history,
            "sentiment_history": self.sentiment_history,
            "learning_profile": self.learning_profile,
            "proficiency_level": self.proficiency_level,
            "stress_level": self.stress_level,
            "engagement_level": self.engagement_level
        }

class PersonalizationEngine:
    def __init__(self):
        self.db = db
        
    def get_or_create_profile(self, student_id: str, name: str = "New Student") -> StudentProfile:
        """Get or create student profile from MongoDB"""
        user_data = self.db.get_user_profile(student_id)
        
        if not user_data:
            profile = StudentProfile(student_id, name)
            self.db.create_user_profile(student_id, profile.to_dict())
            
            # Log profile creation
            self.db.log_user_action(student_id, "profile_created", {
                "name": name,
                "initial_difficulty": 3
            })
            
            return profile
        
        profile = StudentProfile(student_id, user_data.get("name", name))
        profile.current_difficulty = user_data.get("current_difficulty", 3)
        profile.performance_history = user_data.get("performance_history", [])
        profile.sentiment_history = user_data.get("sentiment_history", [])
        profile.learning_profile = user_data.get("learning_profile", "visual")
        profile.proficiency_level = user_data.get("proficiency_level", "beginner")
        profile.stress_level = user_data.get("stress_level", "low")
        profile.engagement_level = user_data.get("engagement_level", "medium")
        
        return profile

    def update_performance(self, student_id: str, performance_score: float) -> int:
        """Update performance with digital twin logging"""
        profile = self.get_or_create_profile(student_id)
        old_difficulty = profile.current_difficulty
        
        profile.performance_history.append(performance_score)
        
        # Dynamic difficulty adjustment
        if performance_score > 0.8 and profile.current_difficulty < 5:
            profile.current_difficulty = min(5, profile.current_difficulty + 1)
        elif performance_score < 0.4 and profile.current_difficulty > 1:
            profile.current_difficulty = max(1, profile.current_difficulty - 1)
        
        # Update proficiency level based on performance
        avg_performance = sum(profile.performance_history[-5:]) / min(5, len(profile.performance_history))
        if avg_performance > 0.8:
            profile.proficiency_level = "expert"
        elif avg_performance > 0.6:
            profile.proficiency_level = "intermediate"
        else:
            profile.proficiency_level = "beginner"
        
        # Update stress level based on performance trend
        if len(profile.performance_history) >= 3:
            recent_scores = profile.performance_history[-3:]
            if all(score < 0.4 for score in recent_scores):
                profile.stress_level = "high"
            elif all(score > 0.7 for score in recent_scores):
                profile.stress_level = "low"
            else:
                profile.stress_level = "medium"
        
        # Save to MongoDB
        self.db.users.update_one(
            {"user_id": student_id},
            {"$set": profile.to_dict()},
            upsert=True
        )
        
        # Log performance update
        self.db.log_user_action(student_id, "performance_updated", {
            "score": performance_score,
            "old_difficulty": old_difficulty,
            "new_difficulty": profile.current_difficulty,
            "proficiency_level": profile.proficiency_level,
            "stress_level": profile.stress_level
        })
        
        return profile.current_difficulty

    def log_sentiment(self, student_id: str, sentiment_data: dict):
        """Log sentiment with digital twin tracking"""
        profile = self.get_or_create_profile(student_id)
        profile.sentiment_history.append(sentiment_data)
        
        # Update engagement level based on sentiment
        emotion = sentiment_data.get("emotion", "neutral")
        if emotion == "positive":
            profile.engagement_level = "high"
        elif emotion == "negative":
            profile.engagement_level = "low"
        else:
            profile.engagement_level = "medium"
        
        # Save to MongoDB
        self.db.users.update_one(
            {"user_id": student_id},
            {"$set": {
                "sentiment_history": profile.sentiment_history,
                "engagement_level": profile.engagement_level
            }}
        )
        
        # Log sentiment analysis
        self.db.log_user_action(student_id, "sentiment_analyzed", {
            "emotion": emotion,
            "sentiment_scores": sentiment_data.get("vader_scores", {}),
            "engagement_level": profile.engagement_level
        })

    def get_profile_data(self, student_id: str) -> dict:
        """Get profile data from MongoDB"""
        user_data = self.db.get_user_profile(student_id)
        if user_data:
            # Remove MongoDB _id field
            user_data.pop("_id", None)
            return user_data
        return {"error": "Student not found"}
    
    def set_learning_profile(self, student_id: str, learning_type: str):
        """Set learning profile (visual/auditory/kinesthetic)"""
        if learning_type not in ["visual", "auditory", "kinesthetic"]:
            return False
        
        self.db.users.update_one(
            {"user_id": student_id},
            {"$set": {"learning_profile": learning_type}},
            upsert=True
        )
        
        # Log learning profile update
        self.db.log_user_action(student_id, "learning_profile_set", {
            "learning_type": learning_type
        })
        
        return True

    @property
    def student_profiles(self):
        """Get all student IDs for backward compatibility"""
        users = self.db.users.find({}, {"user_id": 1})
        return {user["user_id"]: None for user in users}

# Global personalization engine instance
personalization_engine = PersonalizationEngine()