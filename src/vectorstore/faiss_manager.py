import os
from langchain_community.vectorstores import FAISS

def load_or_create_embeddings(source_text_chunks, onedrive_path, embeddings):
    """
    Load or create embeddings and save them to FAISS index.

    Args:
        source_text_chunks (list): List of dictionaries with 'text' and 'metadata'.
        onedrive_path (str): Path to save or load the FAISS index.
        embeddings: Embedding model to generate embeddings for text chunks.

    Returns:
        vectorstore: The FAISS index with loaded or created embeddings.
    """
    if os.path.exists(onedrive_path):
        print(f"Ładowanie istniejących embeddingów z: {onedrive_path}")
        # Ładowanie zapisanych embeddingów FAISS
        vectorstore = FAISS.load_local(onedrive_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print(f"Embeddingi nie istnieją. Generowanie nowych embeddingów i zapis do: {onedrive_path}")
        # Oddziel teksty i metadane z `source_text_chunks`
        texts = [chunk["text"] for chunk in source_text_chunks]           # Pobieramy tylko teksty
        metadatas = [chunk["metadata"] for chunk in source_text_chunks]   # Pobieramy metadane (nazwy plików)

        # Tworzenie FAISS z tekstami i metadanymi
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

        # Zapisanie embeddingów FAISS na dysku
        vectorstore.save_local(onedrive_path)
    return vectorstore
