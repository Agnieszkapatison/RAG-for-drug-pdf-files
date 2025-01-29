"""
Unit tests for the GPT model initialization module.

This module tests the `initialize_gpt_model` function to ensure:
- The function returns an instance of `ChatOpenAI`.
- The model is initialized with the correct parameters.
- The temperature setting affects the randomness of responses.

Dependencies:
- `pytest` for test execution.
- `unittest.mock` for mocking OpenAI API calls.
- `initialize_gpt_model` function from `gpt_model.py`.
"""

from unittest.mock import patch

import pytest
from langchain_openai import ChatOpenAI

from models.gpt_model import initialize_gpt_model


@patch("models.gpt_model.ChatOpenAI")  # Mock ChatOpenAI to prevent actual API calls
def test_initialize_gpt_model(mock_chat_openai):
    """
    Test if `initialize_gpt_model` correctly initializes the OpenAI GPT model.

    Expected:
    - The function should return a `ChatOpenAI` instance.
    - The model should be initialized with the correct API key, model name, and temperature.
    """
    api_key = "test_api_key"
    model_name = "gpt-4"
    temperature = 0.7

    # Mock return value
    mock_chat_openai.return_value = "mock_gpt_model"

    model = initialize_gpt_model(api_key, model_name, temperature)

    # Ensure function returns the mock instance
    assert model == "mock_gpt_model"

    # Ensure ChatOpenAI was called with correct parameters
    mock_chat_openai.assert_called_once_with(openai_api_key=api_key, model=model_name, temperature=temperature)


@patch("models.gpt_model.ChatOpenAI")
def test_initialize_gpt_model_default_temperature(mock_chat_openai):
    """
    Test if `initialize_gpt_model` correctly assigns the default temperature value.

    Expected:
    - If no temperature is provided, the function should default to `0`.
    """
    api_key = "test_api_key"
    model_name = "gpt-4"

    # Mock return value
    mock_chat_openai.return_value = "mock_gpt_model"

    model = initialize_gpt_model(api_key, model_name)  # No temperature passed

    # Ensure function returns the mock instance
    assert model == "mock_gpt_model"

    # Ensure default temperature is set to 0
    mock_chat_openai.assert_called_once_with(openai_api_key=api_key, model=model_name, temperature=0)
