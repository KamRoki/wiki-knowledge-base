from ..domain.search_result import SearchResult
from ..infrastructure.embeddings import semantic_search
from ..infrastructure.wiki_repository import list_wiki_pages


def search_wiki(query: str, limit: int = 5) -> list[SearchResult]:
    pages = list_wiki_pages()
    return semantic_search(pages=pages, query=query, limit=limit)