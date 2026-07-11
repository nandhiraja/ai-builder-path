# LLM Engineering: Observability, Evaluation, and Guardrails

This covering LLM monitoring, tracing, trajectory evaluation, and safety guardrails
---

## Module 1: LangFuse for LLM Observability & Monitoring


### 1. The Production Problem

When moving large language model (LLM) applications out of development and into production, developers lose visibility over what happens inside complex agentic pipelines. Without tracing, it is impossible to debug multi-step calls, determine the exact location of high latency, calculate precise API token costs, or trace down prompt failures.

### 2. The Solution: LangFuse

LangFuse provides a fully open-source LLM engineering platform designed to record interactions, evaluate traces, and manage prompts seamlessly across diverse foundation models.

### 3. Architecture & Local Setup

LangFuse relies on a decoupled architecture containing an application frontend/API server and a persistent data layer:

* **API/Application Server:** Handles the collection of trace telemetry via SDKs.
* **Database:** A postgreSQL instance managing configuration, traces, sessions, and metrics.
* **Deployment:** Containerized through Docker Compose for persistent local execution on port `3000`.

#### Barebones Docker-Compose Structure

```yaml
version: '3.8'
services:
  langfuse-server:
    image: langfuse/langfuse:latest
    depends_on:
      - db
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
      - NEXTAUTH_SECRET=my_super_secret_string
      - SALT_SECRET=my_salt_secret_string

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:

```

### 4. Implementation Workflow (Native Python)

To trace raw LLM pipelines, developers employ native decorators to log every generation step safely:

```python
from langfuse.openai import openai  # Native drop-in client wrapper
from langfuse.decorators import observe

# Configure through standard environment keys
# LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST="http://localhost:3000"

@observe()
def classify_email(email_content: str):
    # Generates trace context natively under the hood
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Classify this: {email_content}"}]
    )
    return response

@observe()
def run_email_pipeline(email_content: str, session_id: str):
    # Overriding trace properties to bundle multiple execution steps together
    category = classify_email(email_content)
    return category

```

---

## Module 2: Practical LangChain Integration with LangFuse

### 1. The Architectural Problem

Manually instrumenting deep, nested routing structures like LangChain expressions or LangGraph graphs using explicit functions or decorators becomes tedious and error-prone.

### 2. The Solution: Global Callback Handlers

LangChain offers a native event callback system (`BaseCallbackHandler`). LangFuse exploits this hook system via `CallbackHandler`, allowing developers to intercept and capture nested agent traces automatically without changing core application workflows.

### 3. Step-by-Step Native Integration

Integration is accomplished using environment variables or explicit execution hooks.

#### Method A: Environment Configuration (Recommended)

By simply exposing system environment variables, the underlying LangChain framework intercepts actions and uploads trace telemetry directly to your server instance.

```bash
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_HOST="http://localhost:3000" # Or cloud URI

```

#### Method B: Explicit Dynamic Callbacks

For dynamic environments, pass an instantiated handler straight into your runner config block.

```python
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the LangFuse handler tracking system
langfuse_handler = CallbackHandler()

# 2. Setup your standard LLM step
model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Explain the following concept: {concept}")
chain = prompt | model

# 3. Inject the handler directly at runtime execution execution
response = chain.invoke(
    {"concept": "Model Context Protocol"},
    config={"callbacks": [langfuse_handler]}
)

```

---

## Module 3: Evaluating Agent Trajectories with AgentEvals


### 1. The Evaluation Deficit

Traditional LLM metrics focus entirely on validating the final textual response. However, an agent can often deliver a completely "correct" looking final response through inefficient, incorrect, or hallucinated execution steps. For instance, a scheduling agent might report that a meeting was booked while completely omitting the execution call to the actual booking database tool.

### 2. Trajectory Match vs. LLM-as-a-Judge

The open-source package `agent-evals` fixes this by providing two primary operational evaluation patterns:

1. **Trajectory Match:** Performs structured, deterministic validation over the sequence of tool-calling logs.
2. **LLM-as-a-Judge:** Utilizes an evaluation prompt instructions layer to score the progression logic and semantic efficiency of the step content.

