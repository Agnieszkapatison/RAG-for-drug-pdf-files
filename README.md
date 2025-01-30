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

## Ensuring Reliability
✔ If embeddings **exist**, they are **loaded** instead of being recalculated.  
✔ If embeddings **do not exist**, they are **generated from scratch** and saved.  
✔ **Structured metadata** improves search accuracy and relevance.  
✔ **The system ensures trustworthy responses** by restricting **GPT-3.5** to verified sources.  
