from llm_client import ask_llm


def main() -> None:
    response = ask_llm("Odpowiedź jednym zdaniem: czy połączenie z OpenAI działa?")
    print(response)
    
    
if __name__ == "__main__":
    main()