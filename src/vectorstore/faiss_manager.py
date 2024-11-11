import os
from langchain_community.vectorstores import FAISS


def load_or_create_embeddings(source_text_chunks, onedrive_path, embeddings):
    if os.path.exists(onedrive_path):
        print(f"Ładowanie istniejących embeddingów z: {onedrive_path}")
        # Ładowanie zapisanych embeddingów FAISS
        vectorstore = FAISS.load_local(onedrive_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print(f"Embeddingi nie istnieją. Generowanie nowych embeddingów i zapis do: {onedrive_path}")
        # Generowanie nowych embeddingów
        vectorstore = FAISS.from_texts(source_text_chunks, embeddings)
        # Zapisanie embeddingów FAISS na dysku
        vectorstore.save_local(onedrive_path)
    return vectorstore

