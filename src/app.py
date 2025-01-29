"""This module contains functions for handling the interactive information retrieval system using Streamlit.

It initializes and loads FAISS-based vector search, processes PDF documents, and integrates a GPT model for answering user queries.
Users can interact with the system through a web interface and ask questions in Polish or English.
"""

import os

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.embeddings import OpenAIEmbeddings

from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER
from data_preparation.pdf_loader import load_all_pdfs
from data_preparation.text_splitter import split_text_into_chunks
from models.gpt_model import initialize_gpt_model
from models.retriever import create_retriever
from pipeline.rag_pipeline import create_chain
from prompts.prompt_template import create_prompt_template
from vectorstore.faiss_manager import load_or_create_embeddings

# Inicjalizacja embeddingów OpenAI
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Inicjalizacja parsera
parser = StrOutputParser()

# Sprawdzenie, czy istnieje indeks FAISS
if os.path.exists(os.path.join(FAISS_INDEX_PATH, "index.faiss")):
    print(f"Loading existing embeddings from: {FAISS_INDEX_PATH}")
    pdf_vectorstore = load_or_create_embeddings(None, FAISS_INDEX_PATH, embeddings)
else:
    print("FAISS index not found. Generating a new index...")

    # Ładowanie i przetwarzanie plików PDF
    all_documents = load_all_pdfs(PDF_FOLDER)

    # Upewnienie się, że pliki PDF nie są puste
    if not all_documents:
        raise ValueError("No PDFs found or failed to extract text. Ensure the folder contains valid PDF files.")

    # Dzielenie każdego dokumentu na fragmenty
    all_chunks = []
    for document in all_documents:
        text = document["text"]
        source = document["source"]
        chunks = split_text_into_chunks(text, source)
        all_chunks.extend(chunks)

    # Sprawdzenie, czy fragmenty nie są puste
    if not all_chunks:
        raise ValueError("Failed to split text into chunks. Check your splitter configuration or input data.")

    # Tworzenie nowego indeksu FAISS
    texts = [chunk["text"] for chunk in all_chunks]
    pdf_vectorstore = load_or_create_embeddings(texts, FAISS_INDEX_PATH, embeddings)

# Tworzenie retrievera
retriever = create_retriever(pdf_vectorstore)

# Inicjalizacja modelu GPT
model = initialize_gpt_model(OPENAI_API_KEY, MODEL)

# Tworzenie szablonu prompta
prompt = create_prompt_template()

# Tworzenie łańcucha przetwarzania
chain = create_chain(retriever, prompt, model, parser)

# Streamlit UI
st.title("🔍 Interaktywny System Wyszukiwania Informacji / Interactive Information Retrieval System")

# Inicjalizacja historii pytań i odpowiedzi w sesji
if "history" not in st.session_state:
    st.session_state.history = []

# Informacja dla użytkownika
st.write("Wpisz pytanie, aby uzyskać odpowiedź. Możesz pisać po polsku lub po angielsku.")
st.write("Type your question to get an answer. You can write in Polish or English.")

# Pole do wpisania pytania
question = st.text_input("✍ Twoje pytanie / Your question:")

# Przycisk do wysłania pytania
if st.button("🔎 Zapytaj / Ask"):
    if question:
        # Przetwarzanie zapytania
        response = chain.invoke({"question": question})

        # Wyświetlenie odpowiedzi
        st.write("### ✅ Odpowiedź / Answer")
        st.write(response)

        # Dodanie do historii
        st.session_state.history.append({"question": question, "response": response})
    else:
        st.warning("⚠️ Proszę wpisać pytanie przed kliknięciem przycisku!")

# Historia pytań i odpowiedzi
if st.session_state.history:
    st.write("### 📜 Historia pytań i odpowiedzi / Question & Answer History")
    for item in reversed(st.session_state.history):  # Najnowsze na górze
        st.write(f"**❓ Pytanie / Question:** {item['question']}")
        st.write(f"**📝 Odpowiedź / Answer:** {item['response']}")
