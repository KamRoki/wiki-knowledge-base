from pathlib import Path

from .file_utils import PROJECT_ROOT


def list_raw_files() -> list[Path]:
    """
    Return all Markdown source files located anywhere inside raw/.

    Returns:
        A sorted list of paths to raw source files. An empty list is
        returned if raw/ does not exist.
    """
    raw_root = PROJECT_ROOT / "raw"

    if not raw_root.exists():
        return []

    return sorted(raw_root.rglob("*.md"))


def resolve_raw_path(raw_file_path: str) -> Path:
    """
    Resolve a path argument to an absolute file located inside raw/.

    Args:
        raw_file_path: Path to a source file, as passed by a caller.

    Returns:
        The resolved absolute path.

    Raises:
        ValueError: If the resolved path is not located inside raw/.
    """
    raw_path = Path(raw_file_path).resolve()
    raw_root = (PROJECT_ROOT / "raw").resolve()

    if raw_root not in raw_path.parents:
        raise ValueError(
            "Źródło musi znajdować się w folderze raw/. "
            "Nie przetwarzaj plików spoza raw/."
        )

    return raw_path
