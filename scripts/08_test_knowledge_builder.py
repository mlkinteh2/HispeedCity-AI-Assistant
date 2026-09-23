from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.knowledge.knowledge_builder import KnowledgeBuilder
from backend.models.knowledge import Knowledge

kb = KnowledgeBuilder()

kb.add(

    Knowledge(

        id="FAQ001",

        category="Pricing",

        question="How much is reserved parking?",

        answer="Reserved parking costs RM212/month.",

        source="FAQ"

    )

)

print("Knowledge Records:", kb.total())

print()

print(kb.get_all()[0])