"""
Test FAQ Loader
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.faq_loader import FAQLoader


loader = FAQLoader()

documents = loader.load()

print()

print(documents[0])