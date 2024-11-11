def create_retriever(pdf_vectorstore):
    return pdf_vectorstore.as_retriever()

