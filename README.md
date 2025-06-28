# JAYADHI Educational Platform: AI/ML Backend

## Project Overview and Mission

The JAYADHI Educational Platform aims to revolutionize personalized learning through advanced AI and Machine Learning. Our mission is to create an adaptive and engaging educational experience by leveraging sentiment analysis, intelligent chatbots, and dynamic game logic to cater to individual student needs and optimize learning outcomes.

This repository houses the core AI/ML backend services that power the JAYADHI platform.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Git:** For cloning the repository and version control.
*   **Python 3.8+:** Our backend is built with Python.
*   **Node.js (LTS recommended):** Required for the Google Gemini CLI.
*   **npm (Node Package Manager):** Comes with Node.js, used for installing Gemini CLI.
*   **Google Gemini CLI:** Used for interacting with the Gemini API. Install it globally:
    ```bash
    npm install -g @google/generative-ai-cli
    ```
*   **Make:** A build automation tool used for streamlining development tasks.

## Team Structure and Responsibilities

Our 6-person AI/ML team is structured with clear roles and dedicated working areas within this repository to facilitate efficient collaboration.

*   **Karthik (Lead & Sentiment Analysis):**
    *   **Working Area:** `sentiment-analysis/`
    *   **Responsibilities:** Core sentiment analysis engine development, personalization engine integration, API server management.
*   **Anoop (Chatbot Development):**
    *   **Working Area:** `chatbot-engine/`
    *   **Responsibilities:** Developing and integrating the AI chatbot, consuming sentiment analysis APIs.
*   **Anangsha (Game Logic Implementation):**
    *   **Working Area:** `game-logic/`
    *   **Responsibilities:** Implementing adaptive game logic, integrating with personalization and performance data APIs.
*   **[Team Member 4] (AI Support/General ML):**
    *   **Working Area:** `ai-support/`
    *   **Responsibilities:** General AI/ML model development, supporting various platform features.
*   **[Team Member 5] (Data Curation):**
    *   **Working Area:** `data-curation/`
    *   **Responsibilities:** Managing data pipelines, ensuring data quality for ML models.
*   **[Team Member 6] (Explainability/Monitoring):**
    *   **Working Area:** `explainability/`
    *   **Responsibilities:** Developing tools for model explainability and performance monitoring.

## Technical Architecture Documentation

The JAYADHI AI/ML Backend operates around a central API server that orchestrates various AI/ML functionalities.

**Conceptual Architecture:**

```
+---------------------+       +---------------------+
|                     |       |                     |
|   Student/Teacher   |       |   External Systems  |
|     Frontends       |       |    (e.g., LMS)      |
|                     |       |                     |
+----------+----------+       +----------+----------+
           |                              |
           | (API Calls)                  | (Data Sync/APIs)
           v                              v
+-----------------------------------------------------+
|                                                     |
|             **Central API Server**                  |
|             (e.g., `sentiment-analysis/api_server.py`) |
|             - Routes requests                       |
|             - Orchestrates services                 |
|                                                     |
+----------+----------+----------+----------+----------+
           |          |          |          |          |
           |          |          |          |          |
           v          v          v          v          v
+----------+----------+ +--------+---------+ +--------+---------+ +--------+---------+
|                     | |                   | |                   | |                   |
|  Sentiment Analysis | | Personalization   | |   Chatbot Engine  | |   Game Logic      |
|  (`sentiment-analysis/`) | (`sentiment-analysis/`) | (`chatbot-engine/`) | (`game-logic/`)   |
|                     | |                   | |                   | |                   |
+---------------------+ +-------------------+ +-------------------+ +-------------------+
           ^
           | (Data/Model Interaction)
           |
+----------+----------+
|                     |
|    Data Curation    |
|    (`data-curation/`)   |
|                     |
+---------------------+
```

**Key Components:**

*   **Central API Server:** The primary interface for all frontend and internal service communication. It dispatches requests to specialized modules like sentiment analysis and personalization.
*   **Sentiment Analysis Module:** Processes text input to determine sentiment, providing insights for personalized feedback and adaptive learning paths.
*   **Personalization Engine:** Utilizes sentiment data and student performance to tailor content, difficulty, and recommendations.
*   **Chatbot Engine:** Integrates with the API server to provide interactive, AI-driven conversational support.
*   **Game Logic:** Manages the adaptive difficulty and content within educational games, receiving input from the personalization engine and submitting performance data.
*   **Data Curation:** Responsible for collecting, cleaning, and preparing data for training and evaluating AI/ML models.

