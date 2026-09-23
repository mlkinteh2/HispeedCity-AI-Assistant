"""
19_test_chatbot_portal_integration.py

Tests the end-to-end ChatBot integration with the HispeedCity Portal system and vehicle plate extraction.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.chatbot.chatbot import ChatBot

bot = ChatBot()

print("=" * 60)
print("ChatBot Portal Integration Test")
print("=" * 60)

test_scenarios = [
    {
        "name": "1. Barrier issue with plate (ABC1234)",
        "question": "My barrier won't open. My plate is ABC1234",
        "expected_intent": "barrier",
        "expected_substrings": ["active and valid", "could not find a parking record"]
    },
    {
        "name": "2. Barrier issue with plate (WXY1234)",
        "question": "My barrier won't open. Plate WXY1234.",
        "expected_intent": "barrier",
        "expected_substrings": ["expired", "could not find a parking record"]
    },
    {
        "name": "3. Barrier issue with Unknown plate (UNKNOWN999)",
        "question": "My barrier won't open. Plate UNKNOWN999.",
        "expected_intent": "barrier",
        "expected_substrings": ["could not find a parking record"]
    },
    {
        "name": "4. Barrier issue without plate",
        "question": "My barrier won't open",
        "expected_intent": "barrier",
        "expected_substrings": ["May I have your vehicle plate number"]
    },
    {
        "name": "5. Parking Status with plate (JHG5678)",
        "question": "Is my parking still valid? Plate JHG 5678",
        "expected_intent": "parking_status",
        "expected_substrings": ["currently active", "could not find a parking record"]
    },
    {
        "name": "6. Parking Status without plate",
        "question": "When does my parking expire?",
        "expected_intent": "parking_status",
        "expected_substrings": ["May I have your vehicle plate number"]
    },
    {
        "name": "7. Registration query (Portal link)",
        "question": "How do I register my car?",
        "expected_intent": "registration",
        "expected_substrings": ["https://www.hispeedcity.com/index.html"]
    },
    {
        "name": "8. FAQ Pricing query",
        "question": "How much is the monthly season parking fee?",
        "expected_intent": "pricing",
        "expected_substrings": ["Reserved RM212/month"]
    }
]

passed_count = 0

for test in test_scenarios:
    print("\n" + "-" * 60)
    print(f"Scenario: {test['name']}")
    print(f"Question: '{test['question']}'")
    res = bot.ask(test["question"])
    print(f"Detected Intent: {res['intent']}")
    print(f"Answer:\n{res['answer']}")

    match_intent = res["intent"] == test["expected_intent"]
    match_content = any(sub.lower() in res["answer"].lower() for sub in test["expected_substrings"])

    if match_intent and match_content:
        print("[RESULT: PASS]")
        passed_count += 1
    else:
        print(f"[RESULT: FAIL] Expected substring not found or intent mismatch.")

print("\n" + "=" * 60)
print(f"Portal Integration Test Summary: {passed_count}/{len(test_scenarios)} Passed")
print("=" * 60)

assert passed_count == len(test_scenarios), f"Only {passed_count}/{len(test_scenarios)} scenarios passed."

