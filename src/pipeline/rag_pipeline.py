"""Create and return a processing chain.

This module provides functionality to create a processing chain by
combining a retriever, prompt, model, and parser.
"""

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()


def create_chain(retriever, prompt, model, parser):
    """Create a processing chain using the provided retriever, prompt, model, and parser.

    Args:
        retriever: An object responsible for retrieving relevant information.
        prompt: A prompt to guide the processing chain.
        model: A model used for processing the retrieved information.
        parser: A parser to interpret the processed information.

    Returns:
        A processing chain that integrates the retriever, prompt, model, and parser.
    """
    # noqa: R504 - Keeping explicit variable assignment for clarity
    chain = (  # noqa: R504
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
        }  # noqa: W503
        | prompt  # noqa: W503
        | model  # noqa: W503
        | parser  # noqa: W503
    )
    return chain  # noqa: R504
