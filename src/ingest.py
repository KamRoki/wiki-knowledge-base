import argparse
from pathlib import Path
from datetime import datetime

from llm_client import ask_llm
from utils import PROJECT_ROOT, read_text_file, write_text_file, append_to_log, slugify


def build_ingest_prompt(source_title: str,
                        source_text: str,
                        schema_text: str) -> str:
    return f"""
            Jesteś systemem budującym trwałą bazę wiedzy Markdown zgodnie z zasadami z AGENTS.md.
            
            Oto zasady projektu:
            
            {schema_text}
            
            Twoje zadanie:
            Przeczytaj ponisze źródło i przygotuj stronę Markdown do folderu wiki/sources/.
            
            Wymagania:
            - użyj frontmatter YAML
            - nadaj type: source
            - przygotuj krótki opis
            - wypisz tagi
            - napisz jasne streszczenie
            - wypisz kluczowe punkty
            - wska potencjalne powiązania do przyszłych stron wiki
            - nie wymyślaj faktów spoza źródła
            - pisz prostym, konkretnym językiem.
            
            Tytuł źródła:
            {source_title}
            
            Treść źródła:
            \"\"\"
            {source_text}
            \"\"\"
""".strip()


def update_index(source_title: str,
                 source_slug: str,
                 description: str = "Streszczenie źródła.") -> None:
    index_path = PROJECT_ROOT / "wiki" / "index.md"
    
    if not index_path.exists():
        index_path.write_text("# LLM Wiki - Index\n\n## Sources\n", encoding="utf-8")
        
    index_text = index_path.read_text(encoding = "utf-8")
    new_entry = f"- [[sources/{source_slug}]] - {description}"
    
    if new_entry in index_text:
        return
    
    if "## Sources" in index_text:
        index_text = index_text.replace("## Sources", f"## Sources\n\n{new_entry}", 1)
    else:
        index_text += f"\n\n## Sources\n\n{new_entry}\n"
        
    index_path.write_text(index_text, encoding = "utf-8")
    
    
def ingest_file(raw_file_path: str) -> None:
    raw_path = Path(raw_file_path).resolve()
    
    raw_root = (PROJECT_ROOT / "raw").resolve()
    
    if raw_root not in raw_path.parents:
        raise ValueError("Źródło musi znajdować się w folderze raw/. Nie przetwarzaj plików spoza raw/.")
    
    source_text = read_text_file(raw_path)
    schema_text = read_text_file(PROJECT_ROOT / "AGENTS.md")
    
    source_title = raw_path.stem
    source_slug = slugify(source_title)
    
    prompt = build_ingest_prompt(
        source_title = source_title,
        source_text = source_text,
        schema_text = schema_text
    )
    
    wiki_page = ask_llm(prompt)
    
    output_path = PROJECT_ROOT / "wiki" / "sources" / f"{source_slug}.md"
    write_text_file(output_path, wiki_page)
    
    update_index(source_title = source_title, source_slug = source_slug)
    append_to_log(f"Dodano źródło: {source_title}")
    
    print(f"Gotowe. Utworzono plik: {output_path}")
    
    
def main() -> None:
    parser = argparse.ArgumentParser(description = "Dodaj źródło do LLM Wiki.")
    parser.add_argument("file", help = "Ścieka do pliku źródłowego w raw/.")
    
    args = parser.parse_args()
    ingest_file(args.file)
    
    
    
if __name__ == "__main__":
    main()