from src.infrastructure.file_utils import PROJECT_ROOT
from src.infrastructure.wiki_repository import normalize_wiki_path, path_to_wiki_ref


def test_normalize_wiki_path_without_extension():
    path = normalize_wiki_path("concepts/llm-wiki")

    expected = PROJECT_ROOT / "wiki" / "concepts" / "llm-wiki.md"

    assert path == expected


def test_normalize_wiki_path_with_obsidian_brackets():
    path = normalize_wiki_path("[[concepts/llm-wiki]]")

    expected = PROJECT_ROOT / "wiki" / "concepts" / "llm-wiki.md"

    assert path == expected


def test_normalize_wiki_path_with_md_extension():
    path = normalize_wiki_path("concepts/llm-wiki.md")

    expected = PROJECT_ROOT / "wiki" / "concepts" / "llm-wiki.md"

    assert path == expected


def test_path_to_wiki_ref():
    path = PROJECT_ROOT / "wiki" / "concepts" / "llm-wiki.md"

    assert path_to_wiki_ref(path) == "concepts/llm-wiki"
