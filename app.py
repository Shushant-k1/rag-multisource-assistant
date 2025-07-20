import streamlit as st
from streamlit.components.v1 import html
from transcript_utils import fetch_youtube_transcript
from pdf_utils import extract_text_from_pdf
from vector_db import store_in_vector_db, query_vector_db
from generate_answer import generate_answer
from text_splitter import text_splitter
import shutil
import os
#
VECTOR_DB_PATH = "./vector_db"

def delete_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)
        st.info("🧹 Vector DB cleared.")
    else:
        st.warning("⚠️ Vector DB not found or already deleted.")

# ───────────── Page Config ─────────────
st.set_page_config(page_title="Multi-Source RAG Assistant", layout="wide")

# ───────────── Advanced CSS Styling ─────────────
st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #f6f8fa, #eaf0f5);
        }

        .main > div {
            max-width: 900px !important;
            margin: auto !important;
            padding: 2rem 3rem !important;
        }

        .title-container {
            text-align: center;
            padding-bottom: 20px;
        }

        .title-container h1 {
            font-size: 3rem;
            font-weight: bold;
            color: #1f2937;
        }

        .title-container p {
            font-size: 1.2rem;
            color: #4b5563;
        }

        .rag-image {
            text-align: center;
            margin-top: 20px;
        }

        .rag-image img {
            width: 100%;
            max-width: 700px;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }

        .chunk-box {
            border: 1px solid #ddd;
            padding: 12px;
            border-radius: 10px;
            background-color: #f9fafb;
            margin-bottom: 10px;
        }

        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# ───────────── Title & Image ─────────────
st.markdown("""
    <div class="title-container">
        <h1>🔍 Multi-Source RAG Assistant</h1>
        <p>Upload PDFs, extract from YouTube, or paste your own text — ask anything using Gemini + FAISS</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="rag-image">
        <img src="https://media.geeksforgeeks.org/wp-content/uploads/20250210190608027719/How-Rag-works.webp" alt="RAG Diagram" />
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ───────────── Input Source ─────────────
st.markdown("### 📥 Select Input Source")
input_type = st.radio("Select one", ["📄 Upload PDF", "📝 Paste Text", "🎥 YouTube URL or ID"], horizontal=True, key="input_radio", label_visibility="collapsed")

document_text = ""

if input_type == "📄 Upload PDF":
    pdf_file = st.file_uploader("Upload your PDF file:", type=["pdf"])
    if pdf_file:
        try:
            document_text = extract_text_from_pdf(pdf_file)
            st.success("✅ PDF processed successfully.")
            with st.expander("📜 Extracted Text"):
                st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)
        except ValueError as e:
            st.error(str(e))

elif input_type == "📝 Paste Text":
    document_text = st.text_area("Paste your text below:", label_visibility="visible")
    if document_text.strip():
        st.success("✅ Text captured.")
        with st.expander("📜 Input Text"):
            st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)

elif input_type == "🎥 YouTube URL or ID":
    video_input = st.text_input("Enter YouTube video URL or ID:", label_visibility="visible")
    if video_input:
        try:
            document_text = fetch_youtube_transcript(video_input)
            st.success("✅ Transcript fetched successfully.")
            with st.expander("🎬 Video Transcript"):
                st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)
        except ValueError as e:
            st.error(str(e))

# ───────────── Store & QA Section ─────────────
if document_text.strip():
    st.markdown("### 📦 Store and Ask Questions")

    if st.button("📥 Store in Vector DB"):
        try:
            st.info("🔄 Splitting text into chunks...")
            chunks = text_splitter(document_text)

            st.success(f"✅ Split into {len(chunks)} chunks.")
            with st.expander("🧩 Preview Text Chunks"):
                for i, chunk in enumerate(chunks[:5]):
                    st.markdown(f"<div class='chunk-box'><b>Chunk {i+1}:</b><br>{chunk}</div>", unsafe_allow_html=True)

            st.info("📦 Storing in vector database...")
            store_in_vector_db(chunks)
            st.success("✅ Chunks stored successfully.")

        except Exception as e:
            st.error(f"❌ Failed to store chunks: {str(e)}")

    st.divider()
    st.subheader("💬 Ask a Question")

    query = st.text_input("Type your question here:", label_visibility="visible")
    if query.strip():
        with st.spinner("🔍 Retrieving relevant content..."):
            context_chunks = query_vector_db(query)

            with st.expander("📂 Top Matching Chunks Used"):
                for i, chunk in enumerate(context_chunks[:3]):
                    st.markdown(f"<div class='chunk-box'><b>Chunk {i+1}:</b><br>{chunk}</div>", unsafe_allow_html=True)

        with st.spinner("🧠 Generating answer..."):
            response = generate_answer(query, context_chunks)

        st.success("✅ Answer generated:")
        st.markdown("### 💬 Answer:")
        st.write(response)

    if st.button("🧹 Clear Vector DB"):
        delete_vector_db()

# ───────────── Footer ─────────────
st.markdown("---")
st.markdown("""
    <div style='text-align: center; font-size: 14px; color: gray; margin-top: 2rem;'>
        Made with ❤️ by <b>Shushant Kumar</b> using Gemini + Streamlit + FAISS.
    </div>
""", unsafe_allow_html=True)
