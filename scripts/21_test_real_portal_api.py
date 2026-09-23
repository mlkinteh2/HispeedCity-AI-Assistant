"""
21_test_real_portal_api.py

Tests the live portal vehicle status API endpoint GET /api/parking/status/{vehicle_plate}.
"""

import sys
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PORTAL_API_URL = "http://localhost:8000/api/parking/status"

print("=" * 60)
print("Real Portal Status API Endpoint Test")
print("=" * 60)

test_plates = ["ABC1234", "WXY1234", "JVP8886", "UNKNOWN999"]

for plate in test_plates:
    url = f"{PORTAL_API_URL}/{plate}"
    print(f"\nQuerying: {url}")
    try:
        res = requests.get(url, timeout=3.0)
        print(f"Status Code: {res.status_code}")
        print("Response JSON:")
        print(res.json())
    except Exception as e:
        print(f"API Connection Note: Could not connect to live portal server at {url} ({type(e).__name__}).")
        print("Ensure 'python -m uvicorn server:app --reload' is running inside parking-registration/backend.")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
