"""
Unit test for the create_chain function.

This test ensures that `create_chain` initializes a processing chain 
using retriever, prompt, model, and parser.

It verifies that:
1. The function executes without error.
2. The returned object is callable.
"""

from unittest.mock import MagicMock

import pytest

from pipeline.rag_pipeline import create_chain


def test_create_chain_structure():
    """
    Test if `create_chain` returns a processing chain with the expected structure.

    This test verifies that:
    - The function executes without raising an error.
    - The returned object is callable.

    Expected Result:
    - `create_chain` should return a valid processing chain object.
    """
    # Mocking components that support | operator
    mock_retriever = MagicMock()
    mock_prompt = MagicMock()
    mock_model = MagicMock()
    mock_parser = MagicMock()

    # Call function
    chain = create_chain(mock_retriever, mock_prompt, mock_model, mock_parser)

    # Ensure chain is not None
    assert chain is not None, "create_chain returned None"

    # Ensure chain is callable (pipeline behavior)
    assert callable(chain.invoke), "Returned chain should be callable"
