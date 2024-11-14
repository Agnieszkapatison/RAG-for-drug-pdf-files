import streamlit as st
from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER
from data_preparation.pdf_loader import load_all_pdfs
from data_preparation.text_splitter import split_text_into_chunks
from vectorstore.faiss_manager import load_or_create_embeddings
from models.retriever import create_retriever
from models.gpt_model import initialize_gpt_model
from prompts.prompt_template import create_prompt_template
from pipeline.rag_pipeline import create_chain
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_openai.embeddings import OpenAIEmbeddings

# Inicjalizacja parsera
parser = StrOutputParser()

@st.cache_resource
def get_vectorstore(FAISS_INDEX_PATH, _embeddings, PDF_FOLDER):
    if os.path.exists(FAISS_INDEX_PATH):
        return load_or_create_embeddings(None, FAISS_INDEX_PATH, _embeddings)
    else:
        # Ładowanie i przetwarzanie PDF-ów
        documents = load_all_pdfs(PDF_FOLDER)
        all_chunks = []

        for doc in documents:
            # Dzielimy każdy tekst z osobna i dodajemy metadane z nazwą pliku
            chunks = split_text_into_chunks(doc["text"], doc["source"])
            all_chunks.extend(chunks)  # Dodajemy każdy chunk z metadanymi do listy

        return load_or_create_embeddings(all_chunks, FAISS_INDEX_PATH, _embeddings)


# Wczytanie vectorstore
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
pdf_vectorstore = get_vectorstore(FAISS_INDEX_PATH, embeddings, PDF_FOLDER)

# Tworzenie retrievera
retriever = create_retriever(pdf_vectorstore)

# Inicjalizacja modelu GPT
model = initialize_gpt_model(OPENAI_API_KEY, MODEL)

# Tworzenie szablonu prompta
prompt = create_prompt_template()

# Tworzenie łańcucha z parserem
chain = create_chain(retriever, prompt, model, parser)

# Streamlit UI
st.title("Interaktywny System Wyszukiwania Informacji")

# Inicjalizacja historii pytań i odpowiedzi w sesji
if "history" not in st.session_state:
    st.session_state.history = []

# Filtry wyszukiwania
st.sidebar.write("### Filtry wyszukiwania")
keywords = st.sidebar.text_input("Słowa kluczowe")

# Opcje wyświetlania kontekstu i historii
show_context = st.sidebar.checkbox("Pokaż fragment kontekstu", value=True)
show_history = st.sidebar.checkbox("Pokaż historię pytań i odpowiedzi", value=True)

# Wprowadzenie pytania przez użytkownika
question = st.text_input("Wpisz swoje pytanie:")

if st.button("Zapytaj"):
    # Przetworzenie zapytania za pomocą łańcucha
    response = chain.invoke({"question": question})
    st.write("### Odpowiedź")
    st.write(response)

    # Dodanie pytania i odpowiedzi do historii
    st.session_state.history.append({"question": question, "response": response})

    # Wyświetlenie fragmentu kontekstu, jeśli zaznaczono
    if show_context:
        context_snippet = pdf_vectorstore.similarity_search(question, k=3)
        if context_snippet:
            st.write("#### Fragment kontekstu")
            for snippet in context_snippet:
                st.write(f"Źródło: {snippet.metadata.get('source', 'Nieznane')}")
                st.write(snippet.page_content)



# Wyświetlanie historii pytań i odpowiedzi, jeśli zaznaczono
if show_history:
    st.write("### Historia pytań i odpowiedzi")
    for item in st.session_state.history:
        st.write(f"**Pytanie**: {item['question']}")
        st.write(f"**Odpowiedź**: {item['response']}")


