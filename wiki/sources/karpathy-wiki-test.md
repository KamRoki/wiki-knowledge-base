---
type: source
title: "karpathy-wiki-test"
description: "Testowy dokument opisujący koncepcję LLM Wiki: model buduje trwałą bazę wiedzy w plikach Markdown, a surowe źródła pozostają niezmienione."
tags: [LLM, wiki, baza-wiedzy, RAG, ingest]
timestamp: 2026-07-07
sources: []
---

# Karpathy Wiki Test

## Streszczenie

Dokument opisuje koncepcję LLM Wiki: model językowy nie tylko odpowiada na pytania, lecz tworzy trwałą bazę wiedzy w formie plików Markdown. Surowe źródła pozostają niezmienione, a AI przetwarza je do uporządkowanych stron wiki. W przeciwieństwie do klasycznego RAG, wiedza nie jest za każdym razem składana od zera — jest stopniowo kompilowana, aktualizowana i łączona z innymi stronami.

## Kluczowe punkty

- Cel LLM Wiki: budować trwałą bazę wiedzy w plikach Markdown.
- Surowe źródła (raw) pozostają niezmienione.
- AI przetwarza surowe źródła do uporządkowanych stron wiki.
- Różnica względem klasycznego RAG: wiedza jest kompilowana i utrzymywana stopniowo, zamiast być rekonstruowaną od zera przy każdym zapytaniu.
- Kładzenie nacisku na aktualizację i łączenie istniejących stron.

## Cytaty / ważne fragmenty

- "Koncepcja LLM Wiki polega na tym, że model językowy nie tylko odpowiada na pytania, ale buduje trwałą bazę wiedzy w plikach Markdown."
- "Surowe źródła pozostają niezmienne, a AI przetwarza je do postaci uporządkowanych stron wiki."
- "W przeciwieństwie do klasycznego RAG, wiedza nie jest za kadym razem  składana od zera. Jest stopniowo kompilowana, aktualizowana i łączona z innymi stronami."

## Powiązania

- Porównanie: LLM Wiki vs klasyczne RAG
- Proces ingest: zasady dodawania i przetwarzania plików surowych
- Struktura repozytorium: role katalogów raw/ i wiki/
- Format stron wiki (frontmatter YAML, sekcje obowiązkowe)
- Zasady logowania i aktualizacji indeksu po każdym ingest