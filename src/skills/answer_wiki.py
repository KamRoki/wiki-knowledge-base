# src/skills/answer_wiki.py
from langchain_core.tools import tool

from ..use_cases.answer_question import answer_question


@tool
def answer_wiki(question: str) -> str:
    """
    Odpowiada na pytania o zawartości Wiki, wyszukując semantycznie 
    (embeddingi) najlepiej pasujące strony.
    """
    result = answer_question(question = question)
    return result.answer