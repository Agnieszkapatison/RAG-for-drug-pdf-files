"""
Main script for testing the configuration of environment variables.

This script imports the necessary environment variables from the configuration module
and uses helper functions to load PDFs and split their text into manageable chunks.
"""

from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER
from data_preparation.pdf_loader import load_all_pdfs
from data_preparation.text_splitter import split_text_into_chunks
from vectorstore.faiss_manager import load_or_create_embeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER
from data_preparation.pdf_loader import load_all_pdfs
from data_preparation.text_splitter import split_text_into_chunks
from vectorstore.faiss_manager import load_or_create_embeddings
from models.retriever import create_retriever
from models.gpt_model import initialize_gpt_model
from prompts.prompt_template import create_prompt_template
from pipeline.rag_pipeline import create_chain
import os


# Inicjalizacja embeddingów z OpenAI
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
from langchain_core.output_parsers import StrOutputParser

# Inicjalizacja parsera
parser = StrOutputParser()


# Display the values of the variables to verify that they are correctly loaded
#print(f"OpenAI API Key: {OPENAI_API_KEY}")
#print(f"Model: {MODEL}")
#print(f"PDF Folder Path: {PDF_FOLDER}")
#print(f"FAISS Index Path: {FAISS_INDEX_PATH}")

# Sprawdzenie, czy istnieje już zapisany indeks FAISS
if os.path.exists(FAISS_INDEX_PATH):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pdf_vectorstore = load_or_create_embeddings(None, FAISS_INDEX_PATH, embeddings)  # Przekazujemy None, bo chunks nie są potrzebne
else:
    # Jeśli indeks nie istnieje, ładujemy i przetwarzamy pliki PDF oraz tworzymy embeddingi
    print("Ładowanie i przetwarzanie plików PDF...")
    all_text = load_all_pdfs(PDF_FOLDER)
    
    # Dzielenie tekstu na fragmenty (chunks), ponieważ embeddingi będą generowane od nowa
    chunks = split_text_into_chunks(all_text)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pdf_vectorstore = load_or_create_embeddings(chunks, FAISS_INDEX_PATH, embeddings)

# Tworzenie retrievera
retriever = create_retriever(pdf_vectorstore)

# Inicjalizacja modelu GPT
model = initialize_gpt_model(OPENAI_API_KEY, MODEL)

# Tworzenie szablonu prompta
prompt = create_prompt_template()

# Tworzenie łańcucha przetwarzania
chain = create_chain(retriever, prompt, model, parser)

# Interaktywny prompt
print("\n=== Interaktywny System Wyszukiwania Informacji ===")
print("Wpisz pytanie, aby uzyskać odpowiedź.")
print("Aby zakończyć, wpisz 'exit'.\n")

while True:
    question = input("Twoje pytanie: ")
    
    # Sprawdzenie, czy użytkownik chce zakończyć program
    if question.lower() == "exit":
        print("Zakończenie programu. Dziękuję za korzystanie z systemu!")
        break
    
    # Przetworzenie zapytania za pomocą łańcucha
    result = chain.invoke({"question": question})
    
    # Wyświetlenie odpowiedzi
    print("\n=== Odpowiedź ===")
    print(result)
    print("=================\n")