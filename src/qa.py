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

    # -----------------------------
    # Build context
    # -----------------------------
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
   তুমি "বিশ্বের উপাদান" বইভিত্তিক একটি Knowledge Base Chatbot।
   
   তোমার কাজ হলো ব্যবহারকারীর প্রশ্নের উত্তর শুধুমাত্র নিচে দেওয়া
   BOOK CONTEXT থেকে দেওয়া।
   
   নিয়ম:
   
   1. শুধুমাত্র BOOK CONTEXT-এর তথ্য ব্যবহার করবে।
   
   2. নিজের সাধারণ জ্ঞান বা বাইরের কোনো তথ্য ব্যবহার করবে না।
   
   3. BOOK CONTEXT-এর যেকোনো অংশে প্রশ্নের উত্তর বা প্রাসঙ্গিক তথ্য থাকলে
      সেই তথ্য ব্যবহার করে উত্তর দেবে।
   
   4. Context-এর ভাষা পুরোনো বা কঠিন হলেও তার অর্থ বুঝে সহজ বাংলায় উত্তর দেবে।
   
   5. যদি BOOK CONTEXT-এর কোথাও প্রশ্নের উত্তর বা প্রাসঙ্গিক তথ্য না থাকে,
      তাহলে শুধু বলবে:
   
      "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"
   
   6. একই উত্তরে কখনো উত্তর এবং "এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।"
      দুটো একসাথে দেবে না।
   
   7. উত্তর বাংলায় দেবে।
   
   8. উত্তর দেওয়ার শেষে অবশ্যই সংশ্লিষ্ট Chapter এবং Source উল্লেখ করবে।
   
   9. বইয়ের তথ্যের বাইরে কোনো তথ্য যোগ করবে না।
   
   -------------------------
   BOOK CONTEXT
   -------------------------
   
   {context}
   
   -------------------------
   QUESTION
   -------------------------
   
   {question}
   
   -------------------------
   
   এখন BOOK CONTEXT ব্যবহার করে প্রশ্নের উত্তর দাও।
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
    response = llm.invoke(formatted_prompt)

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

    answer = answer_question(question)

    print("Answer:")
    print(answer)


# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main()