import argparse

from ..use_cases.answer_question import answer_question


def main() -> None:
    parser = argparse.ArgumentParser(description="Zadaj pytanie do lokalnej Wiki.")
    parser.add_argument("question", help="Pytanie do Wiki.")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Zapisz odpowiedź jako nową stronę Wiki.",
    )
    parser.add_argument(
        "--mode",
        choices=["search", "llm"],
        default="search",
        help="Sposób wyboru stron Wiki: search albo llm.",
    )

    args = parser.parse_args()

    result = answer_question(
        question=args.question,
        save=args.save,
        mode=args.mode,
    )

    print("\nWybrane strony Wiki:")
    if result.selected_paths:
        for path in result.selected_paths:
            print(f"- {path}")
    else:
        print("- brak")

    print("\nOdpowiedź:\n")
    print(result.answer)

    if result.saved_path:
        print(f"\nOdpowiedź zapisana jako: {result.saved_path}")


if __name__ == "__main__":
    main()
