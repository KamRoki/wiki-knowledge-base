import shutil

from ..domain.reset_summary import ResetSummary
from ..infrastructure.file_utils import PROJECT_ROOT


def reset_wiki() -> ResetSummary:
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

    raw_exists = raw_root.exists()
    raw_file_count = 0

    if raw_exists:
        raw_file_count = len([path for path in raw_root.rglob("*") if path.is_file()])

    return ResetSummary(
        wiki_root=wiki_root,
        raw_root=raw_root,
        raw_exists=raw_exists,
        raw_file_count=raw_file_count,
    )
