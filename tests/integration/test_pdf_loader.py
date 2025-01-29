"""
Integration test for the PDF Loader module.

This test verifies that the `load_all_pdfs` function correctly reads and extracts text
from all PDF files in a specified directory. It checks:
- If the function processes valid PDFs without errors.
- If the returned data structure is correct (list of dictionaries).
- If it correctly handles an empty directory.

Dependencies:
- PyMuPDF (fitz) for reading PDFs.
- Pytest for test execution.
- TemporaryDirectory from tempfile for safe testing.

Test Strategy:
1. **Setup**: Create a temporary directory with sample PDFs.
2. **Execution**: Call `load_all_pdfs` and capture results.
3. **Validation**: Check output structure and expected behavior.
4. **Teardown**: Automatically clean up temporary files.

"""

import os
from tempfile import TemporaryDirectory

import fitz  # PyMuPDF
import pytest

from data_preparation.pdf_loader import load_all_pdfs


@pytest.fixture
def sample_pdf(tmp_path):
    """
    Fixture to create a sample PDF file for testing.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Returns:
        str: Path to the generated PDF file.
    """
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This is a test PDF.")  # Add sample text
    doc.save(pdf_path)
    doc.close()
    return str(pdf_path)


def test_load_all_pdfs_with_valid_pdf(sample_pdf):
    """
    Test if `load_all_pdfs` correctly reads and extracts text from a valid PDF.

    Steps:
    1. Place a sample PDF in a test directory.
    2. Call `load_all_pdfs` to read it.
    3. Verify the extracted text and structure.

    Expected Result:
    - A list with one dictionary containing 'text' and 'source' keys.
    - The extracted text should match the content written to the PDF.
    """
    test_dir = os.path.dirname(sample_pdf)
    result = load_all_pdfs(test_dir)

    assert isinstance(result, list), "Result should be a list."
    assert len(result) == 1, "Should return exactly one document."
    assert "text" in result[0] and "source" in result[0], "Each entry must contain 'text' and 'source' keys."
    assert result[0]["source"] == "sample.pdf", "Source filename should match."
    assert "This is a test PDF." in result[0]["text"], "Extracted text should match the PDF content."


def test_load_all_pdfs_with_empty_directory():
    """
    Test if `load_all_pdfs` correctly handles an empty directory.

    Steps:
    1. Create an empty temporary directory.
    2. Call `load_all_pdfs` on it.
    3. Verify that it returns an empty list.

    Expected Result:
    - The function should return an empty list without errors.
    """
    with TemporaryDirectory() as empty_dir:
        result = load_all_pdfs(empty_dir)
        assert result == [], "Should return an empty list for an empty directory."


def test_load_all_pdfs_with_non_pdf_files():
    """
    Test if `load_all_pdfs` ignores non-PDF files in the directory.

    Steps:
    1. Create a temporary directory with a mix of PDF and non-PDF files.
    2. Call `load_all_pdfs` to process the directory.
    3. Verify that only PDFs are read.

    Expected Result:
    - Only PDF files should be processed.
    - Non-PDF files should be ignored.
    """
    with TemporaryDirectory() as test_dir:
        # Create a sample PDF
        pdf_path = os.path.join(test_dir, "valid.pdf")
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "PDF content")
        doc.save(pdf_path)
        doc.close()

        # Create a non-PDF file
        txt_path = os.path.join(test_dir, "textfile.txt")
        with open(txt_path, "w") as f:
            f.write("This is a text file, not a PDF.")

        # Run function
        result = load_all_pdfs(test_dir)

        assert len(result) == 1, "Should only process PDFs."
        assert result[0]["source"] == "valid.pdf", "Only the PDF file should be returned."
        assert "PDF content" in result[0]["text"], "Extracted text should match PDF content."


def test_load_all_pdfs_with_corrupt_pdf():
    """
    Test if `load_all_pdfs` gracefully handles a corrupt PDF file.

    Steps:
    1. Create a temporary directory with a corrupt PDF.
    2. Call `load_all_pdfs` and check for graceful handling.

    Expected Result:
    - The function should skip the corrupt file and log an error.
    - The function should not raise an unhandled exception.
    """
    with TemporaryDirectory() as test_dir:
        corrupt_pdf_path = os.path.join(test_dir, "corrupt.pdf")

        # Create a corrupt PDF (write invalid content)
        with open(corrupt_pdf_path, "wb") as f:
            f.write(b"Not a valid PDF content")

        result = load_all_pdfs(test_dir)

        assert result == [], "Should return an empty list if all PDFs are corrupt."
