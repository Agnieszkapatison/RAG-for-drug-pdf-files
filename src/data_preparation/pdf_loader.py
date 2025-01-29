"""
PDF Loader Module.

This module contains functions for loading text from all PDF files in a specified folder.
The `load_all_pdfs` function reads all PDF files in the given directory and returns
a list of dictionaries, each containing the text and filename.

Dependencies:
- PyMuPDF (fitz) for PDF file handling.
- tqdm for displaying the progress bar.

Usage Example:
    from data_preparation.pdf_loader import load_all_pdfs

    pdf_folder = "/path/to/pdf/folder"
    documents = load_all_pdfs(pdf_folder)
"""

import os

import fitz  # PyMuPDF
from tqdm import tqdm


def load_all_pdfs(pdf_folder):
    """
    Load and return text from all PDF files in the specified folder.

    Args:
        pdf_folder (str): The path to the folder containing PDF files.

    Returns:
        list: A list of dictionaries, each containing 'text' and 'source' (filename).
    """
    documents = []
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    # Iterate through all PDF files in the folder with a progress bar
    for filename in tqdm(pdf_files, desc="Processing PDF files"):
        pdf_path = os.path.join(pdf_folder, filename)
        file_text = ""

        try:
            # Open the PDF using PyMuPDF (fitz)
            doc = fitz.open(pdf_path)

            # Iterate through pages and collect text
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                file_text += page.get_text()  # Extract text from each page

            # Append the text and filename to the list of documents
            documents.append({"text": file_text, "source": filename})

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    return documents
