import re
from pathlib import Path
from typing import Any

import frontmatter

from .utils import (
    PROJECT_ROOT,
    list_wiki_content_files,
    path_to_wiki_ref,
    read_text_file,
    write_text_file,
)


REQUIRED_FRONTMATTER_FIELDS = [
    "type",
    "title",
    "description",
    "tags",
    "timestamp",
    "sources",
]

VALID_TYPES = {
    "source",
    "entity",
    "concept",
    "query-answer",
}


def extract_obsidian_links(text: str) -> list[str]:
    """
    Wyciąga linki Obsidiana z tekstu.

    Obsługuje:
    [[concepts/llm-wiki]]
    [[concepts/llm-wiki|LLM Wiki]]
    """
    raw_links = re.findall(r"\[\[([^\]]+)\]\]", text)
    links = []

    for link in raw_links:
        clean_link = link.split("|")[0].strip()

        if clean_link.endswith(".md"):
            clean_link = clean_link[:-3]

        links.append(clean_link)

    return links


def wiki_ref_to_path(ref: str) -> Path:
    """
    Zamienia:
    concepts/llm-wiki

    na:
    wiki/concepts/llm-wiki.md
    """
    clean_ref = ref.strip()

    if clean_ref.startswith("[[") and clean_ref.endswith("]]"):
        clean_ref = clean_ref[2:-2]

    if clean_ref.endswith(".md"):
        clean_ref = clean_ref[:-3]

    return PROJECT_ROOT / "wiki" / f"{clean_ref}.md"


def check_frontmatter(files: list[Path]) -> list[str]:
    issues = []

    for file_path in files:
        try:
            post = frontmatter.load(file_path)
        except Exception as error:
            issues.append(f"- `{file_path}`: nie udało się odczytać frontmatter: {error}")
            continue

        metadata = post.metadata

        if not metadata:
            issues.append(f"- `{file_path}`: brak frontmatter YAML.")
            continue

        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in metadata:
                issues.append(f"- `{file_path}`: brak pola frontmatter `{field}`.")

        page_type = metadata.get("type")

        if page_type and page_type not in VALID_TYPES:
            issues.append(
                f"- `{file_path}`: niepoprawny type `{page_type}`. "
                f"Dozwolone: {', '.join(sorted(VALID_TYPES))}."
            )

    return issues


def check_broken_links(files: list[Path]) -> list[str]:
    issues = []

    for file_path in files:
        text = read_text_file(file_path)
        links = extract_obsidian_links(text)

        for link in links:
            target_path = wiki_ref_to_path(link)

            if not target_path.exists():
                issues.append(
                    f"- `{file_path}`: link `[[{link}]]` prowadzi do nieistniejącej strony."
                )

    return issues


def check_orphan_pages(files: list[Path]) -> list[str]:
    """
    Strona-sierota = strona, do której nie prowadzi żaden link z innych stron
    ani z index.md.

    Uwaga: sources/ często będą sierotami, jeśli nie linkujesz ich ręcznie.
    To jest ostrzeżenie, a nie błąd krytyczny.
    """
    all_refs = {path_to_wiki_ref(file_path) for file_path in files}

    incoming_links: dict[str, int] = {ref: 0 for ref in all_refs}

    index_path = PROJECT_ROOT / "wiki" / "index.md"
    all_texts = []

    if index_path.exists():
        all_texts.append(read_text_file(index_path))

    for file_path in files:
        all_texts.append(read_text_file(file_path))

    for text in all_texts:
        for link in extract_obsidian_links(text):
            if link in incoming_links:
                incoming_links[link] += 1

    issues = []

    for ref, count in sorted(incoming_links.items()):
        if count == 0:
            issues.append(f"- `[[{ref}]]`: strona-sierota, brak linków przychodzących.")

    return issues


def check_index_coverage(files: list[Path]) -> list[str]:
    issues = []

    index_path = PROJECT_ROOT / "wiki" / "index.md"

    if not index_path.exists():
        return ["- Brak pliku `wiki/index.md`."]

    index_text = read_text_file(index_path)

    for file_path in files:
        ref = path_to_wiki_ref(file_path)

        if f"[[{ref}]]" not in index_text:
            issues.append(f"- `[[{ref}]]`: strona nie jest ujęta w `index.md`.")

    return issues


