"""This module contains functions for handling FAISS-based vector search and embedding storage.

It allows loading existing embeddings or generating new ones and saving them into a FAISS index. The module:
- Loads embeddings from a FAISS index if it exists.
- Generates new embeddings if no index is found.
- Supports processing text chunks either as plain strings or dictionaries with metadata.
"""

import os

from langchain_community.vectorstores import FAISS


def load_or_create_embeddings(source_text_chunks, index_path, embeddings):
    """
    Load or create embeddings and save them to FAISS index.

    Args:
        source_text_chunks (list): List of text chunks or dictionaries with 'text' and 'metadata'.
        index_path (str): Path to save or load the FAISS index.
        embeddings: Embedding model to generate embeddings.

    Returns:
        vectorstore: The FAISS index with loaded or created embeddings.
    """
    faiss_index_path = os.path.join(index_path, "index.faiss")

    if os.path.exists(faiss_index_path):
        print(f"Loading existing embeddings from: {faiss_index_path}")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    else:
        if not source_text_chunks:
            raise ValueError("source_text_chunks must be provided to create new embeddings.")

        print(f"Embeddings do not exist. Generating new embeddings and saving to: {faiss_index_path}")

        # Check if input is a list of dictionaries or strings
        if isinstance(source_text_chunks[0], dict):
            texts = [chunk["text"] for chunk in source_text_chunks]
            metadatas = [chunk.get("metadata", {}) for chunk in source_text_chunks]
        elif isinstance(source_text_chunks[0], str):
            texts = source_text_chunks
            metadatas = None
        else:
            raise ValueError(
                "source_text_chunks must be a list of strings or dictionaries with 'text' and 'metadata' keys."
            )

        # Generate embeddings and save them to FAISS
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        vectorstore.save_local(index_path)

    return vectorstore
