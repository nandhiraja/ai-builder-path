

#  Tokens & Embeddings in LLMs

***

## 🔑 The Foundational Truth

> **AI does not read text. It only understands numbers.**
> Every word you type goes through a transformation pipeline before the model touches it.
> Understanding this pipeline = understanding how LLMs actually work.

***

## 🔁 The Complete Pipeline (Always Keep This in Mind)

```
You type:  "I love programming"
                    ↓
         Tokenizer (BPE Algorithm)
                    ↓
               Tokens
         ["I", "love", "program", "ming"]
                    ↓
              Token IDs
              [24, 891, 1832, 442]
                    ↓
          Embedding Layer (dense vectors)
     [[0.41, -0.88, ...], [0.73, 0.12, ...], ...]
                    ↓
       + Positional Encoding (adds order info)
                    ↓
         Transformer Layers (self-attention)
                    ↓
         Next Token Prediction (probabilities)
                    ↓
          Detokenizer (joins tokens back)
                    ↓
    Output: "I love programming because it is creative."
```

***

# Stage 1 — Raw Text Input

- When you type `"I love programming"`, the AI first receives it as a **plain sequence of characters**
- It does NOT see three words — it sees a stream of characters: `I`, ` `, `l`, `o`, `v`, `e`, ` `, ...
- Humans naturally segment text into words — AI has to be explicitly taught how to segment

***

# Stage 2 — What is Tokenization?

**Definition:**
Tokenization is the process of splitting raw text into smaller meaningful units called **tokens**.

**A token can be:**
- A full word → `"love"` = 1 token
- A part of a word (subword) → `"programming"` = `["program", "ming"]`
- A single character → `"a"`
- Punctuation → `"."`, `"!"`, `","`
- A space + word → `" love"` (GPT tokenizers often include the space)
- An emoji → `"😊"`
- A number → `"9000"`

**Why NOT split by spaces?**

Suppose you split only by spaces:
```
"unbelievableness"   → 1 token  (fine)
"electroencephalography" → 1 token  (fine)
"antidisestablishmentarianism" → 1 token
```

If every possible word = its own token:
- Vocabulary would need **millions of entries**
- Rare words appear once in training → model never learns them well
- Different forms of the same word (`run`, `running`, `runner`) are treated as completely different

**Solution → Subword Tokenization (BPE)**

***

# Stage 3 — BPE: Byte Pair Encoding (Deep Dive)

## What is BPE?

BPE is the tokenization algorithm used by **GPT-2, GPT-3, GPT-4, LLaMA-2, RoBERTa**, and many others.

It learns a **vocabulary of common subword pieces** from training data by repeatedly merging the most frequent adjacent character pairs.

***

## Why Subwords?

Look at these related words:
```
playing  →  play + ing
played   →  play + ed
player   →  play + er
plays    →  play + s
```

Instead of storing 4 separate tokens, BPE stores:
```
play, ing, ed, er, s
```

This way:
- The vocabulary stays **compact**
- The model still understands the **root meaning** (`play`)
- Even **unseen words** can be broken into known pieces

***

## How BPE Learns — Step by Step

### Training Phase (happens before you use the model):

**Step 1:** Take a large corpus of training text. Split every word into individual characters.
```
low      →  l o w
lowest   →  l o w e s t
new      →  n e w
newest   →  n e w e s t
```

**Step 2:** Count every **adjacent pair** of symbols in the corpus:
```
Pair   Count
lo     4
ow     4
we     2
es     2
st     2
ne     2
ew     2
```

**Step 3:** Find the most frequent pair → **merge it** into a new token
```
Most frequent: "lo" (count = 4)
Merge "l" + "o" → "lo"
```

Updated corpus:
```
low     →  lo w
lowest  →  lo w e s t
new     →  n e w
newest  →  n e w e s t
```

**Step 4:** Count pairs again in updated corpus:
```
Pair   Count
low    2   ← "lo"+"w" now frequent
ow     2
we     2
...
```

**Step 5:** Merge next most frequent pair → `"low"`

**Repeat** this process thousands of times until you reach the **target vocabulary size**.

- GPT-2 vocabulary: **50,257 tokens**
- GPT-4 vocabulary: **~100,000 tokens**

### The result: a vocabulary of subword pieces
```
play, ing, ed, er, s, low, est, new, ...
```

***

## BPE in Action — Examples

**Example 1:**
```
"internationalization"
→ ["inter", "national", "ization"]
```

**Example 2:**
```
"I love programming"
→ ["I", " love", " program", "ming"]
```
*(Note: GPT-style tokenizers include the leading space as part of the token)*

**Example 3:**
```
"Hello!"
→ ["Hello", "!"]
```

**Example 4 — Rare word:**
```
"Nandhraja"  (a name the model never saw)
→ ["N", "and", "hr", "aja"]
```
→ BPE handles unknown words by falling back to smaller known pieces

***

