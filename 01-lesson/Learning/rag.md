

# RAG — Retrieval-Augmented Generation

***

## 🔑 Why RAG Exists — The Core Problem First

LLMs have two fundamental limitations: 

| Problem | Explanation |
|---|---|
| **Knowledge cutoff** | Model was trained up to a certain date — knows nothing after that |
| **No private data** | Model was never trained on your company's documents, database, or codebase |
| **Hallucination** | When the model doesn't know, it confidently makes things up |
| **Context window limit** | Can't stuff 10 million tokens of knowledge into a 200K window |

> **RAG is the solution:** Instead of relying on what the model "memorized," you give it the **right information at the right time** — retrieved from an external knowledge base.

***

## 📖 What RAG Stands For

```
Retrieval  → Fetch relevant data based on similarity to the query
Augmented  → Use that fetched data as additional context in the prompt
Generation → LLM generates a response using that enriched context
```


***

## 🔁 The RAG Pipeline 

```
User Query
    ↓
Embed the Query  (query → vector)
    ↓
Search Vector Database  (find similar chunks)
    ↓
Retrieve Top-K Relevant Chunks
    ↓
Augment the Prompt  (original query + retrieved chunks)
    ↓
Send Augmented Prompt → LLM
    ↓
LLM Generates Context-Aware Response
    ↓
User sees accurate, grounded answer
```


***

# Part 1 — The Two Types of LLM Memory

Before building RAG, understand this foundational distinction: 

| Type | What It Is | Example |
|---|---|---|
| **Parametric Memory** | Knowledge baked into model **weights** during training | GPT knows Paris is the capital of France |
| **Non-Parametric Memory** | External data **retrieved at runtime** — not in weights | Your company policy PDF retrieved via RAG |

**RAG adds Non-Parametric Memory** to LLMs — making them dynamic, updatable, and grounded in real data.

> Think of parametric = long-term memory baked into the brain. Non-parametric = looking something up in a book right now.

***

# Part 2 — The Three Stages of RAG

## Stage 1: INGESTION (Build the Knowledge Base)

This happens **before** any user query — you prepare your data.

### Step 1 — Load Documents
Load all your source data:
- PDFs, Word docs, CSVs, web pages, code files, databases
- These are your "knowledge base"

### Step 2 — Chunking
Split large documents into smaller pieces called **chunks**:

```
Full Document (100 pages)
        ↓
Chunk 1: Page 1–2 content
Chunk 2: Page 2–3 content  (with overlap)
Chunk 3: Page 3–4 content
...
Chunk N: Page 99–100 content
```

**Why chunking matters:**
- Embedding models have token limits (e.g., BERT max = 512 tokens)
- Smaller chunks = more precise retrieval
- Overlap between chunks prevents losing context at boundaries 

**Common chunk sizes:**
| Chunk Size | Best For |
|---|---|
| 128–256 tokens | Precise fact retrieval |
| 512 tokens | General Q&A |
| 1024 tokens | Complex reasoning tasks |

### Step 3 — Embed Each Chunk
Each chunk → run through an **embedding model** → becomes a dense vector: 

```
Chunk: "The refund policy allows returns within 30 days."
          ↓  (Embedding Model e.g. BERT, text-embedding-ada-002)
Vector: [0.23, -0.88, 0.41, 1.02, ...]   (768 or 1536 dimensions)
```

### Step 4 — Store in Vector Database
All chunk vectors are stored in a **Vector Database**: 

```
Vector DB stores:
┌────────────────────────────────────────────────┐
│  ID  │  Vector (768 dims)  │  Original Text    │
├────────────────────────────────────────────────┤
│  1   │  [0.23, -0.88, ...] │  "Refund policy…" │
│  2   │  [0.91, 0.44, ...]  │  "Shipping info…" │
│  3   │  [-0.12, 0.67, ...] │  "Return guide…"  │
└────────────────────────────────────────────────┘
```

**Popular Vector Databases:**

