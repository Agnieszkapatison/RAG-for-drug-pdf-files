"""
Performance tests for the RAG pipeline.

These tests measure the execution time of different components of the RAG system,
including FAISS search and GPT model inference.
"""

import os

import pytest
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.embeddings import OpenAIEmbeddings

# Load environment variables
from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY
from models.gpt_model import initialize_gpt_model
from models.retriever import create_retriever
from pipeline.rag_pipeline import create_chain
from prompts.prompt_template import create_prompt_template
from vectorstore.faiss_manager import load_or_create_embeddings


@pytest.fixture(scope="module")
def setup_chain():
    """
    Fixture to initialize the RAG pipeline with required components.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    parser = StrOutputParser()
    pdf_vectorstore = load_or_create_embeddings(None, FAISS_INDEX_PATH, embeddings)
    retriever = create_retriever(pdf_vectorstore)
    model = initialize_gpt_model(OPENAI_API_KEY, MODEL)
    prompt = create_prompt_template()

    return create_chain(retriever, prompt, model, parser)


@pytest.mark.benchmark
def test_faiss_search_performance(benchmark, setup_chain):
    """
    Measure the execution time of the FAISS-based retriever processing a query.
    """
    query = "What are the side effects of ibuprofen?"
    result = benchmark(setup_chain.invoke, {"question": query})

    assert result is not None