## Why It's Called "Byte Pair Encoding"

Originally used in data compression:
- Find the most frequent pair of bytes in data
- Replace that pair with a single new symbol
- Repeat

NLP borrowed this idea and applied it to characters/subwords instead of raw bytes.

***

## Other Tokenization Methods (For Reference)

| Method | Used By | Key Idea |
|---|---|---|
| **BPE** | GPT-2/3/4, LLaMA | Merge most frequent adjacent pairs |
| **WordPiece** | BERT, DistilBERT | Similar to BPE but uses likelihood instead of frequency |
| **Unigram** | SentencePiece, T5 | Starts with large vocab, prunes unlikely tokens |
| **SentencePiece** | T5, mT5, ALBERT | Language-agnostic, treats spaces as characters |

> For most of your learning, **focus on BPE** — it's the most widely used.

***

# Stage 4 — Token IDs

After tokenization, every token is mapped to a **unique integer** from the vocabulary:

```
Vocabulary mapping:
"I"           →   24
" love"       →  891
" program"    → 1832
"ming"        →  442
```

So your input becomes:
```
"I love programming"  →  [24, 891, 1832, 442]
```

**Important to understand:**
- These IDs are just **labels/indices** — like a dictionary lookup
- `442 > 24` means NOTHING — "ming" is not "greater than" "I"
- IDs carry **zero semantic meaning** on their own
- That's exactly why we need embeddings next

***

# Stage 5 — Embedding Layer (Deep Dive)

## The Problem with Token IDs

If the model directly used IDs like `[24, 891, 1832, 442]`:
- ID `20 = Cat`, ID `21 = Dog` — does `21 > 20` mean Dog is better than Cat? **No.**
- There's no mathematical relationship between IDs
- The model can't compute anything meaningful with raw integers

## Solution: Convert IDs → Dense Vectors

Each Token ID is looked up in an **Embedding Matrix** and converted to a vector of real numbers.

```
" love" (ID: 891)  →  [0.41, -0.88, 1.62, 0.09, -0.33, 0.71, ...]
                                    (768 numbers for BERT-base)
```

This vector is the **embedding** — and it captures meaning.

***

## What is an Embedding Matrix?

- It's a large table: rows = every token in vocabulary, columns = embedding dimensions
- GPT-2: 50,257 tokens × 768 dimensions = ~38 million numbers just for embeddings
- When you input Token ID `891`, the model grabs **row 891** from this matrix

```
Embedding Matrix (simplified):
       dim1   dim2   dim3  ...  dim768
ID 0:  0.12  -0.44   0.91  ...   0.07
ID 1:  0.88   0.31  -0.22  ...   0.55
...
ID 891 (love): 0.41  -0.88   1.62  ...   0.09   ← this row is returned
...
```

***

## Why Vectors Capture Meaning

In a simplified 3D embedding space:
```
King     →  (5, 8, 7)
Queen    →  (5, 8, 6)   ← very close to King
Prince   →  (5, 5, 7)
Princess →  (5, 5, 6)

Mango    →  (1, 0, 2)   ← far from King/Queen
Pizza    →  (1, 0, 3)
```

Words with **similar meanings cluster together** in embedding space.

**Famous relationship:**
```
King - Man + Woman ≈ Queen
```
This arithmetic actually works in embedding space!

Real models use **768 to 8192+ dimensions**, encoding thousands of such relationships.

***

## Embedding Sizes by Model

| Model | Embedding Dimensions |
|---|---|
| BERT-base | 768 |
| BERT-large | 1024 |
| GPT-2 | 768 |
| GPT-3 | 12,288 |
| LLaMA-2 7B | 4,096 |
| LLaMA-2 70B | 8,192 |

More dimensions = more nuance the model can encode = more parameters to train.

***

## Types of Embeddings (Evolution)

### 1. Static Embeddings (older)
- Each word always has the **same vector**, regardless of context
- **Word2Vec** (Google, 2013) — neural network trained to predict surrounding words
- **GloVe** (Stanford) — based on word co-occurrence statistics
- **FastText** (Facebook) — Word2Vec but also uses character n-grams (handles misspellings)

**Problem:** The word `"bank"` has one vector — can't distinguish:
- `"river bank"` (geography)
- `"bank account"` (finance)

### 2. Contextual Embeddings (modern)
- Same word → **different vector** depending on surrounding context
- **ELMo** (2018) — used deep LSTM to produce context-aware embeddings
- **BERT** (Google, 2018) — bidirectional transformer; reads left AND right context
- **GPT series** (OpenAI) — unidirectional (left to right), but deeply contextual

**BERT example:**
```
"I went to the river bank."
"bank" → [0.23, -0.91, 0.55, ...]   ← geography vector

"I deposited money at the bank."
"bank" → [0.81, 0.44, -0.12, ...]   ← finance vector
```
Same word, completely different embedding — this is the power of contextual embeddings.

***

## Embeddings Are Part of Model Weights

