import re
from typing import Dict, Any, Optional

class RequestValidator:
    """
    Validates API requests for security and data integrity.
    """

    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """Validates student ID format."""
        if not student_id or len(student_id) < 3 or len(student_id) > 50:
            return False
        # Allow alphanumeric and underscores only
        return bool(re.match(r'^[a-zA-Z0-9_]+$', student_id))

    @staticmethod
    def validate_message(message: str) -> bool:
        """Validates student message content."""
        if not message or len(message.strip()) == 0:
            return False
        # Reasonable length limits
        if len(message) > 1000:
            return False
        return True

    @staticmethod
    def validate_performance_score(score: Any) -> bool:
        """Validates performance score is numeric and in range."""
        try:
            score_float = float(score)
            return 0 <= score_float <= 100
        except (ValueError, TypeError):
            return False

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Basic input sanitization."""
        if not isinstance(text, str):
            return ""
        # Remove potential script injections
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    @classmethod
    def validate_sentiment_request(cls, data: Dict[str, Any]) -> Optional[str]:
        """Validates sentiment analysis request data."""
        if not data:
            return "Request body cannot be empty"
        if 'student_id' not in data:
            return "Missing required field: student_id"
        if 'message' not in data:
            return "Missing required field: message"
        if not cls.validate_student_id(data['student_id']):
            return "Invalid student_id format"
        if not cls.validate_message(data['message']):
            return "Invalid message content"
        return None  # No validation errors

    @classmethod
    def validate_performance_request(cls, data: Dict[str, Any]) -> Optional[str]:
        """Validates performance update request data."""
        if not data:
            return "Request body cannot be empty"
        if 'student_id' not in data:
            return "Missing required field: student_id"
        if 'score' not in data:
            return "Missing required field: score"
        if not cls.validate_student_id(data['student_id']):
            return "Invalid student_id format"
        if not cls.validate_performance_score(data['score']):
            return "Invalid score: must be number between 0-100"
        return None  # No validation errors