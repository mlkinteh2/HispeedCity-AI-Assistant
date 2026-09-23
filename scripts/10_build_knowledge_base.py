from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.faq_loader import FAQLoader
from backend.converters.faq_converter import FAQConverter
from backend.knowledge.knowledge_builder import KnowledgeBuilder

faq_loader = FAQLoader()

faq_documents = faq_loader.load()

converter = FAQConverter()

faq_knowledge = converter.convert(faq_documents)

kb = KnowledgeBuilder()

kb.add_many(faq_knowledge)

kb.summary()