from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import config

class SentimentAnalyzer:
    """
    A class to analyze the sentiment of a given text using VADER and TextBlob.
    """

    def __init__(self):
        """
        Initializes the VADER sentiment analyzer.
        """
        self.vader_analyzer = SentimentIntensityAnalyzer()

    def classify_emotion(self, compound_score: float) -> str:
        """
        Classifies emotion based on VADER's compound score from the config.
        
        Args:
            compound_score: The compound score from VADER.

        Returns:
            A string representing the emotion ('positive', 'negative', 'neutral').
        """
        if compound_score >= config.POSITIVE_THRESHOLD:
            return 'positive'
        elif compound_score <= config.NEGATIVE_THRESHOLD:
            return 'negative'
        else:
            return 'neutral'

    def analyze(self, text: str) -> dict:
        """
        Analyzes the sentiment of the text and returns a structured result.

        Args:
            text: The input string to analyze.

        Returns:
            A dictionary containing the analysis results from VADER and TextBlob.
        """
        vader_scores = self.vader_analyzer.polarity_scores(text)
        blob = TextBlob(text)
        
        return {
            'text': text,
            'emotion': self.classify_emotion(vader_scores['compound']),
            'vader_scores': vader_scores,
            'textblob_scores': {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
        }