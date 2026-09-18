import json
import sys
import os


# Project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Add src folder to Python path
SRC_DIR = os.path.join(
    PROJECT_ROOT,
    "src"
)

sys.path.insert(
    0,
    SRC_DIR
)


from retriever import create_retriever


TEST_FILE = os.path.join(
    PROJECT_ROOT,
    "tests",
    "test_questions.json"
)


def load_questions():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    questions = load_questions()

    print("=" * 70)
    print("RETRIEVAL TEST")
    print("=" * 70)

    print(
        f"Total questions: {len(questions)}"
    )

    print(
        "\nLoading retriever...\n"
    )

    retriever = create_retriever()

    passed = 0
    checked = 0

    for test in questions:

        test_id = test["id"]
        question = test["question"]
        expected_chapter = test.get(
            "expected_chapter"
        )

        print("-" * 70)

        print(
            f"Test {test_id}: {question}"
        )

        # Retrieve top 10 documents
        results = retriever.vectorstore.similarity_search_with_score(
            question,
            k=10
        )

        chapters = []

        for document, score in results:

            chapter = document.metadata.get(
                "chapter",
                ""
            )

            chapters.append(
                chapter
            )

        # No-answer question
        if expected_chapter is None:

            print(
                "Type: No-answer"
            )

            print(
                "Result: RETRIEVED DOCUMENTS"
            )

            print(
                "Note: No expected chapter."
            )

            continue

        checked += 1

        # Check whether expected chapter
        # appears in top 10
        found = any(
            expected_chapter in chapter
            for chapter in chapters
        )

        if found:

            print(
                "Result: PASS"
            )

            print(
                f"Expected chapter: {expected_chapter}"
            )

            passed += 1

        else:

            print(
                "Result: FAIL"
            )

            print(
                f"Expected chapter: {expected_chapter}"
            )

        print(
            "\nTop retrieved chapters:"
        )

        for i, chapter in enumerate(
            chapters[:5],
            start=1
        ):

            print(
                f"{i}. {chapter}"
            )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(
        f"Answerable tests passed: {passed}/{checked}"
    )

    if checked > 0:

        accuracy = (
            passed / checked
        ) * 100

        print(
            f"Retrieval hit rate: {accuracy:.1f}%"
        )


if __name__ == "__main__":

    main()