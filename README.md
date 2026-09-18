# 📚 বিশ্বের উপাদান — Knowledge Base Chatbot

A Bengali book-based Retrieval-Augmented Generation (RAG) chatbot built using **LangChain, multilingual embeddings, FAISS, Groq, and Streamlit**.

The chatbot answers questions using only the selected Bengali book **“বিশ্বের উপাদান”** and provides the relevant chapter and source URL with each answer.

---

## 🎯 Project Objective

The goal of this project is to build a **Knowledge Base Chatbot with a Vector Database** that can:

* Crawl a complete Bengali book from Wikisource
* Clean and preprocess the collected text
* Split the book into meaningful chunks
* Generate multilingual embeddings
* Store embeddings in a FAISS vector database
* Retrieve relevant book passages
* Generate answers using an LLM
* Provide chapter and source information
* Avoid using outside knowledge for book-specific questions
* Clearly respond when information is not available in the selected book

---

## 📖 Knowledge Source

### Selected Book

**Book:** বিশ্বের উপাদান
**Author:** শ্রীচারুচন্দ্র ভট্টাচার্য
**Publication Year:** 1952
**Publisher:** Visva-Bharati
**Source:** Bengali Wikisource

**Source URL:**

https://bn.wikisource.org/wiki/বিশ্বের_উপাদান

The selected book is a completed Bengali prose book containing six main chapters.

### Chapters

1. অণু, পরমাণু
2. ইলেক্‌ট্রন ও প্রোটন
3. পজিট্রন, নিউট্রন, নিউট্রিনো, মিসোট্রন
4. উপাদানের প্রকৃতি
5. শক্তি ও তড়িৎ
6. উপসংহার

---

## 🧠 RAG Architecture

```text
Bengali Wikisource Book
        ↓
      Crawler
        ↓
   Raw Text Files
        ↓
   Text Processor
        ↓
   Cleaned Documents
        ↓
      Chunking
        ↓
   103 Text Chunks
        ↓
Multilingual Embeddings
        ↓
     FAISS Vector DB
        ↓
      Retriever
        ↓
Relevant Book Context
        ↓
      Groq LLM
        ↓
Bengali Answer
        ↓
Chapter + Source Citation
```

---

## 🔍 Retrieval Configuration

The final chunking configuration is:

```text
Chunk size: 1000 characters
Chunk overlap: 200 characters
```

The processed book produces:

```text
Total chunks: 103
```

The chatbot uses:

```text
Embedding Model:
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

The retriever uses FAISS similarity search with:

```text
k = 10
```

This configuration was selected after testing different chunk sizes.

---

## 📊 Retrieval Evaluation

The project includes **10 test questions**:

* 9 answerable questions
* 1 no-answer question

For the 9 answerable questions, the expected chapter was found within the top-10 retrieved results.

### Result

```text
Answerable tests passed: 9/9
Retrieval hit rate: 100%
```

> Note: This 100% result represents **retrieval coverage at top-10**, not 100% end-to-end answer accuracy.

The no-answer test is separately used to evaluate whether the chatbot can avoid answering questions outside the selected book.

---

## 🗂️ Project Structure

```text
module-24-knowledge-base-chatbot/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
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
└── vectorstore/
    └── FAISS index files
```

> `venv/` and `.env` are intentionally excluded from Git because they are listed in `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rabiul9137/module-24-knowledge-base-chatbot.git
cd module-24-knowledge-base-chatbot
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the real API key to GitHub.

The project `.gitignore` contains:

```text
.env
```

so the API key remains local.

---

## 🚀 Run the Chatbot

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the Streamlit application:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## 🧪 Test Questions

The project contains 10 test questions.

### 1. পরমাণু কী?

### 2. ইলেক্ট্রন কী?

### 3. প্রোটন কী?

### 4. নিউট্রন কী?

### 5. পজিট্রন কী?

### 6. মিসোট্রন বা মেসন সম্পর্কে বইটিতে কী বলা হয়েছে?

### 7. মৌলিক পদার্থের পরমাণুগুলোর মধ্যে কী পার্থক্য আছে?

### 8. শক্তি ও তড়িৎ সম্পর্কে বইটিতে কী আলোচনা করা হয়েছে?

### 9. প্রাউটের মত কী ছিল?

### 10. বাংলাদেশের বর্তমান জনসংখ্যা কত?

Question 10 is intentionally outside the selected book and is used as a **no-answer test**.

Expected behavior:

```text
এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।
```

---

## 🛡️ Hallucination Control

The chatbot is instructed to answer book-specific questions only from the retrieved book context.

The prompt enforces the following rules:

1. Use only the retrieved book context.
2. Do not use outside knowledge.
3. Use relevant information even if the wording differs from the question.
4. Answer in Bengali.
5. Include the relevant chapter and source.
6. If the information is not available in the selected book, clearly say:

```text
এই তথ্যটি নির্বাচিত বইটিতে পাওয়া যায়নি।
```

This prevents the chatbot from behaving like a general-purpose knowledge engine.

