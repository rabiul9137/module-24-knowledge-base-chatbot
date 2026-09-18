
import os
import re


BOOK_DIR = "data/book"
CLEANED_DIR = "data/cleaned"


def clean_text(text):
    """
    Basic text cleaning.
    """

    # Remove invisible Unicode characters
    text = text.replace("\u200b", "")
    text = text.replace("\u200c", "")
    text = text.replace("\u200d", "")

    # Fix common extraction/OCR issue
    text = text.replace("উহ|", "উহা")

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_metadata(lines):
    """
    Extract book name, chapter and source URL.
    """

    book_line = ""
    chapter_line = ""
    source_line = ""

    for line in lines:

        line = line.strip()

        if line.startswith("বই:"):
            book_line = line

        elif line.startswith("অধ্যায়:"):
            chapter_line = line

        elif line.startswith("Source URL:"):
            source_line = line

    return (
        book_line,
        chapter_line,
        source_line
    )


def find_content_start(lines):
    """
    Find the beginning of the actual book content.

    The actual content starts after the Wikisource
    navigation/header section.

    We look for a meaningful heading followed by
    Bengali prose.
    """

    # Known chapter headings from the selected book
    possible_headings = [
        "অণু-পরমাণু",
        "ইলেক্‌ট্রন ও প্রোটন",
        "পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন",
        "উপাদানের প্রকৃতি",
        "শক্তি ও তড়িৎ",
        "উপসংহার"
    ]

    for i, line in enumerate(lines):

        stripped = line.strip()

        if stripped in possible_headings:

            # Make sure this is followed by actual text
            if i + 1 < len(lines):

                next_line = lines[i + 1].strip()

                if len(next_line) > 20:

                    return i

    return None


def remove_navigation_lines(lines):
    """
    Remove obvious Wikisource navigation/header lines
    that may remain inside the content.
    """

    unwanted_exact = {
        "►",
        "◄",
        "পৃ.",
    }

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        if stripped in unwanted_exact:
            continue

        cleaned_lines.append(line)

    return cleaned_lines


def process_chapter(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    lines = text.splitlines()

    # Extract metadata before removing anything
    (
        book_line,
        chapter_line,
        source_line
    ) = extract_metadata(lines)

    # Find actual book content
    content_start = find_content_start(lines)

    if content_start is not None:

        content_lines = lines[content_start:]

    else:

        # Fallback
        content_lines = lines[3:]

    # Remove obvious navigation lines
    content_lines = remove_navigation_lines(
        content_lines
    )

    # Join content
    content = "\n".join(
        content_lines
    )

    # Clean content
    content = clean_text(
        content
    )

    # Build metadata
    metadata = []

    if book_line:
        metadata.append(book_line)

    if chapter_line:
        metadata.append(chapter_line)

    if source_line:
        metadata.append(source_line)

    metadata.append("")

    # Final cleaned document
    final_text = (
        "\n".join(metadata)
        + content
    )

    return final_text.strip()


def main():

    print(
        "Processing book chapters...\n"
    )

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

            file.write(
                cleaned_text
            )

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
