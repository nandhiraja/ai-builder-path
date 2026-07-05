# LangChain & LangGraph

Reference notes for LangChain v1.4+ and LangGraph v1.2+, covering the modern component/orchestration split, LCEL, agent middleware, and chain-vs-graph mental models.

## The Core Rule

You don't choose between LangChain and LangGraph — they operate at different layers.

- **LangChain** = the Component Library (models, tools, vector stores, prompts).
- **LangGraph** = the Orchestration Runtime (state machines, cyclic execution, memory, persistence).
- Since v1.0, LangChain's high-level `create_agent` API runs entirely on top of the LangGraph engine under the hood.

Legacy classes — `AgentExecutor`, `LLMChain`, `SequentialChain` — are deprecated and no longer part of modern architecture.

***

## Layer 1: LangChain — The Building Blocks

LangChain standardizes how you talk to models, format data, and load files. Everything is composed via **LCEL (LangChain Expression Language)** using the pipe operator `|`.

### Core Components

- **Models** — standardized interfaces for chat models (`ChatOpenAI`, `ChatAnthropic`); outputs map to standardized **Content Blocks**, natively handling text, reasoning traces, citations, and tool calls.
- **Prompts & Structured Outputs** — `ChatPromptTemplate` combined with provider-native structured outputs; pass a Pydantic model or schema directly into the model config to guarantee deterministic JSON output.
- **Vector Stores & RAG** — `DocumentLoaders` and `TextSplitters` process private data; combined with embedding models and vector stores (Chroma, Pinecone), they form a Retriever pipeline.

### Modern LCEL Composition (Stateless, Linear Pipelines)

Linear pipelines are written cleanly using the pipe operator instead of legacy chain classes:

```python
chain = prompt | model.with_structured_output(DesiredSchema) | parser
```

***

## Layer 2: LangGraph — The Stateful Engine

Step down into raw LangGraph when you need loops, state persistence, multi-agent collaboration, or human verification.

### Core Graph Concepts

- **State** — an explicit, shared data schema (typically extending `TypedDict`) that passes through every node; acts as the shared database for the entire agent run.
- **Nodes** — standard Python functions (sync or async) that receive current state, perform an action (LLM call, tool call), and return updated state.
- **Edges & Conditional Edges** — routes controlling execution flow; a conditional edge evaluates current state to dynamically decide the next node (e.g., route to a tool, or terminate at `END`).

### Advanced 2026 Graph Features

- **DeltaChannel** — a specialized data channel storing only incremental changes (e.g., appending one message to a large thread) instead of re-serializing the full historical state, cutting latency significantly.
- **Per-Node Timeouts** — `add_node("node_name", func, timeout=30)` sets hard wall-clock limits and automatic retry policies at the node level.
- **Durable Checkpointing** — automatic state persistence at every step, making long-running multi-agent tasks resilient against crashes or execution failures.

***

## The Entry Point: `create_agent` & Middleware

For standard agentic workflows (Model ↔ Tools ↔ Response), you no longer build a `StateGraph` from scratch — you use LangChain's unified front door, which injects middleware for advanced execution logic.

```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[search_tool, sql_tool],
    system_prompt="You are a production assistant.",
    middleware=[...]  # Where advanced logic lives
)
```

### Production-Ready Middleware Built-Ins

- **Human-in-the-loop Middleware** — automatically pauses graph execution and triggers an interrupt whenever a tool is about to perform a sensitive transaction (SQL write, API call), waiting for user approval.
- **Summarization Middleware** — monitors token usage via model capability profiles and auto-condenses older conversation history near context window limits, preventing `ContextOverflowError`.
- **PII Redaction Middleware** — scans and redacts sensitive data (emails, tokens, IDs) via pattern-matching before sending payloads to third-party LLM providers.

***

## Strategic Breakdown: Chain vs. Graph vs. Deep Agents

