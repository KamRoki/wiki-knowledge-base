import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from rank_bm25 import BM25Okapi

from .utils import (
    list_wiki_content_files,
    path_to_wiki_ref,
    read_text_file,
)


@dataclass
class SearchResult:
    ref: str
    path: Path
    score: float
    snippet: str


def tokenize(text: str) -> list[str]:
    """
    Prosta tokenizacja tekstu:
    - zamienia tekst na małe litery,
    - usuwa znaki specjalne,
    - dzieli na słowa.

    To wystarczy dla prostego BM25.
    """
    text = text.lower()
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]+", text)


def make_snippet(text: str, query: str, max_length: int = 240) -> str:
    """
    Tworzy krótki fragment strony do pokazania w wynikach.
    Jeżeli znajdzie słowo z zapytania, pokazuje okolice tego słowa.
    """
    clean_text = re.sub(r"\s+", " ", text).strip()
    query_terms = tokenize(query)

    lower_text = clean_text.lower()

    best_position = None

    for term in query_terms:
        position = lower_text.find(term.lower())

        if position != -1:
            best_position = position
            break

    if best_position is None:
        return clean_text[:max_length] + ("..." if len(clean_text) > max_length else "")

    start = max(best_position - 80, 0)
    end = min(start + max_length, len(clean_text))

    snippet = clean_text[start:end]

    if start > 0:
        snippet = "..." + snippet

    if end < len(clean_text):
        snippet = snippet + "..."

    return snippet


def build_search_index() -> tuple[BM25Okapi, list[Path], list[str]]:
    """
    Buduje indeks BM25 na podstawie plików Markdown w wiki/sources,
    wiki/entities i wiki/concepts.
    """
    files = list_wiki_content_files()

    documents = []

    for file_path in files:
        text = read_text_file(file_path)
        documents.append(text)

    tokenized_documents = [tokenize(document) for document in documents]

    bm25 = BM25Okapi(tokenized_documents)

    return bm25, files, documents


def search_wiki(query: str, limit: int = 5) -> list[SearchResult]:
    bm25, files, documents = build_search_index()

    if not files:
        return []

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        enumerate(scores),
        key=lambda item: item[1],
        reverse=True,
    )

    results = []

    for index, score in ranked[:limit]:
        if score <= 0:
            continue

        file_path = files[index]
        document = documents[index]

        results.append(
            SearchResult(
                ref=path_to_wiki_ref(file_path),
                path=file_path,
                score=float(score),
                snippet=make_snippet(document, query),
            )
        )

    return results


def print_results(results: list[SearchResult]) -> None:
    if not results:
        print("Brak wyników.")
        return

    print("Najlepsze wyniki:\n")

    for number, result in enumerate(results, start=1):
        print(f"{number}. {result.ref}")
        print(f"   Wynik: {result.score:.2f}")
        print(f"   {result.snippet}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Szukaj w lokalnej Wiki.")
    parser.add_argument("query", help="Fraza do wyszukania.")
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maksymalna liczba wyników.",
    )

    args = parser.parse_args()

    results = search_wiki(
        query=args.query,
        limit=args.limit,
    )

    print_results(results)


if __name__ == "__main__":
    main()