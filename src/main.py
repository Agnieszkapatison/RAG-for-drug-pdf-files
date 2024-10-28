"""
Main script for testing the configuration of environment variables.

This script imports the necessary environment variables from the configuration module
and uses helper functions to load PDFs and split their text into manageable chunks.
"""

from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER
from data_preparation.pdf_loader import load_all_pdfs
from data_preparation.text_splitter import split_text_into_chunks

# Display the values of the variables to verify that they are correctly loaded
print(f"OpenAI API Key: {OPENAI_API_KEY}")
print(f"Model: {MODEL}")
print(f"PDF Folder Path: {PDF_FOLDER}")
print(f"FAISS Index Path: {FAISS_INDEX_PATH}")

# Load all text from PDF files in the folder
all_text = load_all_pdfs(PDF_FOLDER)

# Split the loaded text into chunks
chunks = split_text_into_chunks(all_text)

# Print the number of chunks
print(f"Number of chunks: {len(chunks)}")
