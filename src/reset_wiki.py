from pathlib import Path

from utils import PROJECT_ROOT, write_text_file


def remove_markdown_files(directory: Path) -> None:
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        return

    for file_path in directory.glob("*.md"):
        file_path.unlink()


def reset_wiki() -> None:
    wiki_root = PROJECT_ROOT / "wiki"

    remove_markdown_files(wiki_root / "sources")
    remove_markdown_files(wiki_root / "entities")
    remove_markdown_files(wiki_root / "concepts")

    write_text_file(
        wiki_root / "index.md",
        """# LLM Wiki - Index

## Sources

## Entities

## Concepts
""",
    )

    write_text_file(
        wiki_root / "log.md",
        """# LLM Wiki - Log

Dziennik operacji wykonywanych na wiki.
""",
    )

    write_text_file(
        wiki_root / "overview.md",
        """# Overview

To jest robocza baza wiedzy budowana przez AI na podstawie źródeł z folderu raw/.
""",
    )

    print("Wiki została wyczyszczona. Folder raw/ nie został zmieniony.")


if __name__ == "__main__":
    reset_wiki()