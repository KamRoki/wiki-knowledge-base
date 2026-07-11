from src.lint import extract_obsidian_links, wiki_ref_to_path
from src.utils import PROJECT_ROOT


def test_extract_obsidian_links_simple():
    text = "Zobacz [[concepts/llm-wiki]] oraz [[concepts/rag]]."

    links = extract_obsidian_links(text)

    assert links == ["concepts/llm-wiki", "concepts/rag"]


def test_extract_obsidian_links_with_alias():
    text = "Zobacz [[concepts/llm-wiki|LLM Wiki]]."

    links = extract_obsidian_links(text)

    assert links == ["concepts/llm-wiki"]


def test_extract_obsidian_links_with_md_extension():
    text = "Zobacz [[concepts/llm-wiki.md]]."

    links = extract_obsidian_links(text)

    assert links == ["concepts/llm-wiki"]


def test_wiki_ref_to_path():
    path = wiki_ref_to_path("concepts/llm-wiki")

    expected = PROJECT_ROOT / "wiki" / "concepts" / "llm-wiki.md"

    assert path == expected