- The Embedding Matrix is **not fixed** — it's learned during training
- Training adjusts embedding values to minimize prediction error
- After training, the embeddings encode rich semantic knowledge from billions of words
- When you load a pretrained model (like BERT), you're loading these trained embeddings

***

# Stage 6 — Positional Encoding

## The Problem

Look at these two sentences:
```
"Dog bites man"
"Man bites dog"
```

Same three tokens. Same embeddings. But completely different meanings.

Without positional info, the model sees them as **identical input**.

## The Solution: Add Position Information

Each token gets an additional vector that encodes **its position in the sequence**:

```
Token     Position   Token Embedding          Positional Embedding
"Dog"   →    1    →  [0.5, 0.3, ...]    +    [0.0, 1.0, 0.0, ...]
"bites" →    2    →  [0.2, -0.7, ...]   +    [0.84, 0.54, ...]
"man"   →    3    →  [0.9, 0.1, ...]    +    [0.91, -0.41, ...]
```

**Final input to transformer = Token Embedding + Positional Embedding**

## Types of Positional Encoding
| Type | Used By | How |
|---|---|---|
| **Sinusoidal** | Original Transformer, BERT | Fixed mathematical sin/cos functions |
| **Learned** | GPT-2 | Positional embeddings also trained |
| **RoPE** (Rotary) | LLaMA, GPT-NeoX | Encodes relative positions via rotation |
| **ALiBi** | Some models | Adds bias to attention scores based on distance |

***

# Stage 7 — Transformer Layers

Now the model has a vector for each token (embedding + position).

The **Transformer** processes these vectors through multiple layers, each asking:

> *"For each token, which other tokens in the sequence are relevant to understanding it?"*

**Self-Attention Example:**
```
"The animal didn't cross the road because it was too tired."
```
When processing `"it"` → self-attention figures out that `"it"` refers to `"animal"`, not `"road"`.

**What each layer does:**
- Layer 1 → learns basic syntax (noun, verb relationships)
- Middle layers → learns semantics (meaning, entity references)
- Final layers → task-specific features (what comes next, sentiment, etc.)

*(Self-attention is a full topic on its own — this is just the overview)*

***

# Stage 8 — Next Token Prediction

After processing all layers, the model outputs a **probability distribution** over the entire vocabulary for the next token:

```
Input: "I love"

Possible next tokens:
pizza      → 45%
coding     → 35%
music      → 15%
coffee     →  5%
[all other 50,000 tokens] → ~0%
```

One token is selected based on a **decoding strategy**:
- **Greedy** → always pick highest probability
- **Temperature sampling** → add randomness (creative outputs)
- **Top-K** → pick from top K most likely tokens
- **Top-P (nucleus)** → pick from tokens that together make up P% of probability

The selected token is **appended** to the input, and the entire process runs again to predict the next token.

> This is why LLMs generate text one token at a time — it's **autoregressive**.

***

# Stage 9 — Detokenization

After all tokens are generated:
```
Tokens: ["I", " love", " program", "ming", " because", " it", " is", " creative", "."]
```

The tokenizer **joins them back** into readable text:
```
"I love programming because it is creative."
```

Special rules apply (e.g., no space before punctuation, handle capitalization) — the detokenizer handles this automatically.

***

# 📊 The Full Pipeline Table

| Stage | What Happens | Input → Output |
|---|---|---|
| 1 | Raw Input | You type text |
| 2 | Tokenization | `"I love programming"` → `["I", "love", "program", "ming"]` |
| 3 | BPE Algorithm | Learned vocabulary of subword pieces |
| 4 | Token IDs | `["I", "love", "program", "ming"]` → `[24, 891, 1832, 442]` |
| 5 | Embedding Layer | IDs → Dense vectors (768–8192 dimensions each) |
| 6 | Positional Encoding | Adds position index to each vector |
| 7 | Transformer | Processes vectors with self-attention across all layers |
| 8 | Prediction | Outputs probability for next token |
| 9 | Detokenization | Token sequence → readable text |

***

# ⚡ Must-Remember Points (Exam/Revision Ready)

1. **Characters** → the raw bytes you type
2. **Tokens** → subword pieces created by the tokenizer (not always full words)
3. **BPE** → repeatedly merges the most frequent adjacent pairs to build vocabulary
4. **Token IDs** → integer labels (indices), carry no meaning by themselves
5. **Embeddings** → dense vectors that encode semantic meaning; similar words = nearby vectors
6. **Embedding Matrix** → large lookup table; one row per token; trained with the model
7. **Static vs Contextual** → BERT/GPT give same word different vectors based on context
8. **Positional Encoding** → tells the model the order of tokens; added to embeddings
9. **Transformer** → uses all vectors + self-attention to build deep understanding
10. **Autoregressive** → LLMs generate **one token at a time**, not one word or sentence
11. **Detokenization** → tokens rejoined into human-readable text at the end

***
