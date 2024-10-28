"""
Main script for testing the configuration of environment variables.

This script imports the necessary environment variables from the configuration module
and prints them to verify that they are loaded correctly.

Environment Variables Imported:
- OPENAI_API_KEY: The API key for OpenAI services.
- MODEL: The name of the model to be used (e.g., GPT-3.5).
- PDF_FOLDER: The path to the folder containing PDF files.
- FAISS_INDEX_PATH: The path to the FAISS index file for storing vector embeddings.

This is a simple example to ensure all required variables are loaded successfully before
being used in subsequent components, such as model initialization or other project logic.

Example Usage:
    $ python src/main.py

Dependencies:
- The `config` module must be accessible and correctly configured to load
  the required variables from the `.env` file.

"""

from config import FAISS_INDEX_PATH, MODEL, OPENAI_API_KEY, PDF_FOLDER

# Display the values of the variables to verify that they are correctly loaded
print(f"OpenAI API Key: {OPENAI_API_KEY}")
print(f"Model: {MODEL}")
print(f"PDF Folder Path: {PDF_FOLDER}")
print(f"FAISS Index Path: {FAISS_INDEX_PATH}")
