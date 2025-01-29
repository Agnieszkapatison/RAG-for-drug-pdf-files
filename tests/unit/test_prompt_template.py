"""
Unit test for the `create_prompt_template` function.

This test ensures that:
1. The function returns a `PromptTemplate` instance.
2. The template contains the required placeholders `{context}` and `{question}`.
3. The template includes the expected instruction text.
"""

import pytest
from langchain.prompts import PromptTemplate

from prompts.prompt_template import create_prompt_template


def test_create_prompt_template():
    """
    Test if `create_prompt_template` returns a valid prompt template.

    Expected:
    - The returned object should be an instance of `PromptTemplate`.
    - The template should contain `{context}` and `{question}` placeholders.
    - The template should include key instructions for the assistant.
    """
    # Call function
    prompt = create_prompt_template()

    # Ensure the returned object is a PromptTemplate
    assert isinstance(prompt, PromptTemplate), "Returned object should be an instance of PromptTemplate"

    # Ensure the template contains required placeholders
    assert "{context}" in prompt.template, "Template is missing the `{context}` placeholder"
    assert "{question}" in prompt.template, "Template is missing the `{question}` placeholder"

    # Ensure the template includes key instructions
    assert "No data in the attached sources." in prompt.template, "Missing expected instruction about unavailable data"
    assert "If the question is asked in Polish, answer in Polish." in prompt.template, "Missing language instruction"
    assert "If the question is asked in English, answer in English." in prompt.template, "Missing language instruction"
