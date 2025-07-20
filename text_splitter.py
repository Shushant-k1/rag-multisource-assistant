from langchain.text_splitter import RecursiveCharacterTextSplitter

def text_splitter(text):
    if len(text) > 20000 :
        chunk_size = 400
        chunk_overlap = 200
    else :
        chunk_size = 200
        chunk_overlap = 75
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    split_docs = splitter.create_documents([text])
    chunks = [doc.page_content for doc in split_docs]
    return chunks
