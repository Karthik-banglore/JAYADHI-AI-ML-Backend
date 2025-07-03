# JAYADHI AI for ALL – Frontend API Integration Guide

## Base URL  
http://localhost:5001

---
## Authentication & CORS

Our backend is configured to accept JSON and allow cross-origin requests from any origin (including your React dev server on `localhost:3000`):

This CORS setup is a professional security practice that grants your React app permission to call our AI services.

- All endpoints accept `application/json`
- CORS is enabled for all origins: CORS(app, resources={r”/api/”: {“origins”: “”}})


## Available Endpoints

### 1. AI Tutor Chatbot ✅ WORKING  
**Endpoint:** POST `/api/chatbot`  
**Purpose:** Conversational AI assistance with emotional awareness and generative, kid-friendly answers for AI/ML questions.

**Request**  

{
“student_id”: “test_001”,
“message”: “I feel stuck”,
“topic”: “general” //optional
}
**Test Command:**
curl -X POST -H "Content-Type: application/json" -d '{"student_id":"test_001","message":"I feel stuck"}' http://localhost:5001/api/chatbot

**Verified Response:**
{
  "emotion_detected": "negative",
  "reply": "I\u2019m sorry you\u2019re feeling stuck. Let\u2019s tackle it together\u2014what part is most confusing?",
  "student_id": "test_001",
  "tone": "empathetic",
  "topic": "general"
}

**Request (AI/ML-related, Generative Example)**

{
  "student_id": "test_001",
  "message": "What is AI?",
  "topic": "general"
}

**Test Command**
   curl -X POST -H "Content-Type: application/json" \
  -d '{"student_id":"test_001","message":"What is AI?","topic":"general"}' \
  http://localhost:5001/api/chatbot
**Verified Response:**
{
  "emotion_detected": "informative",
  "reply": "Hey there, curious kiddo! Ever wished your toys could think and do things on their own? Well, that's kind of what AI is all about!\n\n**AI stands for Artificial Intelligence.** It's like giving computers a brain, so they can learn, solve problems, and make decisions, just like you do!\n\nImagine you have a super smart **dog** that can learn tricks.\n\n*   First, you **TEACH** it something: \"Sit!\"\n*   Then, the dog **PRACTICES** and learns what \"Sit\" means.\n*   Finally, when you say \"Sit,\" the dog **KNOWS** what to do!\n\nAI is similar! We teach computers using lots of information, then they practice, and eventually, they can do things like:\n\n*   **Understand what you say:** Like Siri or Alexa on your parent's phone. They listen to your questions and try to answer them!\n*   **Recognize pictures:** Like when you take a photo and the phone knows it's a picture of a cat or a dog.\n*   **Play games:** Some video games use AI to make the characters you are playing against smarter each time you play!\n\nSo, AI is all about making computers smart and capable so they can help us with all sorts of things! It's a bit like magic, but it's real, and it's changing the world!",
  "student_id": "test_001",
  "tone": "generative",
  "topic": "general"
}

NOTES: 
- The endpoint automatically detects if the message is about AI/ML and switches to generative mode.
- For all other topics, it uses template-based, emotionally aware replies.
-No request/response format changes are needed for the frontend.

### 2. Sentiment Analysis ✅ WORKING

**Endpoint:** `POST /api/sentiment`
**Purpose:** Detect emotional tone of a student’s message.

**Request**  

{
“student_id”: “test_001”,
“message”: “I am confused”
}

**Test Command:**
curl -X POST -H "Content-Type: application/json" \
  -d '{"student_id":"test_001", "message":"I am confused"}' \
  http://localhost:5001/api/sentiment

**Verified Response:**
{“emotion”: “negative”,
“scores”: {
    “compound”: -0.3182,
    “neg”: 0.535,
    “neu”: 0.465,
    “pos”: 0.0
    },
    “suggested_tone”: “empathetic”
}
### 3. Adaptive Difficulty ✅ WORKING

**Endpoint:** `GET /api/difficulty/<student_id>`
**Purpose:**  Retrieve current difficulty level for personalized challenges.

**Test Command:**
curl -X GET http://localhost:5001/api/difficulty/test_001

**Verified Response:**
{
  "difficulty_level": 4,
  "student_id": "test_001"
}

### 4. Performance Tracking ✅ WORKING

**Endpoint:** `POST /api/performance`
**Purpose:** Log a student’s score and automatically adjust difficulty.

**Request**
{
“student_id”: “test_001”,
“score”: 85
}

**Test Command:**
curl -X POST -H "Content-Type: application/json" \
  -d '{"student_id":"test_001", "score":85}' \
  http://localhost:5001/api/performance

**verified response**
{
  "message": "Performance updated successfully",
  "new_difficulty": 5
}


## Frontend Integration Examples

### React Components

const API_BASE_URL = ‘http://localhost:5001’;
// Chatbot
async function chatWithBot(studentId, message, topic = ‘general’) {
    const res = await fetch(`${API_BASE_URL}/api/chatbot`, {
        method: ‘POST’,

        headers: { ‘Content-Type’: ‘application/json’ },
        body: JSON.stringify({
            student_id: studentId,
            message: message,
            topic: topic
            })
            });
            return res.json();  //response.json()
            };

// Sentiment Analysis
async function analyzeSentiment(studentId, message) {
    const res = await fetch(`${API_BASE_URL}/api/sentiment`, {
        method: ‘POST’,
        headers: { ‘Content-Type’: ‘application/json’ },
        body: JSON.stringify({ student_id: studentId, message })
        });
        return res.json();
        };

