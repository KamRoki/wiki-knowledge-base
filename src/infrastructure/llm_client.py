import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise RuntimeError(
            "Brakuje OPENAI_API_KEY. Dodaj klucz do pliku .env albo ustaw zmienną środowiskową."
        )
        
    return OpenAI(api_key = api_key)


def ask_llm(prompt: str) -> str:
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    
    response = client.responses.create(
        model = model,
        input = prompt
    )
    
    return response.output_text 