| Dimension | LangChain (LCEL) | LangChain (`create_agent`) | LangGraph (`StateGraph`) | Deep Agents |
|---|---|---|---|---|
| Architecture | Linear pipeline (DAG) | Prebuilt agentic loop | Cyclic state machine | High-autonomy harness |
| Execution flow | A → B → C, no looping | Model ↔ Tool cycles managed by a standard loop | Fully custom routing, branching, multi-agent systems | Pre-configured planning loops with sub-agent spawning |
| State control | Stateless by default | Managed internal agent state | Low-level, explicit `TypedDict` control | Virtual filesystem sandbox + managed state |
| Best used for | Data processing, simple RAG, text transformations | Quick deployment of tool-using assistant apps | Custom enterprise bots, complex multi-agent architectures, custom recovery states | Highly autonomous, long-running background tasks (autonomous research/coding bots) |

***

## Chain vs. Graph

### The Chain Paradigm (LangChain & LCEL) — The Assembly Line

Raw material (user query) enters one end, travels down a single conveyor belt through fixed machines (Prompts, LLM, Parser, API calls), and exits as a finished product:

```
[ User Input ] → [ Prompt Template ] → [ LLM Model ] → [ Output Parser ] → [ Final JSON ]
```

**Architectural details:**

- **Directed Acyclic Graph (DAG)** — strictly one-way; cannot loop back. If Step 3 errors or needs re-evaluation, a chain cannot "go back to Step 1 and try again."
- **Implicit data flow** — data passes directly from one component's output into the next's input via `|`; there's no shared "memory notebook" — each step only knows what the immediately preceding step handed it.
- **When it fails** — an autonomous coding assistant built with LCEL alone fails, because coding requires testing code, reading errors, and looping back to rewrite until it passes.

### The Graph Paradigm (LangGraph) — Mission Control

A shared whiteboard (**State**) sits in the center of the room. Multiple specialists (**Nodes**) pass the project folder back and forth based on strict or dynamic rules (**Edges/Conditional Edges**), modifying the whiteboard as they go:

```
           ┌───────────────┐
           │     START     │
           └───────┬───────┘
                   ▼
           ┌───────────────┐
     ┌────>│  Supervisor   ├────────┐
     │     └───────┬───────┘        │
     │             │                ▼
     │             │        ┌───────────────┐
     │             ▼        │ Specialist B  │
     │     ┌───────────────┐│   (Writer)    │
     │     │ Specialist A  │└───────┬───────┘
     │     │  (Researcher) │        │
     │     └───────┬───────┘        │
     │             ▼                │
     └─────────────┴────────────────┴──────> [ END ]
```

**Architectural details:**

- **Cyclic workflows (loops)** — nodes can route back to earlier nodes or themselves (e.g., an agent hits an API timeout, updates a retry counter in state, and tries again).
- **Explicit state and reducers** — every node reads from and writes to a central state (Pydantic or `TypedDict`); **Reducers** control how data is written when parallel nodes update state simultaneously — "last write wins" (overwrite) vs. append (e.g., adding a new message to a list).
- **Durable state checkpointing** — since graphs execute step-by-step through a state machine, the framework snapshots the entire environment (state, variables, execution path) after every node transaction and saves it to a database (PostgreSQL, SQLite).

***

## Feature Visualizer: Execution Primitives Compared

| Capability | LangChain (Chains / LCEL) | LangGraph (StateGraph) |
|---|---|---|
| Error handling | Fallbacks — if Model A fails/drops connection, route to backup Model B | Retry loops — if tool output fails validation, loop back to the LLM node with the error log to self-correct |
| Parallel execution | `RunnableParallel` — runs independent API calls concurrently, joins them linearly | Parallel fan-out/fan-in (`Send`) — spawns multiple independent specialist nodes dynamically based on input size, then collapses them back together |
| Human interactivity | Blocking — entire pipeline halts synchronously while waiting for a network payload | Interrupts — graph saves state to a checkpointer, shuts down execution to save compute, resumes days later when a webhook receives human approval |

***

## Tip

1. Write data extractors, prompt structures, and vector retrievers as lightweight **LCEL Chains**.
2. Package those chains and place them inside **LangGraph Nodes**.
3. Let **LangGraph** orchestrate business logic, loops, human approvals, and database error checks.