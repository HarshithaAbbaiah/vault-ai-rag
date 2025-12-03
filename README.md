# 🔒 VaultAI | Secure Enterprise RAG System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green?style=flat)
![Llama 3.3](https://img.shields.io/badge/AI_Model-Llama_3.3_70B-purple?style=flat)

> **A privacy-first Retrieval-Augmented Generation (RAG) engine that enables secure, local-first document analysis for enterprise environments.**

---

## 📖 Project Overview
**VaultAI** addresses the critical "Data Privacy Gap" in corporate AI adoption. While public LLMs (like ChatGPT) are powerful, they pose significant security risks for sensitive internal documents (Legal Contracts, HR Policies, Financial Reports).

**VaultAI solves this via a Hybrid Architecture:**
* **Local Storage:** Documents are ingested, chunked, and embedded **locally** on the host machine using `FAISS` and `HuggingFace`. No raw file contents are stored in the cloud.
* **Secure Inference:** We utilize **Groq's LPU Inference Engine** to process *only* the specific retrieved context, ensuring high speed with minimal data exposure.

## ✨ Key Features
* **📂 Multi-Document Ingestion:** Capable of processing and indexing multiple PDF files simultaneously.
* **🧠 Hybrid RAG Pipeline:** Combines local vector search (CPU-based FAISS) with cloud-based LLM inference (Llama 3.3).
* **⚡ Zero-Latency Search:** Optimized vector retrieval for sub-second response times.
* **🛡️ Enterprise Grade Privacy:** Adheres to a "Transient Processing" model where data is not used for model training.
* **📝 Citation-Backed Answers:** Every response includes exact source document references to prevent hallucinations.

## 🛠️ Tech Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Reactive web interface for seamless user interaction. |
| **Orchestration** | LangChain | Framework for chaining LLM prompts and retrieval steps. |
| **Vector DB** | FAISS (CPU) | Local, high-efficiency similarity search for dense vectors. |
| **Embeddings** | HuggingFace | `all-MiniLM-L6-v2` model runs locally to vectorize text. |
| **Inference** | Groq API | Ultra-low latency inference for Llama 3.3 (70B). |

## 🏗️ System Architecture

```text
                                       User
                                        │
                                        │ 1. Upload Documents (PDF)
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Streamlit Application (Local Host)                                     │
│                                                                         │
│   ┌──────────────────────┐          ┌───────────────────────────────┐   │
│   │   Ingestion Engine   │          │   Retrieval Engine (RAG)      │   │
│   │                      │          │                               │   │
│   │  • PyPDF Loader      │          │  1. Semantic Search (FAISS)   │   │
│   │  • Text Splitter     │          │  2. Context Extraction        │   │
│   │  • Embeddings Model  │          │  3. Prompt Engineering        │   │
│   └──────────┬───────────┘          └──────────────▲────────────────┘   │
│              │                                     │                    │
│              │ (Vectors)                           │ (Relevant Context) │
│              ▼                                     │                    │
│   ┌──────────────────────┐                         │                    │
│   │  Local Vector Store  │ ────────────────────────┘                    │
│   │  (FAISS Index)       │                                              │
│   └──────────────────────┘                                              │
└──────────────┬──────────────────────────────────────────────────────────┘
               │ 2. Send Prompt + Context
               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Groq Cloud API (LPU Inference)                                         │
│                                                                         │
│   • Model: Llama-3.3-70b-versatile                                      │
│   • Processing: Zero Data Retention                                     │
└──────────────┬──────────────────────────────────────────────────────────┘
               │ 3. Return AI Answer
               ▼
          User Screen
