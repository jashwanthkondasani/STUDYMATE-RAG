import streamlit as st
import os
import time
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration for desktop and mobile responsiveness
st.set_page_config(
    page_title="StudyMate-RAG | Advanced AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design, Mobile Responsiveness & Flashcards
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hero Header Styling */
    .hero-container {
        background: linear-gradient(135deg, #0B3D91 0%, #1E50A2 50%, #12284C 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(11, 61, 145, 0.25);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.02rem;
        color: #E2E8F0;
        margin-top: 0.5rem;
        font-weight: 400;
        line-height: 1.5;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        padding: 0.35rem 0.9rem;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #7DD3FC;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Developer Contact Profile Card */
    .dev-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .dev-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0B3D91;
        margin-bottom: 0.2rem;
    }
    .dev-role {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 0.8rem;
    }
    
    /* Social Contact Buttons */
    .social-btn-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }
    .social-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    .social-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .btn-email { background-color: #EA4335; color: #FFFFFF !important; }
    .btn-linkedin { background-color: #0A66C2; color: #FFFFFF !important; }
    .btn-github { background-color: #24292E; color: #FFFFFF !important; }

    /* RAG Confidence Badge */
    .confidence-badge {
        display: inline-block;
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-left: 0.5rem;
    }

    /* Flashcard Card UI */
    .flashcard {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0B3D91;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .flashcard-term {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0B3D91;
        margin-bottom: 0.4rem;
    }
    .flashcard-def {
        font-size: 0.92rem;
        color: #334155;
        line-height: 1.5;
    }

    /* Source Citation Drawer */
    .source-box {
        background-color: #F1F5F9;
        border-left: 4px solid #0B3D91;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.88rem;
        color: #334155;
    }

    /* Mobile Touch Adjustments */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.7rem; }
        .hero-container { padding: 1.4rem 1.1rem; }
        .social-btn-container { flex-direction: column; }
        .social-btn { width: 100%; justify-content: center; }
    }
</style>
""", unsafe_allow_html=True)

# Import backend components
from backend.pdf_processor import PDFProcessor
from backend.chunker import TextChunker
from backend.vector_store import VectorStoreManager
from backend.rag_engine import RAGEngine

# Initialize & Refresh Session State Variables
if "vector_manager" not in st.session_state or not hasattr(st.session_state.vector_manager, "get_all_filenames"):
    st.session_state.vector_manager = VectorStoreManager()
if "chunker" not in st.session_state:
    st.session_state.chunker = TextChunker(chunk_size=1000, chunk_overlap=200)

if "rag_engine" not in st.session_state or not hasattr(st.session_state.rag_engine, "generate_quiz"):
    st.session_state.rag_engine = RAGEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "flashcards_data" not in st.session_state:
    st.session_state.flashcards_data = None

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/000000/open-book.png", width=64)
    st.title("StudyMate-RAG v2.0")
    st.caption("⚡ Grounded AI Study Assistant with Multi-PDF & Voice")
    
    st.markdown("---")

    # 👨‍💻 Developer Profile & Direct Contact Links
    st.markdown("""
    <div class="dev-card">
        <div class="dev-name">👨‍💻 Jashwanth Kondasani</div>
        <div class="dev-role">AI / ML Engineer & Developer</div>
        <div class="social-btn-container">
            <a href="mailto:jashwanthkumarreddy53@gmail.com" target="_blank" class="social-btn btn-email">
                📧 Email Me
            </a>
            <a href="https://www.linkedin.com/in/jashwanth-reddy-3919152a0?utm_source=share_via&utm_content=profile&utm_medium=member_android" target="_blank" class="social-btn btn-linkedin">
                💼 LinkedIn
            </a>
            <a href="https://github.com/jashwanthkondasani" target="_blank" class="social-btn btn-github">
                🐙 GitHub
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 🔒 Secure API Key Configuration
    st.subheader("⚙️ API & Model Security")
    existing_key = os.getenv("GEMINI_API_KEY", "")
    
    if existing_key and len(existing_key) > 5:
        st.success("🔒 System API Key Active & Secured", icon="✅")
        with st.expander("🔑 Custom API Key Override", expanded=False):
            custom_key = st.text_input("Custom Gemini API Key", type="password")
            if custom_key:
                os.environ["GEMINI_API_KEY"] = custom_key
                st.success("Custom API key updated!")
    else:
        with st.expander("🔑 Setup Gemini API Key", expanded=True):
            user_key = st.text_input("Gemini API Key", type="password")
            if user_key:
                os.environ["GEMINI_API_KEY"] = user_key
                st.success("API Key saved!")

    st.markdown("---")
    
    # 📁 Multi-PDF Upload Section
    st.subheader("📚 Multi-PDF Document Upload")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload lecture notes, textbooks, or syllabi"
    )

    if uploaded_files:
        for u_file in uploaded_files:
            if u_file.name not in st.session_state.uploaded_files_list:
                with st.spinner(f"⏳ Processing {u_file.name}..."):
                    file_bytes = u_file.read()
                    full_text, page_data = PDFProcessor.extract_text_from_bytes(file_bytes, filename=u_file.name)
                    if page_data:
                        chunks = st.session_state.chunker.chunk_page_data(page_data)
                        st.session_state.vector_manager.add_chunks(chunks)
                        st.session_state.uploaded_files_list.append(u_file.name)
                        st.success(f"Indexed **{u_file.name}** ({len(page_data)} pages)")

    # 🔍 Document Filter Selector
    all_files = st.session_state.vector_manager.get_all_filenames() if hasattr(st.session_state.vector_manager, 'get_all_filenames') else []
    doc_options = ["All Documents"] + all_files
    selected_doc_filter = st.selectbox("🎯 Target Document Filter", options=doc_options, index=0)

    st.markdown("---")
    
    # 🧹 Session Controls
    if st.button("🗑️ Clear Session & Reset Database", use_container_width=True):
        st.session_state.vector_manager.clear_collection()
        st.session_state.messages = []
        st.session_state.uploaded_files_list = []
        st.session_state.quiz_data = None
        st.session_state.flashcards_data = None
        st.success("Session reset clean!")
        st.rerun()

# --- MAIN AREA ---

# Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ Advanced Grounded RAG Platform v2.0</div>
    <h1 class="hero-title">StudyMate-RAG</h1>
    <div class="hero-subtitle">
        Interactive Grounded Q&A, Multi-Turn Memory, Audio TTS Summaries, AI Quizzes & Smart Concept Flashcards.
    </div>
</div>
""", unsafe_allow_html=True)

# Define Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Grounded AI Chat & Audio", 
    "📝 AI Practice Quiz", 
    "🎴 Smart Flashcards", 
    "📁 Document Library"
])

# --- TAB 1: GROUNDED AI CHAT & AUDIO ---
with tab1:
    if not st.session_state.vector_manager.count_chunks():
        st.info("👈 **Get Started**: Upload a PDF in the sidebar to start asking questions!", icon="💡")
    
    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            if "confidence" in msg and msg["confidence"] > 0:
                st.markdown(f"""<span class="confidence-badge">🟢 {msg['confidence']}% Relevance Confidence</span>""", unsafe_allow_html=True)

            if "sources" in msg and msg["sources"]:
                with st.expander("📌 Grounded Sources & Page Citations"):
                    for src in msg["sources"]:
                        conf_str = f" | Match: {src.get('confidence_score', 90.0)}%" if "confidence_score" in src else ""
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>Page {src['page_number']}</strong> ({src['filename']}{conf_str})<br>
                            <em>"{src['snippet']}"</em>
                        </div>
                        """, unsafe_allow_html=True)

    # User Query Input
    if prompt := st.chat_input("Ask a question about your uploaded document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching vector database & generating grounded answer..."):
                retrieved_chunks = st.session_state.vector_manager.similarity_search(
                    query=prompt, 
                    top_k=4,
                    target_filename=selected_doc_filter
                )

                result = st.session_state.rag_engine.generate_grounded_answer(
                    question=prompt,
                    retrieved_chunks=retrieved_chunks,
                    conversation_history=st.session_state.messages[:-1],  # Multi-turn memory
                    api_key=os.getenv("GEMINI_API_KEY", "")
                )

                answer = result["answer"]
                sources = result["sources"]
                confidence = result.get("confidence", 90.0)

                st.markdown(answer)
                st.markdown(f"""<span class="confidence-badge">🟢 {confidence}% Relevance Confidence</span>""", unsafe_allow_html=True)

                if sources:
                    with st.expander("📌 Grounded Sources & Page Citations"):
                        for src in sources:
                            conf_str = f" | Match: {src.get('confidence_score', 90.0)}%" if "confidence_score" in src else ""
                            st.markdown(f"""
                            <div class="source-box">
                                <strong>Page {src['page_number']}</strong> ({src['filename']}{conf_str})<br>
                                <em>"{src['snippet']}"</em>
                            </div>
                            """, unsafe_allow_html=True)

                # HTML5 Web Speech Voice Synthesizer Button
                clean_audio_text = answer.replace('"', "'").replace("\n", " ")
                st.components.v1.html(f"""
                <button onclick="speakText()" style="background-color:#0B3D91; color:white; border:none; padding:8px 16px; border-radius:8px; cursor:pointer; font-weight:600; margin-top:8px;">
                    🔊 Listen to Voice Summary
                </button>
                <script>
                function speakText() {{
                    var msg = new SpeechSynthesisUtterance();
                    msg.text = "{clean_audio_text[:500]}";
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """, height=50)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "confidence": confidence
                })

