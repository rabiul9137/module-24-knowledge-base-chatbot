# 📚 Knowledge Base Chatbot — বিশ্বের উপাদান

A Bengali book-based RAG (Retrieval-Augmented Generation) chatbot built using LangChain, multilingual embeddings, FAISS, and Groq LLM.

The chatbot answers questions using only the selected Bengali book **“বিশ্বের উপাদান”** by **শ্রীচারুচন্দ্র ভট্টাচার্য**.

---

## 🎯 Project Objective

The goal of this project is to build a Knowledge Base Chatbot that can:

* Crawl a complete Bengali book from Wikisource
* Clean and preprocess the collected text
* Split the book into meaningful chunks
* Generate multilingual embeddings
* Store embeddings in a FAISS vector database
* Retrieve relevant book content for a user question
* Generate answers using an LLM
* Provide Chapter and Source information with the answer
* Clearly respond when information is not available in the selected book

---

## 📖 Knowledge Source

**Book:** বিশ্বের উপাদান
**Author:** শ্রীচারুচন্দ্র ভট্টাচার্য
**Year:** 1952
**Publisher:** Visva-Bharati
**Source:** Bengali Wikisource

### Main Chapters

1. অণু, পরমাণু
2. ইলেক্‌ট্রন ও প্রোটন
3. পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন
4. উপাদানের প্রকৃতি
5. শক্তি ও তড়িৎ
6. উপসংহার

---

## 🏗️ RAG Architecture

```text
Bengali Wikisource
        │
        ▼
     Crawler
        │
        ▼
   Raw Text Files
        │
        ▼
 Text Cleaning & Processing
        │
        ▼
      Chunking
        │
        ▼
Multilingual Embeddings
        │
        ▼
   FAISS Vector DB
        │
        ▼
     Retriever
        │
        ▼
     Groq LLM
        │
        ▼
      Answer
        │
        ▼
 Chapter + Source
```

---

## 🔄 Project Pipeline

### 1. Web Crawling

The project collects the complete book chapters from Bengali Wikisource.

Crawler:

```text
src/crawler.py
```

The crawler discovers the chapter URLs and saves the raw text inside:

```text
data/book/
```

---

### 2. Text Processing

Raw Wikisource text contains metadata and navigation elements.

The processor:

* Removes unnecessary navigation text
* Normalizes whitespace
* Extracts metadata
* Identifies chapter titles
* Preserves source URLs
* Saves cleaned documents

Processor:

```text
src/processor.py
```

Cleaned files are stored in:

```text
data/cleaned/
```

---

### 3. Chunking

The cleaned documents are divided into smaller overlapping chunks.

Configuration:

```text
Chunk size: 1000 characters
Chunk overlap: 200 characters
```

Chunking uses LangChain's:

```text
RecursiveCharacterTextSplitter
```

Implementation:

```text
src/chunker.py
```

Each chunk preserves metadata such as:

* Book
* Chapter
* Source URL
* Filename

---

### 4. Multilingual Embeddings

The project uses a multilingual sentence-transformer model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

This model was selected because the knowledge base contains Bengali text.

Implementation:

```text
src/embedding.py
```

---

### 5. FAISS Vector Database

The generated embeddings are stored in a FAISS vector database.

```text
vectorstore/
```

FAISS allows the chatbot to search for semantically relevant book chunks.

---

### 6. Retrieval

The retriever loads the FAISS database and searches for relevant documents.

The current retrieval configuration uses:

```text
k = 10
```

This helps retrieve relevant Bengali content even for short questions.

Implementation:

```text
src/retriever.py
```

---

### 7. Question Answering

The QA system:

1. Receives a user question
2. Retrieves relevant book chunks
3. Builds a context
4. Sends the context and question to the LLM
5. Generates a Bengali answer
6. Includes Chapter and Source information

Implementation:

```text
src/qa.py
```

The LLM used in this project is:

```text
openai/gpt-oss-20b
```

through the Groq API.

---

## 💬 Chatbot Interface

The project includes a Streamlit interface.

Main application:

```text
app.py
```

The UI provides:

