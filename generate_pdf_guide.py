import pymupdf

def create_pdf_guide(filename="StudyMate_RAG_Project_Guide.pdf"):
    doc = pymupdf.open()
    font_bold = "hebo"
    font_regular = "helv"
    
    # Primary Theme Colors
    primary_color = (11/255, 61/255, 145/255)
    header_color = (18/255, 40/255, 76/255)
    bg_light = (240/255, 244/255, 255/255)
    text_dark = (30/255, 41/255, 59/255)
    accent_green = (4/255, 120/255, 87/255)

    def add_page_header(page, title_text):
        page.draw_rect(pymupdf.Rect(0, 0, 595, 50), fill=primary_color)
        page.insert_text(pymupdf.Point(30, 32), title_text, fontsize=16, fontname=font_bold, color=(1,1,1))
        page.draw_line(pymupdf.Point(30, 810), pymupdf.Point(565, 810), color=(0.8, 0.8, 0.8), width=0.5)
        page.insert_text(pymupdf.Point(30, 825), "StudyMate-RAG v2.0 — End-to-End Master Project & Interview Guide", fontsize=8, fontname=font_regular, color=(0.5,0.5,0.5))
        page.insert_text(pymupdf.Point(500, 825), f"Page {doc.page_count}", fontsize=8, fontname=font_regular, color=(0.5,0.5,0.5))

    # ==========================================
    # PAGE 1: COVER & OBJECTIVE
    # ==========================================
    page1 = doc.new_page(width=595, height=842)
    
    # Title Block
    page1.draw_rect(pymupdf.Rect(30, 40, 565, 160), fill=primary_color)
    page1.insert_text(pymupdf.Point(50, 85), "StudyMate-RAG v2.0", fontsize=26, fontname=font_bold, color=(1,1,1))
    page1.insert_text(pymupdf.Point(50, 115), "End-to-End AIML Architecture & Deployment Guide", fontsize=14, fontname=font_bold, color=(0.8, 0.9, 1))
    page1.insert_text(pymupdf.Point(50, 140), "Master every single line of code, design pattern & recruiter question.", fontsize=11, fontname=font_regular, color=(0.9, 0.95, 1))
    page1.insert_text(pymupdf.Point(50, 155), "Prepared by: Jashwanth Kondasani", fontsize=10, fontname=font_bold, color=(1,1,1))

    # Project Summary Box
    page1.draw_rect(pymupdf.Rect(30, 175, 565, 275), fill=bg_light, color=primary_color, width=1)
    page1.insert_text(pymupdf.Point(45, 198), "📌 1. What is StudyMate-RAG in Plain Words?", fontsize=13, fontname=font_bold, color=header_color)
    
    summary_p1 = (
        "StudyMate-RAG is an AI-powered personal study tutor that ingests PDF documents (lecture notes, "
        "textbook chapters, syllabi) and answers student questions in plain English. Unlike generic AI chatbots "
        "that answer from general memory (prone to hallucinations and outdated facts), StudyMate-RAG grounds "
        "every single answer STRICTLY inside your uploaded document pages and provides page-level citations."
    )
    rect_sum = pymupdf.Rect(45, 208, 550, 270)
    page1.insert_textbox(rect_sum, summary_p1, fontsize=9.5, fontname=font_regular, color=text_dark)

    # Core Value Proposition Box
    page1.draw_rect(pymupdf.Rect(30, 285, 565, 400), fill=(236/255, 253/255, 245/255), color=accent_green, width=1)
    page1.insert_text(pymupdf.Point(45, 308), "💡 Think Of It Like This:", fontsize=12, fontname=font_bold, color=accent_green)
    analogy_text = (
        "It is like hiring a personal tutor who has read your exact textbook page by page. "
        "During an open-book exam, instead of trying to answer from memory, the tutor turns directly to "
        "the exact pages containing the answer, highlights the facts, and says: 'Here is your answer, based "
        "strictly on Page 12 of your notes.' If the textbook doesn't cover something, the tutor honestly states "
        "'That is not mentioned in your notes' rather than making things up."
    )
    page1.insert_textbox(pymupdf.Rect(45, 318, 550, 395), analogy_text, fontsize=9, fontname=font_regular, color=text_dark)

    # Key Highlights
    page1.insert_text(pymupdf.Point(30, 425), "⚡ Key Highlights of System Architecture", fontsize=12, fontname=font_bold, color=header_color)
    highlights = [
        "• PyMuPDF Text Extraction: Fast page-by-page text parsing with exact page metadata.",
        "• High-Precision Chunking: 800-character sliding windows with 150-character overlap.",
        "• Dual Vector Embeddings: Google Gemini (text-embedding-004) + Local Neural SentenceTransformers.",
        "• ChromaDB Vector Database: Fast cosine-similarity vector index and metadata retrieval.",
        "• Anti-Hallucination Grounding Prompt: Prevents model from fabricating outside facts.",
        "• Advanced Feature Suite: Multi-PDF search, Multi-turn memory, Voice TTS, AI Quizzes & Flashcards.",
        "• Full-Stack Deployment: Mobile-responsive Streamlit UI + FastAPI REST API + Docker setup."
    ]
    y_h = 445
    for h in highlights:
        page1.insert_text(pymupdf.Point(40, y_h), h, fontsize=9, fontname=font_regular, color=text_dark)
        y_h += 19

    # Contact & Portfolio Details Box
    page1.draw_rect(pymupdf.Rect(30, 595, 565, 785), fill=bg_light, color=primary_color, width=1)
    page1.insert_text(pymupdf.Point(45, 618), "👨‍💻 Developer & Author Profile", fontsize=12, fontname=font_bold, color=header_color)
    page1.insert_text(pymupdf.Point(45, 638), "Name: Jashwanth Kondasani", fontsize=10, fontname=font_bold, color=text_dark)
    page1.insert_text(pymupdf.Point(45, 655), "Email: jashwanthkumarreddy53@gmail.com", fontsize=9.5, fontname=font_regular, color=text_dark)
    page1.insert_text(pymupdf.Point(45, 672), "GitHub: https://github.com/jashwanthkondasani", fontsize=9.5, fontname=font_regular, color=primary_color)
    page1.insert_text(pymupdf.Point(45, 689), "LinkedIn: https://www.linkedin.com/in/jashwanth-reddy-3919152a0", fontsize=9.5, fontname=font_regular, color=primary_color)

    # ==========================================
    # PAGE 2: FULL TECH STACK BREAKDOWN
    # ==========================================
    page2 = doc.new_page(width=595, height=842)
    add_page_header(page2, "2. Full Tech Stack — Every Tool Explained")

    page2.insert_text(pymupdf.Point(30, 75), "Here is every single piece of technology in your project and why it was chosen over alternatives:", fontsize=10, fontname=font_regular, color=text_dark)

    # Table Header
    y_t = 95
    page2.draw_rect(pymupdf.Rect(30, y_t, 565, y_t+25), fill=primary_color)
    page2.insert_text(pymupdf.Point(35, y_t+17), "Piece", fontsize=10, fontname=font_bold, color=(1,1,1))
    page2.insert_text(pymupdf.Point(120, y_t+17), "Its Job In Plain Words", fontsize=10, fontname=font_bold, color=(1,1,1))
    page2.insert_text(pymupdf.Point(320, y_t+17), "Why This Choice Over Alternatives", fontsize=10, fontname=font_bold, color=(1,1,1))

    tech_data = [
        ("Python 3.11+", "Core programming language gluing components together.", "Standard language for AI/ML with rich library ecosystem."),
        ("PyMuPDF (fitz)", "Opens PDF files and extracts text page-by-page.", "Blazing fast, handles scanned/complex PDFs with page metadata."),
        ("Text Chunker", "Splits long text into overlapping 800-char pieces.", "Keeps sentences contiguous so no idea gets awkwardly chopped."),
        ("SentenceTransformers", "Generates 384-dim neural semantic vectors locally.", "Provides deep neural vector retrieval without requiring API key."),
        ("Gemini Embeddings", "Generates 768-dim semantic vectors via Google API.", "Captures conceptual meaning across hundreds of dimensions."),
        ("ChromaDB", "Vector database storing embeddings & metadata.", "Purpose-built for fast cosine similarity search at scale."),
        ("Gemini 2.5 Flash", "Reads question + retrieved chunks to write answer.", "Free tier available, strong quality, strict grounded prompt following."),
        ("FastAPI", "Backend REST API server receiving requests.", "Modern, fast async framework with automatic Swagger docs."),
        ("Streamlit v2.0", "Responsive web and mobile frontend UI.", "Lets you build a sleek UI in Python with responsive CSS."),
        ("Docker", "Packages app code & dependencies into portable box.", "Guarantees identical execution on laptop and cloud servers.")
    ]

    y_row = y_t + 25
    for idx, (piece, job, why) in enumerate(tech_data):
        row_bg = (248/255, 250/255, 252/255) if idx % 2 == 0 else (1,1,1)
        page2.draw_rect(pymupdf.Rect(30, y_row, 565, y_row+45), fill=row_bg, color=(0.85, 0.85, 0.85), width=0.5)
        
        page2.insert_textbox(pymupdf.Rect(35, y_row+5, 115, y_row+40), piece, fontsize=8.5, fontname=font_bold, color=header_color)
        page2.insert_textbox(pymupdf.Rect(120, y_row+5, 315, y_row+40), job, fontsize=8.5, fontname=font_regular, color=text_dark)
        page2.insert_textbox(pymupdf.Rect(320, y_row+5, 560, y_row+40), why, fontsize=8.5, fontname=font_regular, color=text_dark)
        y_row += 45

    # ==========================================
    # PAGE 3: THE 10-STEP JOURNEY OF ONE QUESTION
    # ==========================================
    page3 = doc.new_page(width=595, height=842)
    add_page_header(page3, "3. The 10-Step Journey of One Question")

    page3.insert_text(pymupdf.Point(30, 75), "If a recruiter or guide asks: 'Walk me through what happens when a user asks a question', recite this:", fontsize=10, fontname=font_regular, color=text_dark)

    steps = [
        ("STEP 1 — PDF Upload", "The user uploads a PDF (notes/textbook/syllabus) via Streamlit UI or FastAPI endpoint."),
        ("STEP 2 — PyMuPDF Text Extraction", "PyMuPDF opens the PDF and extracts raw text page-by-page, attaching page number metadata."),
        ("STEP 3 — Text Chunking", "Text is cut into overlapping 800-character chunks with 150-char overlap to preserve context."),
        ("STEP 4 — Vector Embedding Generation", "Each text chunk is converted into a numeric embedding vector representing its semantic meaning."),
        ("STEP 5 — ChromaDB Vector Storage", "Text chunks, embedding vectors, and page metadata are stored and indexed in ChromaDB."),
        ("STEP 6 — User Question", "The user types a question in the chat box (e.g. 'What is photosynthesis?')."),
        ("STEP 7 — Question Embedding", "The exact same vector model converts the question into a numeric query vector."),
        ("STEP 8 — Similarity Search", "ChromaDB performs cosine similarity search to find top-5 chunks closest in meaning to the query."),
        ("STEP 9 — Grounded Prompt Construction", "Retrieved chunks are combined into a strict prompt: 'Answer using ONLY these snippets. Say I don't know if missing.'"),
        ("STEP 10 — Gemini LLM Generation", "Gemini LLM generates a natural language answer with page citations [Page X], rendered in the UI.")
    ]

    y_s = 95
    for title, desc in steps:
        page3.draw_rect(pymupdf.Rect(30, y_s, 565, y_s+42), fill=bg_light, color=primary_color, width=0.5)
        page3.insert_text(pymupdf.Point(40, y_s+16), title, fontsize=9.5, fontname=font_bold, color=header_color)
        page3.insert_textbox(pymupdf.Rect(40, y_s+20, 555, y_s+38), desc, fontsize=8.5, fontname=font_regular, color=text_dark)
        y_s += 46

    # ==========================================
    # PAGE 4: THE 6 CORE AI/ML CONCEPTS
    # ==========================================
    page4 = doc.new_page(width=595, height=842)
    add_page_header(page4, "4. The 6 Concepts You Must Explain Confidently")

    concepts = [
        ("4.1 Embeddings", "A numeric representation of meaning. Two pieces of text with similar meaning get numerically similar embeddings, even if they don't share exact words.", "Q. What is an embedding in your own words?\nA. It's a way of turning text into numbers that capture meaning so computers can measure concept similarity."),
        ("4.2 Vector Database (ChromaDB)", "A database specifically built to store numeric embeddings and quickly answer 'which stored items are most similar to this new vector?'", "Q. Why not use a regular SQL database here?\nA. SQL is built for exact text matches, whereas vector DBs compare high-dimensional meaning spaces efficiently."),
        ("4.3 Text Chunking", "Splitting a long document into smaller overlapping pieces before embedding and storing them.", "Q. Why split into chunks instead of embedding the whole PDF?\nA. A single embedding for an entire document blurs topics together. Chunks allow precise paragraph retrieval."),
        ("4.4 Similarity Search", "Comparing the question's embedding against stored chunk embeddings using Cosine Distance.", "Q. How does ChromaDB decide which chunks are relevant?\nA. It measures the cosine angle between query vector and stored vectors, returning the closest matches."),
        ("4.5 Context Window", "The maximum amount of text an LLM can read at once in a single prompt.", "Q. Why use RAG instead of feeding the whole PDF to LLM?\nA. Large documents exceed context limits, and focused relevant text produces more accurate answers."),
        ("4.6 Hallucination & Grounding", "Hallucination is when an LLM confidently invents false facts. Grounding forces answers to use retrieved snippets.", "Q. How does your project reduce hallucination?\nA. By instructing Gemini to answer ONLY from retrieved chunks and say 'I don't know' if missing.")
    ]

    y_c = 75
    for name, desc, qa in concepts:
        page4.draw_rect(pymupdf.Rect(30, y_c, 565, y_c+88), fill=(250/255, 250/255, 250/255), color=(0.8, 0.8, 0.8), width=0.5)
        page4.insert_text(pymupdf.Point(40, y_c+16), name, fontsize=10.5, fontname=font_bold, color=primary_color)
        page4.insert_textbox(pymupdf.Rect(40, y_c+20, 555, y_c+48), desc, fontsize=8.5, fontname=font_regular, color=text_dark)
        page4.draw_rect(pymupdf.Rect(40, y_c+50, 555, y_c+82), fill=bg_light)
        page4.insert_textbox(pymupdf.Rect(45, y_c+52, 550, y_c+80), qa, fontsize=8, fontname=font_bold, color=header_color)
        y_c += 96

    # ==========================================
    # PAGE 5: RECRUITER Q&A BANK
    # ==========================================
    page5 = doc.new_page(width=595, height=842)
    add_page_header(page5, "5. Recruiter & Interviewer Q&A Bank")

    qa_list = [
        ("Q. Walk me through your project in 90 seconds.",
         "A. StudyMate-RAG is a grounded study assistant where students upload PDF notes and ask questions in plain English. Under the hood, it parses text using PyMuPDF, chunks it into overlapping 800-character windows, generates semantic embeddings using Google Gemini and SentenceTransformers, and indexes them in ChromaDB. When a user asks a question, ChromaDB retrieves top relevant chunks via cosine similarity search, and Google Gemini synthesizes an accurate answer grounded strictly in the document with page citations."),

        ("Q. Why RAG instead of Fine-Tuning?",
         "A. Fine-tuning is expensive, slow to retrain whenever notes change, and still hallucinates. RAG allows instant document swapping with zero retraining costs and provides exact page-level source traceability."),

        ("Q. What was the hardest part of building this?",
         "A. Tuning chunk size and overlap so retrieval was precise without losing sentence context across chunk boundaries, and implementing multi-turn memory without exceeding prompt bounds."),

        ("Q. What happens if the PDF doesn't contain the answer?",
         "A. The grounded prompt explicitly instructs Gemini to reply 'I cannot find the answer to this question in your uploaded document' rather than guessing from general knowledge."),

        ("Q. How did you deploy this project?",
         "A. Pushed code to GitHub, managed dependencies in requirements.txt, secured API keys in .env / Streamlit secrets, and deployed on Streamlit Community Cloud and Docker.")
    ]

    y_q = 75
    for q, a in qa_list:
        page5.draw_rect(pymupdf.Rect(30, y_q, 565, y_q+110), fill=bg_light, color=primary_color, width=0.5)
        page5.insert_text(pymupdf.Point(40, y_q+18), q, fontsize=10, fontname=font_bold, color=primary_color)
        page5.insert_textbox(pymupdf.Rect(40, y_q+25, 555, y_q+102), a, fontsize=8.8, fontname=font_regular, color=text_dark)
        y_q += 118

    # ==========================================
    # PAGE 6: STEP-BY-STEP DEPLOYMENT GUIDE
    # ==========================================
    page6 = doc.new_page(width=595, height=842)
    add_page_header(page6, "6. Detailed Step-by-Step Deployment Guide")

    page6.insert_text(pymupdf.Point(30, 75), "Here are the 3 complete ways to deploy StudyMate-RAG v2.0 for mobile and public access:", fontsize=10, fontname=font_regular, color=text_dark)

    dep_steps = [
        ("OPTION 1 — Streamlit Community Cloud (Free Public Link)", 
         "1. Push code to GitHub: git init && git add . && git commit -m 'Deploy' && git push origin main\n"
         "2. Connect to share.streamlit.io, select repository and set main file path to app.py.\n"
         "3. Add GEMINI_API_KEY under Advanced Settings -> Secrets and click Deploy.\n"
         "4. Get a live URL (e.g. https://studymate-rag.streamlit.app) accessible on any mobile phone browser!"),

        ("OPTION 2 — Docker Container Production Deployment",
         "1. Build Docker image: docker build -t studymate-rag:v2 .\n"
         "2. Run container: docker run -d -p 8501:8501 -e GEMINI_API_KEY='your_key' studymate-rag:v2\n"
         "3. Deploy using Docker Compose: docker-compose up --build -d\n"
         "4. Host on Render, Railway, or AWS EC2 for production container execution."),

        ("OPTION 3 — Instant Mobile Access via Local Tunneling",
         "1. Ensure local Streamlit server is running: streamlit run app.py --server.port 8501\n"
         "2. Run local tunnel command in terminal: npx localtunnel --port 8501\n"
         "3. Open generated public URL on your phone's Safari/Chrome browser to upload PDFs and ask questions on the go!")
    ]

    y_d = 95
    for title, desc in dep_steps:
        page6.draw_rect(pymupdf.Rect(30, y_d, 565, y_d+110), fill=bg_light, color=primary_color, width=0.5)
        page6.insert_text(pymupdf.Point(40, y_d+18), title, fontsize=10, fontname=font_bold, color=primary_color)
        page6.insert_textbox(pymupdf.Rect(40, y_d+25, 555, y_d+102), desc, fontsize=8.8, fontname=font_regular, color=text_dark)
        y_d += 120

    # Save PDF to disk
    doc.save(filename)
    doc.close()
    print(f"✅ Generated master PDF guide: {filename}")

if __name__ == "__main__":
    create_pdf_guide()
