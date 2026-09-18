import os
import sys

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from src.retriever import create_retriever


# Load environment variables
load_dotenv()


# -----------------------------
# Create LLM
# -----------------------------
def create_llm():

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )


# -----------------------------
# Answer Question
# -----------------------------
def answer_question(question):

    retriever = create_retriever()

    # Retrieve relevant documents
    documents = retriever.invoke(question)

    # If no documents are retrieved
    if not documents:
        return "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"

    # Build context
    context_parts = []

    for doc in documents:

        book = doc.metadata.get("book", "Unknown")
        chapter = doc.metadata.get("chapter", "Unknown")
        source = doc.metadata.get("source", "Unknown")

        content = doc.page_content

        context_parts.append(
            f"""
Book: {book}

Chapter: {chapter}

Source: {source}

Content:
{content}
"""
        )

    context = "\n\n-------------------------\n\n".join(
        context_parts
    )

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = ChatPromptTemplate.from_template(
        """
তুমি একটি বাংলা বইভিত্তিক Knowledge Base Chatbot।

তোমাকে শুধুমাত্র নির্বাচিত বই "বিশ্বের উপাদান" থেকে
প্রশ্নের উত্তর দিতে হবে।

নিয়ম:

1. শুধুমাত্র Book Context-এর তথ্য ব্যবহার করে উত্তর দেবে।

2. Context-এর বাইরে কোনো তথ্য ব্যবহার করবে না।

3. Context-এর কোনো অংশে প্রশ্নের উত্তর বা প্রশ্নের সঙ্গে
   সরাসরি সম্পর্কিত তথ্য থাকলে অবশ্যই সেই তথ্য ব্যবহার করে
   উত্তর দেবে।

4. শুধু তখনই
   "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"
   বলবে, যখন দেওয়া সব Context পরীক্ষা করে প্রশ্নের উত্তর
   দেওয়ার মতো কোনো তথ্যই নেই।

5. উত্তর দেওয়ার পরে কখনো
   "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"
   যোগ করবে না।

6. একই উত্তরে answer এবং no-answer—দুটো একসাথে দেবে না।

7. উত্তর বাংলায় দেবে।

8. উত্তর পাওয়া গেলে শেষে Chapter এবং Source উল্লেখ করবে।

9. যদি প্রশ্নটি বইয়ের বিষয়বস্তুর বাইরে হয় এবং Context-এ
   তার উত্তর না থাকে, তাহলে শুধু বলবে:

   "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"

10. Context-এ থাকা কোনো সম্পর্কিত তথ্য পাওয়া গেলে
    শুধু "তথ্যটি পাওয়া যায়নি" বলবে না।

-------------------------
BOOK CONTEXT
-------------------------

{context}

-------------------------
QUESTION
-------------------------

{question}

-------------------------

এখন প্রশ্নের উত্তর দাও।
"""
    )

    formatted_prompt = prompt.format(
        context=context,
        question=question
    )

    # -----------------------------
    # Create LLM
    # -----------------------------

    llm = create_llm()

    # -----------------------------
    # Generate response
    # -----------------------------

    response = llm.invoke(
        formatted_prompt
    )

    answer = response.content

    # -----------------------------
    # Empty response handling
    # -----------------------------

    if not answer or not answer.strip():

        return "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"

    return answer


# -----------------------------
# Main
# -----------------------------
def main():

    question = "পরমাণু কী?"

    print("\nQuestion:")
    print(question)

    print("\nGenerating answer...\n")

    answer = answer_question(
        question
    )

    print("Answer:")
    print(answer)


# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main()