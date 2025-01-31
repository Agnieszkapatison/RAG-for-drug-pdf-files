# RAG-for-Drug-PDF-Files

## Project Overview

This system was designed for **medical professionals**, allowing them to quickly retrieve **essential drug information** from **Summaries of Product Characteristics (ChPL)** available in the **official Polish Ministry of Health database** [(🔗 Link)](https://rejestry.ezdrowie.gov.pl/rpl/search/public).

The **Retrieval-Augmented Generation (RAG)** model was developed by a **pharmacist**, ensuring that **all responses are validated by an expert** before being made available in the system.

The system supports **both Polish and English queries**, enabling **healthcare workers** to access **reliable, evidence-based drug-related information efficiently**.

This project was developed using a dataset of **1,001 Summaries of Product Characteristics (ChPL) in PDF format**.

---

## How the RAG System Works?

### 1️⃣ Processing Source Text
Each document is **converted from PDF** and **split into smaller text chunks**, preserving metadata _(e.g., drug name, section)._  

### 2️⃣ Checking for Existing Embeddings
- If an **existing FAISS index** is found, the system **loads precomputed embeddings**.  
- If **no index exists**, the system **extracts text** from ChPL and **generates new embeddings**.  

### 3️⃣ Generating Embeddings
- The system was **tested with OpenAI Ada v2 embeddings**, but it allows **switching to other available embedding models** via configuration.  
- **OpenAI embeddings** are used to create **vector representations** of text chunks.  
- All queries are converted into embeddings and matched against vectorized text chunks.

### 4️⃣ Indexing with FAISS
- The generated **embeddings** are **stored in a FAISS index**.  
- This allows for **fast and accurate similarity-based retrieval** when responding to queries.  

### 5️⃣ Creating the RAG Pipeline
- The system **retrieves relevant text passages** using **FAISS-based vector search**.  
- A **retriever model** searches for the **most relevant embeddings** based on user input.  
- A **GPT-3.5 Turbo -0125** model generates responses based on retrieved context.  
- **The prompt is structured to ensure that GPT only uses provided sources and does not hallucinate.**  
- **If no relevant data is found,** the system responds with:  
  > *"No data in the attached sources."*

---

## How to Run the Drug Information Search System (RAG)?

### 1️⃣ Create a `.env` File
Before running the system, create a `.env` file in the **project root directory** and add the following **environment variables**:

```ini
OPENAI_API_KEY=your_openai_key_here
MODEL= gpt-your_model
PDF_FOLDER=your_patch_to_database/database
ONEDRIVE_PATH_PDF=your_patch_to_database/database
FAISS_INDEX_PATH=your_patch_to_database/database
```

> **You can replace `gpt-3.5-turbo` with any other OpenAI model** (e.g., `gpt-4-turbo`, `gpt-4`).  
> The system was **tested on `gpt-3.5-turbo-0125` and OpenAI Ada v2 embeddings**.

---

### 2️⃣ Install Dependencies
You need to install **all required packages** before running the project. Run:

```bash
pip install -r requirements.txt
```
### 3️⃣ Run the System Using Either Option
The system provides two interface options, allowing users to choose the method that best suits their needs:

🔹 CLI Mode (Command-Line Interface) – main.py


```bash
python src/main.py
```
<img width="868" alt="Zrzut ekranu 2025-01-30 o 23 29 47" src="https://github.com/user-attachments/assets/e7636e8b-7737-47e1-bd79-c5392a361db1" />

🔹 GUI Mode (Graphical Web Interface) – app.py (Streamlit-based)


```bash
streamlit run src/app.py
```
![Zrzut ekranu 2025-01-30 o 23 37 38](https://github.com/user-attachments/assets/28b940b8-5be6-4c49-a0a8-6265bc4155a4)


## Testing Framework
The project includes unit, integration, and performance tests to ensure the reliability and correctness of the Retrieval-Augmented Generation (RAG) model.


- Unit Tests (tests/unit/): Validate individual components, such as text splitting and embedding storage.
- Integration Tests (tests/integration/): Ensure different modules work together correctly.
- Performance Tests (tests/performance/): Evaluate the system’s efficiency and response time.
<img width="860" alt="Zrzut ekranu 2025-01-31 o 10 58 11" src="https://github.com/user-attachments/assets/d8494ace-19ea-4d7b-b0c8-5f25486068c9" />


## Tools Directory
The tools/ directory contains useful scripts to automate testing and security checks:

- run_tests.sh / run_tests.cmd → Runs all tests and generates reports.
- scan_security.sh / scan_security.cmd → Performs a security scan using bandit to detect vulnerabilities.
  <img width="687" alt="Zrzut ekranu 2025-01-31 o 11 22 29" src="https://github.com/user-attachments/assets/712b8b42-5f97-4736-8209-242783115be9" />

- check_locally.sh / check_locally.cmd → Ensures that local dependencies and pre-commit hooks are correctly configured.

#  **Author**
This project was developed and validated by **Agnieszka Wyłupek, M.Sc. in Pharmacy, licensed pharmacist**.

---

## ⚠ **Copyright & Usage Restrictions**
📢 **Unauthorized copying, distribution, or use of this project without the author's explicit permission is strictly prohibited.**  
📢 This project is intended for **educational and research purposes only**.  
📢 For commercial or professional use, please contact the author.  

---

## 📬 **Contact**
For inquiries or collaboration opportunities, feel free to reach out via:  
📧 **Email:** [agnieszka.chrastek@wp.pl]  
🔗 **LinkedIn:** [www.linkedin.com/in/agnieszka-wyłupek-348b21278]  
