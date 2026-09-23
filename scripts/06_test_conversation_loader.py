from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.conversation_loader import ConversationLoader

loader = ConversationLoader()

docs = loader.load()

print()

print(docs[0].title)

print()

print(docs[0].content[:1500])