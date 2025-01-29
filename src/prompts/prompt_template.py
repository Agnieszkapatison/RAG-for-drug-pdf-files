"""This module contains functions for handling prompt templates for the interactive information retrieval system.

It defines a template that guides the assistant to answer questions based on provided context. The assistant:
- Responds with "No data in the attached sources." if relevant information is not found.
- Provides comprehensive answers and, if possible, includes the source of information.
- Answers in Polish if the question is in Polish, and in English if the question is in English.
"""

from langchain.prompts import PromptTemplate


def create_prompt_template():
    """Create a prompt template for an assistant that provides answers based on the provided context.

    The template includes instructions for the assistant to:
    - Respond with "No data in the attached sources." if relevant information is not found in the sources.
    - Provide a comprehensive answer and indicate the source of the information if possible.
    - Answer in Polish if the question is asked in Polish, and in English if the question is asked in English.

    Returns:
        PromptTemplate: An instance of PromptTemplate created from the defined template.
    """
    template = """You are an assistant that provides answers exclusively based on the provided context.
        If you cannot find relevant information in the attached sources, respond: "No data in the attached sources."
        Please provide a comprehensive answer and, if possible, indicate the source of the information.
        If the question is asked in Polish, answer in Polish. If the question is asked in English, answer in English.
        Context: {context}
        Question: {question}
        """
    return PromptTemplate.from_template(template)
