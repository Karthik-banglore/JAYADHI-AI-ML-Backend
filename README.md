# JAYADHI AI for ALL - AI/ML Backend

This repository contains the AI/ML backend for the JAYADHI Educational Platform. It provides sentiment analysis, personalization, and adaptive learning algorithms for students in grades 5-10.

## Team Members
- **Karthik**: Personalization & Sentiment Analysis (`/sentiment-analysis`)
- **Anoop**: Chatbot Engineer (`/chatbot-engine`)
- **Anangsha**: Game Logic Developer (`/game-logic`)
- **Tanuja**: Data Curator (`/data-curation`)
- **Dipantu**: Explainability & Testing Lead (`/tests`)
- **Anshika**: AI Support Intern (`/docs`)

---

## Quick Start

To run the core sentiment and personalization server:

```bash
pip install -r sentiment-analysis/requirements.txt
python sentiment-analysis/api_server.py
```

## Core API Endpoints
- `POST /api/sentiment` - Analyzes sentiment for chatbot messages.
- `GET /api/difficulty/<student_id>` - Retrieves dynamic difficulty levels for games.
- `POST /api/performance` - Tracks and updates student performance from games.