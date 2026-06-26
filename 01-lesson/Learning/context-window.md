
#  Context Windows in LLMs 

***

## 🔑 The Core Idea

> **A context window is the "working memory" of an LLM** — the total amount of text (measured in tokens) the model can see and reference at one time when generating a response.

Think of it this way:
- **Training data** = the model's long-term memory (everything it ever learned)
- **Context window** = the model's short-term/working memory (what it's actively thinking about right now)

Whatever is **outside** the context window — the model simply **cannot access** it. It's as if it never existed.

***

##  What Goes Inside a Context Window?

The context window holds **everything in a single API call or conversation turn** :

```
┌──────────────────────────────────────────┐
│           CONTEXT WINDOW                 │
│                                          │
│  System Prompt / Instructions            │
│  + All Previous Conversation History     │
│  + Current User Message                  │
│  + Documents / Code / Data Passed In     │
│  + Model's Output (being generated)      │
│                                          │
└──────────────────────────────────────────┘
         Total = must fit within token limit
```

- Every new turn → previous turns are preserved and **accumulate** in the window 
- Growth is **linear** — each turn adds more tokens to the running total 
- The model's generated response also **counts toward the token limit** 

***

##  Context Window Sizes — Real Models

| Model | Context Window |
|---|---|
| GPT-3 | 2,000 tokens |
| GPT-3.5 Turbo | 16,385 tokens |
| GPT-4 Turbo | 128,000 tokens |
| Claude Sonnet 4.5 | 200,000 tokens |
| Claude Opus 4.6 / Sonnet 4.6 | **1,000,000 tokens** |
| Claude Fable 5 / Mythos 5 | **1,000,000 tokens** |


**As a rough rule of thumb:**
- ~1 token ≈ 0.75 words (English)
- 1,000 tokens ≈ 750 words ≈ ~1.5 pages of text
- 100,000 tokens ≈ a full novel
- 1,000,000 tokens ≈ several large books combined

***

## 🔁 How the Context Window Grows Turn by Turn

```
Turn 1:
[System Prompt] + [User Message 1]  →  Model generates Response 1
                                        Context used: ~500 tokens

Turn 2:
[System Prompt] + [User 1] + [Response 1] + [User Message 2]  →  Response 2
                                        Context used: ~1100 tokens

Turn 3:
[Everything above] + [Response 2] + [User Message 3]  →  Response 3
                                        Context used: ~1800 tokens
...keeps growing...
```

Eventually → you hit the **context window limit** 

**What happens when you exceed the limit?**
- On Claude 4.5+: the API accepts the request, generates until the limit, then stops with reason `"model_context_window_exceeded"` 
- On older models: the API returns a **validation error** 
- On chat UIs (like claude.ai): uses a rolling **FIFO (First In, First Out)** system — oldest messages get dropped first 

***

## ⚠️ Bigger Context ≠ Always Better — "Context Rot"

This is a critical concept many beginners miss.

> As token count grows, **accuracy and recall degrade** — this is called **"Context Rot"** 

### The "Lost in the Middle" Problem

Research shows LLMs pay more attention to the **beginning and end** of the context window, and tend to **ignore information buried in the middle**: 

```
ATTENTION DISTRIBUTION IN CONTEXT WINDOW:

Start ████████████  ← High attention (strong recall)
 ...
Middle ██            ← Low attention (often ignored!)
 ...
End   ████████████  ← High attention (strong recall)
```

**Practical implication:**
- Put your **most important instructions at the start** (system prompt)
- Put your **most critical data near the end** (just before the question)
- Avoid burying key info in the middle of long documents

***

## 🔧 Context Window Components (Claude API Specific)

### Input Tokens
Everything the model receives :
- System instructions
- Conversation history
- Documents, code, images passed in
- Tool/function definitions

### Output Tokens
The model's generated response — also counted :
- Claude models: up to **128K output tokens** per single request

