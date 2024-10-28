"""
Configuration module for loading environment variables.

This module loads all required environment variables from the `.env` file
and raises errors if any essential variable is missing. It provides a centralized
location to access these variables, making the project configuration consistent
and easier to manage.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys and other configuration parameters
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")
PDF_FOLDER = os.getenv("PDF_FOLDER")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")

# Ensure all required environment variables are loaded
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not MODEL:
    raise ValueError("MODEL not found in .env file")
if not PDF_FOLDER:
    raise ValueError("PDF_FOLDER not found in .env file")
if not FAISS_INDEX_PATH:
    raise ValueError("FAISS_INDEX_PATH not found in .env file")
