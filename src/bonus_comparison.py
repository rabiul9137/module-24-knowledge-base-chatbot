from pathlib import Path
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.chunker import load_documents, split_documents


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

TEST_QUESTIONS = [
    {
        "question": "পরমাণু কী?",
        "expected_chapter": "অণু, পরমাণু",
    },
    {
        "question": "ইলেক্ট্রন কী?",
        "expected_chapter": "ইলেক্‌ট্রন ও প্রোটন",
    },
    {
        "question": "প্রোটন কী?",
        "expected_chapter": "ইলেক্‌ট্রন ও প্রোটন",
    },
    {
        "question": "নিউট্রন কী?",
        "expected_chapter": "পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন",
    },
    {
        "question": "পজিট্রন কী?",
        "expected_chapter": "পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন",
    },
    {
        "question": "মিসোট্রন বা মেসন সম্পর্কে বইটিতে কী বলা হয়েছে?",
        "expected_chapter": "পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন",
    },
    {
        "question": "মৌলিক পদার্থের পরমাণুগুলোর মধ্যে কী পার্থক্য আছে?",
        "expected_chapter": "অণু, পরমাণু",
    },
    {
        "question": "শক্তি ও তড়িৎ সম্পর্কে বইটিতে কী আলোচনা করা হয়েছে?",
        "expected_chapter": "শক্তি ও তড়িৎ",
    },
    {
        "question": "প্রাউটের মত কী ছিল?",
        "expected_chapter": "অণু, পরমাণু",
    },
]


# ============================================================
# Embedding model
# ============================================================

def create_embeddings():
    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print("Embedding model loaded.")
    return embeddings


# ============================================================
# Normalize chapter name
# ============================================================

def normalize_chapter(chapter):
    """
    Converts metadata such as:

        বিশ্বের উপাদান/অণু, পরমাণু

    into:

        অণু, পরমাণু
    """

    if not chapter:
        return ""

    chapter = str(chapter).strip()

    if "/" in chapter:
        chapter = chapter.split("/")[-1]

    return chapter.strip()


# ============================================================
# Test one strategy
# ============================================================

def evaluate_strategy(strategy_name, chunk_size, chunk_overlap, embeddings):

    print()
    print("=" * 70)
    print(strategy_name)
    print("=" * 70)

    print(
        f"\nCreating chunks: size={chunk_size}, overlap={chunk_overlap}"
    )

    # Load cleaned documents
    documents = load_documents()

    # Create chunks
    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    print(f"Total chunks created: {len(chunks)}")

    # Create temporary FAISS database
    print("Creating temporary FAISS vector store...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings,
    )

    print("Vector store created.")

    # Retrieval evaluation
    correct = 0
    total = len(TEST_QUESTIONS)

    print()
    print("Retrieval Results:")
    print("-" * 70)

    for i, test in enumerate(TEST_QUESTIONS, start=1):

        question = test["question"]
        expected = test["expected_chapter"]

        # Retrieve top 10 chunks
        results = vectorstore.similarity_search(
            question,
            k=10,
        )

        retrieved_chapters = []

        for doc in results:

            chapter = doc.metadata.get("chapter", "")

            normalized = normalize_chapter(chapter)

            retrieved_chapters.append(normalized)

        # Check whether expected chapter appears in top 10
        hit = expected in retrieved_chapters

        if hit:
            correct += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(
            f"{i}. {status} | {question}"
        )

        print(
            f"   Expected: {expected}"
        )

        print(
            f"   Retrieved: {retrieved_chapters}"
        )

    # Calculate hit rate
    hit_rate = (correct / total) * 100

    print("-" * 70)

    print(
        f"Correct retrievals: {correct}/{total}"
    )

    print(
        f"Hit rate: {hit_rate:.1f}%"
    )

    return {
        "strategy": strategy_name,
        "chunks": len(chunks),
        "correct": correct,
        "total": total,
        "hit_rate": hit_rate,
    }


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("BONUS — CHUNKING STRATEGY COMPARISON")
    print("=" * 70)

    print()
    print("Embedding model:")
    print(MODEL_NAME)

    embeddings = create_embeddings()

    # --------------------------------------------------------
    # Strategy A
    # --------------------------------------------------------

    strategy_a = evaluate_strategy(
        "Strategy A — 700 / 150",
        chunk_size=700,
        chunk_overlap=150,
        embeddings=embeddings,
    )

    # --------------------------------------------------------
    # Strategy B
    # --------------------------------------------------------

    strategy_b = evaluate_strategy(
        "Strategy B — 1000 / 200",
        chunk_size=1000,
        chunk_overlap=200,
        embeddings=embeddings,
    )

    # --------------------------------------------------------
    # Final comparison
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"{'Strategy':<30}"
        f"{'Chunks':<10}"
        f"{'Correct':<12}"
        f"{'Hit Rate':<10}"
    )

    print("-" * 70)

    print(
        f"{strategy_a['strategy']:<30}"
        f"{strategy_a['chunks']:<10}"
        f"{strategy_a['correct']}/{strategy_a['total']:<10}"
        f"{strategy_a['hit_rate']:.1f}%"
    )

    print(
        f"{strategy_b['strategy']:<30}"
        f"{strategy_b['chunks']:<10}"
        f"{strategy_b['correct']}/{strategy_b['total']:<10}"
        f"{strategy_b['hit_rate']:.1f}%"
    )

    print("=" * 70)

    print()
    print(
        "Hit Rate = Correct Retrievals / Total Answerable Questions × 100"
    )

    print()
    print("Evaluation note:")
    print(
        "A hit means the expected chapter appeared within the "
        "top 10 retrieved chunks."
    )

    print(
        "This measures retrieval coverage, not end-to-end answer accuracy."
    )


if __name__ == "__main__":
    main()