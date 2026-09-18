from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTORSTORE_DIR = "vectorstore"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def create_retriever():

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    print("Loading FAISS vector database...")

    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 10
        }
    )

    return retriever


def main():

    retriever = create_retriever()

    question = "প্রোটন কী?"

    print("\nQuestion:")
    print(question)

    print("\nSearching relevant book sections...\n")

    documents = retriever.invoke(question)

    for i, document in enumerate(
        documents,
        start=1
    ):

        print(
            f"--- Result {i} ---"
        )

        print(
            f"Book: {document.metadata.get('book')}"
        )

        print(
            f"Chapter: {document.metadata.get('chapter')}"
        )

        print(
            f"Source: {document.metadata.get('source')}"
        )

        print(
            f"\n{document.page_content[:700]}"
        )

        print("\n")


if __name__ == "__main__":

    main()