### Extended Thinking (Claude-specific)
When Claude uses extended thinking (chain-of-thought reasoning) :
- Thinking tokens count toward the context window
- BUT — previous thinking blocks are **automatically stripped** from future turns (they don't pile up)
- So Claude's thinking doesn't eat up your context window over a long conversation

***

## 🛠️ Managing Context — Key Strategies

### 1. Compaction (Server-Side)
- Claude automatically **summarizes earlier parts** of a long conversation
- Frees up space without losing all context
- Available on Claude Fable 5, Opus 4.6+, Sonnet 4.6 
- Best for: long-running agents, chatbots, multi-turn workflows

### 2. Tool Result Clearing
- In agentic workflows, old tool call results can be **cleared** from history
- Only keep the results that are still relevant 

### 3. Token Counting Before Sending
- Use Claude's **token counting API** to estimate usage before sending messages
- Prevent overflow errors proactively 

### 4. Prompt Engineering for Context Efficiency
| Strategy | What to Do |
|---|---|
| **Prune noise** | Remove unnecessary content from history |
| **Summarize** | Replace long past exchanges with a brief summary |
| **Structure** | Use Markdown/XML to help model focus its "spotlight" |
| **Echo key terms** | Repeat important concepts near the end of prompts |
| **Position matters** | Important info → start or end, never middle |


***

## 🧩 Context Awareness (Claude Sonnet 4.5/4.6, Haiku 4.5)

Some Claude models have a feature called **Context Awareness** — the model can track how many tokens it has used and how many remain :

```xml
<!-- Claude receives this at conversation start -->
<budget:token_budget>1000000</budget:token_budget>

<!-- After each tool call, Claude gets an update -->
<system_warning>Token usage: 35000/1000000; 965000 remaining</system_warning>
```

**Why this matters:**
- Claude can pace itself and not waste tokens
- Like giving a developer a countdown timer while coding
- Prevents running out of context mid-task 

***

## 🔗 Context Window vs. Attention — The Relationship

| | Context Window | Attention |
|---|---|---|
| **What it is** | Max token capacity | Mechanism to focus on relevant tokens |
| **Scope** | Sets the outer boundary | Works **within** the context window |
| **Limit** | Hard token count limit | Can't attend to tokens outside the window |
| **Analogy** | Size of your desk | Where you choose to look on the desk |


> No matter how good attention is — it **cannot attend to tokens outside the context window**. The window defines the absolute boundary.

***

## 📊 Why Context Windows Matter for Real Applications

| Use Case | Why Context Window Is Critical |
|---|---|
| **Long conversations** | History accumulates → runs out of space |
| **Document summarization** | Whole doc must fit in context |
| **Code review** | Large codebases exceed limits |
| **RAG systems** | Retrieved chunks + query must fit together |
| **Agents/Automation** | Multi-step tasks accumulate many tool results |


***

## ⚡ Must-Remember Points

1. **Context window = working memory** — not training memory
2. **Everything counts** — system prompt, history, documents, your question, model's answer
3. **Token limit is hard** — exceed it and content gets dropped or errors occur
4. **Bigger is not always better** — Context Rot and the "Lost in the Middle" problem are real
5. **Start and End = hot zones** — Middle = danger zone for important info
6. **Managing context is a skill** — especially critical for RAG, agents, and long apps
7. **Claude's 1M token window** = ~750,000 words — but you still need to manage it wisely 

***

##   Bridge to RAG

Here's **why context windows directly lead to RAG**:

```
Problem:
  Your knowledge base = 10 million tokens
  Context window      =      200K tokens
  → You CANNOT fit everything in!

RAG Solution:
  → Search the knowledge base for only the RELEVANT chunks
  → Inject just those chunks into the context window
  → Ask the model to answer using only that focused context
```

> **RAG exists specifically because context windows are limited.** Instead of fitting everything in, you retrieve only what's needed — making context windows efficient and accurate.