### 3. Trajectory Match Modes

The `create_trajectory_match_evaluator` offers 4 specific operational modes to customize trajectory verification:

| Mode | Definition | Use Case Example |
| --- | --- | --- |
| **Strict** | Matches the exact set of expected tools in the precise order specified. | Enforcing a policy lookup tool *before* invoking an account action. |
| **Unordered** | Verifies the exact tool set is invoked, allowing arbitrary sequence ordering. | Fetching information across multiple independent internal products. |
| **Superset** | Ensures the required tools are present, ignoring arbitrary extra steps. | Relaxing execution rules while guaranteeing a specific notification tool runs. |
| **Subset** | Confirms all executed actions are bounded inside a strict reference set. | Enforcing efficiency bounds; preventing agents from making irrelevant tool calls. |

### 4. Enterprise Rigor: Multi-Iteration Runs

Because LLM engine decisions are inherently non-deterministic, isolated individual testing samples fail to reflect systemic stability. Best practices dictate executing multiple experimental repetitions inside LangSmith using custom data sets to accurately pinpoint failure rates and improve prompt design over time.

---

## Module 4: Guardrails with NeMo in LangChain


### 1. The Safety Challenge

Relying entirely on complex prompt structures to enforce safe boundaries increases prompt token bloat and allows malicious inputs to bypass constraints through prompt injection.

### 2. Solution: The Semantic Interceptor Pattern

NeMo Guardrails inserts a programmatic, vectorized verification layer between user inputs and the model. By utilizing specialized embeddings to run semantic similarity checks against a set of predefined examples, the system can instantly intercept unsafe queries and return deterministic fallback statements without contacting the core engine.

### 3. Structural Syntax: CoLang

Guardrail behavior is constructed inside specialized configuration profiles using `.co` files, governed by three core primitive structural blocks:

```colang
# 1. User Intent Block: Declares matching input utterances
define user express greeting
  "Hello bot"
  "Hi"
  "Hey there"

# 2. Bot Response Block: Defines exact response text 
define bot express greeting
  "Hello user! I provide secure banking support."

# 3. Flow Controller Block: Coordinates state logic 
define flow
  user express greeting
  bot express greeting

```

### 4. Advanced Control: Context Variables, Catch-Alls, and Custom Actions

NeMo Guardrails allows developers to handle complex conditional checks, direct unhandled traffic to underlying frameworks, or call external application features dynamically:

* **Dynamic Variables:** Inject runtime details using standard context structures (`$username`) to personalize responses dynamically.
* **Catch-All Rerouting:** Implement wildcard matches (`user ...`) to catch out-of-bounds inputs and redirect them to standard backend components, like a LangChain vector store engine.
* **Arbitrary Code Execution:** Use the `execute` keyword inside your runtime flows to invoke registered Python scripts or third-party database APIs on the fly.

#### Unified Guardrail Integration Workflow Example

```python
import asyncio
from nemoguardrails import RailsConfig, LLMRails

# 1. Outline CoLang Policy Engine Mechanics
colang_content = """
define user ask about competitor
  "What services does BankY offer?"
  "Is BankY better than you?"

define bot refuse competitor talk
  "I am only configured to discuss CatBank financial services."

define flow
  user ask about competitor
  bot refuse competitor talk

define user ask general question
  user ...

define flow
  user ask general question
  execute my_langchain_rag_action
"""

async def main():
    # 2. Instantiate and compile our security configuration policy
    config = RailsConfig.from_content(
        yaml_content="models: [{type: 'main', engine: 'openai', model: 'gpt-4o-mini'}]",
        colang_content=colang_content
    )
    rails = LLMRails(config)
    
    # 3. Register our internal production business logic action
    @rails.register_action(name="my_langchain_rag_action")
    async def run_rag():
        return {"content": "This is verified documentation returned out from the RAG store."}

    # 4. Process queries securely through the guardrail layer
    response = await rails.generate_async(prompt="Is BankY better than you?")
    print(response) # Triggers deterministic restriction policy safely

asyncio.run(main())

```
