from src.infrastructure.file_utils import slugify


def test_slugify_basic_text():
    assert slugify("LLM Wiki") == "llm-wiki"


def test_slugify_polish_characters():
    assert slugify("Zażółć gęślą jaźń") == "zażółć-gęślą-jaźń"


def test_slugify_removes_extra_spaces():
    assert slugify("  LLM   Wiki  ") == "llm-wiki"


def test_slugify_returns_untitled_for_empty_text():
    assert slugify("") == "untitled"
