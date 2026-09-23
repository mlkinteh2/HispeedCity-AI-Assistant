from pathlib import Path
import sys

# ---------------------------------------------------------
# Add project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Import chatbot
# ---------------------------------------------------------

from backend.chatbot.chatbot import ChatBot


# ---------------------------------------------------------
# Start chatbot
# ---------------------------------------------------------

bot = ChatBot()


print("\n")
print("=" * 60)
print("             HispeedCity AI Assistant")
print("=" * 60)

print("\nType 'exit' to quit.\n")


# ---------------------------------------------------------
# Chat loop
# ---------------------------------------------------------

while True:

    question = input("You: ")

    if question.lower().strip() == "exit":

        print("\nGoodbye!")

        break

    result = bot.ask(question)

    print("\nAssistant:")
    print(result["answer"])

    print("\nIntent:", result["intent"])

    print(
        "Confidence:",
        round(result["confidence"], 2)
    )

    print("\n" + "-" * 60)