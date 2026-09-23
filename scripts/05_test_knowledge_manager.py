from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.knowledge_manager import KnowledgeManager

km = KnowledgeManager()

documents = km.load_all()

print()

print(documents[0])

print()

print(documents[-1])