from langchain.prompts import PromptTemplate

def create_prompt_template():
    template = """
    Jesteś asystentem, który udziela odpowiedzi wyłącznie na podstawie dostarczonego kontekstu.
    Jeśli nie znajdziesz odpowiednich informacji w załączonych źródłach, odpowiedz: "Brak danych w załączonych źródłach".

    Proszę, podaj wyczerpującą odpowiedź, a jeśli to możliwe, wskaż źródło informacji. Odpwiadaj zawsze po polsku.

    Kontekst: {context}

    Pytanie: {question}

    """
    return PromptTemplate.from_template(template)

