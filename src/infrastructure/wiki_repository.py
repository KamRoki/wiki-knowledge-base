from datetime import datetime
from pathlib import Path

from .file_utils import PROJECT_ROOT, list_markdown_files

from ..domain.wiki_page import WikiPage
from .file_utils import read_text_file


def append_to_log(message: str) -> None:
    """
    Append a dated ingestion entry to the wiki operation log.

    The log is stored in wiki/log.md. The parent directory is created automatically if it does not exist.

    Args:
        message: Description of the ingestion operation to append to the log.
    """
    log_path = PROJECT_ROOT / "wiki" / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    with log_path.open("a", encoding="utf-8") as file:
        file.write(f"\n\n## [{today}] ingest | {message}\n")


def normalize_wiki_path(path: str) -> Path:
    """
    Convert a logical wiki reference into an absolute Markdown file path.

    The function accepts references with optional Obsidian brackets and an
    optional ``.md`` extension.

    Examples:
        ``concepts/llm-wiki``
        ``[[concepts/llm-wiki]]``
        ``concepts/llm-wiki.md``

    Args:
        path: Logical wiki reference to normalize.

    Returns:
        Absolute path to the corresponding Markdown file inside ``wiki/``
    """
    clean_path = path.strip()

    if clean_path.startswith("[[") and clean_path.endswith("]]"):
        clean_path = clean_path[2:-2]

    if clean_path.endswith(".md"):
        clean_path = clean_path[:-3]

    return PROJECT_ROOT / "wiki" / f"{clean_path}.md"


def read_wiki_page(path: str) -> str:
    """
    Read a wiki page using its logical wiki reference.

    Args:
        path: Wiki reference such as ``concepts/llm-wiki`` or
            ``[[concepts/llm-wiki]]``.

    Returns:
        The complete contents of the corresponding Markdown page.
    """
    wiki_path = normalize_wiki_path(path)

    if not wiki_path.is_file():
        raise FileNotFoundError(f"Nie znaleziono strony Wiki: {wiki_path}")

    return wiki_path.read_text(encoding="utf-8")


def list_wiki_content_files() -> list[Path]:
    """
    Return all generated content pages from the main wiki directories.

    The function collects Markdown files from:

    - ``wiki/sources/``
    - ``wiki/entities/``
    - ``wiki/concepts/``

    Files such as ``index.md``,``log.md`` and health reports are not included.

    Returns:
        A sorted list of paths to all source,entity,and concept pages.
    """
    wiki_root = PROJECT_ROOT / "wiki"

    folders = [
        wiki_root / "sources",
        wiki_root / "entities",
        wiki_root / "concepts",
    ]

    files: list[Path] = []

    for folder in folders:
        files.extend(list_markdown_files(folder))

    return sorted(files)


def path_to_wiki_ref(path: Path) -> str:
    """
    Convert a Markdown file path into a logical wiki reference.

    For example:

    ``/project/wiki/concepts/llm-wiki.md``

    becomes:

    ``concepts/llm-wiki``

    Args:
        path: Path to a Markdown file located inside the ``wiki/`` directory.

    Returns:
        A POSIX-style wiki reference without the ``.md`` extension.
    """
    wiki_root = PROJECT_ROOT / "wiki"
    relative_path = path.relative_to(wiki_root)

    return relative_path.with_suffix("").as_posix()


def list_wiki_pages() -> list[WikiPage]:
    files = list_wiki_content_files()
    return [
        WikiPage(ref = path_to_wiki_ref(f), 
                 path = f,
                 content = read_text_file(f)) for f in files
    ]
