from typing import Dict, List
import json
import os
import config

class StudentProfile:
    """
    Represents a single student's profile, tracking their learning state.
    """
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.current_difficulty = 3  # Start at a neutral difficulty (scale 1-5)
        self.performance_history: List[float] = []
        self.sentiment_history: List[Dict] = []

    def to_dict(self):
        """Serializes the profile to a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "current_difficulty": self.current_difficulty,
            "performance_history": self.performance_history,
            "sentiment_history": self.sentiment_history
        }

class PersonalizationEngine:
    """
    Manages all student profiles and adjusts learning difficulty.
    Persists data to a JSON file.
    """
    def __init__(self):
        self.student_profiles: Dict[str, StudentProfile] = {}
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.storage_file = os.path.join(project_root, 'student_profiles.json')
        self._load_profiles()

    def _load_profiles(self):
        """Loads student profiles from the JSON storage file if it exists."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    profiles_data = json.load(f)
                    for student_id, data in profiles_data.items():
                        profile = StudentProfile(student_id, data['name'])
                        profile.current_difficulty = data['current_difficulty']
                        profile.performance_history = data['performance_history']
                        profile.sentiment_history = data.get('sentiment_history', []) # For backwards compatibility
                        self.student_profiles[student_id] = profile
                print(f"Loaded {len(self.student_profiles)} student profiles from {self.storage_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading profiles from {self.storage_file}: {e}. Starting with empty profiles.")
                self.student_profiles = {}

    def _save_profiles(self):
        """Saves all student profiles to the JSON storage file."""
        profiles_to_save = {
            student_id: profile.to_dict()
            for student_id, profile in self.student_profiles.items()
        }
        with open(self.storage_file, 'w') as f:
            json.dump(profiles_to_save, f, indent=4)

    def get_or_create_profile(self, student_id: str, name: str = "New Student") -> StudentProfile:
        """Retrieves an existing student profile or creates a new one."""
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = StudentProfile(student_id, name)
            self._save_profiles()
        return self.student_profiles[student_id]

    def update_performance(self, student_id: str, performance_score: float) -> int:
        """
        Updates a student's performance and adjusts difficulty.
        Score should be between 0.0 (poor) and 1.0 (excellent).
        """
        profile = self.get_or_create_profile(student_id)
        profile.performance_history.append(performance_score)

        # Dynamic Difficulty Adjustment Algorithm
        if performance_score > 0.8 and profile.current_difficulty < 5:
            profile.current_difficulty = min(5, profile.current_difficulty + 1)
        elif performance_score < 0.4 and profile.current_difficulty > 1:
            profile.current_difficulty = max(1, profile.current_difficulty - 1)
        
        self._save_profiles()
        return profile.current_difficulty

    def log_sentiment(self, student_id: str, sentiment_data: dict):
        """Logs a sentiment analysis result to a student's profile."""
        profile = self.get_or_create_profile(student_id)
        profile.sentiment_history.append(sentiment_data)
        self._save_profiles()

    def get_profile_data(self, student_id: str) -> dict:
        """Returns the full profile data for a student."""
        if student_id in self.student_profiles:
            return self.student_profiles[student_id].to_dict()
        return {"error": "Student not found"}