import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PromptPair:
    id: str
    category: str
    english: str
    bangla: str


def load_dataset(path: Path) -> list[PromptPair]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != ["id", "category", "english", "bangla"]:
            raise ValueError("Expected TSV headers: id, category, english, bangla")
        return [PromptPair(**row) for row in reader]
