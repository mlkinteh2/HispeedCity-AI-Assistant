"""
23_test_session_memory.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.chatbot.chatbot import ChatBot

bot = ChatBot()

print("=" * 60)
print("Conversational Memory Test")
print("=" * 60)

context = {}

print("User: My barrier won't open")
res1 = bot.ask("My barrier won't open", context=context)
if res1.get("intent"):
    context["intent"] = res1["intent"]
print(f"Bot: {res1['answer']}")

print("\nUser: JJE797")
res2 = bot.ask("JJE797", context=context)
if res2.get("vehicle_plate"):
    context["vehicle_plate"] = res2["vehicle_plate"]
print(f"Bot: {res2['answer']}")

print("\nUser: Is it expired?")
# Here we expect the bot to remember JJE797 and check status
res3 = bot.ask("Is it expired?", context=context)
print(f"Bot: {res3['answer']}")
print(f"Intent detected: {res3['intent']}")

if res3.get("vehicle_plate") == "JJE797":
    print("\n[PASS] Memory successfully carried forward!")
else:
    print("\n[FAIL] Memory was not carried forward.")
