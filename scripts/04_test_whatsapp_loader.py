from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.loaders.whatsapp_loader import WhatsAppLoader

loader = WhatsAppLoader()

documents = loader.load()

print()

print(documents[0])