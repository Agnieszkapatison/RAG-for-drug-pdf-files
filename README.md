# RAG-for-Drug-PDF-Files

## Project Overview

### System Overview
This system was designed for **medical professionals**, allowing them to quickly retrieve **essential drug information** from **Summaries of Product Characteristics (ChPL)** available in the **official Polish Ministry of Health database** [(🔗 Link)](https://rejestry.ezdrowie.gov.pl/rpl/search/public).

The **Retrieval-Augmented Generation (RAG)** model was developed by a **pharmacist (MSc in Pharmacy)**, ensuring that **all responses are validated by an expert** before being made available in the system.

The system supports **both Polish and English queries**, enabling **healthcare workers** to access **reliable, evidence-based drug-related information efficiently**.

This project was developed using a dataset of **1,001 Summaries of Product Characteristics (ChPL) in PDF format**, sourced from the **official Ministry of Health website**.

---

## How the RAG System Works?

### 1️⃣ Processing Source Text
Each document is **converted from PDF** and **split into smaller text chunks**, preserving metadata _(e.g., drug name, section)._  

### 2️⃣ Checking for Existing Embeddings
If an **existing FAISS index** is found, the system **loads precomputed embeddings**.  
If **no index exists**, the system **extracts text** from ChPL and **generates new embeddings**.  

### 3️⃣ Generating Embeddings
The system was **tested with OpenAI Ada v2 embeddings**, but it allows **switching to other available embedding models** via configuration.  
**OpenAI embeddings** are used to create **vector representations** of text chunks.  
The system supports **both plain text and metadata-enriched embeddings**.  

### 4️⃣ Indexing with FAISS
The generated **embeddings** are **stored in a FAISS index**.  
This allows for **fast and accurate similarity-based retrieval** when responding to queries.  

### 5️⃣ Creating the RAG Pipeline
The system **retrieves relevant text passages** using **FAISS-based vector search**.  
A **retriever model** searches for the **most relevant embeddings** based on user input.  
A **GPT-3.5 Turbo -0125** model generates responses based on retrieved context.  
**The prompt is structured to ensure that GPT only uses provided sources and does not hallucinate.**  
**If no relevant data is found, the system responds with:**  
   _"No data in the attached sources."_

---
# How to Run the Drug Information Search System (RAG)?

## 1️⃣ Create a `.env` File  
Before running the system, create a `.env` file in the **project root directory** and add the following **environment variables**:

```ini
OPENAI_API_KEY=your_openai_key_here
MODEL=gpt-3.5-turbo
PDF_FOLDER=your_patch_to_database/database
ONEDRIVE_PATH_PDF=your_patch_to_database/database
FAISS_INDEX_PATH=your_patch_to_database/database
You can replace gpt-3.5-turbo with any other OpenAI model (e.g., gpt-4-turbo, gpt-4).
The system was tested on gpt-3.5-turbo-0125 and OpenAI Ada v2 embeddings.

##2️⃣ Install Dependencies
You need to install all required packages before running the project. Run:

```ini
pip install -r requirements.txt

###3️⃣ Run the System Using Either Option
The system provides two interface options, allowing users to choose the method that best suits their needs:

🔹 CLI Mode (Command-Line Interface) – main.py
🔹 GUI Mode (Graphical Web Interface) – app.py (Streamlit-based)

Both interfaces work identically in retrieving Summaries of Product Characteristics (ChPL) and using OpenAI embeddings and FAISS for vector search.
However, they differ in how users interact with the system.

🔹 CLI Mode (Command-Line Interface) – main.py
Run this if you prefer using a terminal-based interface:

```ini
python src/main.py
The system will ask you to type a question and display the response in the terminal, along with the source of the retrieved information.

🔹 GUI Mode (Graphical Web Interface) – app.py
Run this if you prefer using a web interface with Streamlit:

```ini
streamlit run src/app.py
A browser window will open, allowing you to enter a question and see the response in a structured format.

The source of each retrieved answer is displayed along with the response.
