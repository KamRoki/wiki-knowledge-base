from pathlib import Path
from datetime import datetime
import re


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