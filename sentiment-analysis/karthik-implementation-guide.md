# Implementation Guide: AI Personalization & Sentiment Server

This guide provides instructions for setting up and interacting with the AI server. This is the central hub for student personalization.

---

## 1. Environment Setup

First, ensure you have Python 3.8+ installed. Then, set up a virtual environment and install the required packages.

```bash
# 1. Navigate to the project directory
cd /path/to/JAYADHI AI for ALL Project/

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# 4. Install the required packages
pip install -r requirements.txt
```

## 2. Running the Server

To start the API server, run the `api_server.py` script from your terminal.

```bash
python api_server.py
```

You should see output indicating the server is running on `http://127.0.0.1:5000`. When you make API calls, a `student_profiles.json` file will be created automatically.

## 3. API Endpoints for Teammates

You can use tools like `curl` or Postman to test the APIs.

### 3.1. Get Sentiment Analysis (For Anoop - Chatbot)

Send a `POST` request with the student's ID and their message.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"student_id": "anoop_test_01", "message": "I am finding this a bit too difficult"}' http://127.0.0.1:5000/api/sentiment
```

### 3.2. Get Game Difficulty (For Anangsha - Games)

Send a `GET` request with the student's ID.

```bash
curl http://127.0.0.1:5000/api/difficulty/anangsha_test_01
```

### 3.3. Update Performance Data (For Anangsha - Games)

Send a `POST` request with the student's ID and their score (from 0 to 100).

```bash
curl -X POST -H "Content-Type: application/json" -d '{"student_id": "anangsha_test_01", "score": 35}' http://127.0.0.1:5000/api/performance
```