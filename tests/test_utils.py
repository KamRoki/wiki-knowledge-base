from pathlib import Path

from src.utils import slugify, normalize_wiki_path, path_to_wiki_ref, PROJECT_ROOT


def test_slugify_basic_text():
    assert slugify("LLM Wiki") == "llm-wiki"


def test_slugify_polish_characters():
    assert slugify("Zażółć gęślą jaźń") == "zażółć-gęślą-jaźń"


def test_slugify_removes_extra_spaces():
    assert slugify("  LLM   Wiki  ") == "llm-wiki"


def test_slugify_returns_untitled_for_empty_text():
    assert slugify("") == "untitled"


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