# Contributing to JAYADHI AI/ML Backend

We welcome contributions to the JAYADHI Educational Platform AI/ML Backend! This guide will help you get started with setting up your development environment, understanding your working area, and following our collaborative Git workflow.

## Table of Contents

1.  [Cloning the Repository](#1-cloning-the-repository)
2.  [Setting Up Your Development Environment](#2-setting-up-your-development-environment)
3.  [Designated Working Folders](#3-designated-working-folders)
4.  [Git Workflow](#4-git-workflow)
    *   [Feature Branches](#feature-branches)
    *   [Commit Messages](#commit-messages)
    *   [Pull Requests (PRs)](#pull-requests-prs)
    *   [Code Reviews](#code-reviews)
    *   [Conflict Resolution](#conflict-resolution)

---

## 1. Cloning the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/Karthik-banglore/JAYADHI-AI-ML-Backend.git
cd JAYADHI-AI-ML-Backend
```

## 2. Setting Up Your Development Environment

We use a `Makefile` to streamline the setup process. Ensure you have `make` installed on your system.

*   **Install Dependencies:**
    This command will create a Python virtual environment (`venv/`) and install all required Python dependencies from `requirements.txt`.
    ```bash
    make install
    ```

*   **Run API Server:**
    This command will start the main Flask API server (from `sentiment-analysis/api_server.py`) in the background.
    ```bash
    make run
    ```
    You can check the server logs for details.

*   **Run Tests:**
    This command will execute automated API tests for the sentiment, difficulty, and performance endpoints.
    ```bash
    make test-api
    ```

*   **Clean Up:**
    This command will remove the virtual environment and cache files.
    ```bash
    make clean
    ```

## 3. Designated Working Folders

Each team member has a designated primary working folder to organize their contributions. Please focus your development efforts within your assigned directory.

*   **Karthik (Lead & Sentiment Analysis):** `sentiment-analysis/`
    *   Focus: Core sentiment analysis engine, personalization engine, API server.
*   **Anoop (Chatbot Development):** `chatbot-engine/`
    *   Focus: Developing and integrating the AI chatbot.
*   **Anangsha (Game Logic Implementation):** `game-logic/`
    *   Focus: Implementing adaptive game logic, integrating with personalization and performance data.
*   **Tanuja (Data Curation):** `data-curation/`
    *   Focus: Managing data pipelines, ensuring data quality for ML models.
*   **Dipantu (Explainability/Monitoring):** `explainability/`
    *   Focus: Developing tools for model explainability and performance monitoring.
*   **Anshika (AI Support/General ML):** `ai-support/`
    *   Focus: General AI/ML model development, supporting various platform features.

## 4. Git Workflow

We follow a feature branch workflow to ensure a clean and collaborative development process.

### Feature Branches

*   All new features, bug fixes, or significant changes must be developed on a dedicated feature branch.
*   **Branch Naming Convention:**
    *   `feature/<your-feature-name>` (e.g., `feature/add-sentiment-cache`)
    *   `bugfix/<issue-description>` (e.g., `bugfix/fix-api-error`)
    *   `refactor/<area-of-refactor>` (e.g., `refactor/sentiment-module`)
*   Always branch off the `main` branch:
    ```bash
    git checkout main
    git pull origin main # Ensure your main is up-to-date
    git checkout -b feature/your-feature-name
    ```

### Commit Messages

Write clear, concise, and descriptive commit messages.

*   **Subject Line:** Start with a verb in the imperative mood (e.g., "Add", "Fix", "Refactor"). Keep it short (under 50 characters).
*   **Body (Optional):** Provide a more detailed explanation if necessary, focusing on *why* the change was made rather than just *what* was changed.

```
feat: Add user authentication endpoint

- Implemented JWT-based authentication for user login.
- Added /api/auth/login and /api/auth/register endpoints.
- Updated user model to include password hashing.
```

### Pull Requests (PRs)

Once your feature branch is complete and thoroughly tested:

1.  Push your feature branch to the remote repository:
    ```bash
    git push origin feature/your-feature-name
    ```
2.  Go to the GitHub repository page and open a new Pull Request from your feature branch to the `main` branch.
3.  **Provide a clear description** of your changes, including:
    *   What problem does this PR solve?
    *   How was it solved?
    *   Any relevant issue numbers (e.g., `Closes #123`).
    *   Instructions for testing (if applicable).
4.  **Ensure all automated tests pass** before requesting a review.

### Code Reviews

*   Assign at least one team member (preferably someone familiar with the affected area) for code review.
*   Address all review comments promptly.
*   Do not merge your own PRs. A second pair of eyes helps maintain code quality.

### Conflict Resolution

*   If your branch has merge conflicts with `main`, resolve them locally before pushing your changes and requesting a review.
    ```bash
    git checkout feature/your-feature-name
    git pull origin main
    # Resolve conflicts
    git add .
    git commit -m "Resolve merge conflicts"
    git push origin feature/your-feature-name
    ```

Thank you for contributing to the JAYADHI Educational Platform!
