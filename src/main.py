"""
Main script for testing the configuration of environment variables.

This script imports the necessary environment variables from the configuration module
and uses helper functions to load PDFs and split their text into manageable chunks.
"""

import os

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

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Initialize parser
parser = StrOutputParser()

# Check if the FAISS index already exists
if os.path.exists(os.path.join(FAISS_INDEX_PATH, "index.faiss")):
    print(f"Loading existing embeddings from: {FAISS_INDEX_PATH}")
    pdf_vectorstore = load_or_create_embeddings(None, FAISS_INDEX_PATH, embeddings)
else:
    print("FAISS index not found. Generating a new index...")

    # Load all PDFs from the specified folder
    all_documents = load_all_pdfs(PDF_FOLDER)

    # Ensure documents are not empty
    if not all_documents:
        raise ValueError(
            "No PDFs found or failed to extract text from PDFs. Ensure the folder contains valid PDF files."
        )

    # Split each document's text into chunks with source metadata
    all_chunks = []
    for document in all_documents:
        text = document["text"]
        source = document["source"]

        # Split the text into chunks
        chunks = split_text_into_chunks(text, source)
        all_chunks.extend(chunks)

    # Ensure chunks are not empty
    if not all_chunks:
        raise ValueError("Failed to split text into chunks. Check your splitter configuration or input data.")

    # Create a new FAISS index with the text chunks
    texts = [chunk["text"] for chunk in all_chunks]  # Wyodrębnij teksty z chunków
    pdf_vectorstore = load_or_create_embeddings(texts, FAISS_INDEX_PATH, embeddings)


# Create retriever
retriever = create_retriever(pdf_vectorstore)

# Initialize GPT model
model = initialize_gpt_model(OPENAI_API_KEY, MODEL)

# Create prompt template
prompt = create_prompt_template()

# Create processing chain
chain = create_chain(retriever, prompt, model, parser)

# Interactive prompt
print("\n=== Interaktywny System Wyszukiwania Informacji ===")
print("=== Interactive Information Retrieval System ===")
print("Wpisz pytanie, aby uzyskać odpowiedź. Mozesz pisać po polsku lub po angielsku.")
print("Type your question to get an answer. You can write in Polish or English.")
print("Aby zakończyć, wpisz 'exit'.")
print("Type 'exit' to quit.\n")

while True:
    question = input("Twoje pytanie / Your question: ")

    # Exit condition
    if question.lower() == "exit":
        print("Zakończenie programu. Dziękuję za korzystanie z systemu!")
        print("Exiting the program. Thank you for using the system!")
        break

    # Process the query using the chain
    result = chain.invoke({"question": question})

    # Display the result
    print("\n=== Odpowiedź / Answer ===")
    print(result)
    print("=================\n")
