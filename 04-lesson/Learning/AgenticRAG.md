# Agentic RAG 

Agentic RAG extends traditional Retrieval-Augmented Generation by adding AI agents that plan, decide, and iterate on retrieval and generation — instead of running a fixed, one-pass pipeline.

## What is Traditional RAG?

Traditional RAG is a simple, one-shot pipeline: embed the query, search a vector store, retrieve top-k chunks, stuff them into the LLM prompt, generate an answer.

```
[ User Query ] → [ Embed ] → [ Vector Search ] → [ Retrieve Chunks ] → [ LLM ] → [ Answer ]
```

- No decision-making — it always retrieves once, the same way, regardless of query complexity.
- If retrieval fails or is insufficient, the pipeline still generates an answer anyway (often causing hallucination).

## What is Agentic RAG?

Agentic RAG adds an agent layer on top of RAG that can reason, plan, choose tools, evaluate results, and loop back if needed. Instead of one fixed retrieval step, the agent actively decides how to retrieve, what to retrieve, and whether the retrieved content is good enough.

```
        [ User Query ]
              │
              ▼
        [ Agent: Plan ]  ──► decides strategy (single search, multi-hop, tool call, etc.)
              │
              ▼
        [ Retrieve ]     ──► vector search / keyword search / API / DB / web
              │
              ▼
        [ Agent: Evaluate ] ──► "Is this enough to answer?"
              │
   ┌──────────┴───────────┐
   │ No                   │ Yes
   ▼                      ▼
[ Retry/ Refine ]   [ Generate Answer ]
   │    
   │
   └──► back to Retrieve
```

## Core Difference: RAG vs Agentic RAG

| Aspect | Traditional RAG | Agentic RAG |
|---|---|---|
| Retrieval | Single-pass, fixed | Iterative, adaptive, multi-hop |
| Decision-making | None — always same flow | Agent decides strategy, tools, and when to stop |
| Tool use | Only vector search | Vector search, APIs, SQL, web search, calculators |
| Self-correction | None | Validates own output, retries if gaps found |
| Query handling | Treats query as-is | Can decompose, rewrite, or split complex queries |
| Best for | Simple factual Q&A | Complex, multi-step, ambiguous, or multi-source questions |

## Core Components / Architecture Layers

| Layer | Component | Function |
|---|---|---|
| Orchestration | Planning agent | Decomposes the goal into subtasks, routes to specialized agents |
| Reasoning | Agent controller (LLM) | Generates plans, selects tools, evaluates intermediate outputs |
| Action | Tool library | Exposes retrieval, APIs, code execution, external systems |
| Retrieval | Retriever + vector store | Returns semantically relevant documents on agent request |
| Generation | Generator LLM | Synthesizes retrieved context into a final output |
| Memory | Short-term / long-term stores | Maintains task context within a session and across sessions |

## How the Agent Loop Works

1. **Understand the query** — the agent parses intent and decides if the query needs to be broken into smaller sub-questions.
2. **Plan** — decide which data sources to consult (vector DB, SQL DB, web, knowledge graph) and in what order.
3. **Retrieve** — run the chosen retrieval strategy (single search, multi-hop, cross-source).
4. **Augment/structure context** — clean, deduplicate, summarize, and rank retrieved content before it reaches the LLM (raw dumps are never passed directly).
5. **Reason and validate** — check if retrieved evidence actually answers the question; detect contradictions or missing pieces.
6. **Loop or generate** — if evidence is insufficient, go back to retrieval with a refined query; if sufficient, generate the final answer.
7. **Log everything** — every retrieval decision, reasoning step, and validation check is logged for observability and auditing.

## Key Techniques Inside Agentic RAG

- **Dynamic query rewriting** — the agent rewrites the query based on partial evidence found so far.
- **Multi-hop retrieval** — one retrieved result triggers another retrieval (chaining lookups).
- **Cross-source retrieval** — combining vector search, keyword search, structured DB queries, and domain-specific repositories.
- **Confidence scoring** — filtering out irrelevant or low-value retrieved chunks.
- **Context synthesis** — merging multiple sources into one coherent context block instead of dumping raw chunks.
- **Self-correction cycles** — the agent critiques its own draft answer and loops back to retrieval/augmentation if something's wrong.
- **Ontology / knowledge graph integration** — using structured relationships between entities for more precise, context-sensitive retrieval.

## When to Use Agentic RAG

**Use traditional RAG when:**
- Queries are simple, factual, single-source lookups.
- Speed and low cost matter more than deep accuracy.
- The knowledge base is small and well-structured.

**Use Agentic RAG when:**
- Questions are complex, multi-part, or ambiguous.
- Answers require combining multiple data sources (DB + API + documents).
- Accuracy and fact-grounding matter more than latency (e.g., legal research, enterprise knowledge management, customer support with policy lookups).
- The system needs to self-correct instead of confidently returning a wrong answer.

## Benefits

- Higher accuracy through iterative validation instead of one-shot retrieval.
- Handles complex, multi-step, or multi-source questions traditional RAG can't.
- Reduces hallucination by grounding answers in validated, re-checked evidence.
- Adapts dynamically — different queries can trigger different retrieval strategies.

## Limitations

- Significantly more complex to build and maintain than plain RAG.
- Higher latency — multiple reasoning/retrieval loops take more time.
- Higher computational and API cost per query due to repeated LLM calls.
- Requires careful design of stopping conditions (avoid infinite retrieval loops).
- Harder to debug — more moving parts (planning, tools, memory, validation).

## Where This Fits With LangChain / LangGraph

Agentic RAG is a natural fit for **LangGraph** rather than plain LangChain chains, because it needs looping, conditional retrieval, and state tracking:

- **Retriever + vector store** → built using LangChain components (embeddings, Chroma/Pinecone/FAISS).
- **Planning, looping, evaluation** → implemented as LangGraph nodes and conditional edges (retrieve → evaluate → loop back or generate).
- **Memory across retrieval attempts** → tracked in LangGraph's shared state object.
- **Tool calls (SQL, API, web search)** → exposed as LangChain tools, invoked from within the graph.

This mirrors the general rule from your other notes: LangChain provides the retrieval/tool components, LangGraph orchestrates the iterative agentic logic around them.

## Real-World Use Cases

- Enterprise knowledge search where questions span multiple documents, databases, and policies.
- Customer support bots that need to check multiple systems (order DB, FAQ docs, ticketing API) before answering.
- Legal or compliance research requiring cross-referencing multiple sources and self-verification.
- Log/anomaly analysis where the agent may need to query logs, then cross-check with a database, then summarize.
- Research assistants that decompose a broad question into sub-questions and retrieve iteratively.