def check_index_dead_entries() -> list[str]:
    index_path = PROJECT_ROOT / "wiki" / "index.md"

    if not index_path.exists():
        return ["- Brak pliku `wiki/index.md`."]

    index_text = read_text_file(index_path)
    links = extract_obsidian_links(index_text)

    issues = []

    for link in links:
        target_path = wiki_ref_to_path(link)

        if not target_path.exists():
            issues.append(
                f"- `index.md`: wpis `[[{link}]]` prowadzi do nieistniejącej strony."
            )

    return issues


def calculate_status(
    frontmatter_issues: list[str],
    broken_link_issues: list[str],
    orphan_issues: list[str],
    index_coverage_issues: list[str],
    index_dead_entry_issues: list[str],
) -> str:
    critical_count = (
        len(frontmatter_issues)
        + len(broken_link_issues)
        + len(index_dead_entry_issues)
    )

    warning_count = len(orphan_issues) + len(index_coverage_issues)

    if critical_count == 0 and warning_count == 0:
        return "🟢"

    if critical_count == 0:
        return "🟡"

    return "🔴"


def format_section(title: str, issues: list[str]) -> str:
    if not issues:
        return f"## {title}\n\nBrak problemów.\n"

    return f"## {title}\n\n" + "\n".join(issues) + "\n"


def build_report(
    files: list[Path],
    frontmatter_issues: list[str],
    broken_link_issues: list[str],
    orphan_issues: list[str],
    index_coverage_issues: list[str],
    index_dead_entry_issues: list[str],
) -> str:
    status = calculate_status(
        frontmatter_issues=frontmatter_issues,
        broken_link_issues=broken_link_issues,
        orphan_issues=orphan_issues,
        index_coverage_issues=index_coverage_issues,
        index_dead_entry_issues=index_dead_entry_issues,
    )

    total_issues = (
        len(frontmatter_issues)
        + len(broken_link_issues)
        + len(orphan_issues)
        + len(index_coverage_issues)
        + len(index_dead_entry_issues)
    )

    report = f"""# Wiki Health Report

Status: {status}

## Podsumowanie

- Liczba sprawdzonych stron: {len(files)}
- Liczba wszystkich wykrytych problemów: {total_issues}
- Problemy frontmatter: {len(frontmatter_issues)}
- Zepsute linki: {len(broken_link_issues)}
- Strony-sieroty: {len(orphan_issues)}
- Strony pominięte w index.md: {len(index_coverage_issues)}
- Martwe wpisy w index.md: {len(index_dead_entry_issues)}

"""

    report += format_section("Frontmatter", frontmatter_issues)
    report += "\n"
    report += format_section("Zepsute linki", broken_link_issues)
    report += "\n"
    report += format_section("Strony-sieroty", orphan_issues)
    report += "\n"
    report += format_section("Pokrycie index.md", index_coverage_issues)
    report += "\n"
    report += format_section("Martwe wpisy w index.md", index_dead_entry_issues)

    return report


def lint_wiki() -> None:
    files = list_wiki_content_files()

    frontmatter_issues = check_frontmatter(files)
    broken_link_issues = check_broken_links(files)
    orphan_issues = check_orphan_pages(files)
    index_coverage_issues = check_index_coverage(files)
    index_dead_entry_issues = check_index_dead_entries()

    report = build_report(
        files=files,
        frontmatter_issues=frontmatter_issues,
        broken_link_issues=broken_link_issues,
        orphan_issues=orphan_issues,
        index_coverage_issues=index_coverage_issues,
        index_dead_entry_issues=index_dead_entry_issues,
    )

    report_path = PROJECT_ROOT / "wiki" / "reports" / "health-report.md"
    write_text_file(report_path, report)

    print(report)
    print(f"\nRaport zapisany w: {report_path}")


if __name__ == "__main__":
    lint_wiki()