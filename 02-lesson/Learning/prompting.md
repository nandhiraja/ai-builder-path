#  Prompting Techniques 

***

## 1. What is Prompt Engineering?

Prompt engineering is the skill of **designing inputs (prompts)** for AI models to get the most accurate, useful, and relevant responses. It's not just writing questions — it includes understanding how LLMs work, what they can and cannot do, and how to structure instructions clearly.

**Why it matters:**
- Better prompts = better, faster answers
- Saves time and cost (fewer retries)
- Reduces hallucination and irrelevant output
- Helps AI follow instructions precisely

***

## 2. The CLEAR Framework

> **C — Concise · L — Logical · E — Explicit · A — Adaptive · R — Reflective**

***

### C — Concise
Be **short, direct, and specific.** Remove all words that don't add meaning.

- Use **declarative sentences** for context
- Use **imperative sentences** for commands
- Every word should earn its place

| ❌ Vague | ✅ Clear |
|---|---|
| "Write something about science" | "Write a 300-word essay on ethical implications of genetic engineering in humans" |
| "Tell me about dogs" | "List 10 interesting facts about Golden Retrievers" |

***

### L — Logical
Structure your prompt in **clear, ordered steps.** AI rewards logical flow over conversational rambling.

- Break multi-part requests into numbered steps
- Put the most important instruction first

| ❌ Messy | ✅ Structured |
|---|---|
| "Write a speech about renewable energy and include carbon stats" | "Step 1: Write a 5-minute speech about renewable energy. Step 2: Include at least 2 carbon emission statistics to support the argument." |

***

### E — Explicit
**Never assume** the AI knows what you want. Say everything out loud — like explaining to someone with zero context.

> 💡 *"Imagine explaining to the world's most knowledgeable two-year-old."*

- Include format, length, audience, tone
- Provide sample output when possible
- Specify what to include AND what to exclude

| ❌ Implicit | ✅ Explicit |
|---|---|
| "What's Georgetown University like?" | "Give me a concise summary of the top 3 strengths and top 2 weaknesses of Georgetown University for an undergraduate applicant." |

***

### A — Adaptive
**Iterate.** Don't stop at the first response. Use the AI's output to refine your next prompt.

- Pick keywords from the AI's answer and use them in follow-up prompts
- Tell the AI where it went wrong
- Try different angles if the answer is incomplete

**Example Iteration:**
```
Round 1 → "Why doesn't Georgetown have a Metro station?"
AI mentions: "geological obstacles"

Round 2 → "What are the geological obstacles and engineering
            challenges of building a Metro in Georgetown?"
→ Much deeper, more specific answer ✅
```

***

### R — Reflective
After every session, **pause and review:**

- Was the prompt clear enough?
- Did the AI misunderstand anything?
- What follow-up worked best?
- What would I do differently next time?

> 💡 Prompting is a skill. Small improvements every session add up over time.

Also ask about the output:
- Does it make sense?
- Is it based on facts or hallucinated?
- Are there missing perspectives?
- Is the information current?

***

## 3. Chain-of-Thought (CoT) Prompting

### What is it?
CoT prompting guides the AI to **show its reasoning step by step** before giving a final answer — instead of jumping straight to the conclusion.

> Instead of: *"What's the answer?"*
> You ask: *"Walk me through how to solve this step by step."*

***

### Why Does it Work?
- Reveals the model's thinking (you can catch errors early)
- Breaks complex problems into smaller, manageable parts
- Ensures no logical step is skipped
- Dramatically improves accuracy on math, logic, and multi-step tasks

> ⚠️ CoT works best with **larger, more capable models** (GPT-4o, Claude Sonnet). Smaller models may still struggle.

***

### Type 1 — Zero-Shot CoT
Just add one magic phrase to any prompt. No examples needed.

**Magic phrase:**
```
Let's think step by step.
```

**Without CoT:**
```
Prompt: I bought 10 apples, gave 2 to my neighbor, 2 to a repairman,
        bought 5 more, and ate 1. How many do I have?
Output: 11 ❌ (Wrong)
```

**With Zero-Shot CoT:**
```
Prompt: ...same question... Let's think step by step.

Output:
- Started with 10
- Gave away 2 + 2 = 4 → 6 remaining
- Bought 5 more → 11
- Ate 1 → 10 apples ✅
```

***

### Type 2 — Few-Shot CoT
Show **1–5 worked examples with reasoning steps visible**, then ask your real question. The model copies the reasoning pattern.

**Example prompt:**
```
Q: The odd numbers in this group add up to an even number:
   4, 8, 9, 15, 12, 2, 1.
A: The odd numbers are 9, 15, 1. Their sum = 25. 25 is odd. Answer: False.

Q: The odd numbers in this group add up to an even number:
   15, 32, 5, 13, 82, 7, 1.
A:
```

**Output:**
```
The odd numbers are 15, 5, 13, 7, 1. Their sum = 41. 41 is odd. Answer: False. ✅
```

***

### Type 3 — Auto-CoT
Automatically generates reasoning examples — no manual effort needed.

**Two stages:**
1. **Cluster** similar questions together
2. **Auto-generate** one step-by-step example per cluster using Zero-Shot CoT

**Rules for good auto-generated examples:**
- Question length: ~60 tokens
- Reasoning steps: ~5 steps
- Must be simple to avoid injecting wrong reasoning

***

### Real Example — CoT in Action

**Problem:** A store gives 50% off the cheapest item when you buy 3.
You buy items for ₹85, ₹40, and ₹55. Total?

```
Step 1: Find the cheapest item → ₹40
Step 2: 50% off ₹40 = ₹20 discount
Step 3: Total without discount = ₹85 + ₹40 + ₹55 = ₹180
Step 4: Final total = ₹180 - ₹20 = ₹160 ✅
```

Without CoT, the model might apply the discount to the wrong item.

***

### When to Use CoT

| ✅ Use CoT | ❌ Skip CoT |
|---|---|
| Math & calculations | Simple factual questions |
| Multi-step logic | Single-step lookups |
| Code with complex constraints | Creative writing |
| Workflow / process planning | Short definitions |
| Common sense reasoning tasks | Straightforward Q&A |

***

## 4. Quick Cheat Sheet

| Technique | One-Line Summary | Key Phrase |
|---|---|---|
| **Concise** | Remove all vague words | Be specific |
| **Logical** | Structure in steps | "First… Then… Finally…" |
| **Explicit** | Leave nothing assumed | "List exactly 5 items…" |
| **Adaptive** | Use AI output to improve prompt | Iterate every round |
| **Reflective** | Review every session | What worked? What didn't? |
| **Zero-Shot CoT** | Ask AI to reason aloud | `"Let's think step by step."` |
| **Few-Shot CoT** | Show examples with reasoning | Provide 1–5 solved samples |
| **Auto-CoT** | Auto-generate CoT examples | Cluster → Sample → Generate |

***

> 📌 **Golden Rule of Prompting:**
> *Be the person who writes the clearest, most specific instruction possible — then let the AI do the heavy lifting.*