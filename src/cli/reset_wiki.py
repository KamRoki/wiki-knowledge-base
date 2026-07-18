from ..use_cases.reset_wiki import reset_wiki


def main() -> None:
    summary = reset_wiki()

    print(f"Wyczyszczono zawartość folderu Wiki: {summary.wiki_root}")
    print("Folder wiki/ pozostał na miejscu.")

    if summary.raw_exists:
        print(f"Folder raw/ pozostał bez zmian: {summary.raw_root}")
        print(f"Liczba zachowanych plików źródłowych: {summary.raw_file_count}")
    else:
        print(f"Uwaga: folder raw/ nie istnieje: {summary.raw_root}")


if __name__ == "__main__":
    main()
