import streamlit as st
from transcript_utils import fetch_youtube_transcript
from pdf_utils import extract_text_from_pdf
from vector_db import store_in_vector_db, query_vector_db
from rag_pipeline import generate_answer

st.set_page_config(page_title="Multi-Source RAG Assistant", layout="wide")
st.title("🔎 Multi-Source RAG Assistant")

st.markdown("This app lets you upload PDFs, input text, or use YouTube video transcripts to ask questions using RAG (Retrieval-Augmented Generation).")

# Sidebar for input selection
st.sidebar.header("📥 Input Options")
input_type = st.sidebar.radio("Select Input Type:", ["📄 Upload PDF", "📝 Paste Text", "🎥 YouTube URL or ID"])

document_text = ""

# Input method logic
if input_type == "📄 Upload PDF":
    pdf_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf_file:
        document_text = extract_text_from_pdf(pdf_file)
        with st.expander("📜 Extracted Text from PDF", expanded=False):
            st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)

elif input_type == "📝 Paste Text":
    document_text = st.sidebar.text_area("Paste your text here:")
    if document_text:
        with st.expander("📜 Pasted Text", expanded=False):
            st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)

elif input_type == "🎥 YouTube URL or ID":
    video_input = st.sidebar.text_input("Enter YouTube URL or Video ID")
    if video_input:
        try:
            document_text = fetch_youtube_transcript(video_input)
            with st.expander("🎬 Transcript from YouTube", expanded=False):
                st.write(document_text[:2000] + "..." if len(document_text) > 2000 else document_text)
        except Exception as e:
            st.error(f"Error: {e}")

# Process and store
if document_text:
    if st.button("✅ Store in Vector Database"):
        store_in_vector_db(document_text)
        st.success("Document content embedded and stored in vector DB.")

    st.divider()

    st.subheader("💬 Ask a question based on the uploaded content:")
    query = st.text_input("Your Question:")

    if query:
        with st.spinner("Retrieving relevant chunks..."):
            context_chunks = query_vector_db(query)
            with st.expander("📂 Top Retrieved Chunks"):
                for i, chunk in enumerate(context_chunks[:3]):
                    st.markdown(f"**Chunk {i+1}:** {chunk}")

        with st.spinner("Generating answer..."):
            response = generate_answer(query, context_chunks)

        st.success("Answer generated:")
        st.write("### 🧠 Answer:")
        st.markdown(response)
