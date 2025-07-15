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

```json
{
“student_id”: “test_001”,
“message”: “I feel stuck”,
“topic”: “general” //optional
}
```

**Test Command:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"student_id":"test_001","message":"I feel stuck"}' http://localhost:5001/api/chatbot
```

**Verified Response:**

```json
{
  "emotion_detected": "negative",
  "reply": "I\u2019m sorry you\u2019re feeling stuck. Let\u2019s tackle it together\u2014what part is most confusing?",
  "student_id": "test_001",
  "tone": "empathetic",
  "topic": "general"
}
```

**Request (AI/ML-related, Generative Example)**

```json
{
  "student_id": "test_001",
  "message": "What is AI?",
  "topic": "general"
}
```

**Test Command**

```bash
curl -X POST -H "Content-Type: application/json" \
 -d '{"student_id":"test_001","message":"What is AI?","topic":"general"}' \
 http://localhost:5001/api/chatbot
```

**Verified Response:**

```json
{
  "emotion_detected": "informative",
  "reply": "Hey there, curious kiddo! Ever wished your toys could think and do things on their own? Well, that's kind of what AI is all about!\n\n**AI stands for Artificial Intelligence.** It's like giving computers a brain, so they can learn, solve problems, and make decisions, just like you do!\n\nImagine you have a super smart **dog** that can learn tricks.\n\n* First, you **TEACH** it something: \"Sit!\"\n* Then, the dog **PRACTICES** and learns what \"Sit\" means.\n* Finally, when you say \"Sit,\" the dog **KNOWS** what to do!\n\nAI is similar! We teach computers using lots of information, then they practice, and eventually, they can do things like:\n\n* **Understand what you say:** Like Siri or Alexa on your parent's phone. They listen to your questions and try to answer them!\n* **Recognize pictures:** Like when you take a photo and the phone knows it's a picture of a cat or a dog.\n* **Play games:** Some video games use AI to make the characters you are playing against smarter each time you play!\n\nSo, AI is all about making computers smart and capable so they can help us with all sorts of things! It's a bit like magic, but it's real, and it's changing the world!",
  "student_id": "test_001",
  "tone": "generative",
  "topic": "general"
}
```

**NOTES:**

- The endpoint automatically detects if the message is about AI/ML and switches to generative mode.
- For all other topics, it uses template-based, emotionally aware replies.
  -No request/response format changes are needed for the frontend.

### 2. Sentiment Analysis ✅ WORKING

**Endpoint:** `POST /api/sentiment`
**Purpose:** Detect emotional tone of a student’s message.

**Request**

```json
{
“student_id”: “test_001”,
“message”: “I am confused”
}
```

**Test Command:**

```bash
curl -X POST -H "Content-Type: application/json" \
 -d '{"student_id":"test_001", "message":"I am confused"}' \
 http://localhost:5001/api/sentiment
```

**Verified Response:**

```json
{
  "emotion": "negative",
  "scores": {
    "compound": -0.3182,
    "neg": 0.535,
    "neu": 0.465,
    "pos": 0.0
  },
  "suggested_tone": "empathetic"
}
```

### 3. Adaptive Difficulty ✅ WORKING

**Endpoint:** `GET /api/difficulty/<student_id>`
**Purpose:** Retrieve current difficulty level for personalized challenges.

**Test Command:**

```bash
curl -X GET http://localhost:5001/api/difficulty/test_001
```

**Verified Response:**

```json
{
  "difficulty_level": 4,
  "student_id": "test_001"
}
```

### 4. Performance Tracking ✅ WORKING

**Endpoint:** `POST /api/performance`
**Purpose:** Log a student’s score and automatically adjust difficulty.

**Request**

```json
{
“student_id”: “test_001”,
“score”: 85
}
```

**Test Command:**

```bash
curl -X POST -H "Content-Type: application/json" \
 -d '{"student_id":"test_001", "score":85}' \
 http://localhost:5001/api/performance