# --- TAB 2: AI PRACTICE QUIZ ---
with tab2:
    st.subheader("📝 AI Practice Quiz Generator")
    st.caption("Generate instant multiple-choice revision questions grounded in your document.")
    
    if st.button("✨ Generate 5 Practice Questions", type="primary"):
        with st.spinner("Generating grounded quiz questions..."):
            chunks = st.session_state.vector_manager.similarity_search("overview key topics", top_k=6, target_filename=selected_doc_filter)
            st.session_state.quiz_data = st.session_state.rag_engine.generate_quiz(chunks, api_key=os.getenv("GEMINI_API_KEY", ""))

    if st.session_state.quiz_data:
        score = 0
        for idx, q in enumerate(st.session_state.quiz_data, 1):
            st.markdown(f"#### Q{idx}. {q['question']}")
            user_opt = st.radio(f"Select option for Q{idx}:", options=q.get("options", []), key=f"q_{idx}")
            if st.checkbox(f"Check Answer for Q{idx}", key=f"chk_{idx}"):
                if user_opt == q.get("answer"):
                    st.success("✅ Correct! " + q.get("explanation", ""))
                    score += 1
                else:
                    st.error(f"❌ Incorrect. Correct Answer: **{q.get('answer')}**\n\n{q.get('explanation', '')}")

