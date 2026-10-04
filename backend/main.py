import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging

from backend.pdf_processor import PDFProcessor
from backend.chunker import TextChunker
from backend.vector_store import VectorStoreManager
from backend.rag_engine import RAGEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("StudyMateBackend")

app = FastAPI(
    title="StudyMate-RAG API",
    description="FastAPI Backend for StudyMate RAG - Document extraction, ChromaDB vector indexing, Gemini LLM question answering, quizzes & flashcards.",
    version="2.0.0"
)

# Enable CORS for frontend/mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vector_manager = VectorStoreManager()
chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
rag_engine = RAGEngine()


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 4
    target_filename: Optional[str] = None
    api_key: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    grounded: bool
    confidence: float

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "StudyMate-RAG API",
        "version": "2.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "total_chunks_stored": vector_manager.count_chunks(),
        "documents": vector_manager.get_all_filenames(),
        "vector_store": "ChromaDB",
        "llm_engine": "Google Gemini"
    }

@app.get("/api/documents")
def get_documents():
    """List all unique documents currently stored in ChromaDB."""
    return {
        "documents": vector_manager.get_all_filenames(),
        "total_chunks": vector_manager.count_chunks()
    }

@app.post("/api/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    """Upload PDF, extract text, chunk text, generate embeddings & save to ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        contents = await file.read()
        logger.info(f"Received file upload: {file.filename} ({len(contents)} bytes)")

        # Extract text & metadata
        full_text, page_data = PDFProcessor.extract_text_from_bytes(contents, filename=file.filename)
        
        if not page_data:
            raise HTTPException(status_code=400, detail="Could not extract readable text from PDF.")

        # Chunk text
        chunks = chunker.chunk_page_data(page_data)

        # Store in ChromaDB
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        stored_count = vector_manager.add_chunks(chunks)

        return {
            "message": "PDF uploaded and processed successfully!",
            "filename": file.filename,
            "total_pages": len(page_data),
            "chunks_created": stored_count,
            "total_chunks_in_db": vector_manager.count_chunks(),
            "all_documents": vector_manager.get_all_filenames()
        }

    except Exception as e:
        logger.error(f"Error processing PDF upload: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
def query_doc(request: QueryRequest):
    """Query document with multi-turn memory & confidence scoring."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        if request.api_key:
            os.environ["GEMINI_API_KEY"] = request.api_key

        retrieved_chunks = vector_manager.similarity_search(
            query=request.question, 
            top_k=request.top_k or 4,
            target_filename=request.target_filename
        )

        result = rag_engine.generate_grounded_answer(
            question=request.question,
            retrieved_chunks=retrieved_chunks,
            conversation_history=request.conversation_history,
            api_key=request.api_key
        )

        return QueryResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
            grounded=result["grounded"],
            confidence=result.get("confidence", 90.0)
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")

@app.post("/api/quiz")
def generate_quiz(api_key: Optional[str] = Form(None), target_filename: Optional[str] = Form(None)):
    """Generate 5 multiple-choice practice study questions."""
    chunks = vector_manager.similarity_search("overview core topics summary", top_k=6, target_filename=target_filename)
    quiz_data = rag_engine.generate_quiz(chunks, api_key=api_key)
    return {"quiz": quiz_data}

@app.post("/api/flashcards")
def generate_flashcards(api_key: Optional[str] = Form(None), target_filename: Optional[str] = Form(None)):
    """Generate 5 smart concept flashcards."""
    chunks = vector_manager.similarity_search("key concepts definitions summary", top_k=6, target_filename=target_filename)
    cards = rag_engine.generate_flashcards(chunks, api_key=api_key)
    return {"flashcards": cards}

@app.post("/api/clear")
def clear_db():
    """Clear session data and ChromaDB collection."""
    vector_manager.clear_collection()
    return {"message": "Session reset successfully. All uploaded document data cleared."}

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
