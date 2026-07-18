import argparse

from ..domain.search_result import SearchResult
from ..use_cases.search_wiki import search_wiki


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