| Database | Type | Best For |
|---|---|---|
| **FAISS** (Facebook) | Local library | Fast prototyping, local use |
| **Pinecone** | Cloud, managed | Production apps |
| **Weaviate** | Open-source | Self-hosted, multi-modal |
| **Chroma** | Lightweight | Python dev, small projects |
| **Qdrant** | Rust-based | High performance |
| **pgvector** | PostgreSQL extension | ← **You can use this with your existing Postgres!** |


***

## Stage 2: RETRIEVAL (Find What's Relevant)

When a user sends a query, the retrieval stage begins: 

### Step 1 — Embed the Query
```
User Query: "What is the refund policy?"
          ↓  (Same embedding model used during ingestion)
Query Vector: [0.21, -0.85, 0.39, 1.01, ...]
```

> ⚠️ **Critical:** You must use the **same embedding model** for both ingestion and retrieval. Different models = incompatible vector spaces.

### Step 2 — Similarity Search
The query vector is compared against all stored chunk vectors using **Cosine Similarity**:

```
cosine_similarity(query_vector, chunk_vector) = score between 0 and 1
                                                1 = identical meaning
                                                0 = completely unrelated
```

The top-K most similar chunks are retrieved (e.g., top 3 or top 5).

### Step 3 — Return Top-K Chunks
```
Query: "What is the refund policy?"

Retrieved Chunks (sorted by similarity):
1. Score: 0.94 → "The refund policy allows returns within 30 days..."
2. Score: 0.88 → "To initiate a return, contact support@..."
3. Score: 0.81 → "Refunds are processed within 5–7 business days..."
```

***

## Stage 3: GENERATION (Augment + Answer)

### Step 1 — Build the Augmented Prompt
Combine the original query + retrieved chunks into one prompt: 

```
AUGMENTED PROMPT STRUCTURE:
────────────────────────────────────────────
[System Instruction]
You are a helpful assistant. Answer using ONLY the context below.
If the answer is not in the context, say "I don't know."

[Retrieved Context]
Context 1: "The refund policy allows returns within 30 days..."
Context 2: "To initiate a return, contact support@..."
Context 3: "Refunds are processed within 5–7 business days..."

[User Question]
What is the refund policy?
────────────────────────────────────────────
```

### Step 2 — LLM Generates Grounded Response
The LLM now has the **exact relevant information** in its context window and generates a factual, grounded answer — without hallucinating.

***

# Part 3 — Retrieval Strategies (Basic to Advanced)

## 1. Naive / Standard RAG
- Same chunk used for **both** embedding and synthesis
- Simple, fast, straightforward 

```
[Document] → [Fixed Chunks] → [Embed] → [Retrieve] → [Send to LLM]
```

**Limitations:** Chunk might be too small to give enough context for answering.

***

## 2. Sentence-Window Retrieval (Small-to-Large)
- Embed **small sentences** (precise retrieval)
- But when retrieved, **expand** the surrounding context before sending to LLM

```
Embed:   [Single Sentence]       ← small = precise search
Retrieve: [Sentence + 3 before + 3 after]  ← larger = rich context for LLM
```

**Why:** Small chunks = better search accuracy. Large context = better answer quality. Best of both worlds.

***

## 3. Auto-Merging / Hierarchical Retrieval
- Store chunks at **multiple levels** simultaneously: sentence → paragraph → section 
- Retrieve small chunks, but auto-merge into parent chunk if multiple child chunks from the same parent are retrieved

```
Chunk sizes: 128  |  256  |  512  |  1024
                ↕      ↕      ↕
If 3 of 4 children retrieved → return the parent instead
```

***

## 4. Hybrid Search
- Combine **dense retrieval** (semantic vectors) + **sparse retrieval** (keyword BM25/TF-IDF) 

```
Query: "refund policy 30 days"

Dense Search (semantic): finds meaning-similar chunks
Sparse Search (keyword): finds exact matches of "refund", "30 days"
          ↓
Ensemble both results → Re-rank → Top-K
```

Best for: when users use exact terminology that semantic search might miss.

***

## 5. Re-Ranking
After initial retrieval, run a **Re-Ranker model** to re-score and reorder results for better quality: 

