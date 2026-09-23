from pathlib import Path
import sys

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Import our modules
# ---------------------------------------------------------

from backend.loaders.faq_loader import FAQLoader
from backend.converters.faq_converter import FAQConverter
from backend.intents.detector import IntentDetector
from backend.filters.knowledge_filter import KnowledgeFilter


# ---------------------------------------------------------
# Load FAQ
# ---------------------------------------------------------

print("=" * 60)
print("Loading FAQ")
print("=" * 60)

loader = FAQLoader()

docs = loader.load()

converter = FAQConverter()

knowledge = converter.convert(docs)

print(f"\nTotal Knowledge Records: {len(knowledge)}")


# ---------------------------------------------------------
# Create detector and filter
# ---------------------------------------------------------

detector = IntentDetector()

filterer = KnowledgeFilter()


# ---------------------------------------------------------
# Test questions
# ---------------------------------------------------------

test_questions = [

    "How do I register?",

    "I want to register my car",

    "How do I renew?",

    "My parking is about to expire",

    "How do I rebew my parking",

    "Cancel my parking",

    "I want to deregister",

    "How much is parking?",

    "How can I make payment?",

    "My barrier won't open",

    "I cannot exit the barrier",

    "What is ANPR?",

    "My number plate is not recognized",

    "Is my parking still valid?",

    "When does my parking expire?",

    "Hello"
]


# ---------------------------------------------------------
# Run tests
# ---------------------------------------------------------

for question in test_questions:

    print("\n" + "=" * 60)

    print("Question:")
    print(question)

    # Detect intent
    intent = detector.detect(question)

    print("\nDetected Intent:")
    print(intent)

    # Filter knowledge
    filtered = filterer.filter(
        knowledge,
        intent
    )

    print("\nKnowledge Records After Filtering:")
    print(len(filtered))

    # Show categories
    categories = sorted(
        set(record.category for record in filtered)
    )

    print("\nCategories:")
    
    for category in categories:
        print("-", category)


print("\n" + "=" * 60)

print("TEST COMPLETED")

print("=" * 60)