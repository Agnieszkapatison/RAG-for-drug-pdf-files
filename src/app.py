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
# Inicjalizacja embeddingów z OpenAI
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# Flaga do sprawdzenia, czy embeddingi zostały załadowane
embedding_loaded = False

# Sprawdzenie, czy istnieje już zapisany indeks FAISS i ładowanie tylko raz
if os.path.exists(FAISS_INDEX_PATH) and not embedding_loaded:
    pdf_vectorstore = load_or_create_embeddings(None, FAISS_INDEX_PATH, embeddings)
    embedding_loaded = True  # Ustawienie flagi na True, aby uniknąć ponownego ładowania
else:
    all_text = load_all_pdfs(PDF_FOLDER)
    chunks = split_text_into_chunks(all_text)
    pdf_vectorstore = load_or_create_embeddings(chunks, FAISS_INDEX_PATH, embeddings)
    embedding_loaded = True

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

# Wprowadzenie pytania przez użytkownika
question = st.text_input("Wpisz swoje pytanie:")

if st.button("Zapytaj"):
    # Przetworzenie zapytania za pomocą łańcucha
    response = chain.invoke({"question": question})
    
    # Wyświetlenie odpowiedzi
    st.write("### Odpowiedź")
    st.write(response)
