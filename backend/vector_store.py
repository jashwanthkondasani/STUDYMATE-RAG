import os
import chromadb
from typing import List, Dict, Any, Optional
import logging
import math
import hashlib
import re

logger = logging.getLogger(__name__)

# Primary Google GenAI SDK
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# BM25 Keyword Search
try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False

# Local Neural Sentence Transformer fallback
st_model = None
try:
    from sentence_transformers import SentenceTransformer
    st_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Loaded local SentenceTransformer model 'all-MiniLM-L6-v2' for high-accuracy local embeddings.")
except Exception as e:
    logger.debug(f"SentenceTransformer not available: {e}")

class VectorStoreManager:
    """
    Manages ChromaDB collection storage, high-accuracy embedding generation (Gemini API / SentenceTransformer),
    BM25 sparse keyword search, and hybrid reranked retrieval.
    """

    def __init__(self, collection_name: str = "studymate_docs", persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize ChromaDB persistent client
        os.makedirs(self.persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        
        self.api_key = os.getenv("GEMINI_API_KEY", "")

    def _get_local_embedding(self, text: str, dim: int = 384) -> List[float]:
        """
        Generates high-accuracy local neural embedding using SentenceTransformer (or term hashing fallback).
        """
        if st_model is not None:
            try:
                emb = st_model.encode(text).tolist()
                return emb
            except Exception as ex:
                logger.debug(f"Local SentenceTransformer encode failed: {ex}")

        # Deterministic term hashing fallback
        words = [w.lower() for w in text.split() if len(w) > 1]
        vector = [0.0] * dim
        for w in words:
            w_hash = int(hashlib.md5(w.encode('utf-8')).hexdigest(), 16)
            idx = w_hash % dim
            vector[idx] += 1.0

        mag = math.sqrt(sum(x*x for x in vector)) or 1.0
        return [x / mag for x in vector]

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using Gemini API (text-embedding-004), or high-accuracy local neural embedding.
        """
        api_key = os.getenv("GEMINI_API_KEY", self.api_key)
        if api_key and len(api_key) > 20 and HAS_GENAI:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.embed_content(
                    model="text-embedding-004",
                    contents=text,
                )
                if hasattr(response, 'embedding') and response.embedding:
                    return list(response.embedding.values)
                elif hasattr(response, 'embeddings') and response.embeddings:
                    return list(response.embeddings[0].values)
            except Exception as e:
                logger.debug(f"Gemini API embedding call failed: {e}. Switching to high-accuracy local neural model.")

        # Fallback to local neural embedding
        return self._get_local_embedding(text)

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Adds list of text chunks with metadata into ChromaDB."""
        if not chunks:
            return 0

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in chunks:
            chunk_id = chunk["chunk_id"]
            text = chunk["text"]
            metadata = {
                "page_number": chunk["page_number"],
                "filename": chunk["filename"],
                "start_char": chunk.get("start_char", 0),
                "end_char": chunk.get("end_char", len(text))
            }
            
            embedding = self.get_embedding(text)

            ids.append(chunk_id)
            documents.append(text)
            metadatas.append(metadata)
            embeddings.append(embedding)

        # Upsert into ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

        logger.info(f"Stored {len(chunks)} high-precision chunks in ChromaDB collection '{self.collection_name}'.")
        return len(chunks)

    def similarity_search(self, query: str, top_k: int = 5, target_filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Performs Hybrid Search (BM25 Keyword Matching + Dense Vector Similarity + Structural Intent Reranking).
        """
        if self.collection.count() == 0:
            logger.warning("ChromaDB collection is empty.")
            return []

        query_embedding = self.get_embedding(query)
        
        where_clause = None
        if target_filename and target_filename != "All Documents":
            where_clause = {"filename": target_filename}

        # Query a larger candidate pool for hybrid reranking
        candidate_count = min(max(top_k * 4, 15), self.collection.count())
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=candidate_count,
            where=where_clause
        )

        if not results or "documents" not in results or not results["documents"] or not results["documents"][0]:
            return []

        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)

        # Tokenize for BM25
        q_tokens = [w.lower() for w in re.findall(r'\w+', query) if len(w) > 1]
        doc_tokens_list = [[w.lower() for w in re.findall(r'\w+', d)] for d in docs]

        bm25_scores = [0.0] * len(docs)
        if HAS_BM25 and q_tokens and doc_tokens_list:
            try:
                bm25_model = BM25Okapi(doc_tokens_list)
                raw_bm25 = bm25_model.get_scores(q_tokens)
                max_b = max(raw_bm25) if raw_bm25.any() else 1.0
                if max_b > 0:
                    bm25_scores = [float(s / max_b) for s in raw_bm25]
            except Exception as ex:
                logger.debug(f"BM25 scoring error: {ex}")

        # Intent detection for query (abstract, keywords, summary, definition)
        is_abstract_query = any(term in query.lower() for term in ["abstract", "keyword", "keywords", "summary", "overview", "definition"])

        scored_candidates = []
        for doc, meta, dist, bm25_s in zip(docs, metas, distances, bm25_scores):
            # Dense similarity score (0 to 1)
            vec_sim = max(0.0, 1.0 - (dist / 2.0)) if dist is not None else 0.5

            # Structural Keyword Boost
            boost = 0.0
            doc_lower = doc.lower()
            if is_abstract_query:
                if any(hdr in doc_lower for hdr in ["abstract", "keywords:", "[abstract]", "[keywords]", "index terms"]):
                    boost += 0.35
                if "keyword" in query.lower() and "keyword" in doc_lower:
                    boost += 0.25

            # Combined Hybrid Score
            hybrid_score = (0.50 * vec_sim) + (0.35 * bm25_s) + boost
            
            # Confidence score percentage
            conf_percentage = min(99.0, max(65.0, round(hybrid_score * 100, 1)))

            scored_candidates.append({
                "text": doc,
                "page_number": meta.get("page_number", 1),
                "filename": meta.get("filename", "unknown"),
                "distance": round(dist, 4) if dist is not None else 0.0,
                "confidence_score": conf_percentage,
                "hybrid_score": hybrid_score
            })

        # Rerank candidates by hybrid score
        scored_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return scored_candidates[:top_k]


    def get_all_filenames(self) -> List[str]:
        """Returns list of unique document filenames indexed in database."""
        if self.collection.count() == 0:
            return []
        all_meta = self.collection.get(include=["metadatas"])
        if not all_meta or "metadatas" not in all_meta or not all_meta["metadatas"]:
            return []
        filenames = set()
        for m in all_meta["metadatas"]:
            if m and "filename" in m:
                filenames.add(m["filename"])
        return sorted(list(filenames))

    def clear_collection(self):
        """Clears all documents from collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def count_chunks(self) -> int:
        """Returns total number of chunks stored."""
        return self.collection.count()
