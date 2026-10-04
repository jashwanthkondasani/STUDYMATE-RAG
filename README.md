# 📚 StudyMate-RAG v2.0

> **Advanced Grounded AI Study Assistant with Multi-PDF RAG, Multi-Turn Chat, Audio TTS, AI Quizzes & Smart Flashcards**

StudyMate-RAG v2.0 turns your PDF notes, textbook chapters, or syllabus documents into an interactive AI study platform. It uses **Retrieval-Augmented Generation (RAG)** to ensure all answers are **strictly grounded in your uploaded document content**, eliminating AI hallucinations.

---

## 🚀 Advanced Features Suite (v2.0)

1. 📚 **Multi-PDF Document Management**: Upload multiple PDFs simultaneously and filter search by specific document or search all documents.
2. 💬 **Multi-Turn Chat Memory**: Retains conversation history so follow-up questions work seamlessly while remaining grounded in retrieved chunks.
3. 🔊 **Voice Audio Summaries (TTS)**: Built-in Web Speech API voice synthesis player so users can listen to answer summaries on mobile or desktop.
4. 📝 **AI Practice Quiz Generator**: Generates 5 multiple-choice revision questions with option selectors, instant scoring, and page citation explanations.
5. 🎴 **Smart Concept Flashcards**: Automatically extracts core terms and definitions with page citations into interactive study cards.
6. 🟢 **RAG Relevance Confidence Metrics**: Computes and displays real-time similarity confidence scores (%) per answer and source snippet.
7. 👨‍💻 **Developer Contact Card**: Direct clickable badges for Email, LinkedIn, and GitHub.
8. 🔒 **Secure API Key Protection**: Safely loads API key from `.env` without exposing keys on screen.

---

## 🛠️ Architecture & Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Core programming glue |
| **PDF Extraction** | PyMuPDF (`pymupdf`) | Fast PDF text parsing with page metadata |
| **Text Chunking** | Custom Sliding Window | 500-char chunks with 50-char overlap |
| **Embeddings** | Google Gemini / Local Vectors | Captures 768-dim semantic vectors |
| **Vector DB** | ChromaDB | Persistent vector storage & cosine similarity search |
| **LLM Model** | Google Gemini 2.5/1.5 Flash | Grounded natural language generation |
| **Backend API** | FastAPI + Uvicorn | Async REST API endpoints (`/api/upload`, `/api/query`, `/api/quiz`, `/api/flashcards`) |
| **Frontend UI** | Streamlit v2.0 + Custom CSS | Multi-tab UI (Chat, Quiz, Flashcards, Library) with navy theme |

---

## 🏃 Quick Start Guide

```bash
cd /Users/kondasanijashwanth/Desktop/study-rag
source venv/bin/activate

# Launch Streamlit Multi-Tab UI
streamlit run app.py

# Launch FastAPI REST API Backend
python -m backend.main
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser
live demo:https://studymate-rag-kmlrhcbqe4kmxazhw4sbfb.streamlit.app/
