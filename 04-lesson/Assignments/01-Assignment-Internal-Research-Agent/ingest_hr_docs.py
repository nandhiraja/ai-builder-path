from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = Path("data/")
PERSIST_DIR = "chroma_hr_policies"
COLLECTION_NAME = "hr_policy_docs"

def load_all_pdfs():
    docs = []
    for pdf_file in DATA_DIR.glob("*.txt"):
        with open(pdf_file, "r", encoding="utf-8") as f:
            docs.append(Document(page_content=f.read(), metadata={"source": str(pdf_file)}))
    return docs

def main():
    docs = load_all_pdfs()
    if not docs:
        print("No HR policy TXT files found in data/")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
    )

    vectorstore.add_documents(splits)
    print(f"Ingested {len(splits)} chunks into {PERSIST_DIR}")

if __name__ == "__main__":
    main()