```

**verified response**

```json
{
  "message": "Performance updated successfully",
  "new_difficulty": 5
}
```

## Frontend Integration Examples

### React Components

```javascript
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
```

---

## Educational Games Integration Readiness

The AI backend supports five core modules:

1. **What Is AI?** – Interactive quiz with chatbot hints
2. **Machine Learning 101** – Fruit classification using the Fruits-360 subset
3. **Data Detective** – Data cleaning puzzle with sentiment assistance
4. **Train Your Bot** – Pattern recognition training & adaptive difficulty
5. **Neural Network Maze** – Visual maze illustrating neural network layers

---

**NOTE:** To enable immediate integration and testing. All endpoints are CORS-enabled and return clear JSON responses. For any issues, contact the AI/ML team .

## Next: Step-by-Step Project Completion Plan

1. Fruit Classifier Game: Curate a diverse dataset, train the model, integrate `/api/game/fruit/classify`.
2. “What Is AI?” Quiz: Build interactive quiz with sentiment-aware hints.
3. “Data Detective” Puzzle: Implement data-cleaning game with adaptive difficulty.
4. “Train Your Bot” Simulator: Develop pattern-recognition game.
5. “Neural Network Maze”: Create visual neural-network navigation game.
6. Teacher Dashboard: Aggregate class analytics and reports.
7. Production Deployment: Containerize, secure, and deploy our backend and frontend.

---

## Date: 2 July 2025 (Updates)

### 5 Fruit Classifier Game API Integration Guide

**Base URL:** `http://localhost:5001`

**5.1 Get Fruit Classes**
**Endpoint:** `GET /api/game/fruit/classes`
**Description:** Fetches a list of all fruit names the AI model can recognize. Use this to dynamically build the UI buttons or dropdown for user guesses.
**Request:** No request body or parameters.
**Response (200 OK):** A JSON array of unique, sorted fruit names (strings). Example:

```json
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
```

**Error Responses:**
`500 Internal Server Error` if the model or class list is not loaded.

```json
{ "error": "Fruit classes not available" }
```

**Frontend Usage Example (JavaScript):**

