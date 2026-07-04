
# Memory for AI Agents 

## Core Idea

Memory is one of the most important capabilities being built into modern AI agents, and it enables **personalized, differentiated applications**. LangChain's key philosophy: **there is no one-size-fits-all memory solution** — memory must be application-specific, built around exactly what your app needs to remember.

Instead of offering a generic memory abstraction, LangChain provides **low-level building blocks** so developers can design memory that fits their own use case.

## Two Types of Memory

| Type | Scope | LangGraph Implementation |
|---|---|---|
| **Short-term memory** | Within a single conversation (a "thread") | Checkpoints |
| **Long-term memory** | Across multiple conversations/threads | Store |

- **Checkpoints** save the state of one specific conversation thread — this is standard conversation memory.
- **Store** is a newer concept that holds memory *across* threads, letting the agent learn from one conversation and apply that knowledge in a completely different, later conversation.

## Short-Term Memory Techniques

As a conversation goes back and forth, the message list keeps growing, so it needs to be managed:

- **Filtering messages** — the simplest approach, e.g. keep only the last 10 messages.
- **Token-based filtering** — trim based on total token count rather than message count.
- **Type-based filtering** — prioritize keeping human and AI messages, and drop less important ones like tool-call messages.
- **Summarization** — instead of just deleting old messages, call an LLM to summarize the earlier conversation and store that summary as an attribute in the agent's state, preserving context in a compressed form.

## Long-Term Memory: Two Update Strategies

### 1. In the Hot Path
- Memory is updated **as part of the live application logic**, during the actual conversation.
- **Pros:** Transparent (can be shown to the user in real time); updates are immediately available even if the user starts a new conversation right away.
- **Cons:** Adds latency to the response; makes application logic more complex since you must handle both the core task and the memory-update logic together.

### 2. In the Background
- A **separate process** updates memory outside the main conversation flow — could run instantly, or minutes/hours later.
- **Pros:** No added latency to the user-facing response; keeps core application logic cleanly separated from memory-update logic.
- **Cons:** Updates can't be easily shown to the user in real time; if a new conversation starts before the background job finishes, it may not have the latest memory. Also requires extra logic to decide **when** to trigger the background update.

## Shapes of Long-Term Memory

Long-term memory isn't just "raw text" — it can be structured in different ways depending on the use case:

### A. Instructions
- Stored as text and inserted directly into the **system prompt** to control how the agent behaves.
- Usually updated based on user feedback or interaction patterns.
- Example: In a tweet-writing app, if the user keeps removing emojis from suggestions, an LLM can synthesize that pattern and update the system prompt to say "don't use emojis."

### B. Profile
- A **single structured object** (dictionary/key-value pairs) representing facts about the user.
- Example: for a companion chatbot — name, age, friends, etc.
- The memory process extracts new facts from conversations and **updates** the existing profile (not just appends).
- This profile gets inserted into the system message for future conversations.

### C. Collection (List of Profiles/Objects)
- A **list of structured objects**, one level more complex than a single profile.
- Example: remembering a list of the user's favorite restaurants (each with name, location, type).
- Harder to manage because the LLM must decide whether to **add a new item, update an existing one, or delete one** — this requires more careful prompt engineering than a single profile.

## Summary Table

| Memory Shape | Structure | Example | Complexity |
|---|---|---|---|
| Instructions | Plain text in system prompt | "Don't use emojis" | Low |
| Profile | Single dictionary | Name, age, friends | Medium |
| Collection | List of dictionaries | List of favorite restaurants | High (add/update/delete logic needed) |

## Key Takeaways

- Memory splits into **short-term** (within one conversation) and **long-term** (across conversations).
- Short-term memory is managed mainly through **filtering** or **summarization** of the message history.
- Long-term memory can be updated **in the hot path** (real-time, more transparent, but adds latency) or **in the background** (faster response, cleaner code, but less immediately visible).
- Long-term memory can be stored as **instructions**, a **profile**, or a **collection** — increasing in complexity in that order.
- There is no universal memory solution — the right shape and update strategy depends entirely on what your specific agent needs to remember and how it needs to use that information.