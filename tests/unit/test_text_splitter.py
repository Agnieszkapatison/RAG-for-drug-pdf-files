"""
Unit tests for the Text Splitter module.

This module tests the `split_text_into_chunks` function to ensure:
- Text is correctly split into chunks of the specified size.
- Overlapping text between chunks is correctly handled.
- Each chunk retains its original source metadata.

Dependencies:
- `pytest` for test execution.
- `split_text_into_chunks` function from `text_splitter.py`.
"""

import pytest

from data_preparation.text_splitter import split_text_into_chunks


def test_split_text_into_chunks_basic():
    """
    Test if `split_text_into_chunks` correctly splits text into chunks of the specified size.

    Expected:
    - Chunks should be within the given `chunk_size` limit.
    - Overlapping content should be correctly handled.
    - Each chunk should retain its source metadata.
    """
    text = "This is a sample text that will be split into chunks. " * 10  # A long repeated text
    source = "sample.pdf"
    chunk_size = 50
    chunk_overlap = 10

    chunks = split_text_into_chunks(text, source, chunk_size, chunk_overlap)

    # Ensure the output is a list of dictionaries
    assert isinstance(chunks, list)
    assert all(isinstance(chunk, dict) for chunk in chunks)

    # Ensure each chunk has 'text' and 'metadata' keys
    assert all("text" in chunk and "metadata" in chunk for chunk in chunks)

    # Ensure each chunk has metadata with the correct source
    assert all(chunk["metadata"]["source"] == source for chunk in chunks)

    # Ensure chunk sizes are within expected limits
    assert all(len(chunk["text"]) <= chunk_size for chunk in chunks)


def test_split_text_into_chunks_overlap():
    """
    Test if `split_text_into_chunks` correctly handles overlapping content between chunks.

    Expected:
    - The last `chunk_overlap` characters of one chunk should appear at the beginning of the next chunk.
    """
    text = "0123456789" * 10  # 100 characters
    source = "overlap_test.pdf"
    chunk_size = 20
    chunk_overlap = 5

    chunks = split_text_into_chunks(text, source, chunk_size, chunk_overlap)

    # Check that there are multiple chunks
    assert len(chunks) > 1

    # Check that overlapping content is present between consecutive chunks
    for i in range(1, len(chunks)):
        prev_chunk = chunks[i - 1]["text"]
        curr_chunk = chunks[i]["text"]
        assert prev_chunk[-chunk_overlap:] == curr_chunk[:chunk_overlap]  # Check overlap consistency


def test_split_text_into_chunks_exact_fit():
    """
    Test if `split_text_into_chunks` handles cases where text fits exactly into chunks.

    Expected:
    - If text length matches `chunk_size`, there should be no unnecessary splits.
    """
    text = "A" * 50
    source = "exact_fit.pdf"
    chunk_size = 50
    chunk_overlap = 10

    chunks = split_text_into_chunks(text, source, chunk_size, chunk_overlap)

    # Expecting only one chunk since text length == chunk size
    assert len(chunks) == 1
    assert chunks[0]["text"] == text
    assert chunks[0]["metadata"]["source"] == source


def test_split_text_into_chunks_small_text():
    """
    Test if `split_text_into_chunks` handles cases where text is smaller than chunk size.

    Expected:
    - The function should return a single chunk without unnecessary splitting.
    """
    text = "Short text"
    source = "small_text.pdf"
    chunk_size = 50
    chunk_overlap = 10

    chunks = split_text_into_chunks(text, source, chunk_size, chunk_overlap)

    # Expecting a single chunk because text is smaller than chunk size
    assert len(chunks) == 1
    assert chunks[0]["text"] == text
    assert chunks[0]["metadata"]["source"] == source