**Types:**
- **Semantic Re-Ranking** — use BERT/cross-encoder to score query-chunk relevance
- **Learning-to-Rank (LTR)** — trained model that ranks by multiple features (lexical + semantic)

```
Initial Retrieved: [Chunk 3, Chunk 7, Chunk 1, Chunk 12]
After Re-Ranking:  [Chunk 7, Chunk 3, Chunk 12, Chunk 1]  ← reordered by relevance
```

***

# Part 4 — RAG vs Fine-Tuning (Important Distinction)

| | RAG | Fine-Tuning |
|---|---|---|
| **What it does** | Retrieves external knowledge at runtime | Trains model on new data |
| **Knowledge update** | Just update the vector DB | Retrain the model |
| **Cost** | Low (just embedding + retrieval) | High (GPU hours) |
| **Hallucination** | Reduced (grounded in retrieved data) | Can still hallucinate |
| **Private data** | Yes, stays in your DB | Baked into weights (risky) |
| **Best for** | Dynamic, changing knowledge | Specific tone/style/task |


> For most real-world applications (chatbots, document Q&A, support systems) — **RAG is preferred** over fine-tuning because it's cheaper, updatable, and more transparent.

***

# Part 5 — Advanced RAG Concepts (For Later)

These build on top of basic RAG — know they exist, study them next

| Concept | What It Is |
|---|---|
| **Query Expansion** | Rewrite user query into multiple versions to retrieve more |
| **HyDE** (Hypothetical Document Embeddings) | Generate a hypothetical answer, embed it, use it to search |
| **Contextual Compression** | Compress retrieved chunks to remove irrelevant sentences |
| **Self-RAG** | Model decides when to retrieve and when to use its own knowledge |
| **Agentic RAG** | Agent decides which tool/retriever to call dynamically |
| **GraphRAG** | Uses knowledge graphs instead of flat vector search |

***

# Part 6 — RAG Implementation Stack

```
Typical RAG Stack:
┌──────────────────────────────────┐
│  LLM (Claude / GPT-4 / LLaMA)    │ ← Generation
├──────────────────────────────────┤
│  Orchestration Framework         │ ← LangChain / LlamaIndex
├──────────────────────────────────┤
│  Embedding Model                 │ ← text-embedding-ada-002 / BERT
├──────────────────────────────────┤
│  Vector Database                 │ ← pgvector / Pinecone / FAISS
├──────────────────────────────────┤
│  Document Loader + Chunker       │ ← PDFs, CSVs, web pages
└──────────────────────────────────┘
```

**Simple Python RAG (LangChain skeleton):** 
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load + embed documents
documents = TextLoader('your_docs.txt').load()
vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

# 2. Build RAG chain
chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever()
)

# 3. Query
answer = chain.run("What is the refund policy?")
```

***

# 📊 Full RAG Summary Table

| Stage | Action | Tool/Component |
|---|---|---|
| Load | Read documents | TextLoader, PDFLoader |
| Chunk | Split into pieces | RecursiveTextSplitter |
| Embed | Text → vectors | BERT, Ada-002, E5 |
| Store | Save vectors | pgvector, FAISS, Pinecone |
| Query | Embed user question | Same embedding model |
| Retrieve | Similarity search | Cosine similarity, Top-K |
| Augment | Build final prompt | Prompt template |
| Generate | LLM answers | Claude, GPT-4, LLaMA |

***

# ⚡ Must-Remember Points

1. **RAG = Retrieve → Augment → Generate** — in that order
2. **Vector DB is the heart of RAG** — stores your knowledge as searchable embeddings
3. **Same embedding model** must be used for ingestion AND retrieval
4. **Chunking strategy matters** — chunk size directly affects retrieval quality
5. **RAG reduces hallucination** by grounding the model in actual retrieved text
6. **Context window connects to RAG** — retrieved chunks must fit in the window
7. **Naive RAG is the starting point** — sentence-window and hybrid are improvements
8. **pgvector** lets you add RAG to PostgreSQL — directly relevant to your C# + Postgres stack!
9. **RAG ≠ Fine-tuning** — RAG is cheaper, dynamic, and doesn't risk leaking private data into weights 

***
