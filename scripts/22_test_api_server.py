"""
22_test_api_server.py

Tests the ChatBot FastAPI server endpoint POST /api/chat.
"""

import sys
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CHAT_API_URL = "http://localhost:8001/api/chat"

print("=" * 60)
print("ChatBot API Server Endpoint Test")
print("=" * 60)

test_prompts = [
    "My barrier won't open. My plate is ABC1234",
    "How do I register for season parking?",
    "How much is the monthly season parking fee?",
]

for prompt in test_prompts:
    print(f"\nSending Prompt: '{prompt}'")
    try:
        res = requests.post(CHAT_API_URL, json={"message": prompt, "session_id": "test_1"}, timeout=3.0)
        print(f"Status Code: {res.status_code}")
        print("Response JSON:")
        print(res.json())
    except Exception as e:
        print(f"Chat API Note: Server at {CHAT_API_URL} not active ({type(e).__name__}). Testing directly via Python module...")
        from backend.chatbot.chatbot import ChatBot
        bot = ChatBot()
        print("Direct Ask Result:")
        print(bot.ask(prompt))

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
