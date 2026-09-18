
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


CLEANED_DIR = "data/cleaned"


def load_documents():

    documents = []

    files = sorted(
        filename
        for filename in os.listdir(CLEANED_DIR)
        if filename.endswith(".txt")
    )

    print(
        f"Found {len(files)} cleaned files.\n"
    )

    for filename in files:

        filepath = os.path.join(
            CLEANED_DIR,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        lines = text.splitlines()

        book_name = ""
        chapter_name = ""
        source_url = ""

        for line in lines:

            line = line.strip()

            if line.startswith("বই:"):
                book_name = line.replace(
                    "বই:",
                    ""
                ).strip()

            elif line.startswith("অধ্যায়:"):
                chapter_name = line.replace(
                    "অধ্যায়:",
                    ""
                ).strip()

            elif line.startswith("Source URL:"):
                source_url = line.replace(
                    "Source URL:",
                    ""
                ).strip()

        document = Document(
            page_content=text,
            metadata={
                "book": book_name,
                "chapter": chapter_name,
                "source": source_url,
                "filename": filename
            }
        )

        documents.append(document)

        print(
            f"Loaded: {filename}"
        )

    return documents


def split_documents(
    documents,
    chunk_size=1000,
    chunk_overlap=200
):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            "। ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks


def main():

    print(
        "Loading cleaned documents...\n"
    )

    documents = load_documents()

    print(
        f"\nTotal documents: {len(documents)}"
    )

    print(
        "\nSplitting documents into chunks..."
    )

    chunks = split_documents(
        documents,
        chunk_size=1000,
        chunk_overlap=200
    )

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    print(
        "\nFirst 3 chunks:\n"
    )

    for i, chunk in enumerate(
        chunks[:3],
        start=1
    ):

        print(
            f"--- Chunk {i} ---"
        )

        print(
            f"Book: {chunk.metadata['book']}"
        )

        print(
            f"Chapter: {chunk.metadata['chapter']}"
        )

        print(
            f"Source: {chunk.metadata['source']}"
        )

        print(
            f"Characters: {len(chunk.page_content)}"
        )

        print(
            chunk.page_content[:500]
        )

        print()


if __name__ == "__main__":

    main()
