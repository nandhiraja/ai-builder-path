
# Model Context Protocol (MCP)

Model Context Protocol (MCP), the universal standard for connecting AI models to external tools, data, and applications — donated by Anthropic to the Linux Foundation and adopted across the industry by Anthropic, OpenAI, Google, and Microsoft.

## The Big Picture

If LangChain and LangGraph are the engines that control an agent's internal thoughts, **MCP is the USB-C port** that lets that agent instantly plug into external data, apps, and files — without writing custom API integration code for every single combination.

```
┌──────────────────────┐        ┌─────────────────────┐
│  Agent Brain Layer   │        │  Outside World      │
│  (LangGraph / Claude/│  MCP   │  (DBs, APIs, Files, │
│   GPT / Gemini)      │◄──────►│   Slack, GitHub...) │
└──────────────────────┘        └─────────────────────┘

```

### The Problem MCP Solved: The $N \times M$ Bottleneck

Before MCP, connecting AI models to external tools required a separate custom connector for every single model-tool pair.

* **Old Way:** 3 models $\times$ 3 tools = **9 separate integrations** to build and maintain.
* **The Downside:** A new model release meant completely rewriting tool logic to match that vendor's unique, proprietary function-calling API. There was no reusability; a Slack connector built for Claude couldn't be reused for GPT or Gemini without heavy rework.

### The MCP Fix

```
        Claude      GPT-5       Gemini
GitHub   ─────────── one MCP server ───────────►
Postgres ─────────── one MCP server ───────────►
Slack    ─────────── one MCP server ───────────►

```

You write **one** MCP server for your database or tool. Because every major LLM provider natively speaks MCP, that server instantly works across Claude Desktop, Cursor, OpenAI Agents SDK, and custom LangGraph setups with zero extra integration code.

---

## The Three Core Roles in MCP

MCP architecture strictly splits into three distinct layers:

```
┌────────────────────────────┐
│   MCP HOST (The Brain)     │   e.g., Claude Desktop, Cursor,
│                            │   or your custom LangGraph agent
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│  MCP CLIENT (The Cable)    │   Lives inside the host,
│                            │   manages the connection pipeline
└──────────────┬─────────────┘
               │  JSON-RPC 2.0
               │  (STDIO or Streamable HTTP)
               ▼
┌────────────────────────────┐
│  MCP SERVER (The Bridge)   │   Exposes Tools, Resources,
│                            │   and Prompts
└────────────────────────────┘

```

| Role | Description |
| --- | --- |
| **Host** | The orchestration layer running the LLM. Manages security, asks the user for permission before running dangerous tools, and decides when to talk to a server. |
| **Client** | A lightweight connector running inside the host that establishes and manages the bridge to the server. |
| **Server** | A separate process (local or remote) that exposes your actual code, APIs, or databases to the client. |

> 💡 **Key Insight:** The Host and Client always live together (inside Claude Desktop, Cursor, or your custom agent app); the Server is the independent piece you build once and reuse everywhere.

---

## The 3 Primitives a Server Exposes

When building an MCP server, you describe your system to the AI using exactly three concepts:

### 1. Resources (Passive Data) 📖

Read-only files or data points the LLM can pull for context. Reading a resource never changes anything in the real world.

* *Examples:* Reading a live log file (`file://logs/error.log`), checking a database schema (`sqlite://schema`), or fetching a company policy markdown document.

### 2. Tools (Active Actions) 🛠️

Executable functions or API endpoints the LLM can explicitly call to take an action. Tools accept arguments, execute code, and return results.

* *Examples:* Running an SQL write query, sending a Slack message, or triggering a production code build.

### 3. Prompts (Templates) 📝

Pre-packaged prompt structures or slash-commands built directly into the server that help users interact with that specific toolset effectively.

* *Example:* A `/debug-logs` prompt template that automatically configures the LLM with the right instructions to inspect an error resource.

---

## How It Works Under the Hood: The Handshake

Client and server communicate using **JSON-RPC 2.0**, a lightweight remote-procedure-call protocol.

```
   HOST/CLIENT                          SERVER
       │                                   │
       │  1. Discovery                     │
       │  "What can you do?"               │
       │──────────────────────────────────►│
       │                                   │
       │   list of tools/resources/prompts │
       │   + descriptions + JSON Schemas   │
       │◄──────────────────────────────────│
       │                                   │
       │  2. Reasoning (inside the LLM)    │
       │  "User asked about products in    │
       │   the DB → use tool 'run_query'"  │
       │                                   │
       │  3. Execution                     │
       │  { tool: "run_query",             │
       │    args: { sql_string: "..." } }  │
       │──────────────────────────────────►│
       │                                   │
       │        query results              │
       │◄──────────────────────────────────│
       │                                   │
       │  4. LLM formats final answer      │
       │  for the user                     │

```

1. **Discovery:** The server sends the client a list of its tools, resources, and prompts, each with rich natural-language descriptions and full JSON Schemas explaining required arguments.
2. **Reasoning:** The LLM reads those descriptions and matches them to the user's intent (e.g., realizing the server exposes a tool called `run_query` that takes a `sql_string`).
3. **Execution:** The LLM generates the exact arguments; the client passes the structured request to the server over the transport layer; the server executes the underlying code and returns results to the host.

---

## The Modern State of MCP

MCP has matured into a production-grade enterprise standard featuring several key infrastructure upgrades:

### Stateless Protocol Layer

* Session IDs and complex handshakes at connection time are eliminated.
* Versioning and capability info now travel natively inside metadata on individual requests.
* **Result:** Applications scale horizontally across multiple container instances without needing complex sticky load balancing.

### Transport Protocols

* **Local (STDIO):** The host spins up the server as a background subprocess and communicates over standard input/output with zero network surface exposed.
* **Remote (Streamable HTTP):** For cloud deployments, allowing servers to live independently as microservices and stream responses over the network.

### MCP Apps & Rich UI

Modern MCP servers aren't limited to raw text. They can serve rich, sandboxed HTML user interfaces directly into host applications — letting an agent render interactive charts, forms, or UI controls mid-chat instead of returning markdown tables.

### Sampling & Elicitation Loops

Servers can actively participate in the conversation loop rather than just responding passively:

* **Sampling:** A server can pause mid-task and ask the LLM itself for intermediate reasoning or secondary opinions before continuing execution.
* **Elicitation:** A server can trigger a flow that securely redirects the user to an external OAuth URL for login credentials, suspending the graph or pipeline and cleanly resuming execution once authentication completes.

---

## Strategic Architecture Breakdown

| Without MCP | With MCP |
| --- | --- |
| Custom connector per model-tool pair. | One server, works with any MCP-compatible model. |
| Rewrite integration layers when switching LLM providers. | Swap models freely — your tool interfaces remain unchanged. |
| Tool logic tightly coupled to vendor's proprietary function-calling format. | Tool logic standardized via JSON Schema, completely model-agnostic. |
| Hard to scale or distribute a team's internal tool ecosystem. | Plug-and-play tool ecosystem across hosts (Claude Desktop, Cursor, LangGraph agents). |

> 📌 **Practical Takeaway:** If you're building agents with LangGraph, exposing your PostgreSQL database, internal APIs, or log monitors as an **MCP Server** means any current or future LLM-based host can use them immediately. You build your business logic once, and it stays decoupled from changing AI model frameworks.