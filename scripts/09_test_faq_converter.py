from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.faq_loader import FAQLoader
from backend.converters.faq_converter import FAQConverter

loader = FAQLoader()

documents = loader.load()

converter = FAQConverter()

knowledge = converter.convert(documents)

print()

print("First Knowledge Record")

print()

print(knowledge[0])