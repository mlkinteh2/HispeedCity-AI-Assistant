"""
knowledge_exporter.py

Export knowledge records into CSV.
"""

from pathlib import Path
import pandas as pd
from backend.utils.priorities import get_priority


class KnowledgeExporter:

    def export(self, records, output_file):

        rows = []

        for r in records:

            rows.append({
                "id": r.id,
                "category": r.category,
                "question": r.question,
                "answer": r.answer,
                "source": r.source,
                "status": r.status,
                "confidence": r.confidence,
                "priority": get_priority(r.source)
            })

        df = pd.DataFrame(rows)

        output_file = Path(output_file)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_file, index=False)

        print("\nKnowledge Base Exported")
        print("=" * 50)
        print(f"Records : {len(df)}")
        print(f"Saved to: {output_file}")