---

## 🌐 Multilingual Embeddings

The source material is Bengali, so an English-only embedding model would not be appropriate for semantic retrieval.

The project uses:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

This model supports multilingual semantic representations and works with the Bengali book content.

---

## 🗄️ Why FAISS?

FAISS is used as the vector database because it provides efficient similarity search over embedding vectors and is convenient for a local RAG application.

The vector store is generated from the processed book chunks.

---

## 🏷️ Metadata Preservation

Each document chunk preserves important metadata such as:

```text
Book
Chapter
Source URL
Filename
```

This allows the chatbot to identify where retrieved information came from and provide source references with answers.

---

## 🧩 Main Components

### `crawler.py`

Downloads the selected book chapters from Bengali Wikisource.

### `processor.py`

Cleans raw scraped text and preserves important metadata.

### `chunker.py`

Splits cleaned documents into overlapping text chunks.

Final configuration:

```text
chunk_size = 1000
chunk_overlap = 200
```

### `embedding.py`

Generates multilingual embeddings and creates the FAISS vector database.

### `retriever.py`

Loads the FAISS database and retrieves the most relevant book chunks.

### `qa.py`

Combines retrieval with the Groq LLM and generates Bengali answers based only on retrieved context.

### `app.py`

Provides the Streamlit chatbot interface.

---

## 🧰 Technologies Used

| Technology               | Purpose                           |
| ------------------------ | --------------------------------- |
| Python                   | Core programming language         |
| LangChain                | RAG pipeline                      |
| LangChain Community      | FAISS and supporting integrations |
| LangChain HuggingFace    | Embedding integration             |
| LangChain Text Splitters | Document chunking                 |
| BeautifulSoup            | Web scraping                      |
| Requests                 | HTTP requests                     |
| Sentence Transformers    | Multilingual embeddings           |
| FAISS                    | Vector similarity search          |
| Groq                     | LLM inference                     |
| Streamlit                | Web interface                     |
| python-dotenv            | Environment variable management   |

---

## 📌 Important Design Decisions

### Multilingual embedding model

The source material is Bengali, so multilingual embeddings were selected instead of an English-only embedding model.

### Chunk size

Different chunking configurations were tested.

The final configuration:

```text
1000 characters
200 character overlap
```

produced 103 chunks and achieved 9/9 expected-chapter retrieval coverage in the current test set.

### Top-k retrieval

The retriever uses:

```text
k = 10
```

This was chosen because some questions, such as `প্রোটন কী?`, did not consistently retrieve the expected chapter within a smaller top-k value but were found when using top-10 retrieval.

---

## 🔮 Future Improvements

Possible improvements include:

* Bengali-specific embedding models
* Hybrid keyword + semantic retrieval
* Reranking retrieved documents
* Better no-answer detection
* Streaming LLM responses
* Improved source citation UI
* Chunking strategy comparison
* Embedding model comparison
* Automated retrieval evaluation
* End-to-end answer evaluation
* Deployment using Streamlit Cloud or another hosting platform

---

## 👨‍💻 Author

**Rabiul Islam**

AI/ML Developer | Computer Vision | Generative AI | AI Agents

GitHub:

https://github.com/rabiul9137

Project Repository:

https://github.com/rabiul9137/module-24-knowledge-base-chatbot

---

## 📜 Disclaimer

This project is an educational RAG application built around the selected Bengali book **“বিশ্বের উপাদান”**.

The chatbot is designed to answer questions using the selected knowledge source and should not be treated as a general-purpose factual search engine.
## ⭐ Bonus — Chunking Strategy Comparison

Two different chunking strategies were evaluated to measure their effect on retrieval performance.

### Approaches Tested

| Strategy   | Chunk Size | Chunk Overlap | Total Chunks |
| ---------- | ---------: | ------------: | -----------: |
| Strategy A |        700 |           150 |          135 |
| Strategy B |       1000 |           200 |          103 |

Both strategies used the same multilingual embedding model:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

The same 9 answerable test questions and the same top-10 retrieval setting were used for both strategies.

### Evaluation Method

For each test question, the FAISS vector store retrieved the top 10 chunks.

A retrieval was counted as a **hit** when the expected chapter appeared in at least one of the top 10 retrieved chunks.

**Hit Rate = Correct Retrievals / Total Answerable Questions × 100**

### Results

| Strategy   | Correct Retrievals |   Hit Rate |
| ---------- | -----------------: | ---------: |
| 700 / 150  |              7 / 9 |  **77.8%** |
| 1000 / 200 |              9 / 9 | **100.0%** |

### Result

The `1000 / 200` configuration achieved a **100.0% retrieval hit rate** on the 9 answerable test questions, compared with **77.8%** for the `700 / 150` configuration.

Therefore, the `1000 / 200` configuration was selected for the final RAG pipeline based on this evaluation.

> **Note:** This hit-rate evaluation measures retrieval coverage only. It does not represent the accuracy of the final LLM-generated answers and should not be interpreted as a universal result for other datasets or books.
