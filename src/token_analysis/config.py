from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class ExperimentConfig:
    model: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
    url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    seed: int = int(os.getenv("EXPERIMENT_SEED", "2026"))
    num_predict: int = int(os.getenv("OLLAMA_NUM_PREDICT", "160"))
    temperature: float = 0.0
    system_prompt: str = "Answer the user's request accurately and concisely. Do not invent facts."

    @property
    def options(self) -> dict:
        return {"temperature": self.temperature, "seed": self.seed, "num_predict": self.num_predict}
