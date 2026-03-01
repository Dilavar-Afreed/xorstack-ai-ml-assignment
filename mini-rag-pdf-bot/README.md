# Mini RAG Bot – PDF Q&A

## 📌 Objective

Build a Retrieval-Augmented Generation (RAG) chatbot that answers questions from a single PDF document.

The system:
- Loads a PDF
- Chunks the text
- Generates embeddings
- Stores them in FAISS
- Retrieves relevant chunks
- Uses an LLM to generate grounded answers

---

# 🏗 Architecture Overview

User Question
      ↓
Convert to embedding
      ↓
Retrieve top-k relevant chunks (FAISS)
      ↓
Pass retrieved context to LLM
      ↓
Generate answer grounded in context

---

# 📂 Project Structure


mini-rag-pdf-bot/
│
├── pdf/
│ └── document.pdf
│
├── faiss_index/ # Saved vector database
├── index_metadata.json # Stores PDF hash
│
├── rag_bot.py
├── requirements.txt
├── .env
└── README.md


---

# 🔎 Chunking Strategy

We use:

- `RecursiveCharacterTextSplitter`
- `chunk_size = 1000`
- `chunk_overlap = 200`

### Why?

- 1000 characters preserves semantic coherence.
- 200 overlap ensures context continuity across chunk boundaries.
- Prevents information loss at chunk edges.

This balances retrieval precision and context completeness.

---

# 🧠 Embedding Approach

We use:

- `OpenAIEmbeddings` (dense vector embeddings)

### Why Dense Embeddings?

- Capture semantic similarity.
- More robust than keyword search.
- Handle paraphrased queries effectively.

Each chunk is converted into a high-dimensional vector and stored in FAISS.

---

# 🗄 Vector Storage (FAISS)

- We use FAISS as a local vector database.
- Embeddings are stored locally on disk.
- Enables fast similarity search.

### Persistence Strategy

On first run:
- PDF is chunked
- Embeddings are created
- FAISS index is saved locally (`faiss_index/`)

On subsequent runs:
- Existing index is loaded
- Re-embedding is skipped

This improves performance and reduces embedding cost.

---

# 🔍 Retrieval Strategy

- Top-k retrieval (k=3)
- Retrieves the most semantically relevant chunks
- Balances recall and precision

---

# 🤖 Answer Reliability

To reduce hallucinations:

- Temperature = 0
- LLM instructed to answer **only from retrieved context**
- If answer not found → responds:
  "The information is not available in the document."

This ensures grounded responses.

---

# ⚙️ Setup Instructions

## 1️⃣ Create Conda Environment

```bash
conda create -n ragbot python=3.10
conda activate ragbot
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Add API Key

Create .env file:

OPENAI_API_KEY=your_key_here
▶️ Run the Bot
python rag_bot.py

Ask questions about the PDF interactively.