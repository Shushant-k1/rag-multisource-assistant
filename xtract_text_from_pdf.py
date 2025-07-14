import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        if doc.page_count == 0:
            raise ValueError("📄 The PDF has no readable pages.")
        
        text = " ".join([page.get_text() for page in doc])
        if not text.strip():
            raise ValueError("❌ No extractable text found in the PDF.")
        
        return text

    except fitz.fitz.FileDataError:
        raise ValueError("⚠️ Invalid PDF file or corrupted format.")

    except Exception as e:
        raise ValueError(f"⚠️ Failed to extract text from PDF: {str(e)}")
