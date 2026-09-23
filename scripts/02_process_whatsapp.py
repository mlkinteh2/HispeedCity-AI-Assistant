"""
02_process_whatsapp.py

Read every exported WhatsApp chat
and convert them into structured data.
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.processors.conversation_cleaner import clean_messages

import pandas as pd
import re


# -----------------------------------------------------
# Project Paths
# -----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

WHATSAPP_FOLDER = PROJECT_ROOT / "data" / "raw" / "whatsapp"

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = OUTPUT_FOLDER / "whatsapp_messages.csv"

# -----------------------------------------------------
# Find all txt files
# -----------------------------------------------------

files = list(WHATSAPP_FOLDER.glob("*.txt"))

print("=" * 60)
print("WhatsApp Files Found")
print("=" * 60)

print(f"Found {len(files)} files\n")

messages = []

# -----------------------------------------------------
# Read every file
# -----------------------------------------------------

pattern = re.compile(
    r"^(.*?) - (.*?): (.*)$"
)

for file in files:

    print(f"Reading {file.name}")

    with open(file, encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            match = pattern.match(line)

            if match:

                date = match.group(1)

                sender = match.group(2)

                message = match.group(3)

                messages.append({
                    "file": file.name,
                    "date": date,
                    "sender": sender,
                    "message": message
                })

# -----------------------------------------------------
# Convert to DataFrame
# -----------------------------------------------------

df = pd.DataFrame(messages)
df = clean_messages(df)

print("\nTotal Messages:", len(df))

OUTPUT_FOLDER.mkdir(exist_ok=True)

df.to_csv(OUTPUT_FILE,index=False)

print("\nSaved")

print(OUTPUT_FILE)

print("\nPreview\n")

print(df.head())