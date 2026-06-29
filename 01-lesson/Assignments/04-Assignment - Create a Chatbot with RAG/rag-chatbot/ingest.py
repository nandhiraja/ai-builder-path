import os
import uuid

from chunking import DocumentChunker
from ollama_client import OllamaClient
from vector_store import VectorStore


DATA_FOLDER = "data"


def ingest_documents():

    chunker = DocumentChunker()
    ollama = OllamaClient()
    vector_store = VectorStore()

    vector_store.reset()

    pdf_files = [
        file
        for file in os.listdir(DATA_FOLDER)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("No PDF files found in data folder")
        return

    total_chunks = 0

    for pdf_file in pdf_files:

        pdf_path = os.path.join(DATA_FOLDER, pdf_file)

        print(f"\nProcessing: {pdf_file}")

        chunks = chunker.process_pdf(pdf_path)

        print(f"Chunks Created: {len(chunks)}")

        embeddings = ollama.generate_embeddings(chunks)

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            ids.append(str(uuid.uuid4()))

            documents.append(chunk)

            metadatas.append(
                {
                    "source": pdf_file,
                    "chunk": index + 1
                }
            )

        vector_store.add_documents(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        total_chunks += len(chunks)

    print("\n--------------------------------")
    print("Ingestion Completed Successfully")
    print("--------------------------------")
    print(f"PDF Files     : {len(pdf_files)}")
    print(f"Total Chunks  : {total_chunks}")
    print(f"Stored Vectors: {vector_store.count()}")


if __name__ == "__main__":
    ingest_documents()