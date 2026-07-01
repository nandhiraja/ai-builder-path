## AI-powered customer support assistant

```py

"""
ASSIGNMENT 1 — PROMPT OPTIMIZATION LAB
========================================

ANALYSIS: WHAT'S LACKING IN THE BASIC PROMPT
----------------------------------------------
Original prompt: "You are a helpful assistant. Answer the user's question 
about their billing issue."

    Issues identified:
    1. No defined role/specialization -> model doesn't know it's a billing expert
    2. No policy grounding -> risk of hallucinating fees, dates, or exceptions
    3. No tone/empathy guidance -> responses feel robotic or inconsistent
    4. No response structure -> answers vary wildly in length and format
    5. No instruction to ask for missing details -> guesses instead of clarifying
    6. No constraints -> can go off-topic (e.g. offering unrelated cancellations)
    This results in generic, incomplete, or inconsistent customer support answers.
"""

COMPANY_POLICY = """
        CloudSync Billing Policy
        - Refund Policy: Full refund within 7 days of purchase. Duplicate charges 
          are fully refundable regardless of the 7-day window.
        - Late Payment Policy: Invoices due within 15 days; 10% late fee applies after.
        - Cancellation Policy: Cancelling stops future billing immediately; current 
          cycle charges are non-refundable.
        - Incorrect Charges Policy: Report within 30 days; investigated in 3-5 
          business days; verified errors refunded within 7 business days.
        - Support: billing@cloudsync.com, Mon-Fri 9AM-6PM IST
    """


def basic_prompt(company_policy: str, user_query: str) -> str:
    return f"You are a helpful assistant. Answer the user's question about their billing issue.\n\nQuestion: {user_query}"


def refined_prompt(company_policy: str, user_query: str) -> str:
    return f"""
        ### ROLE
        You are a professional AI Billing Support Assistant for CloudSync, a SaaS company.

        ### CONTEXT
        Company Billing Policy:
        {company_policy}

        ### OBJECTIVE
        Resolve the customer's billing concern accurately and warmly, using ONLY the policy above.

        ### CONSTRAINTS
        - Use ONLY the policy provided. Never invent fees, dates, discounts, or exceptions.
        - If details are missing, ask exactly ONE clarifying question.
        - Write like a real human agent: warm, concise, no repeated phrases, no meta-comments.
        - Never include placeholders like "[Your Name]".
        - Recommend Billing Support Team only if account-specific verification is truly needed.

        ### RESPONSE FORMAT (blend naturally, do not label parts)
        - Acknowledge the concern in one sentence.
        - State the relevant policy in plain language.
        - Give one clear next step.
        - Ask a clarifying question only if necessary.

        ### CUSTOMER QUESTION
        {user_query}

        ### RESPONSE:
        """


def cot_prompt(company_policy: str, user_query: str) -> str:
    return f"""
        ### ROLE
        You are a warm, experienced SaaS Billing Support Assistant for CloudSync.

        ### CONTEXT
        Company Billing Policy:
        {company_policy}

        ### REASONING INSTRUCTIONS (internal only — never shown to the customer)
        Silently think through:
        1. Billing category (Duplicate Charge, Refund, Late Fee, Cancellation, Incorrect Invoice, Other)
        2. Which exact policy clause applies
        3. Is there enough info, or is one clarifying detail needed?
        4. Does this need human escalation?
        Then write the final answer as a natural, friendly reply.

        ### OUTPUT RULES
        - Never print "Step 1", category names, or internal notes.
        - Never sound clinical or like a checklist.
        - Keep it short: 3-4 sentences max.
        - Ask only ONE question if information is missing.
        - Never invent details not in the policy.

        ### CUSTOMER QUESTION
        {user_query}

        ### FINAL RESPONSE:
        """


"""
SAMPLE RESPONSES (generated via Ollama llama3.1:8b)
-----------------------------------------------------

Q1: Why was I charged twice?

BASIC: 
    "I'd be happy to help you with your billing issue. According to our 
    Refund Policy, duplicate charges are fully refundable regardless of the 
    7-day window... Could you please provide me with your CloudSync account 
    email address... Are you experiencing any issues with your current 
    subscription or would you like to cancel it altogether?"

REFINED: 
    "We're sorry to hear you were charged twice. According to our 
    Refund Policy, duplicate charges are fully refundable regardless of the 
    7-day window, so we can assist with correcting this for you right away. 
    Can you please provide me with your subscription plan and the dates of 
    the two invoices in question?"

CHAIN OF THOUGHT: 
    "That's an easy one! According to our Refund Policy, 
    duplicate charges are fully refundable regardless of when they occurred. 
    We'll go ahead and process a full refund for the extra charge you 
    received. Would you like me to assist with cancelling any future payments 
    that may have been mistakenly charged?"

[Q2-Q5 follow same pattern — see attached output.txt for full samples 
covering: refund eligibility, late fees, cancellation billing errors, 
and incorrect invoice disputes]
"""


"""
EVALUATION & CONCLUSION
--------------------------
Independent scoring by two LLM (Gemini, ChatGPT) across all 5 
test questions:

                    Basic    Refined    CoT
    Gemini (/5)     3.40     4.78       3.84
    ChatGPT (/10)   7.10     9.00       8.10

WINNER: Refined Prompt

CONCLUSION: 

Which Prompt Worked Best and Why?

The Basic Prompt produced natural and conversational responses because the model relied on its pre-trained knowledge. However, the responses were inconsistent and occasionally introduced information that was not present in the provided billing policy, making it less reliable for production use.

The Refined Prompt delivered the best overall performance. It consistently followed the billing policy, maintained a professional and friendly tone, asked only one relevant clarification question when necessary, and generated clear, structured responses. The added role definition, context, constraints, and response guidelines significantly improved both the quality and consistency of the answers.

The Chain-of-Thought (CoT) Prompt performed well for more complex scenarios such as refund eligibility, late fees, and incorrect charges. By encouraging the model to analyze the problem internally before responding, it produced more logical and complete answers. However, the local Ollama model occasionally inferred details that were not explicitly stated in the billing policy, demonstrating that prompt engineering improves reasoning but cannot completely eliminate model hallucinations.

Overall, the Refined Prompt achieved the best balance between response quality, consistency, and policy compliance, making it the most suitable choice for a real-world AI-powered customer support assistant.

"""
``` 