import requests
import json

BASE_URL = "http://localhost:5000"

def test_sentiment_analysis():
    print("--- Testing Sentiment Analysis Endpoint ---")
    endpoints = {
        "positive": {"text": "I am very happy with my progress today!", "expected_sentiment": "positive"},
        "negative": {"text": "I am struggling with this topic, it's very confusing.", "expected_sentiment": "negative"},
        "neutral": {"text": "The weather is nice today.", "expected_sentiment": "neutral"}
    }

    for emotion, data in endpoints.items():
        try:
            response = requests.post(f"{BASE_URL}/sentiment/analyze", json={"text": data["text"]})
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            result = response.json()

            print(f"Test Case: {emotion.capitalize()} Sentiment")
            print(f"  Input: '{data['text']}'")
            print(f"  Response: {result}")

            assert "sentiment" in result and result["sentiment"] == data["expected_sentiment"], \
                f"FAIL: Expected sentiment '{data['expected_sentiment']}', got '{result.get('sentiment')}'"
            assert "score" in result and isinstance(result["score"], (int, float)), \
                f"FAIL: Expected 'score' to be a number, got '{result.get('score')}'"
            print(f"  SUCCESS: Sentiment for '{emotion}' message is as expected.")

        except requests.exceptions.ConnectionError:
            print(f"  FAIL: Could not connect to the API server at {BASE_URL}. Is the server running?")
        except requests.exceptions.HTTPError as e:
            print(f"  FAIL: HTTP Error for {emotion} sentiment test: {e} - Response: {response.text}")
        except json.JSONDecodeError:
            print(f"  FAIL: Invalid JSON response for {emotion} sentiment test: {response.text}")
        except AssertionError as e:
            print(f"  {e}")
        except Exception as e:
            print(f"  FAIL: An unexpected error occurred for {emotion} sentiment test: {e}")
    print("-" * 50 + "\n")

def test_difficulty_retrieval():
    print("--- Testing Difficulty Retrieval Endpoint ---")
    student_id = "student123"
    try:
        response = requests.get(f"{BASE_URL}/personalization/difficulty?student_id={student_id}")
        response.raise_for_status()
        result = response.json()

        print(f"Test Case: Difficulty Retrieval for Student ID: {student_id}")
        print(f"  Response: {result}")

        assert "student_id" in result and result["student_id"] == student_id, \
            f"FAIL: Expected student_id '{student_id}', got '{result.get('student_id')}'"
        assert "recommended_difficulty_level" in result and isinstance(result["recommended_difficulty_level"], str), \
            f"FAIL: Expected 'recommended_difficulty_level' to be a string, got '{result.get('recommended_difficulty_level')}'"
        print(f"  SUCCESS: Difficulty level retrieved successfully for {student_id}.")

    except requests.exceptions.ConnectionError:
        print(f"  FAIL: Could not connect to the API server at {BASE_URL}. Is the server running?")
    except requests.exceptions.HTTPError as e:
        print(f"  FAIL: HTTP Error for difficulty retrieval test: {e} - Response: {response.text}")
    except json.JSONDecodeError:
        print(f"  FAIL: Invalid JSON response for difficulty retrieval test: {response.text}")
    except AssertionError as e:
        print(f"  {e}")
    except Exception as e:
        print(f"  FAIL: An unexpected error occurred for difficulty retrieval test: {e}")
    print("-" * 50 + "\n")

def test_performance_submission():
    print("--- Testing Performance Submission Endpoint ---")
    performance_data = {
        "student_id": "student123",
        "activity_id": "math_quiz_algebra",
        "score": 95,
        "time_taken_seconds": 180
    }
    try:
        response = requests.post(f"{BASE_URL}/personalization/performance", json=performance_data)
        response.raise_for_status()
        result = response.json()

        print(f"Test Case: Performance Submission")
        print(f"  Input: {performance_data}")
        print(f"  Response: {result}")

        assert "status" in result and result["status"] == "success", \
            f"FAIL: Expected status 'success', got '{result.get('status')}'"
        assert "message" in result and isinstance(result["message"], str), \
            f"FAIL: Expected 'message' to be a string, got '{result.get('message')}'"
        print(f"  SUCCESS: Performance data submitted successfully.")

    except requests.exceptions.ConnectionError:
        print(f"  FAIL: Could not connect to the API server at {BASE_URL}. Is the server running?")
    except requests.exceptions.HTTPError as e:
        print(f"  FAIL: HTTP Error for performance submission test: {e} - Response: {response.text}")
    except json.JSONDecodeError:
        print(f"  FAIL: Invalid JSON response for performance submission test: {response.text}")
    except AssertionError as e:
        print(f"  {e}")
    except Exception as e:
        print(f"  FAIL: An unexpected error occurred for performance submission test: {e}")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    print("Starting API Endpoint Tests...")
    test_sentiment_analysis()
    test_difficulty_retrieval()
    test_performance_submission()
    print("All API Endpoint Tests Completed.")
