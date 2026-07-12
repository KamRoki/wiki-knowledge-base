import argparse
import json
from pathlib import Path

from .llm_client import ask_llm
from .utils import (
    PROJECT_ROOT,
    append_to_log,
    read_text_file,
    slugify,
    write_text_file,
)


def build_ingest_prompt(
    source_title: str,
    source_text: str,
    schema_text: str,
) -> str:
    source_slug = slugify(source_title)

    return f"""
Jesteś systemem budującym trwałą bazę wiedzy Markdown zgodnie z zasadami z AGENTS.md.

Oto zasady projektu:

{schema_text}

Twoje zadanie:
Przeczytaj poniższe źródło i zwróć wyłącznie poprawny JSON.

Nie dodawaj komentarzy przed JSON-em.
Nie dodawaj komentarzy po JSON-ie.
Nie używaj markdownowego bloku ```json.
Zwróć sam JSON.

Struktura odpowiedzi musi być dokładnie taka:

{{
  "source": {{
    "title": "Tytuł źródła",
    "slug": "slug-zrodla",
    "description": "Krótki opis źródła",
    "content": "Pełna treść strony Markdown z frontmatter YAML"
  }},
  "entities": [
    {{
      "title": "Nazwa encji",
      "slug": "nazwa-encji",
      "description": "Krótki opis encji",
      "content": "Pełna treść strony Markdown z frontmatter YAML"
    }}
  ],
  "concepts": [
    {{
      "title": "Nazwa pojęcia",
      "slug": "nazwa-pojecia",
      "description": "Krótki opis pojęcia",
      "content": "Pełna treść strony Markdown z frontmatter YAML"
    }}
  ],
  "index_entries": [
    {{
      "section": "Sources",
      "path": "sources/slug-zrodla",
      "description": "Krótki opis strony"
    }},
    {{
      "section": "Entities",
      "path": "entities/nazwa-encji",
      "description": "Krótki opis strony"
    }},
    {{
      "section": "Concepts",
      "path": "concepts/nazwa-pojecia",
      "description": "Krótki opis strony"
    }}
  ]
}}

Wymagania dla treści Markdown:
- każda strona musi mieć frontmatter YAML,
- używaj pól: type, title, description, tags, timestamp, sources,
- strona źródłowa ma mieć type: source,
- strona encji ma mieć type: entity,
- strona pojęcia ma mieć type: concept,
- używaj linków Obsidiana, np. [[concepts/llm-wiki]],
- nie wymyślaj faktów spoza źródła,
- pisz prostym, konkretnym językiem,
- jeżeli w źródle nie ma encji, zwróć pustą listę entities,
- jeżeli w źródle nie ma pojęć, zwróć pustą listę concepts,
- slug źródła powinien być równy: {source_slug}.

Tytuł źródła:
{source_title}

Treść źródła:
\"\"\"
{source_text}
\"\"\"
""".strip()


def parse_llm_json(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Model nie zwrócił poprawnego JSON-a. "
            "Prawdopodobnie dodał komentarz, markdownowy blok ```json albo nie domknął struktury."
        ) from error


