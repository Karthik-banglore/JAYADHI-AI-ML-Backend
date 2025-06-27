import logging
import json
from datetime import datetime
from typing import Dict, Any
import os

class AISystemLogger:
    """
    Comprehensive logging system for AI/ML backend.
    """

    def __init__(self, log_dir: str = "logs"):
        """Initialize logger with separate log files."""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Setup different loggers for different purposes
        self.api_logger = self._setup_logger('api', 'api_requests.log')
        self.sentiment_logger = self._setup_logger('sentiment', 'sentiment_analysis.log')
        self.performance_logger = self._setup_logger('performance', 'student_performance.log')
        self.error_logger = self._setup_logger('errors', 'errors.log')

    def _setup_logger(self, name: str, filename: str) -> logging.Logger:
        """Setup individual logger with file handler."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        handler = logging.FileHandler(os.path.join(self.log_dir, filename))
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def log_api_request(self, endpoint: str, method: str, student_id: str = None,
                       response_code: int = 200, response_time: float = 0.0):
        """Log API request details."""
        log_data = {
            'endpoint': endpoint,
            'method': method,
            'student_id': student_id,
            'response_code': response_code,
            'response_time_ms': round(response_time * 1000, 2)
        }
        self.api_logger.info(json.dumps(log_data))

    def log_sentiment_analysis(self, student_id: str, message: str, emotion: str,
                              vader_compound: float, processing_time: float):
        """Log sentiment analysis results."""
        log_data = {
            'student_id': student_id,
            'message_length': len(message),
            'detected_emotion': emotion,
            'vader_compound_score': vader_compound,
            'processing_time_ms': round(processing_time * 1000, 2)
        }
        self.sentiment_logger.info(json.dumps(log_data))

    def log_performance_update(self, student_id: str, score: float,
                              old_difficulty: int, new_difficulty: int):
        """Log student performance and difficulty adjustments."""
        log_data = {
            'student_id': student_id,
            'performance_score': score,
            'difficulty_change': {
                'from': old_difficulty,
                'to': new_difficulty,
                'adjustment': new_difficulty - old_difficulty
            }
        }
        self.performance_logger.info(json.dumps(log_data))

    def log_error(self, error_type: str, error_message: str, student_id: str = None,
                  endpoint: str = None, stack_trace: str = None):
        """Log errors and exceptions."""
        log_data = {
            'error_type': error_type,
            'error_message': error_message,
            'student_id': student_id,
            'endpoint': endpoint,
            'stack_trace': stack_trace
        }
        self.error_logger.error(json.dumps(log_data))

    def log_teacher_alert(self, student_id: str, alert_type: str,
                         sentiment_pattern: str, recommendation: str):
        """Log teacher intervention alerts."""
        log_data = {
            'alert_type': 'TEACHER_INTERVENTION',
            'student_id': student_id,
            'alert_reason': alert_type,
            'sentiment_pattern': sentiment_pattern,
            'recommendation': recommendation
        }
        self.error_logger.warning(json.dumps(log_data))

# Global logger instance
ai_logger = AISystemLogger()