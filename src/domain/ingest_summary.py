from dataclasses import dataclass
from pathlib import Path


@dataclass
class IngestSummary:
    source_path: Path
    entity_paths: list[Path]
    concept_paths: list[Path]
