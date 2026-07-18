import re

from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

from ..domain.search_result import SearchResult
from ..domain.wiki_page import WikiPage


def tokenize(text: str) -> list[str]:
    """
    Prosta tokenizacja tekstu:
    - zamienia tekst na małe litery,
    - usuwa znaki specjalne,
    - dzieli na słowa.
    """
    text = text.lower()
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]+", text)


def make_snippet(text: str, query: str, max_length: int = 240) -> str:
    """
    Tworzy krótki fragment strony do pokazania w wynikach.
    Jeżeli znajdzie słowo z zapytania, pokazuje okolice tego słowa.
    """
    clean_text = re.sub(r"\s+", " ", text).strip()
    query_terms = tokenize(query)

    lower_text = clean_text.lower()

    best_position = None

    for term in query_terms:
        position = lower_text.find(term.lower())

        if position != -1:
            best_position = position
            break

    if best_position is None:
        return clean_text[:max_length] + ("..." if len(clean_text) > max_length else "")

    start = max(best_position - 80, 0)
    end = min(start + max_length, len(clean_text))

    snippet = clean_text[start:end]

    if start > 0:
        snippet = "..." + snippet

    if end < len(clean_text):
        snippet = snippet + "..."

    return snippet


def semantic_search(pages: list[WikiPage], query: str, limit: int = 5) -> list[SearchResult]:
    """
    Wyszukiwanie semantyczne po znaczeniu tekstu (embeddingi OpenAI),
    zamiast dopasowania dosłownych słów kluczowych (dawniej BM25).
    """
    if not pages:
        return []

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    store = InMemoryVectorStore(embeddings)
    store.add_documents([
        Document(
            page_content=page.content,
            metadata={"ref": page.ref, "path": page.path},
        )
        for page in pages
    ])

    results = store.similarity_search_with_score(query, k=limit)

    return [
        SearchResult(
            ref=doc.metadata["ref"],
            path=doc.metadata["path"],
            score=score,
            snippet=make_snippet(doc.page_content, query),
        )
        for doc, score in results
    ]