```javascript
async function getFruitClasses() {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/classes`);
  if (!res.ok) throw new Error("Failed to fetch fruit classes");
  return res.json();
}
```

**5.2 Get Random Fruit Challenge**
**Endpoint:** `GET /api/game/fruit/random`
**Description:** Returns a random fruit test image (base64 encoded) and its correct simple name. This starts a new game round.
**Request:** No request body or parameters.
**Response (200 OK):** A JSON object with the following fields:

```json
{
  "display_name": "Apple",
  "image_data": "image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```

- `display_name`: The correct answer for this image (e.g., “Apple”).
- `image_data`: Base64-encoded JPEG image string, ready to use as an `<img>` src.

**Error Responses:**

- `500 Internal Server Error` if the model or images are unavailable.
- `404 Not Found` if no test images exist for the selected class.
  **Example:**

```json
{ "error": "No test images found for class: Apple 10" }
```

**Frontend Usage Example (JavaScript):**

```javascript
async function getRandomFruitChallenge() {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/random`);
  if (!res.ok) throw new Error("Failed to fetch random fruit challenge");
  return res.json();
}
```

**5.3 Submit a Guess**
**Endpoint:** `POST /api/game/fruit/classify`
**Description:** Sends the current challenge image and the student’s guess to the backend for classification and feedback.

**Request Body (JSON):**
`json
    {
    "image_data": "image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...", 
    "guess": "Apple"
    }
    `

**Response (200 OK):**
`json
    {
    "predicted_label": "Apple",
    "confidence": 0.9987,
    "is_correct": true,
    "educational_message": "Correct! Did you know there are over 7,500 varieties of apples grown worldwide?"
    }
    `

- `predicted_label`: The AI’s top prediction (simple name).
- `confidence`: Model confidence (0 to 1).
- `is_correct`: True if the student’s guess matches the AI’s prediction.
- `educational_message`: A fun fact or encouragement based on correctness.

**Error Responses:**

- `400 Bad Request` if `image_data` or `guess` is missing.
- `500 Internal Server Error` if the model is unavailable.

**Example:**

```json
{ "error": "Request must contain 'image_data' and 'guess'" }
```

**Frontend Usage Example (JavaScript):**

```javascript
async function submitGuess(imageData, guess) {
  const res = await fetch(`${API_BASE_URL}/api/game/fruit/classify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_data: imageData, guess: guess }),
  });
  if (!res.ok) throw new Error("Failed to submit guess");
  return res.json();
}
```

**NOTE:**

- All endpoints expect and return JSON.
- CORS is enabled for all `/api/*` endpoints, so your frontend can call these APIs directly from `localhost:3000` or any other origin.
- Image data is base64-encoded JPEG strings to avoid file upload complexities.
- Display names are simplified (e.g., `"Apple"`) even if the internal model classes are more specific (e.g., `"Apple 10"`).

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

- The backend compares the student’s guess with the model’s prediction in a case-insensitive substring match to allow flexible matching.

---

## Date: 3 July 2025 (Updates)

### 1. Chatbot Upgradation

(mentioned above)

### 6. Prompt Evaluator Game

**Endpoint:** `POST /api/game/prompt-evaluator`

**Purpose:** Let students practice writing prompts for creative AI tasks. The backend (powered by an LLM) evaluates their prompt for clarity, creativity, and fit, and gives a score and feedback.

**Request:**

```json
{
  "level": "easy",
  "task_index": 0,
  "user_prompt": "Draw a cute cat flying a big red kite in the sky."
}
```

**Test Command:**

```bash
curl -X POST http://localhost:5001/api/game/prompt-evaluator \
-H "Content-Type: application/json" \
-d '{"level":"easy","task_index":0,"user_prompt":"Draw a cute cat flying a big red kite in the sky."}'
```

**Response:**

```json
{
  "task": "You wake up and can talk to animals. What do you say to your pet?",
  "result": "25%",
  "feedback": "This prompt doesn’t follow the instruction of creating a story about waking up and talking to animals. While it’s creative and clear on its own, it completely misses the point of the original assignment. To fix this, the prompt needs to include waking up, talking to animals, and a pet. For example: \"I wake up and my dog is staring at me. I can suddenly understand him! What do I say?\""
}
```

**Sample Prompt Tasks by Level:**

- **easy:**
  - "You wake up and can talk to animals. What do you say to your pet?"
  - "Describe your dream treehouse. What does it look like?"
  - "Write a story about a magic pencil that brings drawings to life."
- **moderate:**
  - "You find a treasure map in your backyard. What happens next?"
  - "You discover a secret door in your school. Where does it lead?"
  - "Write about a day when everything in your house is upside down."
- **hard:**
  - "You are the world’s youngest astronaut and get to fly to the moon. Describe your space trip."
  - "You invent a robot that does your homework. What goes wrong?"
  - "Write a journal entry from the point of view of a time traveler who visits 100 years into the future."

### 7. Pattern Predictor Game

**Endpoint:** `POST /api/game/pattern-predictor`

**Purpose:** Students give a sequence of three numbers. The backend (powered by an LLM) predicts the next number and explains the logic in a kid-friendly way.

**Request:**

```json
{
  "sequence": [10, 20, 30]
}
```

**Response:**

```json
{
  "next_number": 40,
  "reasoning": "The sequence increases by 10 with each subsequent number (10, 20, 30…). Therefore, the next number is 30 + 10 = 40."
}
```

**Test Command:**

```bash
curl -X POST http://localhost:5001/api/game/pattern-predictor \
-H "Content-Type: application/json" \
-d '{"sequence":[10, 20, 30]}'
```

---

## Date: 12 July 2025 (Updates)

## 8. Data Detective Game

### 8.1 Get Messy Dataset

**Endpoint:** `GET /api/game/data-detective/dataset/<difficulty>`

**Purpose:** Fetches a “messy” dataset for the specified difficulty (`easy`, `medium`, `hard`). Used to present students with data-cleaning challenges.

**Example Request:**

```bash
curl http://localhost:5001/api/game/data-detective/dataset/easy | jq .
```

**Example Response:**

```json
{
  "columns": ["student_id", "name", "age", "grade", "test_score", "attendance"],
  "data": [
    {
      "age": 12,
      "attendance": 0.95,
      "grade": "7th",
      "name": "Alice Johnson",
      "student_id": "STU001",
      "test_score": 85.0
    },
    {
      "age": 13,
      "attendance": 0.88,
      "grade": "8th",
      "name": "Bob Smith",
      "student_id": "STU002",
      "test_score": 92.0
    },
    {
      "age": 14,
      "attendance": 0.92,
      "grade": "9th",
      "name": "Carol Davis",
      "student_id": "STU003",
      "test_score": null
    },
    {
      "age": 25,
      "attendance": 0.85,
      "grade": "8",
      "name": "David Wilson",
      "student_id": "STU004",
      "test_score": 88.0
    },
    {
      "age": 12,
      "attendance": 1.5,
      "grade": "7th",
      "name": "Emma Brown",
      "student_id": "STU005",
      "test_score": 95.0
    },
    {
      "age": 13,
      "attendance": 0.89,
      "grade": "8th",
      "name": "Frank Miller",
      "student_id": "STU006",
      "test_score": 150.0
    },
    {
      "age": 14,
      "attendance": 0.94,
      "grade": "9th",
      "name": "Grace Lee",
      "student_id": "STU007",
      "test_score": 78.0
    },
    {
      "age": 13,
      "attendance": 0.91,
      "grade": "8th",
      "name": "Henry Chen",
      "student_id": "STU008",
      "test_score": 82.0
    },
    {
      "age": 12,
      "attendance": 0.87,
      "grade": "7th",
      "name": "Ivy Taylor",
      "student_id": "STU009",
      "test_score": 90.0
    },
    {
      "age": 11,
      "attendance": 0.93,
      "grade": "6th",
      "name": "Jack Moore",
      "student_id": "STU010",
      "test_score": 87.0
    }
  ],
  "dataset_name": "easy_student_data",
  "difficulty": "easy",
  "expected_issues_count": 5,
  "instructions": "Examine this easy dataset and identify data quality issues.",
  "total_rows": 10
}
```

**Example JavaScript Implementation:**

```javascript
async function getMessyDataset(difficulty) {
  const res = await fetch(`/api/game/data-detective/dataset/${difficulty}`);
  if (!res.ok) throw new Error("Failed to fetch dataset");
  return res.json();
}
```

### 8.2 Validate Identified Issues

**Endpoint:** `POST /api/game/data-detective/validate`

**Purpose:** Submits the list of issues a student found in the dataset. The backend checks them against the answer key and returns a score, feedback, and missed issues.

**Example Request:**

```bash
curl -X POST http://localhost:5001/api/game/data-detective/validate \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty":"easy",
    "student_id":"demo_stu",
    "identified_issues":[
      {"type":"outlier","column":"age"},
      {"type":"formatting","column":"grade"},
      {"type":"missing_value","column":"test_score"}
    ]
  }' | jq .
```

**Actual Output:**

```json
{
  "score_percentage": 60.0,
  "issues_found": 3,
  "total_issues": 5,
  "found_issues": [
    {
      "type": "outlier",
      "column": "age",
      "explanation": "Age 25 is too old for elementary school students"
    },
    {
      "type": "formatting",
      "column": "grade",
      "explanation": "Grade format should be consistent (e.g., 8th, not 8)"
    },
    {
      "type": "missing_value",
      "column": "test_score",
      "explanation": "Missing test scores need to be handled"
    }
  ],
  "missed_issues": [
    {
      "type": "impossible_value",
      "column": "test_score",
      "explanation": "Test scores should be between 0-100",
      "hint": "Remove or verify the data entry"
    },
    {
      "type": "impossible_value",
      "column": "attendance",
      "explanation": "Attendance rate cannot exceed 100% (1.0)",
      "hint": "Check if this should be 0.15 or remove"
    }
  ],
  "overall_feedback": "Good job! You caught several key issues.",
  "educational_tip": "Data cleaning is like detective work—search for clues that something looks off!",
  "difficulty": "easy"
}
```

**Example JavaScript Implementation:**

```javascript
async function validateIdentifiedIssues(
  difficulty,
  studentId,
  identifiedIssues
) {
  const res = await fetch("/api/game/data-detective/validate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      difficulty: difficulty,
      student_id: studentId,
      identified_issues: identifiedIssues,
    }),
  });
  return res.json();
}
```

**API Call:**

```bash
 POST /api/game/data-detective/validate \
  --data '{"difficulty":"easy","student_id":"demo_stu","identified_issues":[{"type":"outlier","column":"age"},{"type":"formatting","column":"grade"},{"type":"missing_value","column":"test_score"}]}' --jq .
```

### 8.3 Data Detective Help

**Endpoint:** `GET /api/game/data-detective/help`

**Purpose:** Returns a summary of the types of data issues students should look for, plus actionable tips.

**Example Request:**

```bash
curl http://localhost:5001/api/game/data-detective/help | jq .
```

**Actual Output:**

```json
{
  "game_objective": "Learn to identify common data quality issues",
  "tips": [
    "Check each column for unusual or missing values",
    "Look for values that don't make sense",
    "Ensure all entries follow the same format",
    "Pay attention to outliers and inconsistencies"
  ],
  "types_of_issues": [
    { "description": "Empty or null fields", "type": "missing_value" },
    { "description": "Values far outside the normal range", "type": "outlier" },
    { "description": "Inconsistent data formats", "type": "formatting" },
    {
      "description": "Values that cannot logically occur",
      "type": "impossible_value"
    },
    { "description": "Mixed uppercase/lowercase", "type": "case_inconsistency" }
  ]
}
```

**Example JavaScript Implementation:**

```javascript
async function getDataDetectiveHelp() {
  const res = await fetch("/api/game/data-detective/help");
  if (!res.ok) throw new Error("Failed to fetch help info");
  return res.json();
}
```

**Example command**

```bash
api call GET /api/game/data-detective/help --jq .
```

## Date: 14 July 2025 (Updates)

## 9. AI Quiz Game

### 9.1 Get Quiz Question

**Endpoint:**  
`GET /api/game/quiz/question/<difficulty>`

**Purpose:**  
Fetches a random quiz question for the specified difficulty (`beginner`, `intermediate`, `advanced`). Returns a session ID for tracking the question.

**Test Command:**

```bash
curl http://localhost:5001/api/game/quiz/question/beginner | jq .
```

**Actual Output:**

```json
{
  "difficulty": "beginner",
  "hint_available": true,
  "id": "ai_003",
  "options": [
    "To replace all humans",
    "To make machines that can think and learn",
    "To create robots only",
    "To make computers faster"
  ],
  "question": "What is the main goal of AI?",
  "session_id": "session_8496"
}
```

**JavaScript Implementation:**

```javascript
async function getQuizQuestion(difficulty) {
  const res = await fetch(`/api/game/quiz/question/${difficulty}`);
  if (!res.ok) throw new Error("Failed to fetch quiz question");
  return res.json();
}
```

**Example Command:**

```bash
 GET /api/game/quiz/question/beginner --jq .
```

### 9.2 Submit Quiz Answer

**Endpoint:**  
`POST /api/game/quiz/answer`

**Purpose:**  
Submit a student's answer for the current quiz session and receive feedback with sentiment-aware responses.

**Test Command:**

```bash
curl -X POST http://localhost:5001/api/game/quiz/answer \
  -H "Content-Type: application/json" \
  -d '{"session_id":"session_8496","selected_answer":2,"student_id":"test_student"}' | jq .
```

**Actual Output:**

```json
{
  "correct_answer": 1,
  "correct_option": "To make machines that can think and learn",
  "difficulty": "beginner",
  "educational_fact": "AI systems can now beat humans at chess, Go, poker, and many video games, but they still struggle with common sense reasoning.",
  "explanation": "AI aims to create machines that can perform tasks requiring intelligence, like learning, reasoning, and problem-solving.",
  "feedback": "Not quite, but good thinking! AI aims to create machines that can perform tasks requiring intelligence, like learning, reasoning, and problem-solving.",
  "is_correct": false
}
```

**JavaScript Implementation:**

```javascript
async function submitQuizAnswer(sessionId, selectedAnswer, studentId) {
  const res = await fetch("/api/game/quiz/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      selected_answer: selectedAnswer,
      student_id: studentId,
    }),
  });
  return res.json();
}
```

**Example Command:**

```bash
 POST /api/game/quiz/answer \
  --data '{"session_id":"session_8496","selected_answer":2,"student_id":"test_student"}' --jq .
```

### 9.3 Get Quiz Hint

**Endpoint:**  
`POST /api/game/quiz/hint`

**Purpose:**  
Get an AI-generated hint for the current quiz question session when students are struggling.

**Test Command:**

```bash
curl -X POST http://localhost:5001/api/game/quiz/hint \
  -H "Content-Type: application/json" \
  -d '{"session_id":"session_8496","student_message":"I am stuck"}' | jq .
```

**Actual Output:**

```json
{
  "encouragement": "Take your time and think through each option carefully!",
  "hint": "Okay, here's a little hint to help you with the AI question, without giving it away!\n\nThink about what makes a robot or computer seem smart, like a person. Is it real, or is it something we *make* to seem real? ðŸ˜‰",
  "tone": "generative"
}
```

**JavaScript Implementation:**

```javascript
async function getQuizHint(sessionId, studentMessage) {
  const res = await fetch("/api/game/quiz/hint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      student_message: studentMessage,
    }),
  });
  return res.json();
}
```

** Command:**

```bash
 POST /api/game/quiz/hint \
  --data '{"session_id":"session_8496","student_message":"I am stuck"}' --jq .
```

## 10. Teacher Dashboard & Analytics

### 10.1 Class Overview

**Endpoint:**  
`GET /api/teacher/class-overview`

**Purpose:**  
Provides a summary of all students' performance and sentiment.

**Test Command:**

```bash
curl http://localhost:5001/api/teacher/class-overview | jq .
```

**Actual Output:**

```json
{
  "difficulty_distribution": {
    "1": 0,
    "2": 2,
    "3": 1,
    "4": 0,
    "5": 0
  },
  "emotional_summary": {
    "negative": 0,
    "neutral": 3,
    "positive": 0
  },
  "students_needing_attention": [],
  "timestamp": "2025-07-13T17:23:45.635829",
  "total_students": 3
}
```

**JavaScript Implementation:**

```javascript
async function getClassOverview() {
  const res = await fetch("/api/teacher/class-overview");
  if (!res.ok) throw new Error("Failed to fetch class overview");
  return res.json();
}
```

**Example Command:**

```bash
 GET /api/teacher/class-overview --jq .
```

### 10.2 Individual Student Report

**Endpoint:**  
`GET /api/teacher/student/<student_id>`

**Purpose:**  
Get detailed analytics for a specific student.

**Test Command:**

```bash
curl http://localhost:5001/api/teacher/student/demo_stu | jq .
```

**Actual Output:**

```json
{
  "current_status": {
    "difficulty_level": 3,
    "performance_trend": "stable"
  },
  "raw_data": {
    "performance_history": [0.6],
    "sentiment_history": []
  },
  "recommendations": [],
  "statistics": {
    "average_performance": 0.6,
    "total_assessments": 1
  },
  "student_id": "demo_stu",
  "timestamp": "2025-07-13T17:24:12.554103"
}
```

**JavaScript Implementation:**

```javascript
async function getStudentReport(studentId) {
  const res = await fetch(`/api/teacher/student/${studentId}`);
  if (!res.ok) throw new Error("Failed to fetch student report");
  return res.json();
}
```

**Example Command:**

```bash
 GET /api/teacher/student/demo_stu --jq .
```

### 10.3 Intervention Alerts

**Endpoint:**  
`GET /api/teacher/alerts`

**Purpose:**  
List students needing intervention.

**Test Command:**

```bash
curl http://localhost:5001/api/teacher/alerts | jq .
```

**Actual Output:**

```json
{
  "alerts": [],
  "total_alerts": 0
}
```

**JavaScript Implementation:**

```javascript
async function getInterventionAlerts() {
  const res = await fetch("/api/teacher/alerts");
  if (!res.ok) throw new Error("Failed to fetch intervention alerts");
  return res.json();
}
```

**Example Command:**

```bash
GET /api/teacher/alerts --jq .
```

## 11. Leaderboard

**Endpoint:**  
`GET /api/leaderboard`

**Purpose:**  
Get student XP rankings.

**Test Command:**

```bash
curl http://localhost:5001/api/leaderboard | jq .
```

**Actual Output:**

```json
[
  {
    "name": "New Student",
    "rank": 1,
    "student_id": "demo_stu",
    "xp": 60
  },
  {
    "name": "New Student",
    "rank": 2,
    "student_id": "student001",
    "xp": 25
  },
  {
    "name": "New Student",
    "rank": 3,
    "student_id": "test_student",
    "xp": 0
  }
]
```

**JavaScript Implementation:**

```javascript
async function getLeaderboard() {
  const res = await fetch("/api/leaderboard");
  if (!res.ok) throw new Error("Failed to fetch leaderboard");
  return res.json();
}
```

**Example Command:**

```bash
 GET /api/leaderboard --jq .
```

## 12. Explainability Module

**Endpoint:**  
`GET /api/explainability/<student_id>`

**Purpose:**  
Explain why the AI adjusted a student's difficulty level.

**Test Command:**

```bash
curl http://localhost:5001/api/explainability/demo_stu | jq .
```

**Actual Output:**

```json
{
  "current_difficulty": 3,
  "explanation": "The student's difficulty is currently level 3. This level reflects their moderate performance, allowing for steady progress without overwhelming them.",
  "performance_data_points": 1,
  "student_id": "demo_stu"
}
```

**JavaScript Implementation:**

```javascript
async function getExplainability(studentId) {
  const res = await fetch(`/api/explainability/${studentId}`);
  if (!res.ok) throw new Error("Failed to fetch explainability");
  return res.json();
}
```

**Example Command:**

```bash
 GET /api/explainability/demo_stu --jq .
```

---

**All endpoints above are tested and verified with actual backend responses. Ready for frontend integration**
