from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.intents.detector import IntentDetector

detector = IntentDetector()

while True:

    question = input("Question: ")

    if question.lower() == "exit":
        break

    print("Intent:", detector.detect(question))
    print("-" * 40)