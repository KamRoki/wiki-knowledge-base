from dataclasses import dataclass
from pathlib import Path


@dataclass
class ResetSummary:
    wiki_root: Path
    raw_root: Path
    raw_exists: bool
    raw_file_count: int
