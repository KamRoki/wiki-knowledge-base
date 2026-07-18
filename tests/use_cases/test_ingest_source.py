import pytest

from src.use_cases.ingest_source import parse_llm_json, ensure_required_keys


def test_parse_llm_json_valid_response():
    response = """
{
  "source": {
    "title": "Test",
    "slug": "test",
    "description": "Opis",
    "content": "Treść"
  },
  "entities": [],
  "concepts": [],
  "index_entries": []
}
"""

    data = parse_llm_json(response)

    assert data["source"]["title"] == "Test"
    assert data["entities"] == []
    assert data["concepts"] == []
    assert data["index_entries"] == []


def test_parse_llm_json_invalid_response():
    response = "To nie jest JSON"

    with pytest.raises(ValueError):
        parse_llm_json(response)


def test_ensure_required_keys_valid_data():
    data = {
        "source": {},
        "entities": [],
        "concepts": [],
        "index_entries": [],
    }

    ensure_required_keys(data)


def test_ensure_required_keys_missing_source():
    data = {
        "entities": [],
        "concepts": [],
        "index_entries": [],
    }

    with pytest.raises(ValueError):
        ensure_required_keys(data)
