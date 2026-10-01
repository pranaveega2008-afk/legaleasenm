"""Comprehensive test suite for LegalEase backend and frontend communication."""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("==================================================")
    print("RUNNING LEGALEASE AUTOMATED TEST SUITE")
    print("==================================================")

    # 1. GET /
    print("\n[TEST 1] Testing Root Endpoint: GET /")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.json()}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert r.json().get("service") == "LegalEase", "Service name mismatch"
        print(">>> PASS: Root endpoint is functioning correctly.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 2. GET /health
    print("\n[TEST 2] Testing Health Endpoint: GET /health")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.json()}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert r.json().get("status") == "healthy", "Health status mismatch"
        print(">>> PASS: Health check endpoint returned healthy.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 3. GET /docs
    print("\n[TEST 3] Testing Interactive Docs: GET /docs")
    try:
        r = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"Status Code: {r.status_code}")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print(">>> PASS: Swagger UI documentation is accessible.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 4. POST /ask with empty question (Validation error)
    print("\n[TEST 4] Testing Validation: POST /ask with empty question")
    try:
        r = requests.post(f"{BASE_URL}/ask", json={"question": "   ", "context": "None"}, timeout=5)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.json()}")
        assert r.status_code == 400, f"Expected 400, got {r.status_code}"
        print(">>> PASS: Empty question correctly rejected with 400 Bad Request.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 5. POST /ask with missing required question field (Pydantic validation)
    print("\n[TEST 5] Testing Pydantic Schema Validation: POST /ask missing question field")
    try:
        r = requests.post(f"{BASE_URL}/ask", json={"context": "Some context"}, timeout=5)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.json()}")
        assert r.status_code == 422, f"Expected 422, got {r.status_code}"
        print(">>> PASS: Missing question correctly rejected by Pydantic with 422 Unprocessable Entity.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 6. POST /ask with unconfigured Gemini API key (Error handling)
    print("\n[TEST 6] Testing Gemini Unconfigured Key Handling: POST /ask with empty API key")
    try:
        r = requests.post(f"{BASE_URL}/ask", json={"question": "What is a contract?"}, timeout=5)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.json()}")
        assert r.status_code == 500, f"Expected 500, got {r.status_code}"
        assert "Gemini API key is not configured" in r.json().get("detail", ""), "Expected API key error message"
        print(">>> PASS: Handled missing API key gracefully without crashing backend.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    # 7. Backend connection error handling simulation
    print("\n[TEST 7] Testing Backend Unavailable Simulation (Streamlit logic)")
    try:
        non_existent_url = "http://127.0.0.1:9999"
        try:
            requests.get(f"{non_existent_url}/health", timeout=1)
            print(">>> FAIL: Should have raised ConnectionError")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print(">>> PASS: Connection error successfully caught and identified as expected.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        sys.exit(1)

    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! (7/7)")
    print("==================================================")

if __name__ == "__main__":
    test_endpoints()
