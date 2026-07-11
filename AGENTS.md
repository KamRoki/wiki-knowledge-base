# AGENTS.md

## Cel Projektu

Projekt buduje ywą bazę wiedzy w formie plików Markdown.

## Warstwy

- raw/ - surowe źródła, których nie wolno modyfikować.
- wiki/ - strony Markdown generowane przez AI.
- AGENTS.md - zasady pracy systemu.

## Twarde Zasady

1. Nigdy nie modyfikuj plików w raw/.
2. Wszystkie wygenerowane strony zapisuj w wiki/.
3. Kada strona źródłowa powinna mieć frontmatter YAML.
4. Po każdym ingest dopisz wpis do wiki/log.md.
5. Po każdym ingest zaktualizuj wiki/index.md.


## Workflow: Ingest

Po otrzymaniu źródła z folderu raw/ AI ma wykonać następujące kroki:

1. Przeczytać źródło.
2. Utworzyć stronę źródłową w wiki/sources/.
3. Wskazać najważniejsze encje, np. osoby, firmy, narzędzia, projekty.
4. Wskazać najważniejsze pojęcia, np. metody, koncepcje, problemy, idee.
5. Przygotować lub zaktualizować strony encji w wiki/entities/.
6. Przygotować lub zaktualizować strony pojęć w wiki/concepts/.
7. Zaproponować wpisy do wiki/index.md.
8. Nie modyfikować żadnego pliku w raw/.

## Format odpowiedzi dla ingest

Model ma zwracać wyłącznie poprawny JSON, bez komentarzy przed i po.

Nie wolno zwracać odpowiedzi w bloku mardkown typu ```json.

Struktura JSON:
{
  "source": {
    "title": "...",
    "slug": "...",
    "description": "...",
    "content": "..."
  },
  "entities": [
    {
      "title": "...",
      "slug": "...",
      "description": "...",
      "content": "..."
    }
  ],
  "concepts": [
    {
      "title": "...",
      "slug": "...",
      "description": "...",
      "content": "..."
    }
  ],
  "index_entries": [
    {
      "section": "Sources | Entities | Concepts",
      "path": "sources/example",
      "description": "..."
    }
  ]
}

## Format Strony Źródłowej

Każda strona w wiki/sources/ powinna mieć format:

---
type: source
title: "Tytuł"
description: "Krótki opis"
tags: []
timestamp: YYYY-MM-DD
sources: []
---

# Tytuł

## Streszczenie

## Kluczowe punkty

## Cytaty / ważne fragmenty

## Powiązania


## Workflow: Lint

Lint sprawdza zdrowie Wiki.

Zakres kontroli:

1. Czy każda strona Markdown w wiki/sources, wiki/entities i wiki/concepts ma frontmatter YAML.
2. Czy frontmatter zawiera pola:
  - type
  - title
  - description
  - tags
  - timestamp
  - sources
3. Czy wszytskie linki Obsidiana [[...]] prowadzą do istniejących stron.
4. Czy strony z wiki/sources/, wiki/entities/ i wiki/concepts są wpisane w wiki/index.md.
5. Czy istnieją strony-sieroty, czyli strony, do których nie prowadzi żaden link z innych stron.
6. Czy index.md zawiera wpisy do stron, które nie istnieją.

Lint nie modyfikuje raw/.
Lint nie usuwa stron.
Lint generuje raport w wiki/reports/health-report.md.