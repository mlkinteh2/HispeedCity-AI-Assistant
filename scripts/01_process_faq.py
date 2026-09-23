"""
01_process_faq.py

Reads the FAQ Excel file, cleans it, standardises it,
adds metadata, and creates a professional knowledge base.
"""

from pathlib import Path
import pandas as pd
from datetime import datetime

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FAQ_FILE = PROJECT_ROOT / "data" / "raw" / "faq" / "FAQ.xlsx"

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = OUTPUT_FOLDER / "faq_clean.csv"

# =====================================================
# READ FAQ
# =====================================================

print("=" * 60)
print("Reading FAQ...")
print("=" * 60)

df = pd.read_excel(FAQ_FILE)

print(f"Rows found : {len(df)}")

# =====================================================
# CLEAN DATA
# =====================================================

df = df.dropna(how="all")

df = df.drop_duplicates(subset=["Question"])

df["Question"] = df["Question"].astype(str).str.strip()

df["Answer"] = df["Answer"].astype(str).str.strip()

df = df[
    (df["Question"] != "")
    &
    (df["Answer"] != "")
]

print(f"Rows after cleaning : {len(df)}")

# =====================================================
# CREATE KNOWLEDGE BASE
# =====================================================

knowledge = pd.DataFrame()

knowledge["id"] = [f"FAQ{i:03d}" for i in range(1, len(df)+1)]

knowledge["source"] = "FAQ"

if "Category" in df.columns:
    knowledge["category"] = df["Category"]
else:
    knowledge["category"] = "General"

knowledge["question"] = df["Question"]

knowledge["answer"] = df["Answer"]

# -----------------------
# Intent
# -----------------------

def detect_intent(question):

    q = question.lower()

    if "register" in q:
        return "registration"

    elif "renew" in q:
        return "renewal"

    elif "pay" in q:
        return "payment"

    elif "barrier" in q:
        return "technical_support"

    elif "parking" in q:
        return "parking_information"

    elif "receipt" in q:
        return "receipt"

    return "general"

knowledge["intent"] = knowledge["question"].apply(detect_intent)

# -----------------------
# Keywords
# -----------------------

knowledge["keywords"] = knowledge["question"].str.lower()

# -----------------------
# Tags
# -----------------------

knowledge["tags"] = knowledge["category"].str.lower()

# -----------------------
# Priority
# -----------------------

knowledge["priority"] = "Normal"

# -----------------------
# Language
# -----------------------

knowledge["language"] = "English"

# -----------------------
# Verified
# -----------------------

knowledge["verified"] = True

# -----------------------
# Last Updated
# -----------------------

knowledge["last_updated"] = datetime.today().strftime("%Y-%m-%d")

# -----------------------
# Document
# -----------------------

knowledge["document"] = "FAQ.xlsx"

# =====================================================
# SAVE
# =====================================================

OUTPUT_FOLDER.mkdir(exist_ok=True)

knowledge.to_csv(OUTPUT_FILE, index=False)

print("\nKnowledge Base Created Successfully!")

print(f"\nSaved to:\n{OUTPUT_FILE}")

print("\nPreview\n")

print(knowledge.head())