* Bengali chatbot interface
* Chat history
* Question input
* Loading indicator
* Book information
* Clear chat option
* Chapter and Source information in responses

Run the application with:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
module-24-knowledge-base-chatbot/
│
├── app.py
├── README.md
├── Requirements.txt
├── .env
│
├── data/
│   ├── book/
│   │   ├── chapter_1.txt
│   │   ├── chapter_2.txt
│   │   ├── chapter_3.txt
│   │   ├── chapter_4.txt
│   │   ├── chapter_5.txt
│   │   └── chapter_6.txt
│   │
│   └── cleaned/
│       ├── chapter_1.txt
│       ├── chapter_2.txt
│       ├── chapter_3.txt
│       ├── chapter_4.txt
│       ├── chapter_5.txt
│       └── chapter_6.txt
│
├── src/
│   ├── crawler.py
│   ├── processor.py
│   ├── chunker.py
│   ├── embedding.py
│   ├── retriever.py
│   └── qa.py
│
├── tests/
│   ├── test_questions.json
│   └── run_tests.py
│
├── vectorstore/
│
└── venv/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd module-24-knowledge-base-chatbot
```

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the real API key to GitHub.

Add `.env` to `.gitignore`.

---

## ▶️ Run the Chatbot

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then run:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 🧪 Test Questions

The project contains 10 test questions covering the book's major topics.

Examples:

### Question 1

```text
পরমাণু কী?
```

### Question 2

```text
ইলেক্ট্রন কী?
```

### Question 3

```text
প্রোটন কী?
```

### Question 4

```text
নিউট্রন কী?
```

### Question 5

```text
পজিট্রন কী?
```

### Question 6

```text
মিসোট্রন বা মেসন সম্পর্কে বইটিতে কী বলা হয়েছে?
```

### Question 7

```text
মৌলিক পদার্থের পরমাণুগুলোর মধ্যে কী পার্থক্য আছে?
```

### Question 8

```text
শক্তি ও তড়িৎ সম্পর্কে বইটিতে কী আলোচনা করা হয়েছে?
```

### Question 9

```text
প্রাউটের মত কী ছিল?
```

### Question 10 — No Answer Test

```text
বাংলাদেশের বর্তমান জনসংখ্যা কত?
```

Expected behavior:

```text
এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।
```

---

## 🛡️ Hallucination Control

The chatbot is instructed to answer only from the retrieved book context.

If the required information is not available in the selected book, the chatbot should respond:

```text
এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।
```

The chatbot should not use outside knowledge to answer book-specific questions.

---

## 🧰 Technologies Used

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| LangChain             | RAG pipeline              |
| BeautifulSoup         | Web scraping              |
| Requests              | HTTP requests             |
| Sentence Transformers | Multilingual embeddings   |
| FAISS                 | Vector database           |
| Groq                  | LLM inference             |
| Streamlit             | Web interface             |
| python-dotenv         | Environment variables     |

---

## 📌 Important Design Decisions

### Why a multilingual embedding model?

The source material is Bengali. Therefore, an English-only embedding model would not be suitable for this knowledge base.

The project uses:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

to support Bengali semantic search.

### Why FAISS?

FAISS provides efficient similarity search over vector embeddings and is simple to use for a local knowledge-base project.

### Why metadata?

Each chunk stores:

```text
Book
Chapter
Source URL
Filename
```

This allows the chatbot to identify where an answer came from.

---

## 🚀 Future Improvements

Possible future improvements include:

* Better Bengali-specific embeddings
* Hybrid keyword + semantic retrieval
* Reranking retrieved documents
* Streaming LLM responses
* Improved source citation UI
* Chunking strategy comparison
* Embedding model comparison
* Evaluation using retrieval hit-rate
* Deployment using Streamlit Cloud or another hosting platform

---

## 👨‍💻 Author

**Rabiul Islam**

AI/ML Developer | Computer Vision | Generative AI | AI Agents

GitHub:

```text
https://github.com/rabiul9137
```

---

## 📜 Disclaimer

This project is an educational RAG application built around the selected Bengali book **“বিশ্বের উপাদান”**.

The chatbot is designed to answer based on the selected knowledge source and should not be treated as a general-purpose factual search engine.
