import unittest
import json
import time
import os
import sys

from sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.personalization_engine import PersonalizationEngine
from sentiment_analysis.validators import RequestValidator

class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for sentiment analysis functionality."""

    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_basic_sentiment_analysis(self):
        """Test basic sentiment analysis functionality."""
        # Test positive sentiment
        result = self.analyzer.analyze("I love this lesson!")
        self.assertEqual(result['emotion'], 'positive')
        self.assertIn('vader_scores', result)
        self.assertIn('textblob_scores', result)

        # Test negative sentiment
        result = self.analyzer.analyze("This is too difficult and frustrating")
        self.assertEqual(result['emotion'], 'negative')

        # Test neutral sentiment
        result = self.analyzer.analyze("The lesson is about mathematics")
        self.assertEqual(result['emotion'], 'neutral')

    def test_educational_context_sentiment(self):
        """Test sentiment analysis with educational context."""
        educational_messages = [
            ("I need help with this problem", 'neutral'),
            ("This is confusing me", 'negative'),
            ("I understand it now, thanks!", 'positive'),
            ("Can you explain this again?", 'neutral'),
            ("I hate this subject", 'negative')
        ]

        for message, expected_emotion in educational_messages:
            with self.subTest(message=message):
                result = self.analyzer.analyze(message)
                self.assertEqual(result['emotion'], expected_emotion,
                               f"Failed for message: '{message}'")

    def test_performance_timing(self):
        """Test sentiment analysis performance."""
        start_time = time.time()
        self.analyzer.analyze("This is a test message for performance timing")
        end_time = time.time()

        processing_time = end_time - start_time
        self.assertLess(processing_time, 0.1, "Sentiment analysis too slow")

class TestPersonalizationEngine(unittest.TestCase):
    """Test cases for student personalization functionality."""

    def setUp(self):
        self.engine = PersonalizationEngine()
        # Use test storage file
        self.engine.storage_file = "test_student_profiles.json"

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.engine.storage_file):
            os.remove(self.engine.storage_file)

    def test_student_profile_creation(self):
        """Test creating new student profiles."""
        profile = self.engine.get_or_create_profile("test_student_001", "Test Student")

        self.assertEqual(profile.student_id, "test_student_001")
        self.assertEqual(profile.name, "Test Student")
        self.assertEqual(profile.current_difficulty, 3)  # Default difficulty
        self.assertEqual(len(profile.performance_history), 0)
        self.assertEqual(len(profile.sentiment_history), 0)

    def test_difficulty_adjustment(self):
        """Test dynamic difficulty adjustment algorithms."""
        # Test difficulty increase for high performance
        new_difficulty = self.engine.update_performance("test_student_002", 0.9)
        self.assertEqual(new_difficulty, 4)  # Should increase from 3 to 4

        # Test difficulty decrease for poor performance
        new_difficulty = self.engine.update_performance("test_student_002", 0.2)
        self.assertEqual(new_difficulty, 3)  # Should decrease back to 3

    def test_sentiment_logging(self):
        """Test sentiment data logging functionality."""
        sentiment_data = {
            'emotion': 'positive',
            'vader_scores': {'compound': 0.6},
            'text': 'I love this!'
        }

        self.engine.log_sentiment("test_student_003", sentiment_data)
        profile = self.engine.get_or_create_profile("test_student_003")

        self.assertEqual(len(profile.sentiment_history), 1)
        self.assertEqual(profile.sentiment_history[0]['emotion'], 'positive')

class TestRequestValidator(unittest.TestCase):
    """Test cases for input validation."""

    def test_student_id_validation(self):
        """Test student ID format validation."""
        self.assertTrue(RequestValidator.validate_student_id("student_001"))
        self.assertFalse(RequestValidator.validate_student_id("ab"))  # Too short
        self.assertFalse(RequestValidator.validate_student_id("student@test"))

    def test_message_validation(self):
        """Test message content validation."""
        self.assertTrue(RequestValidator.validate_message("Hello, I need help"))
        self.assertFalse(RequestValidator.validate_message("   "))
        self.assertFalse(RequestValidator.validate_message("x" * 1001))

    def test_performance_score_validation(self):
        """Test performance score validation."""
        self.assertTrue(RequestValidator.validate_performance_score(85))
        self.assertFalse(RequestValidator.validate_performance_score(101))
        self.assertFalse(RequestValidator.validate_performance_score("invalid"))

    def test_request_validation(self):
        """Test complete request validation."""
        valid_request = {"student_id": "test_01", "message": "This is a test"}
        self.assertIsNone(RequestValidator.validate_sentiment_request(valid_request))

        invalid_request = {"student_id": "test_01"}
        self.assertIsNotNone(RequestValidator.validate_sentiment_request(invalid_request))

if __name__ == '__main__':
    unittest.main(verbosity=2)