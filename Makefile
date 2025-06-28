.PHONY: install run test-api clean

# Define variables for paths
PYTHON = python3
VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip
PYTHON_VENV = $(VENV_DIR)/bin/python
API_SERVER = sentiment-analysis/api_server.py
REQUIREMENTS_FILE = requirements.txt

# Default target
all: install run

# Target to set up the virtual environment and install dependencies
install:
	@echo "Setting up virtual environment and installing dependencies..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS_FILE)
	@echo "Installation complete."

# Target to run the Flask API server
run:
	@echo "Starting Flask API server..."
	$(PYTHON_VENV) $(API_SERVER) &
	@echo "Flask server started in the background. Check logs for details."

# Target to run automated curl tests for API endpoints
test-api:
	@echo "Running automated API tests (curl)..."
	# Give the server a moment to start if it was just launched
	sleep 5
	@echo "Testing /sentiment/analyze endpoint..."
	curl -X POST -H "Content-Type: application/json" -d '{"text": "This is a great learning experience!"}' http://localhost:5000/sentiment/analyze
	@echo "\nTesting /personalization/difficulty endpoint..."
	curl http://localhost:5000/personalization/difficulty?student_id=test_student_1
	@echo "\nTesting /personalization/performance endpoint..."
	curl -X POST -H "Content-Type: application/json" -d '{"student_id": "test_student_1", "activity_id": "math_quiz_1", "score": 90, "time_taken_seconds": 120}' http://localhost:5000/personalization/performance
	@echo "\nAPI tests (curl) complete."

test-python-api:
	@echo "Running automated API tests (Python script)..."
	$(PYTHON_VENV) test_api_endpoints.py
	@echo "API tests (Python script) complete."


# Target to clean up the virtual environment and cache files
clean:
	@echo "Cleaning up virtual environment and cache files..."
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	@echo "Cleanup complete."
