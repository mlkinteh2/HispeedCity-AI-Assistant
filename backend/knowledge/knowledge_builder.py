"""
knowledge_builder.py

Central repository for all knowledge records.
"""

from backend.models.knowledge import Knowledge


class KnowledgeBuilder:

    def __init__(self):

        self.records = []

    def add(self, record: Knowledge):

        self.records.append(record)

    def add_many(self, records):

        self.records.extend(records)

    def total(self):

        return len(self.records)

    def get_all(self):

        return self.records

    def summary(self):

        print("\nKnowledge Summary")
        print("=" * 50)

        print(f"Total Records : {len(self.records)}")

        categories = {}

        for record in self.records:

            cat = record.category

            categories[cat] = categories.get(cat, 0) + 1

        print()

        for cat, count in sorted(categories.items()):

            print(f"{cat:20} {count}")