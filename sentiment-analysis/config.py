# --- General Server Settings ---
DEBUG = True
PORT = 5000

# --- Personalization Engine Settings ---
# The file where student profiles will be saved.
PROFILE_STORAGE_FILE = "student_profiles.json"

# --- Sentiment Analysis Settings ---
# VADER compound score thresholds for classifying emotion.
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05