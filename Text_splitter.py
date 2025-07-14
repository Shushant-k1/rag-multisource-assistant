from langchain.text_splitter import RecursiveCharacterTextSplitter

def text_splitter(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    split_docs = splitter.create_documents([text])
    chunks = [doc.page_content for doc in split_docs]
    return chunks
