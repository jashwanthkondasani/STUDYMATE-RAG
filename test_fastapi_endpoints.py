from fastapi.testclient import TestClient
import pymupdf
from backend.main import app

client = TestClient(app)

def test_fastapi_flow():
    print("--- 🧪 Testing FastAPI Backend Endpoints ---")
    
    # 1. Health check endpoint
    response = client.get("/api/health")
    assert response.status_code == 200
    print("1. /api/health ->", response.json())

    # 2. Upload PDF endpoint
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "FastAPI is a modern, fast web framework for building APIs with Python 3.8+ based on standard Python type hints.")
    pdf_bytes = doc.write()
    doc.close()

    files = {"file": ("fastapi_doc.pdf", pdf_bytes, "application/pdf")}
    upload_res = client.post("/api/upload", files=files)
    print("2. /api/upload status:", upload_res.status_code)
    print("   Response:", upload_res.json())
    assert upload_res.status_code == 200
    assert upload_res.json()["chunks_created"] > 0

    # 3. Query endpoint
    query_payload = {
        "question": "What is FastAPI?",
        "top_k": 3
    }
    query_res = client.post("/api/query", json=query_payload)
    print("3. /api/query status:", query_res.status_code)
    print("   Response:", query_res.json())
    assert query_res.status_code == 200
    assert len(query_res.json()["sources"]) > 0

    # 4. Clear endpoint
    clear_res = client.post("/api/clear")
    assert clear_res.status_code == 200
    print("4. /api/clear status:", clear_res.status_code)

    print("\n✅ All FastAPI REST API endpoints verified successfully!")

if __name__ == "__main__":
    test_fastapi_flow()
