"""
Text Splitter Module.

This module contains functions for splitting large pieces of text into smaller chunks.
The `split_text_into_chunks` function uses a character-based splitting approach to
break text into manageable segments with optional overlap between the chunks.

Dependencies:
- langchain's `RecursiveCharacterTextSplitter` for splitting the text efficiently.

Usage Example:
    from data_preparation.text_splitter import split_text_into_chunks

    text = "Some large text to split..."
    chunks = split_text_into_chunks(text, chunk_size=1500, chunk_overlap=100)
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text_into_chunks(text, chunk_size=1500, chunk_overlap=100):
    """
    Split the provided text into smaller chunks.

    Args:
        text (str): The text to be split.
        chunk_size (int, optional): The size of each chunk. Defaults to 1500.
        chunk_overlap (int, optional): The overlap between chunks. Defaults to 100.

    Returns:
        list: A list of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)
