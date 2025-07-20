# 🔍 RAG Multi-Source Assistant

A powerful Retrieval-Augmented Generation (RAG) system built with Streamlit, Google Gemini, FAISS/ChromaDB, and YouTube/PDF input support.

🔗 **Live Demo**: [RAG Assistant App](https://rag-multisource-assistant-yxhtwjjs8p9zx3vpqlq7g5.streamlit.app/)

![How RAG Works](https://media.geeksforgeeks.org/wp-content/uploads/20250210190608027719/How-Rag-works.webp)


---

## 🚀 Features

- 📄 Upload PDFs or paste plain text  
- 🎥 Input YouTube video URLs or IDs  
- 🧠 Uses Gemini Embeddings & Gemini Flash for contextual answers  
- 🗃️ Stores vector DB locally via FAISS (or ChromaDB)  
- 🌐 Clean and responsive Streamlit UI  


---

## 🧩 Project Structure

```
.
├── app.py               # Streamlit app UI  
├── generate_answer.py   # Gemini LLM prompt wrapper  
├── transcript_utils.py  # YouTube transcript fetcher  
├── pdf_utils.py         # PDF text extractor  
├── vector_db.py         # Store/query FAISS vector DB  
├── text_splitter.py     # Chunk text for retrieval  
├── requirements.txt     # Project dependencies  
└── README.md            # Project overview  
```

---

## 🧠 Tech Stack

| Layer       | Technology                     |
|------------|---------------------------------|
| UI         | Streamlit + HTML/CSS            |
| OCR/Text   | PyMuPDF (fitz), Tesseract       |
| Transcript | youtube-transcript-api          |
| Embeddings | Gemini Embeddings (optional)    |
| Vector DB  | ChromaDB / FAISS (fallback)     |
| LLM        | Google Gemini 1.5 Flash         |

---

## ☁️ Deployment

### 🔹 Streamlit Cloud

1. Push this repo to GitHub  
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)  
3. Add your `GOOGLE_API_KEY` in **Secrets** via `Settings → Secrets`  

### 🔹 GCP / Cloud Run (Advanced)

- Use Dockerfile + GitHub Actions for CI/CD  
- Automatically deploy to GCP from GitHub  
- Ask me if you need setup instructions  

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use, share, and modify it.

✨ Made by [Shushant Kumar](https://www.linkedin.com/in/shushant-k1/) with ❤️

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!  
Feel free to fork the repository, create a feature branch, and open a pull request.

If you find a bug or want a new feature:  
- Open an [issue](https://github.com/your-username/rag-multisource-assistant/issues)  
- Or reach out directly via [LinkedIn](https://www.linkedin.com/in/shushant-k1r/)  

---

## 💡 Future Improvements

Here are some potential next steps for this project:

- [ ] Add support for websites/blog URLs as context  
- [ ] Integrate Whisper ASR to extract audio from uploaded video files  
- [ ] Stream output tokens using Gemini streaming API  
- [ ] Add conversation memory for multi-turn chat  
- [ ] Allow user-defined chunk sizes and retrieval models  

---

## 📌 Related Resources

- [Gemini API Docs](https://ai.google.dev/)  
- [ChromaDB](https://docs.trychroma.com/)  
- [Streamlit](https://docs.streamlit.io/)  
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)  
