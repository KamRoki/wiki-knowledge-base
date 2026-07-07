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