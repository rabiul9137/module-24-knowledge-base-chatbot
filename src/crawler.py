```python
import os
import re


BOOK_DIR = "data/book"
CLEANED_DIR = "data/cleaned"


def clean_text(text):
    """
    Remove unnecessary whitespace and invisible characters.
    """

    # Remove invisible Unicode characters
    text = text.replace("\u200b", "")
    text = text.replace("\u200c", "")
    text = text.replace("\u200d", "")

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def remove_wikisource_header(text):
    """
    Remove repeated Wikisource page/header/navigation text.

    Keep:
        - Book name
        - Chapter
        - Source URL

    Remove:
        - Author/header information
        - Page number information
        - Navigation text
    """

    lines = text.splitlines()

    # Find the metadata lines
    book_line = None
    chapter_line = None
    source_line = None

    for line in lines:

        line = line.strip()

        if line.startswith("বই:"):
            book_line = line

        elif line.startswith("অধ্যায়:"):
            chapter_line = line

        elif line.startswith("Source URL:"):
            source_line = line

    # Find where actual book content begins
    content_start = None

    for i, line in enumerate(lines):

        line = line.strip()

        # The actual chapter content starts with the chapter heading.
        # Example: অণু-পরমাণু
        if line == "অণু-পরমাণু":
            content_start = i
            break

    # If we cannot find the exact heading,
    # keep everything after the metadata section.
    if content_start is None:

        content_start = 3

    content_lines = lines[content_start:]

    # Remove trailing navigation/page information
    unwanted_lines = {
        "►",
        "◄",
        "পৃ.",
    }

    cleaned_content = []

    for line in content_lines:

        stripped = line.strip()

        if stripped in unwanted_lines:
            continue

        cleaned_content.append(line)

    content = "\n".join(cleaned_content)

    content = clean_text(content)

    # Build final document with metadata
    metadata = []

    if book_line:
        metadata.append(book_line)

    if chapter_line:
        metadata.append(chapter_line)

    if source_line:
        metadata.append(source_line)

    metadata.append("")

    final_text = "\n".join(metadata) + content

    return final_text.strip()


def load_chapter(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return text


def process_chapter(filepath):

    text = load_chapter(filepath)

    cleaned_text = remove_wikisource_header(text)

    return cleaned_text


def main():

    print("Processing book chapters...\n")

    os.makedirs(
        CLEANED_DIR,
        exist_ok=True
    )

    files = sorted(
        filename
        for filename in os.listdir(BOOK_DIR)
        if filename.endswith(".txt")
    )

    print(
        f"Found {len(files)} chapter files.\n"
    )

    for filename in files:

        filepath = os.path.join(
            BOOK_DIR,
            filename
        )

        cleaned_text = process_chapter(
            filepath
        )

        output_path = os.path.join(
            CLEANED_DIR,
            filename
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(cleaned_text)

        print(
            f"{filename}: "
            f"{len(cleaned_text)} characters"
        )

        print(
            f"Saved to: {output_path}"
        )

    print(
        "\nProcessing completed!"
    )


if __name__ == "__main__":

    main()
```
