import json
import sys
import os


# Add project root and src folder to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    PROJECT_ROOT,
    "src"
)

sys.path.insert(
    0,
    SRC_DIR
)


from qa import answer_question


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

    print(
        f"Total test questions: {len(questions)}"
    )

    print(
        "\nStarting tests...\n"
    )

    for test in questions:

        question_id = test["id"]
        question = test["question"]
        test_type = test["type"]

        print("=" * 70)

        print(
            f"Test {question_id}"
        )

        print(
            f"Question: {question}"
        )

        print(
            f"Type: {test_type}"
        )

        print(
            "\nAnswer:"
        )

        try:

            answer = answer_question(
                question
            )

            print(answer)

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

        print()


if __name__ == "__main__":

    main()