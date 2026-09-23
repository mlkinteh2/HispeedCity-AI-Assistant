from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.faq_loader import FAQLoader
from backend.converters.faq_converter import FAQConverter
from backend.retrieval.keyword_search import KeywordSearch

# Load FAQ
loader = FAQLoader()
documents = loader.load()

# Convert to Knowledge
converter = FAQConverter()
knowledge = converter.convert(documents)

# Search
search = KeywordSearch(knowledge)

query = input("Ask a question: ")

results = search.search(query)

print("\nTop Results\n")

for result in results:

    print("=" * 60)

    print("Score:", round(result.score, 3))

    print("Question:", result.knowledge.question)

    print("Answer:", result.knowledge.answer)

    print()