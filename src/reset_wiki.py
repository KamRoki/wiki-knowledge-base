import shutil

from .utils import PROJECT_ROOT


def reset_wiki() -> None:
    wiki_root = PROJECT_ROOT / "wiki"
    raw_root = PROJECT_ROOT / "raw"

    if wiki_root.exists():
        for item in wiki_root.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        wiki_root.mkdir(parents=True, exist_ok=True)

    wiki_root.mkdir(parents=True, exist_ok=True)

    print(f"Wyczyszczono zawartość folderu Wiki: {wiki_root}")
    print("Folder wiki/ pozostał na miejscu.")

    if raw_root.exists():
        raw_files = [path for path in raw_root.rglob("*") if path.is_file()]
        print(f"Folder raw/ pozostał bez zmian: {raw_root}")
        print(f"Liczba zachowanych plików źródłowych: {len(raw_files)}")
    else:
        print(f"Uwaga: folder raw/ nie istnieje: {raw_root}")


if __name__ == "__main__":
    reset_wiki()