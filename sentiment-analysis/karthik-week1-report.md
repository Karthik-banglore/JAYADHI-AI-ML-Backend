# Week 1 Technical Report: AI Personalization & Sentiment Core

**Author:** Karthik B T
**Project:** JAYADHI AI for ALL
**Date:** Week Ending [27-June-2025]

---

## 1. Executive Summary

This week, the foundational AI intelligence layer for the JAYADHI platform was successfully prototyped and implemented. This system delivers two critical capabilities outlined in the project plan: **real-time sentiment analysis** to understand student emotions and a **dynamic personalization engine** to adapt learning difficulty. The system is exposed via a robust API server, ready for integration with the Chatbot (Anoop) and Game Logic (Anangsha) components. A key achievement is the implementation of data persistence, ensuring student profiles and progress are saved between sessions.

## 2. System Components Implemented

### 2.1. Sentiment Analysis System (`sentiment_analyzer.py`)
- **Technology:** Python, VADER, TextBlob, Config-driven thresholds.
- **Functionality:** Analyzes student text input to classify emotion as `positive`, `negative`, or `neutral`. It provides both a simple classification and detailed scores for nuanced understanding. This directly supports the "AI-Powered Virtual Mentor" feature.

### 2.2. Personalization Engine (`personalization_engine.py`)
- **Technology:** Python, JSON for data persistence.
- **Functionality:** Manages comprehensive student profiles, including performance history, sentiment history, and a dynamic difficulty level (1-5 scale). This is the core of the "Adaptive Learning Paths" feature.
- **Algorithm:** A rule-based algorithm adjusts difficulty based on game performance scores:
  - **Score > 80%**: Difficulty increases to maintain challenge.
  - **Score < 40%**: Difficulty decreases to prevent frustration.

### 2.3. API Server (`api_server.py`)
- **Technology:** Python, Flask.
- **Functionality:** A central integration hub with clear, documented endpoints.
  - `POST /api/sentiment`: For the Chatbot team. Receives `{"student_id": "...", "message": "..."}` and returns emotion analysis.
  - `GET /api/difficulty/<student_id>`: For the Games team. Returns the student's current difficulty level.
  - `POST /api/performance`: For the Games team. Receives `{"student_id": "...", "score": ...}` to update a student's profile and adjust difficulty.

## 3. Progress Against Success Metrics

- **Educational Logic Prototype:** **Complete.** The core algorithms for sentiment analysis and difficulty adjustment are implemented.
- **Data Persistence:** **Achieved.** Student profiles are saved to `student_profiles.json`, providing a stateful system ready for future database integration by the full-stack team.
- **Integration Readiness:** **Ready.** The API is live and documented. Coordination with Anoop and Anangsha can begin immediately.
- **Teacher Dashboard Foundation:** **Laid.** By logging both performance and sentiment history, we are now collecting the necessary data for the Teacher Dashboard feature.

## 4. Team Collaboration & Integration Points

The API server acts as the central hub for the AI/ML team. The following integration points are now live and ready for collaboration:

-   **For Anoop (Chatbot Engineer):**
    -   **Endpoint:** `POST /api/sentiment`
    -   **Workflow:** Anoop's chatbot will send the `student_id` and the student's message to this endpoint. My system will analyze the sentiment, log it to the student's profile, and return a structured response with the emotion (`positive`, `negative`, `neutral`) and a suggested response tone (`empathetic`, `encouraging`). This enables the chatbot to react dynamically to student feelings.

-   **For Anangsha (Game Logic Developer):**
    -   **Endpoints:** `GET /api/difficulty/<student_id>` and `POST /api/performance`
    -   **Workflow:**
        1.  Before starting a game, Anangsha's game logic will call `GET /api/difficulty` to fetch the student's current difficulty level (1-5).
        2.  After the game is complete, her logic will call `POST /api/performance` with the student's score. My system will then update the student's profile and adjust the difficulty level for the next game.

-   **For Tanuja (Data Curator) & Full-Stack Team:**
    -   **Artifact:** `student_profiles.json`
    -   **Workflow:** The structure of the student profile, including `performance_history` and `sentiment_history`, is now defined and being populated in the JSON file. This serves as a concrete schema for the Full-Stack team to implement in the official MongoDB/Firestore database.

-   **For Dipantu (Testing Lead):**
    -   **Artifact:** `karthik-implementation-guide.md`
    -   **Workflow:** The API endpoints are stable and documented with `curl` examples. Dipantu can now begin developing automated test scripts to validate the functionality, accuracy, and response times of the sentiment and personalization APIs.

## 5. My Next Steps

- **Team Integration:** Actively work with Anoop and Anangsha to test and integrate their components with the live API endpoints.
- **Algorithm Refinement:** Based on initial testing data, refine the thresholds for difficulty adjustment and sentiment classification.
- **Database Handover:** Coordinate with the Full-Stack team to transition from JSON file storage to the project's central MongoDB/Firestore database.