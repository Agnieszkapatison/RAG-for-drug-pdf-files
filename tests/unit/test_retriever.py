"""
Unit tests for the retriever creation module.

This module tests the `create_retriever` function to ensure:
- It correctly creates a retriever from a FAISS-based vector store.
- The returned object behaves as expected.

Dependencies:
- `pytest` for test execution.
- `unittest.mock` for mocking FAISS-based vector store.
- `create_retriever` function from `retriever.py`.
"""

from unittest.mock import MagicMock

import pytest

from models.retriever import create_retriever


def test_create_retriever():
    """
    Test if `create_retriever` correctly initializes a retriever from a FAISS vector store.

    Expected:
    - The function should return a retriever object.
    - `as_retriever` should be called on the provided FAISS vector store.
    """
    # Create a mock FAISS vector store with `as_retriever` method
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.return_value = "mock_retriever"

    retriever = create_retriever(mock_vectorstore)

    # Ensure function returns the expected retriever object
    assert retriever == "mock_retriever"

    # Ensure `as_retriever` method was called on the vector store
    mock_vectorstore.as_retriever.assert_called_once()
