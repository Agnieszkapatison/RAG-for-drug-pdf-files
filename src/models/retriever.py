"""
This module provides a function to create a retriever from a FAISS-based vector store.

A retriever is used to retrieve relevant documents based on input queries, making it a key component in information retrieval systems.
"""


def create_retriever(pdf_vectorstore):
    """
    Create a retriever from the provided FAISS-based vector store.

    Args:
        pdf_vectorstore: The FAISS vector store containing document embeddings.

    Returns:
        A retriever object that allows searching for relevant documents based on query similarity.
    """
    return pdf_vectorstore.as_retriever()
