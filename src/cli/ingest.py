import argparse

from ..use_cases.ingest_source import ingest_source


def main() -> None:
    parser = argparse.ArgumentParser(description="Dodaj źródło do LLM Wiki.")
    parser.add_argument("file", help="Ścieżka do pliku źródłowego w raw/.")

    args = parser.parse_args()

    summary = ingest_source(args.file)

    print("Gotowe. Utworzono lub zaktualizowano strony Wiki:")
    print(f"- Source: {summary.source_path}")

    for path in summary.entity_paths:
        print(f"- Entity: {path}")

    for path in summary.concept_paths:
        print(f"- Concept: {path}")


if __name__ == "__main__":
    main()
