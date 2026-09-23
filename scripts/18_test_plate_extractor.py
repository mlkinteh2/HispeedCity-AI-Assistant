"""
18_test_plate_extractor.py

Tests the vehicle plate extractor utility.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.plate_extractor import VehiclePlateExtractor

extractor = VehiclePlateExtractor()

test_cases = [
    ("My plate is ABC1234", "ABC1234"),
    ("ABC1234 barrier won't open", "ABC1234"),
    ("Plate number: WXY1234", "WXY1234"),
    ("My car plate is JVP 8886", "JVP8886"),
    ("Plate: JVP 8886", "JVP8886"),
    ("WXY 1234", "WXY1234"),
    ("Is my parking active for JHG5678?", "JHG5678"),
    ("My plate is KLM 9012", "KLM9012"),
    ("Is my parking active?", None),
    ("My barrier won't open. Plate UNKNOWN999.", None),
    ("How much is parking?", None),

    ("What is ANPR?", None),
]

print("=" * 60)
print("Vehicle Plate Extractor Test")
print("=" * 60)

passed = 0
total = len(test_cases)

for query, expected in test_cases:
    result = extractor.extract(query)
    status = "PASS" if result == expected else "FAIL"
    if result == expected:
        passed += 1
    print(f"[{status}] Query: '{query}' -> Extracted: {result} (Expected: {expected})")

print("=" * 60)
print(f"Result: {passed}/{total} tests passed.")
print("=" * 60)

assert passed == total, f"Only {passed}/{total} tests passed."
