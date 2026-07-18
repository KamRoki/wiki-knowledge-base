# src/skills/ingest_wiki.py
from langchain_core.tools import tool

from ..infrastructure.file_utils import PROJECT_ROOT
from ..use_cases.ingest_source import ingest_source


@tool
def ingest_wiki(file_name: str) -> str:
    """
    Wgrywa (ingestuje) wskazany plik z folderu raw/ do bazy wiedzy
    wiki. file_name to ścieżka względem raw/, np.
    'articles/przyklad.md'.
    """
    raw_path = PROJECT_ROOT / "raw" / file_name
    summary = ingest_source(str(raw_path))
    return f"Zingestowano: {summary.source_path.name}"