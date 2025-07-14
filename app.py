import streamlit as st
from transcript_utils import fetch_youtube_transcript
from pdf_utils import extract_text_from_pdf
from vector_db import store_in_vector_db, query_vector_db
from generate_answer import generate_answer

st.set_page_config(page_title="Multi-Source RAG Assistant", layout="wide")
st.title("🔍 Multi-Source RAG Assistant")

st.markdown(
    """
    This app supports:
    - 📄 PDF upload  
    - 🎥 YouTube video transcript  
    - 📝 Raw text input  
    
    The content is processed and stored in a vector DB for RAG-based Q&A.
    """
)

# Sidebar input selection
st.sidebar.header("📥 Select Input Type")
input_type = st.sidebar.radio("", ["📄 Upload PDF", "📝 Paste Text", "🎥 YouTube URL or ID"])

document_text = ""

# Input Handling
if input_type == "📄 Upload PDF":
    pdf_file = st.sidebar.file_uploader("Upload your PDF", type=["pdf"])
    if pdf_file:
        try:
            document_text = extract_text_from_pdf(pdf_file)
            st.success("✅ PDF processed successfully.")
            with st.expander("📜 Extracted Text", expanded=False):
                st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)
        except ValueError as e:
            st.error(str(e))

elif input_type == "📝 Paste Text":
    document_text = st.sidebar.text_area("Paste your text below:")
    if document_text.strip():
        st.success("✅ Text captured.")
        with st.expander("📜 Input Text", expanded=False):
            st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)

elif input_type == "🎥 YouTube URL or ID":
    video_input = st.sidebar.text_input("Enter YouTube video URL or ID")
    if video_input:
        try:
            document_text = fetch_youtube_transcript(video_input)
            st.success("✅ Transcript fetched successfully.")
            with st.expander("🎬 Video Transcript", expanded=False):
                st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)
        except ValueError as e:
            st.error(str(e))

from text_splitter import text_splitter  # Your custom splitter function

# Store in vector DB
if document_text.strip():
    if st.button("📥 Store in Vector DB"):
        try:
            st.info("🔄 Splitting text into chunks...")
            chunks = text_splitter(document_text)

            st.success(f"✅ Split into {len(chunks)} chunks.")

            with st.expander("🧩 Preview Text Chunks", expanded=False):
                for i, chunk in enumerate(chunks[:5]):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk)

            st.info("📦 Storing chunks in vector database...")
            store_in_vector_db(chunks)
            st.success("✅ Chunks embedded and stored successfully.")

        except Exception as e:
            st.error(f"❌ Failed to split/store text: {str(e)}")

    st.divider()
    st.subheader("💬 Ask a question about the uploaded content")

    query = st.text_input("Your Question:")
    if query.strip():
        with st.spinner("🔍 Retrieving relevant content..."):
            context_chunks = query_vector_db(query)

            with st.expander("📂 Top Matching Chunks Used"):
                for i, chunk in enumerate(context_chunks[:3]):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk)

        with st.spinner("🧠 Generating answer..."):
            response = generate_answer(query, context_chunks)

        st.success("✅ Answer generated:")
        st.markdown("### 💬 Answer:")
        st.write(response)
