from dataclasses import dataclass
from pathlib import Path


@dataclass
class WikiPage:
    ref: str
    path: Path
    content: str