## Automated Workflow Instructions

We utilize `Makefile` to streamline common development tasks. Ensure you have `make` installed on your system.

*   **Install Dependencies:**
    ```bash
    make install
    ```
    This command will install all required Python dependencies from `requirements.txt` into your virtual environment.
*   **Run API Server:**
    ```bash
    make run
    ```
    This command will start the main API server (e.g., `sentiment-analysis/api_server.py`). The server will typically run in the background.
*   **Run Tests (cURL):**
    ```bash
    make test-api
    ```
    This command will execute basic API tests using cURL.

*   **Run Tests (Python Script):**
    ```bash
    make test-python-api
    ```
    This command will execute comprehensive API tests using the `test_api_endpoints.py` script.

*   **Clean Up:**
    ```bash
    make clean
    ```
    This command will remove the virtual environment and cache files.

## Git Collaboration Guidelines

To maintain a clean and efficient codebase, please adhere to the following Git workflow standards:

1.  **Feature Branches:** All new features, bug fixes, or significant changes must be developed on a dedicated feature branch.
    *   Branch naming convention: `feature/<your-feature-name>`, `bugfix/<issue-description>`, `refactor/<area-of-refactor>`.
    *   Always branch off `main`.
2.  **Commit Messages:** Write clear, concise, and descriptive commit messages.
    *   Start with a verb in the imperative mood (e.g., "Add", "Fix", "Refactor").
    *   Keep the subject line short (under 50 characters).
    *   Provide a more detailed body if necessary, explaining *why* the change was made.
3.  **Pull Requests (PRs):**
    *   Once your feature branch is complete and tested, open a Pull Request to merge it into `main`.
    *   Provide a clear description of the changes, including any relevant issue numbers.
    *   Ensure all automated tests pass before requesting a review.
4.  **Code Reviews:**
    *   Assign at least one team member for code review.
    *   Address all review comments promptly.
    *   Do not merge your own PRs.
5.  **Conflict Resolution:** Resolve any merge conflicts locally before pushing your changes.

## API Integration Documentation

This section provides key API endpoints for team members to integrate their components.

### Sentiment Analysis API (Example Endpoints)

*   **Endpoint:** `/sentiment/analyze`
    *   **Method:** `POST`
    *   **Description:** Analyzes the sentiment of provided text.
    *   **Request Body (JSON):**
        ```json
        {
            "text": "The student is very engaged and learning quickly."
        }
        ```
    *   **Response Body (JSON):**
        ```json
        {
            "sentiment": "positive",
            "score": 0.95
        }
        ```

### Personalization Engine API (Example Endpoints)

*   **Endpoint:** `/personalization/difficulty`
    *   **Method:** `GET`
    *   **Description:** Retrieves recommended difficulty adjustment for a student.
    *   **Query Parameters:** `student_id=<ID>`
    *   **Response Body (JSON):**
        ```json
        {
            "student_id": "student123",
            "recommended_difficulty_level": "intermediate"
        }
        ```
*   **Endpoint:** `/personalization/performance`
    *   **Method:** `POST`
    *   **Description:** Submits student performance data for personalization updates.
    *   **Request Body (JSON):**
        ```json
        {
            "student_id": "student123",
            "activity_id": "quiz_math_algebra",
            "score": 85,
            "time_taken_seconds": 300
        }
        ```
    *   **Response Body (JSON):**
        ```json
        {
            "status": "success",
            "message": "Performance data processed."
        }
        ```

## Next Steps for Implementation

To get started with the JAYADHI AI/ML Backend:

1.  Clone this repository:
    ```bash
    git clone https://github.com/Karthik-banglore/JAYADHI-AI-ML-Backend.git
    cd JAYADHI-AI-ML-Backend
    ```
2.  Install dependencies:
    ```bash
    make install
    ```
3.  Start the API server:
    ```bash
    make run
    ```
4.  Begin developing your assigned module!
