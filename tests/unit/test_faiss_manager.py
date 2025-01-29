"""
Unit test for the `load_or_create_embeddings` function.

This test ensures that:
1. The function correctly loads an existing FAISS index if it exists.
2. It generates a new FAISS index if one does not exist.
3. It correctly handles text chunks as both plain strings and dictionaries with metadata.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from langchain_community.vectorstores import FAISS

from vectorstore.faiss_manager import load_or_create_embeddings


@pytest.fixture
def mock_embeddings():
    """Create a mock embedding model for testing."""
    return MagicMock()


@pytest.fixture
def temp_faiss_dir(tmp_path):
    """Create a temporary directory for storing FAISS index files."""
    return str(tmp_path / "faiss_index")


def test_load_existing_faiss_index(mock_embeddings, temp_faiss_dir):
    """
    Test if `load_or_create_embeddings` loads an existing FAISS index correctly.
    """
    # Simulate an existing FAISS index
    os.makedirs(temp_faiss_dir, exist_ok=True)
    faiss_index_path = os.path.join(temp_faiss_dir, "index.faiss")
    open(faiss_index_path, "w").close()  # Create an empty FAISS file

    with patch.object(FAISS, "load_local", return_value="mock_vectorstore") as mock_load:
        vectorstore = load_or_create_embeddings(None, temp_faiss_dir, mock_embeddings)

        # Assertions
        mock_load.assert_called_once_with(temp_faiss_dir, mock_embeddings, allow_dangerous_deserialization=True)
        assert vectorstore == "mock_vectorstore"


def test_create_new_faiss_index_with_text(mock_embeddings, temp_faiss_dir):
    """
    Test if `load_or_create_embeddings` correctly generates a new FAISS index from text chunks.
    """
    text_chunks = ["Sample text 1", "Sample text 2"]

    with patch.object(FAISS, "from_texts", return_value=MagicMock()) as mock_from_texts:
        vectorstore = load_or_create_embeddings(text_chunks, temp_faiss_dir, mock_embeddings)

        # Assertions
        mock_from_texts.assert_called_once_with(text_chunks, mock_embeddings, metadatas=None)
        assert vectorstore is not None


def test_create_new_faiss_index_with_metadata(mock_embeddings, temp_faiss_dir):
    """
    Test if `load_or_create_embeddings` correctly processes text chunks with metadata.
    """
    text_chunks = [
        {"text": "Document 1 content", "metadata": {"source": "doc1.pdf"}},
        {"text": "Document 2 content", "metadata": {"source": "doc2.pdf"}},
    ]

    with patch.object(FAISS, "from_texts", return_value=MagicMock()) as mock_from_texts:
        vectorstore = load_or_create_embeddings(text_chunks, temp_faiss_dir, mock_embeddings)

        # Assertions
        texts = [chunk["text"] for chunk in text_chunks]
        metadatas = [chunk["metadata"] for chunk in text_chunks]
        mock_from_texts.assert_called_once_with(texts, mock_embeddings, metadatas=metadatas)
        assert vectorstore is not None


def test_create_new_faiss_index_with_invalid_input(mock_embeddings, temp_faiss_dir):
    """
    Test if `load_or_create_embeddings` raises an error when given an invalid input type.
    """
    invalid_chunks = [123, 456]  # Invalid input (neither strings nor dicts)

    with pytest.raises(
        ValueError,
        match="source_text_chunks must be a list of strings or dictionaries with 'text' and 'metadata' keys.",
    ):
        load_or_create_embeddings(invalid_chunks, temp_faiss_dir, mock_embeddings)


def test_create_new_faiss_index_with_empty_input(mock_embeddings, temp_faiss_dir):
    """
    Test if `load_or_create_embeddings` raises an error when given an empty list.
    """
    with pytest.raises(ValueError, match="source_text_chunks must be provided to create new embeddings."):
        load_or_create_embeddings([], temp_faiss_dir, mock_embeddings)
