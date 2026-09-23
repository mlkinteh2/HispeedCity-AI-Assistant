from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.faq_loader import FAQLoader
from backend.converters.faq_converter import FAQConverter
from backend.knowledge.knowledge_builder import KnowledgeBuilder
from backend.exporters.knowledge_exporter import KnowledgeExporter

OUTPUT = PROJECT_ROOT / "data" / "knowledge_base.csv"

# Load FAQ
loader = FAQLoader()
documents = loader.load()

# Convert
converter = FAQConverter()
knowledge = converter.convert(documents)

# Build
builder = KnowledgeBuilder()
builder.add_many(knowledge)

# Export
exporter = KnowledgeExporter()
exporter.export(builder.get_all(), OUTPUT)