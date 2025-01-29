"""
Text Splitter Module.

This module contains functions for splitting large pieces of text into smaller chunks
with optional overlap between the chunks. Each chunk will retain metadata about its source file.

Dependencies:
- langchain's `RecursiveCharacterTextSplitter` for splitting the text efficiently.

Usage Example:
    from data_preparation.text_splitter import split_text_into_chunks

    text = "Some large text to split..."
    source = "example.pdf"
    chunks = split_text_into_chunks(text, source, chunk_size=1500, chunk_overlap=100)
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text_into_chunks(text, source, chunk_size=1500, chunk_overlap=100):
    """
    Split the provided text into smaller chunks with source metadata.

    Args:
        text (str): The text to be split.
        source (str): The source filename of the text.
        chunk_size (int, optional): The size of each chunk. Defaults to 1500.
        chunk_overlap (int, optional): The overlap between chunks. Defaults to 100.

    Returns:
        list: A list of dictionaries, each containing a text chunk and its source metadata.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)

    # Add source as metadata to each chunk
    return [{"text": chunk, "metadata": {"source": source}} for chunk in chunks]
