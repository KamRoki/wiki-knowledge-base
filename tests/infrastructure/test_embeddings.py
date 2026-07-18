from src.infrastructure.embeddings import tokenize, make_snippet


def test_tokenize_basic_query():
    tokens = tokenize("LLM Wiki różni się od RAG!")

    assert tokens == ["llm", "wiki", "różni", "się", "od", "rag"]


def test_tokenize_keeps_polish_characters():
    tokens = tokenize("Zażółć gęślą jaźń")

    assert tokens == ["zażółć", "gęślą", "jaźń"]


def test_make_snippet_contains_query_term():
    text = (
        "To jest długi tekst o różnych rzeczach. "
        "Najważniejsze jest tutaj pojęcie LLM Wiki, "
        "które opisuje trwałą bazę wiedzy."
    )

    snippet = make_snippet(text, "LLM Wiki")

    assert "LLM Wiki" in snippet
