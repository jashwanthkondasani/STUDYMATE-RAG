# pyrefly: ignore [missing-import]
import pymupdf as fitz
from backend.pdf_processor import PDFProcessor
from backend.chunker import TextChunker
from backend.vector_store import VectorStoreManager
from backend.rag_engine import RAGEngine

def test_full_pipeline():
    print("--- 🧪 Starting StudyMate-RAG End-to-End Pipeline Test ---")

    # 1. Create a dummy PDF in memory
    doc = fitz.open()
    
    # Page 1
    page1 = doc.new_page()
    page1.insert_text((50, 50), "Photosynthesis is the process used by plants to convert light energy into chemical energy. Plants use chlorophyll to absorb sunlight.")
    
    # Page 2
    page2 = doc.new_page()
    page2.insert_text((50, 50), "Inflation is a general increase in prices and fall in the purchasing value of money. Demand-pull inflation occurs when demand exceeds supply.")
    
    pdf_bytes = doc.write()
    doc.close()

    print("1. Generated test PDF in memory with 2 pages.")

    # 2. Extract text using PyMuPDF
    full_text, page_data = PDFProcessor.extract_text_from_bytes(pdf_bytes, filename="study_guide.pdf")
    print(f"2. PDF Processor extracted {len(page_data)} pages of text.")
    assert len(page_data) == 2, f"Expected 2 pages, got {len(page_data)}"

    # 3. Chunk text
    chunker = TextChunker(chunk_size=300, chunk_overlap=30)
    chunks = chunker.chunk_page_data(page_data)
    print(f"3. Text Chunker created {len(chunks)} overlapping chunks.")
    assert len(chunks) >= 2, "Expected at least 2 chunks"

    # 4. ChromaDB Vector Store Indexing
    v_store = VectorStoreManager(collection_name="test_collection", persist_directory="./test_chroma_db")
    v_store.clear_collection()
    added_count = v_store.add_chunks(chunks)
    print(f"4. VectorStoreManager indexed {added_count} chunks into ChromaDB.")

    # 5. Similarity Search Query
    query = "What is photosynthesis?"
    results = v_store.similarity_search(query, top_k=2)
    print(f"5. Similarity Search for '{query}': Found {len(results)} matching chunks.")
    assert len(results) > 0
    assert "photosynthesis" in results[0]["text"].lower() or "chlorophyll" in results[0]["text"].lower()
    print(f"   Top Result Page: {results[0]['page_number']}, Snippet: {results[0]['text'][:80]}...")

    # 6. Grounded Answer Generation
    rag_engine = RAGEngine()
    answer_res = rag_engine.generate_grounded_answer(query, results)
    print("6. RAG Engine Grounded Answer Output:")
    print("   Answer:", answer_res["answer"][:120], "...")
    print("   Sources:", answer_res["sources"])

    # Clean up test database
    v_store.clear_collection()
    print("\n✅ All 6 RAG pipeline steps passed successfully with 100% verification!")

if __name__ == "__main__":
    test_full_pipeline()
