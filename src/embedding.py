import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from chunker import load_documents, split_documents


VECTORSTORE_DIR = "vectorstore"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def create_embeddings():

    print("Loading documents...\n")

    documents = load_documents()

    print(
        f"Total documents: {len(documents)}"
    )

    print("\nSplitting documents into chunks...")

    chunks = split_documents(
        documents
    )

    print(
        f"Total chunks: {len(chunks)}"
    )

    print("\nLoading multilingual embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    print("Embedding model loaded.")

    print("\nCreating FAISS vector database...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    os.makedirs(
        VECTORSTORE_DIR,
        exist_ok=True
    )

    vectorstore.save_local(
        VECTORSTORE_DIR
    )

    print("\nFAISS vector database created successfully!")

    print(
        f"Saved to: {VECTORSTORE_DIR}"
    )


if __name__ == "__main__":

    create_embeddings()