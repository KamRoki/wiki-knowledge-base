from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    ref: str
    path: Path
    score: float
    snippet: str
