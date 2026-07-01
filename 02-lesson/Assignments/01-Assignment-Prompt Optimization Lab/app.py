from company_data import COMPANY_POLICY, QUESTIONS
from prompts import basic_prompt, refined_prompt, cot_prompt
from ollama_client import OllamaClient


client = OllamaClient(model="llama3.1:8b")

output = []

for i, question in enumerate(QUESTIONS, start=1):

    print("=" * 100)
    print(f"QUESTION {i}")
    print("=" * 100)
    print(question)

    output.append("=" * 100)
    output.append(f"QUESTION {i}")
    output.append("=" * 100)
    output.append(question)

    # -----------------------------
    # Basic Prompt
    # -----------------------------
    prompt = basic_prompt(COMPANY_POLICY, question)
    response = client.chat(prompt)

    print("\nBASIC PROMPT")
    print("-" * 100)
    print(response)

    output.append("\nBASIC PROMPT")
    output.append("-" * 100)
    output.append(response)

    # -----------------------------
    # Refined Prompt
    # -----------------------------
    prompt = refined_prompt(COMPANY_POLICY, question)
    response = client.chat(prompt)

    print("\nREFINED PROMPT")
    print("-" * 100)
    print(response)

    output.append("\nREFINED PROMPT")
    output.append("-" * 100)
    output.append(response)

    # -----------------------------
    # Chain of Thought Prompt
    # -----------------------------
    prompt = cot_prompt(COMPANY_POLICY, question)
    response = client.chat(prompt)

    print("\nCHAIN OF THOUGHT")
    print("-" * 100)
    print(response)

    output.append("\nCHAIN OF THOUGHT")
    output.append("-" * 100)
    output.append(response)

    print("\n")

    output.append("\n\n")


with open("output.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(output))

print("=" * 100)
print("Completed Successfully")
print("Results saved to output.txt")
print("=" * 100)