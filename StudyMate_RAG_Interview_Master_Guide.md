# 📘 StudyMate-RAG v2.0: Project Design, Tech Stack & Recruiter Interview Master Guide

> **Author**: Jashwanth Kondasani  
> **Contact**: jashwanthkumarreddy53@gmail.com | [GitHub](https://github.com/jashwanthkondasani) | [LinkedIn](https://www.linkedin.com/in/jashwanth-reddy-3919152a0)  
> **Project PDF Guide**: [`StudyMate_RAG_Project_Guide.pdf`](file:///Users/kondasanijashwanth/Desktop/study-rag/StudyMate_RAG_Project_Guide.pdf)

---

## 📌 1. Project Objective & Core Concept

**StudyMate-RAG v2.0** is an AI-powered study assistant application designed to ingest PDF study materials (lecture notes, textbook chapters, syllabi) and answer student questions in plain English. 

### 💡 The Core Problem It Solves:
Standard AI chatbots (like asking general models without document retrieval) try to answer questions from general training memory. This leads to **AI hallucinations** (making up facts, giving outdated information, or providing answers that contradict specific course notes).

**StudyMate-RAG fixes this** by using **Retrieval-Augmented Generation (RAG)**:
- It searches your exact uploaded PDF pages first.
- Pulls out the most relevant paragraphs (chunks).
- Instructs Google's Gemini LLM to answer **STRICTLY using those retrieved chunks** with page-level citations.

---

## 🛠️ 2. Full Tech Stack — Every Piece Explained

| Piece | Job in Plain Words | Why Chosen over Alternatives |
| :--- | :--- | :--- |
| **Python 3.11+** | Core programming language gluing everything together. | Standard language for AI/ML with rich library ecosystem. |
| **PyMuPDF (`fitz`)** | Opens PDF files and extracts text page-by-page. | Blazing fast, handles scanned/complex PDFs with exact page tracking. |
| **Text Chunker** | Cuts long text into overlapping 800-character pieces with 150-char overlap. | Keeps sentences contiguous so no idea gets awkwardly chopped. |
| **SentenceTransformers** | Generates 384-dim neural semantic vectors locally. | Provides deep neural vector retrieval without requiring API key. |
| **Gemini Embeddings** | Generates 768-dim semantic vectors via Google API (`text-embedding-004`). | Captures conceptual meaning across hundreds of dimensions. |
| **ChromaDB** | Vector database storing embeddings & metadata. | Purpose-built for fast cosine similarity search at scale. |
| **Gemini 2.5 Flash** | Reads question + retrieved chunks to write answer. | Free tier available, strong quality, strict grounded prompt following. |
| **FastAPI** | Backend REST API server receiving requests (`/api/upload`, `/api/query`, `/api/quiz`). | Modern, fast async framework with automatic Swagger docs. |
| **Streamlit v2.0** | Responsive web and mobile frontend UI. | Lets you build a sleek UI in Python with custom navy CSS. |
| **Docker** | Packages app code & dependencies into portable box. | Guarantees identical execution on laptop and cloud servers. |

---

## 🔄 3. The 10-Step Journey of One Question

If a recruiter or guide asks: *"Walk me through what happens when a user asks a question"*, recite these 10 steps:

1. **PDF Upload**: User selects a PDF via Streamlit UI or FastAPI endpoint.
2. **PyMuPDF Text Extraction**: PyMuPDF opens the PDF and extracts raw text page-by-page with page metadata.
3. **Overlapping Text Chunking**: Text is split into 800-character chunks with 150-character overlap.
4. **Vector Embedding**: Each chunk is converted into a numeric vector representing its semantic meaning.
5. **ChromaDB Indexing**: Text chunks, embedding vectors, and page metadata are stored in ChromaDB.
6. **User Question**: User types a question in the chat box (e.g., *"What is photosynthesis?"*).
7. **Question Embedding**: The exact same vector model converts the question into a numeric query vector.
8. **Similarity Search**: ChromaDB performs cosine similarity search to find top-5 chunks closest in meaning to the query.
9. **Grounded Prompt Construction**: Retrieved chunks are combined into a strict prompt: *"Answer using ONLY these snippets. Say I don't know if missing."*
10. **Gemini LLM Answer Generation**: Gemini LLM generates a natural language answer with page citations `[Page X]`, rendered in the UI.

---

## 🧠 4. The 6 Concepts You Must Explain Confidently

### 4.1 Embeddings
*A numeric representation of meaning.* Two pieces of text with similar meaning get numerically similar embeddings, even if they don't share exact words.

### 4.2 Vector Database (ChromaDB)
*A database built specifically to store embeddings and perform fast nearest-neighbor similarity searches.* Regular SQL databases match exact strings, whereas vector DBs match semantic concepts across hundreds of dimensions.

### 4.3 Text Chunking
*Splitting large documents into smaller overlapping pieces before embedding.* Prevents blurring multiple topics into one vague vector and ensures retrieval pulls out exact relevant paragraphs.

### 4.4 Similarity Search
*The process of measuring the angle (Cosine Similarity) between the question vector and stored document chunk vectors.*

### 4.5 Context Window
*The maximum amount of text an LLM can process in a single request.* RAG avoids exceeding this limit by retrieving only the top-k relevant chunks.

### 4.6 Hallucination & Grounding
*Hallucination occurs when an LLM invents unsupported facts.* StudyMate-RAG eliminates hallucination by feeding retrieved snippets into Gemini with strict instructions to say *"I don't know"* if the answer isn't in the snippets.

---

## 🎯 5. Recruiter Q&A Bank — Specific to This Project

- **Q: Walk me through your project in 90 seconds.**
  - *Answer*: StudyMate-RAG is a grounded study assistant where students upload PDF notes and ask questions in plain English. Under the hood, it parses text using PyMuPDF, chunks it into overlapping 800-character windows, generates semantic embeddings using Google Gemini and SentenceTransformers, and indexes them in ChromaDB. When a user asks a question, ChromaDB retrieves top relevant chunks via cosine similarity search, and Google Gemini synthesizes an accurate answer grounded strictly in the document with page citations.

- **Q: Why RAG instead of Fine-Tuning?**
  - *Answer*: Fine-tuning is expensive, slow to retrain whenever notes change, and still hallucinates. RAG allows instant document swapping with zero retraining costs and provides exact page-level source traceability.

- **Q: What was the hardest part of building this?**
  - *Answer*: Tuning chunk size and overlap so retrieval was precise without losing sentence context across chunk boundaries, and implementing multi-turn memory without exceeding prompt bounds.

- **Q: What happens if the PDF doesn't contain the answer?**
  - *Answer*: The grounded prompt explicitly instructs Gemini to reply *"I cannot find the answer to this question in your uploaded document"* rather than guessing from general knowledge.

- **Q: How did you deploy this project?**
  - *Answer*: Pushed code to GitHub, managed dependencies in requirements.txt, secured API keys in `.env` / Streamlit secrets, and deployed on Streamlit Community Cloud and Docker.

---

## 🌐 6. Detailed Step-by-Step Deployment Guide

### Option A: Streamlit Community Cloud (Free Public Link — Recommended for Mobile & Resumes)

#### Step 1: Push Code to GitHub
```bash
git init
git add .
git commit -m "Deploy StudyMate-RAG v2.0"
git branch -M main
git remote add origin https://github.com/jashwanthkondasani/study-rag.git
git push -u origin main
```

#### Step 2: Connect Repo to Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository (`jashwanthkondasani/study-rag`), branch (`main`), and set Main file path to `app.py`.

#### Step 3: Configure Environment Variables (Secrets)
1. Click **"Advanced settings"** -> **"Secrets"**.
2. Paste your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
3. Click **"Deploy!"**.
4. Streamlit Cloud will build and host your app live (e.g., `https://studymate-rag.streamlit.app`).

---

### Option B: Docker Container Deployment (Production Hosting)

#### Step 1: Build Docker Image
```bash
docker build -t studymate-rag:v2 .
```

#### Step 2: Run Container Locally or Cloud (Render / Railway / AWS EC2)
```bash
docker run -d -p 8501:8501 -e GEMINI_API_KEY="your_actual_api_key" studymate-rag:v2
```

#### Step 3: Run Multi-Container Orchestra with Docker Compose
```bash
docker-compose up --build -d
```
FastAPI backend runs on port 8000, Streamlit frontend runs on port 8501.

---

### Option C: Instant Phone Access via Local Tunneling (Testing on Phone)

1. Make sure your local Streamlit app is running (`streamlit run app.py`).
2. Run Localtunnel or Ngrok in terminal:
   ```bash
   npx localtunnel --port 8501
   ```
3. Open the generated URL on your mobile phone browser!
