from pathlib import Path
from datetime import datetime
import re
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")
    
    return path.read_text(encoding = "utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents = True, exist_ok = True)
    path. write_text(content, encoding = "utf-8")
    
    
def append_to_log(message: str) -> None:
    log_path = PROJECT_ROOT / "wiki" / "log.md"
    today = datetime.now().strftime("%Y-%m-%d")
    
    with log_path.open("a", encoding = "utf-8") as file:
        file.write(f"\n\n## [{today}] ingest | {message}\n")
        
        
def slugify(text:str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9ąćęłńóśźż]+", "-", text)
    text = text.strip("-")
    return text or "untitled"


def normalize_wiki_path(path: str) -> Path:
    """
    Zamienia ścieżkę z index.md, np. 'concepts/llm-wiki',
    na realną ścieżkę pliku: wiki/concepts/llm-wiki.md.
    """
    clean_path = path.strip()

    if clean_path.startswith("[[") and clean_path.endswith("]]"):
        clean_path = clean_path[2:-2]

    if clean_path.endswith(".md"):
        clean_path = clean_path[:-3]

    return PROJECT_ROOT / "wiki" / f"{clean_path}.md"


def read_wiki_page(path: str) -> str:
    wiki_path = normalize_wiki_path(path)

    if not wiki_path.exists():
        raise FileNotFoundError(f"Nie znaleziono strony Wiki: {wiki_path}")

    return wiki_path.read_text(encoding="utf-8")


def list_markdown_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []

    return sorted(directory.glob("*.md"))


def list_wiki_content_files() -> list[Path]:
    wiki_root = PROJECT_ROOT / "wiki"

    folders = [
        wiki_root / "sources",
        wiki_root / "entities",
        wiki_root / "concepts",
    ]

    files = []

    for folder in folders:
        files.extend(list_markdown_files(folder))

    return sorted(files)


def path_to_wiki_ref(path: Path) -> str:
    """
    Zamienia:
    /project/wiki/concepts/llm-wiki.md

    na:
    concepts/llm-wiki
    """
    wiki_root = PROJECT_ROOT / "wiki"
    relative_path = path.relative_to(wiki_root)

    return str(relative_path.with_suffix(""))