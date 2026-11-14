import csv
from pathlib import Path


def load_quality_review(path: Path) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def completed_reviews(rows: list[dict]) -> list[dict]:
    reviewed = []
    for row in rows:
        fields = ["english_correctness", "english_usefulness", "bangla_correctness", "bangla_usefulness"]
        if not all(row.get(k, "").strip() for k in fields):
            continue
        if any(int(row[k]) not in (0, 1, 2) for k in fields):
            raise ValueError(f"Invalid review score in {row.get('id')}")
        reviewed.append(row)
    return reviewed
