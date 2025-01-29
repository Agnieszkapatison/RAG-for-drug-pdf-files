"""
Initialize the GPT model.

This module initializes the GPT model using OpenAI's API.

It provides a function to set up a GPT-based conversational model with specified parameters, such as API key, model name, and temperature.
"""

from langchain_openai import ChatOpenAI


def initialize_gpt_model(api_key, model_name, temperature=0):
    """
    Initialize a GPT model using OpenAI's API.

    Args:
        api_key (str): The API key for OpenAI authentication.
        model_name (str): The name of the GPT model to use (e.g., "gpt-4").
        temperature (float, optional): The temperature setting for response randomness. Defaults to 0 (deterministic output).

    Returns:
        ChatOpenAI: An instance of the OpenAI GPT model ready for inference.
    """
    return ChatOpenAI(openai_api_key=api_key, model=model_name, temperature=temperature)
