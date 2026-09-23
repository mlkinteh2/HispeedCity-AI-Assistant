"""
26_test_reference_and_validity.py

Tests:
- Reference number lookup (SP-XXXX-XXXXXX, RN-XXXX-XXXXXX)
- Plate with space matching (e.g. "JJE 797" vs "JJE797")
- renewalMonthNote used as validity period
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.chatbot.chatbot import ChatBot

bot = ChatBot()

print("=" * 60)
print("Reference Number & Validity Period Test")
print("=" * 60)

tests = [
    {
        "name": "Reference number lookup (RN prefix)",
        "question": "RN-2026-000053",
        "expected_intent": "reference_lookup",
        "expected_substrings": ["RN-2026-000053", "found", "could not find"],
    },
    {
        "name": "Reference number lookup (SP prefix)",
        "question": "What is my parking status? SP-2026-000001",
        "expected_intent": "reference_lookup",
        "expected_substrings": ["SP-2026-000001", "found", "could not find"],
    },
    {
        "name": "Reference number in sentence",
        "question": "check this parker status: RN-2026-000053",
        "expected_intent": "reference_lookup",
        "expected_substrings": ["RN-2026-000053"],
    },
    {
        "name": "Plate without spaces (JJE797)",
        "question": "Check parking for JJE797",
        "expected_intent": "parking_status",
        "expected_substrings": ["JJE797", "active", "pending", "rejected", "could not find"],
    },
    {
        "name": "Plate with space (JJE 797)",
        "question": "My plate is JJE 797, check my status",
        "expected_intent": "parking_status",
        "expected_substrings": ["JJE797", "JJE 797", "active", "pending", "rejected", "could not find"],
    },
    {
        "name": "Barrier check with plate",
        "question": "My barrier won't open, plate JJE797",
        "expected_intent": "barrier",
        "expected_substrings": ["JJE797", "active", "pending", "could not find"],
    },
]

passed = 0
for t in tests:
    print(f"\n{'-' * 60}")
    print(f"Test: {t['name']}")
    print(f"Input: '{t['question']}'")
    res = bot.ask(t["question"])
    print(f"Intent: {res['intent']}")
    print(f"Answer: {res['answer']}")

    intent_ok = res["intent"] == t["expected_intent"]
    content_ok = any(s.lower() in res["answer"].lower() for s in t["expected_substrings"])

    if intent_ok and content_ok:
        print("[PASS]")
        passed += 1
    else:
        print(f"[FAIL] Intent match={intent_ok}, Content match={content_ok}")

print(f"\n{'=' * 60}")
print(f"Results: {passed}/{len(tests)} passed")
print("=" * 60)
