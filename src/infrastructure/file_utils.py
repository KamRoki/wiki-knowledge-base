from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def read_text_file(path: Path) -> str:
    """
    Read and return the contents of a UTF-8 encoded text file.

    Args:
        path: Path to the file that should be read.

    Returns:
        The complete contents of the file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")

    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    """
    Write the content to a UTF-8 encoded file.

    Missing parent directories are created automatically. If the target already exists, its contents are overwritten.

    Args:
        path: Path to the file that sould be created or overwritten.
        content: Text content to write to the file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(text: str) -> str:
    """
    Convert text into a filesystem-friendly slug.

    The function converts the text to lowercase,replaces sequences of
    unsupported characters with hyphens,and removes leading and trailing
    hyphens. Polish letters and digits are preserved.

    Args:
        text: Text to convert into a slug.

    Returns:
        A normalized slug or 'untitled' if the result is empty.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9ąćęłńóśźż]+", "-", text)
    text = text.strip("-")

    return text or "untitled"


def list_markdown_files(directory: Path) -> list[Path]:
    """
    Return Markdown files located directly inside a directory.

    The function does not search recursively.

    Args:
        directory: Directory to inspect.

    Returns:
        A sorted list of paths to ``.md`` files. An empty list is returned
        if the directory does not exist.
    """
    if not directory.exists():
        return []

    return sorted(directory.glob("*.md"))
