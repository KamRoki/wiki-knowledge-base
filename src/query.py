import argparse
import json
from pathlib import Path

from llm_client import ask_llm
from utils import PROJECT_ROOT, read_text_file, read_wiki_page, write_text_file, slugify
from search import search_wiki


def build_page_selection_prompt(question: str, index_text: str) -> str:
    return f"""
Jesteś asystentem pracującym z lokalną bazą wiedzy Markdown.

Twoim zadaniem NIE jest jeszcze odpowiadać na pytanie.
Twoim zadaniem jest wybrać strony Wiki, które trzeba przeczytać, aby dobrze odpowiedzieć.

Masz dostęp wyłącznie do spisu treści Wiki, czyli index.md.

Zwróć wyłącznie poprawny JSON.
Nie dodawaj komentarzy przed JSON-em.
Nie dodawaj komentarzy po JSON-ie.
Nie używaj bloku markdown ```json.

Struktura odpowiedzi:

{{
  "paths": [
    "concepts/example",
    "entities/example",
    "sources/example"
  ]
}}

Zasady:
- wybierz maksymalnie 5 stron,
- wybieraj tylko ścieżki, które realnie występują w index.md,
- nie wymyślaj nowych ścieżek,
- jeżeli nie ma dobrych dopasowań, zwróć pustą listę,
- preferuj strony concepts/ i entities/,
- sources/ wybieraj wtedy, gdy mogą zawierać ważne szczegóły.

Pytanie użytkownika:
{question}

Treść index.md:
\"\"\"
{index_text}
\"\"\"
""".strip()


def parse_json_response(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Model nie zwrócił poprawnego JSON-a podczas wyboru stron."
        ) from error


def select_relevant_pages(question: str, index_text: str) -> list[str]:
    prompt = build_page_selection_prompt(
        question=question,
        index_text=index_text,
    )

    response = ask_llm(prompt)
    data = parse_json_response(response)

    paths = data.get("paths", [])

    if not isinstance(paths, list):
        raise ValueError("Pole 'paths' musi być listą.")

    return paths[:5]


def load_selected_pages(paths: list[str]) -> str:
    loaded_pages = []

    for path in paths:
        try:
            page_text = read_wiki_page(path)
        except FileNotFoundError:
            continue

        loaded_pages.append(
            f"""
--- PAGE: {path} ---

{page_text}
""".strip()
        )

    return "\n\n".join(loaded_pages)


def build_answer_prompt(question: str, context: str) -> str:
    return f"""
Jesteś asystentem odpowiadającym na podstawie lokalnej bazy wiedzy Markdown.

Odpowiedz na pytanie użytkownika wyłącznie na podstawie podanego kontekstu.

Zasady:
- nie wymyślaj faktów spoza kontekstu,
- jeżeli kontekst nie wystarcza, powiedz to jasno,
- odpowiadaj konkretnie i prostym językiem,
- podawaj odniesienia do stron Wiki w formie [[ścieżka/do/strony]],
- jeżeli porównujesz pojęcia, zrób to jasno i rzeczowo,
- nie cytuj raw/ ani plików źródłowych spoza Wiki.

Pytanie użytkownika:
{question}

Kontekst z Wiki:
\"\"\"
{context}
\"\"\"
""".strip()


def answer_question(question: str, selected_paths: list[str]) -> str:
    context = load_selected_pages(selected_paths)

    if not context.strip():
        return (
            "Nie znalazłem w Wiki stron, które pozwalają odpowiedzieć na to pytanie. "
            "Dodaj więcej źródeł przez ingest albo sprawdź, czy index.md zawiera odpowiednie wpisy."
        )

    prompt = build_answer_prompt(
        question=question,
        context=context,
    )

    return ask_llm(prompt)


def build_saved_answer_content(question: str, answer: str, selected_paths: list[str]) -> str:
    sources = ", ".join(selected_paths)

    return f"""---
type: query-answer
title: "{question}"
description: "Odpowiedź wygenerowana na podstawie lokalnej Wiki"
tags: [query, answer]
sources: [{sources}]
---

# {question}

## Odpowiedź

{answer}

## Wykorzystane strony Wiki

{chr(10).join(f"- [[{path}]]" for path in selected_paths)}
"""


def save_answer(question: str, answer: str, selected_paths: list[str]) -> Path:
    slug = slugify(question)
    output_path = PROJECT_ROOT / "wiki" / "concepts" / f"{slug}.md"

    content = build_saved_answer_content(
        question=question,
        answer=answer,
        selected_paths=selected_paths,
    )

    write_text_file(output_path, content)

    return output_path


def query_wiki(question: str, save: bool = False, mode: str = "search") -> None:
    if mode == "search":
        selected_paths = select_relevant_pages_with_search(
            question=question,
            limit=5,
        )
    elif mode == "llm":
        index_path = PROJECT_ROOT / "wiki" / "index.md"
        index_text = read_text_file(index_path)

        selected_paths = select_relevant_pages(
            question=question,
            index_text=index_text,
        )
    else:
        raise ValueError("Nieznany tryb. Użyj: search albo llm.")

    print("\nWybrane strony Wiki:")
    if selected_paths:
        for path in selected_paths:
            print(f"- {path}")
    else:
        print("- brak")

    answer = answer_question(
        question=question,
        selected_paths=selected_paths,
    )

    print("\nOdpowiedź:\n")
    print(answer)

    if save:
        output_path = save_answer(
            question=question,
            answer=answer,
            selected_paths=selected_paths,
        )

        print(f"\nOdpowiedź zapisana jako: {output_path}")
        
        
def select_relevant_pages_with_search(question: str, limit: int = 5) -> list[str]:
    results = search_wiki(
        query=question,
        limit=limit,
    )

    return [result.ref for result in results]


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

    query_wiki(
    question=args.question,
    save=args.save,
    mode=args.mode,
)


if __name__ == "__main__":
    main()