// Get Difficulty

    async function 
    getDifficulty(studentId) {
        const res = await fetch(`${API_BASE_URL}/api/difficulty/${studentId}`);
        return res.json();
        }

// Update Performance
async function updatePerformance(studentId, score) {
    const res = await fetch(`${API_BASE_URL}/api/performance`, {
        method: ‘POST’,
        headers: { ‘Content-Type’: ‘application/json’ },
        body: JSON.stringify({ student_id: studentId, score })
        });
        return res.json();
        }


---

## Educational Games Integration Readiness

The AI backend supports five core modules:

1. **What Is AI?** – Interactive quiz with chatbot hints  
2. **Machine Learning 101** – Fruit classification using the Fruits-360 subset  
3. **Data Detective** – Data cleaning puzzle with sentiment assistance  
4. **Train Your Bot** – Pattern recognition training & adaptive difficulty  
5. **Neural Network Maze** – Visual maze illustrating neural network layers  

---

 NOTE: To enable immediate integration and testing. All endpoints are CORS-enabled and return clear JSON responses. For any issues, contact the AI/ML team .


Next: Step-by-Step Project Completion Plan
1.	Fruit Classifier Game: Curate a diverse dataset, train the model, integrate `/api/game/fruit/classify`.
2.	“What Is AI?” Quiz: Build interactive quiz with sentiment-aware hints.
3.	“Data Detective” Puzzle: Implement data-cleaning game with adaptive difficulty.
4.	“Train Your Bot” Simulator: Develop pattern-recognition game.
5.	“Neural Network Maze”: Create visual neural-network navigation game.
6.	Teacher Dashboard: Aggregate class analytics and reports.
7.	Production Deployment: Containerize, secure, and deploy our backend and frontend.

---
**Date:2 July 2025(Updates)**

### Fruit Classifier Game API Integration Guide

Base URL:
`http://localhost:5001`
1. Get Fruit Classes
**Endpoint**
`GET /api/game/fruit/classes`
**Description**
**Fetches a list of all fruit names the AI model can recognize. Use this to dynamically build the UI buttons or dropdown for user guesses.
**Request**
No request body or parameters.
**Response** (200 OK)
A JSON array of unique, sorted fruit names (strings). Example:
[
  "Apple",
  "Banana",
  "Beans",
  "Blackberrie",
  "Cabbage",
  "Carrot",
  "Cherry",
  "Cucumber",
  "Pear",
  "Tomato"
]

**Error Responses**
`500 Internal Server Error` if the model or class list is not loaded.
{ "error": "Fruit classes not available" }

**Frontend Usage Example (JavaScript)**
async function getFruitClasses() {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/classes`);
  if (!res.ok) throw new Error('Failed to fetch fruit classes');
  return res.json();
}

2. Get Random Fruit Challenge
**Endpoint**
`GET /api/game/fruit/random`
**Description**
Returns a random fruit test image (base64 encoded) and its correct simple name. This starts a new game round.
**Request**
No request body or parameters.
**Response** (200 OK)
A JSON object with the following fields:
{
  "display_name": "Apple",
  "image_data": "image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
`display_name`: The correct answer for this image (e.g., “Apple”).
`image_data`: Base64-encoded JPEG image string, ready to use as an `<img>` src.
**Error Responses**
`500 Internal Server Error` if the model or images are unavailable.
`404 Not Found` if no test images exist for the selected class.
**Example**
{ "error": "No test images found for class: Apple 10" }

**Frontend Usage Example (JavaScript)**

```javascript
async function getRandomFruitChallenge() {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/random`);
  if (!res.ok) throw new Error('Failed to fetch random fruit challenge');
  return res.json();
}
```
3. Submit a Guess
**Endpoint**
`POST /api/game/fruit/classify`
**Description**
Sends the current challenge image and the student’s guess to the backend for classification and feedback.
**Request Body (JSON)**

{
  "image_data": "image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",  // The image string from `/random`
  "guess": "Apple"  // The student's guess (must be one of the display names)
}

**Response (200 OK)**

{
  "predicted_label": "Apple",
  "confidence": 0.9987,
  "is_correct": true,
  "educational_message": "Correct! Did you know there are over 7,500 varieties of apples grown worldwide?"
}

`predicted_label`: The AI’s top prediction (simple name).
`confidence`: Model confidence (0 to 1).
`is_correct`: True if the student’s guess matches the AI’s prediction.
`educational_message`: A fun fact or encouragement based on correctness.

**Error Responses**
`400 Bad Request` if `image_data` or `guess` is missing.
`500 Internal Server Error` if the model is unavailable.

**Example:**
{ "error": "Request must contain 'image_data' and 'guess'" }

**Frontend Usage Example (JavaScript)**
async function submitGuess(imageData, guess) {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_ imageData, guess: guess })
  });
  if (!res.ok) throw new Error('Failed to submit guess');
  return res.json();
}

**NOTE:** 
## All endpoints expect and return JSON.
## CORS is enabled for all `/api/*` endpoints, so your frontend can call these APIs directly from `localhost:3000` or any other origin.
## Image data is base64-encoded JPEG strings to avoid file upload complexities.
## Display names are simplified (e.g., `"Apple"`) even if the internal model classes are more specific (e.g., `"Apple 10"`).
**RESULTS:**
```bash
kend % curl http://localhost:5001/api/game/fruit/classes

[
  "Apple",
  "Banana",
  "Beans",
  "Blackberrie",
  "Cabbage",
  "Cherry",
  "Cucumber",
  "Tomato",
  "carrot",
  "pear"
]
```
## The backend compares the student’s guess with the model’s prediction in a case-insensitive substring match to allow flexible matching.