def ensure_required_keys(data: dict) -> None:
    required_keys = ["source", "entities", "concepts", "index_entries"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Brakuje wymaganego pola w JSON: {key}")


def save_source_page(source: dict) -> Path:
    source_slug = source.get("slug") or slugify(source.get("title", "untitled"))
    output_path = PROJECT_ROOT / "wiki" / "sources" / f"{source_slug}.md"

    if output_path.exists():
        raise FileExistsError(
            f"Źródło zostało już przetworzone: {output_path}. "
            "Przerywam, aby nie tworzyć duplikatu."
        )

    write_text_file(output_path, source["content"])

    return output_path


def save_entity_pages(entities: list[dict]) -> list[Path]:
    saved_paths = []

    for entity in entities:
        entity_slug = entity.get("slug") or slugify(entity.get("title", "untitled"))
        output_path = PROJECT_ROOT / "wiki" / "entities" / f"{entity_slug}.md"

        if output_path.exists():
            existing_content = read_text_file(output_path)
            new_section = "\n\n## Nowe informacje z ostatniego źródła\n\n"
            new_section += entity["content"]

            write_text_file(output_path, existing_content + new_section)
        else:
            write_text_file(output_path, entity["content"])

        saved_paths.append(output_path)

    return saved_paths


def save_concept_pages(concepts: list[dict]) -> list[Path]:
    saved_paths = []

    for concept in concepts:
        concept_slug = concept.get("slug") or slugify(concept.get("title", "untitled"))
        output_path = PROJECT_ROOT / "wiki" / "concepts" / f"{concept_slug}.md"

        if output_path.exists():
            existing_content = read_text_file(output_path)
            new_section = "\n\n## Nowe informacje z ostatniego źródła\n\n"
            new_section += concept["content"]

            write_text_file(output_path, existing_content + new_section)
        else:
            write_text_file(output_path, concept["content"])

        saved_paths.append(output_path)

    return saved_paths


def ensure_index_sections(index_text: str) -> str:
    required_sections = ["## Sources", "## Entities", "## Concepts"]

    for section in required_sections:
        if section not in index_text:
            index_text += f"\n\n{section}\n"

    return index_text


def update_index_from_entries(entries: list[dict]) -> None:
    index_path = PROJECT_ROOT / "wiki" / "index.md"

    if not index_path.exists():
        index_path.write_text(
            "# LLM Wiki - Index\n\n## Sources\n\n## Entities\n\n## Concepts\n",
            encoding="utf-8",
        )

    index_text = index_path.read_text(encoding="utf-8")
    index_text = ensure_index_sections(index_text)

    for entry in entries:
        section = entry["section"]
        path = entry["path"]
        description = entry.get("description", "Brak opisu.")

        section_header = f"## {section}"
        new_entry = f"- [[{path}]] - {description}"

        if new_entry in index_text:
            continue

        if section_header not in index_text:
            index_text += f"\n\n{section_header}\n\n{new_entry}\n"
            continue

        index_text = index_text.replace(
            section_header,
            f"{section_header}\n\n{new_entry}",
            1,
        )

    index_path.write_text(index_text, encoding="utf-8")


def build_log_message(data: dict) -> str:
    source = data["source"]
    entities = data.get("entities", [])
    concepts = data.get("concepts", [])

    source_slug = source["slug"]

    lines = [
        f"- Source: [[sources/{source_slug}]]",
    ]

    if entities:
        entity_links = [f"[[entities/{entity['slug']}]]" for entity in entities]
        lines.append(f"- Entities: {', '.join(entity_links)}")
    else:
        lines.append("- Entities: brak")

    if concepts:
        concept_links = [f"[[concepts/{concept['slug']}]]" for concept in concepts]
        lines.append(f"- Concepts: {', '.join(concept_links)}")
    else:
        lines.append("- Concepts: brak")

    return "\n".join(lines)


def ingest_file(raw_file_path: str) -> None:
    raw_path = Path(raw_file_path).resolve()
    raw_root = (PROJECT_ROOT / "raw").resolve()

    if raw_root not in raw_path.parents:
        raise ValueError(
            "Źródło musi znajdować się w folderze raw/. "
            "Nie przetwarzaj plików spoza raw/."
        )

    source_title = raw_path.stem
    source_text = read_text_file(raw_path)
    schema_text = read_text_file(PROJECT_ROOT / "AGENTS.md")

    prompt = build_ingest_prompt(
        source_title=source_title,
        source_text=source_text,
        schema_text=schema_text,
    )

    response = ask_llm(prompt)
    data = parse_llm_json(response)
    ensure_required_keys(data)

    source_path = save_source_page(data["source"])
    entity_paths = save_entity_pages(data.get("entities", []))
    concept_paths = save_concept_pages(data.get("concepts", []))

    update_index_from_entries(data.get("index_entries", []))

    log_message = build_log_message(data)
    append_to_log(log_message)

    print("Gotowe. Utworzono lub zaktualizowano strony Wiki:")
    print(f"- Source: {source_path}")

    for path in entity_paths:
        print(f"- Entity: {path}")

    for path in concept_paths:
        print(f"- Concept: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dodaj źródło do LLM Wiki.")
    parser.add_argument("file", help="Ścieżka do pliku źródłowego w raw/.")

    args = parser.parse_args()
    ingest_file(args.file)


if __name__ == "__main__":
    main()