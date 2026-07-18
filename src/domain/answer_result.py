from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnswerResult:
    question: str
    selected_paths: list[str]
    answer: str
    saved_path: Path | None
