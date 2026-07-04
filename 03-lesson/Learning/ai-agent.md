
# AI Agents

## 1. Core Definition

**Agentic systems** is the umbrella term. It splits into two architectures:

| Type | How it works | Who controls the path |
|---|---|---|
| **Workflow** | LLMs + tools run through fixed, predefined code paths | Developer |
| **Agent** | LLM decides its own steps dynamically, based on what it observes | The model itself |

**Simple analogy:** A workflow is a recipe — follow the exact steps every time. An agent is a chef — decides what to do next based on what's happening in the kitchen.

## 2. Golden Rule: Start Simple

- Don't default to building an agent. The simplest solution that works is the best solution.
- Often a single well-crafted LLM call with good retrieval and examples solves the problem — no framework, no loop, no agent needed.
- Agentic systems cost more (latency + money) and are harder to predict, so extra complexity must be *earned* by a real improvement in results.
- Add autonomy only when a task genuinely needs flexibility that a fixed workflow can't provide.

## 3. On Frameworks

- Frameworks (LangGraph, Claude Agent SDK, Rivet, Vellum, etc.) make it easier to call LLMs, define tools, and chain steps.
- Risk: they abstract away the actual prompts and responses, making debugging harder and encouraging unnecessary complexity.
- Best practice: understand what's happening under the hood, even if you use a framework. Many patterns can be built directly with a few lines of raw API calls.

## 4. The Building Block: Augmented LLM

Every agentic system — workflow or agent — is built from one core unit: an LLM enhanced with:

- **Retrieval** — pulling in relevant external knowledge
- **Tools** — calling functions/APIs to take real-world actions
- **Memory** — remembering context across steps or sessions

Modern LLMs can generate their own search queries, choose the right tool, and decide what to remember — so the main job of the developer is to design a clean, well-documented interface for these augmentations (this is where protocols like Anthropic's MCP — Model Context Protocol — help standardize tool integration).

## 5. The Five Workflow Patterns

These are fixed, developer-controlled structures — no dynamic decision-making by the model about *what steps* to take, only about *content* within each step.

| Pattern | What it does | Best used when |
|---|---|---|
| **1. Prompt Chaining** | Breaks a task into sequential steps, each LLM call builds on the last, with optional validation "gates" between steps | Task splits cleanly into fixed stages (e.g. outline → write → translate) |
| **2. Routing** | Classifies the input first, then sends it down a specialized path | Inputs fall into clear categories needing different handling (e.g. billing vs. technical support) |
| **3. Parallelization** | Runs multiple LLM calls at once — either splitting work (**sectioning**) or running the same task multiple times for consensus (**voting**) | Subtasks are independent, or multiple perspectives improve reliability (e.g. one model writes, another checks for safety issues) |
| **4. Orchestrator-Workers** | A central LLM dynamically breaks down a task and assigns pieces to worker LLMs, then merges results | Subtasks *can't* be predicted ahead of time — they depend on the specific input (e.g. a coding task touching an unknown number of files) |
| **5. Evaluator-Optimizer** | One LLM generates output, a second LLM critiques it, and the loop repeats until quality improves | Clear evaluation criteria exist and iterative feedback measurably helps (e.g. refining a translation through repeated critique) |

**Memory tip:** Chaining = a relay race. Routing = a triage desk. Parallelization = a team working simultaneously. Orchestrator-Workers = a manager assigning tasks on the fly. Evaluator-Optimizer = a writer and an editor going back and forth.

## 6. Full Agents (Autonomous Loop)

Agents appear once LLMs get reliable enough at reasoning, tool use, and error recovery to be trusted with an open-ended loop.

**How an agent operates:**
1. Receives a goal or command from a human
2. Plans its approach
3. Takes an action (usually a tool call)
4. Observes real "ground truth" feedback from the environment (tool result, code output, error message)
5. Adjusts its plan based on that feedback
6. Repeats until the goal is met or a stopping condition is hit (e.g. max iterations, human checkpoint)

**When to use an agent instead of a workflow:**
- The problem is open-ended
- The number of steps can't be known in advance
- A fixed path genuinely cannot be hardcoded

**The catch:** longer loops mean more chances for small errors to compound into big failures, so agents need:
- Sandboxed testing environments
- Strong guardrails (permission limits, timeouts, human review checkpoints)
- Careful monitoring, since you're trusting the model's judgment over many turns, not just one call

**Real-world examples:** coding agents that resolve GitHub issues across multiple files automatically; "computer use" agents that directly operate a computer's UI to complete tasks.

## 7. Combining Patterns

None of the above patterns are rigid rules — they're building blocks. Real systems often mix them (e.g. a router that sends complex cases to an orchestrator-worker setup, and simple cases to a single prompt chain). The only real principle: measure results and add complexity only when it demonstrably helps.

## 8. Three Principles for Effective Agents

1. **Simplicity** — keep the design as minimal as the task allows.
2. **Transparency** — make the agent's planning steps visible/loggable so its reasoning can be audited, not a black box.
3. **Agent-Computer Interface (ACI)** — design and document tools as carefully as you would a UI for a human; a confusing tool interface leads to a confused agent.

## 9. Where Agents Work Best in Practice

Two domains stand out because they combine conversation + real action + measurable success + human oversight:

- **Customer Support** — naturally conversational, tools can pull account/order data and take actions like refunds, and success is measurable (ticket resolved or not) — some companies even charge only for successful resolutions.
- **Coding Agents** — code correctness is objectively testable, so the agent can use test-run results as direct feedback to self-correct. Human review is still essential since passing tests doesn't guarantee the solution fits the bigger picture.

## 10. Designing Good Tools (Agent-Computer Interface)

Tool design deserves the same craftsmanship as prompt design.

**Format tips:**
- Give the model room to "think" before committing to a final answer/action.
- Use formats close to what the model has seen naturally in training data (plain markdown over rigid JSON, when possible).
- Avoid formats that force tedious manual work (e.g. counting exact line numbers, heavy string-escaping).

**Interface tips:**
- Write tool descriptions like documentation for a junior developer — clear names, clear parameters, clear examples.
- Test with real inputs, observe failure patterns, and iterate the tool design, not just the prompt.
- **"Poka-yoke" your tools** — design them so mistakes are structurally hard to make (e.g. requiring absolute file paths instead of relative ones prevents an entire class of errors — this fixed a real bug Anthropic hit while building their own coding agent).

## Quick Revision Summary

- Agentic systems = workflows (fixed path) + agents (dynamic path)
- Always start simple; add autonomy only when justified
- Core unit = augmented LLM (retrieval + tools + memory)
- 5 workflow patterns: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- Full agents = plan → act → observe → adjust → repeat, until done
- Best agent use cases = customer support & coding, both measurable + action-driven
- Good agents need: simplicity, transparency, and well-designed tools (ACI)