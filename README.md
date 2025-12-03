# 🔒 VaultAI | Secure Enterprise RAG System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Llama 3.3](https://img.shields.io/badge/AI_Model-Llama_3.3_70B-purple?style=flat)
![Status](https://img.shields.io/badge/Status-Deployed-success)

> **A privacy-first Retrieval-Augmented Generation (RAG) engine enabling secure, local-first document analysis.**



## 🌟 Project Overview

### The Problem
Enterprises sit on mountains of valuable internal data (contracts, policies, technical manuals) but are blocked from using modern Generative AI tools like ChatGPT due to severe **data privacy risks**. Uploading sensitive corporate IP to public cloud models violates compliance standards (GDPR, HIPAA, SOC2), leaving employees to manually search through thousands of PDF pages.

### The Objective
The goal was to engineer a **secure, deployable RAG (Retrieval-Augmented Generation) pipeline** that allows users to "chat" with their internal documents while adhering to strict privacy constraints:
1.  **Zero Training:** Data must not be used to train external models.
2.  **Local Storage:** The document corpus must never leave the secure hosting environment.
3.  **Verifiability:** AI answers must cite specific sources to prevent hallucinations.

### The Technical Solution
I architected **VaultAI** using a **Hybrid Local-Cloud strategy** to balance security with performance:
* **Ingestion Engine:** Utilized `PyPDF` and `LangChain` to ingest and chunk multi-page PDFs.
* **Local Vectorization:** Implemented `HuggingFace (all-MiniLM-L6-v2)` embeddings running **locally on the CPU**. This ensures raw document text is converted to vectors without ever touching an external API.
* **Vector Database:** Deployed `FAISS` for high-speed, local similarity search.
* **Inference Layer:** Integrated **Groq's LPU (Language Processing Unit)** API running **Llama 3.3 (70B)**.
    * *Security Protocol:* Only the specific retrieved paragraph (context) is sent to the API, not the full document.
    * *Constraint:* Configured the API for "Transient Processing" (Zero Data Retention).

### The Outcome
* **Performance:** Achieved **sub-second latency** for queries across 100+ page documents using Groq's LPU acceleration.
* **Accuracy:** Reduced hallucination rates by implementing a strict "Answer based ONLY on context" prompt template with mandatory source citations.
* **Scalability:** Successfully deployed to Streamlit Community Cloud with a CI/CD pipeline via GitHub.

---

## 🏗️ System Architecture
<img width="2279" height="1536" alt="system_architecture" src="https://github.com/user-attachments/assets/947312be-20f9-44b4-8d0b-670c29ae4890" />


## How to Run Locally

Prerequisites: Python 3.11+

**1. Clone the Repository**


git clone [https://github.com/your-username/vault-ai-rag.git](https://github.com/your-username/vault-ai-rag.git)
cd vault-ai-rag
Install Dependencies


**2. Create virtual environment**

python -m venv venv
.\venv\Scripts\activate

**3. Install packages**

pip install -r requirements.txt
Configure Credentials Create a .env file in the root directory:
GROQ_API_KEY=gsk_your_actual_key_here

**4. Launch App**
streamlit run app.py




# Demo_Screenshot

<img width="1908" height="958" alt="demo_screenshot" src="https://github.com/user-attachments/assets/e69522be-f8e6-4787-a05c-858ee46fe816" />






