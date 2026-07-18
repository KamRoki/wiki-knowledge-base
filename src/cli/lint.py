from ..use_cases.lint_wiki import lint_wiki


def main() -> None:
    report_path, report = lint_wiki()

    print(report)
    print(f"\nRaport zapisany w: {report_path}")


if __name__ == "__main__":
    main()