# --- TAB 3: SMART FLASHCARDS ---
with tab3:
    st.subheader("🎴 Smart Concept Flashcards")
    st.caption("Review key definitions and core terminology extracted from your notes.")
    
    if st.button("✨ Generate Flashcards", type="primary"):
        with st.spinner("Extracting key concepts & definitions..."):
            chunks = st.session_state.vector_manager.similarity_search("key concepts definitions", top_k=6, target_filename=selected_doc_filter)
            st.session_state.flashcards_data = st.session_state.rag_engine.generate_flashcards(chunks, api_key=os.getenv("GEMINI_API_KEY", ""))

    if st.session_state.flashcards_data:
        cols = st.columns(2)
        for idx, card in enumerate(st.session_state.flashcards_data):
            col = cols[idx % 2]
            with col:
                st.markdown(f"""
                <div class="flashcard">
                    <div class="flashcard-term">💡 {card['term']}</div>
                    <div class="flashcard-def">{card['definition']}</div>
                    <div style="margin-top:10px; font-size:0.8rem; color:#64748B;">📍 {card.get('page_citation', 'Document Source')}</div>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 4: DOCUMENT LIBRARY ---
with tab4:
    st.subheader("📁 Indexed Document Library")
    filenames = st.session_state.vector_manager.get_all_filenames()
    total_chunks = st.session_state.vector_manager.count_chunks()
    
    st.markdown(f"**Total Indexed Chunks in Database**: `{total_chunks}`")
    
    if filenames:
        for f_name in filenames:
            st.markdown(f"- 📄 **{f_name}**")
    else:
        st.info("No documents currently indexed. Upload a PDF in the sidebar!")
