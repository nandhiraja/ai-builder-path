import asyncio
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools.hr_rag import build_hr_retriever
from tools.web_search import build_web_search_tool
from tools.google_docs_mcp import load_google_docs_mcp_tools


SYSTEM_PROMPT = """
            You are Presidio's Internal Research Agent.

            Tool rules:
            1. Use Google Docs MCP tools for internal insurance, team notes, customer feedback, and business documents.
            2. Use search_hr_policies for HR policy, compliance, employee policy, and AI data handling questions.
            3. Use industry_web_search only for external benchmarks, public trends, or current regulatory updates.
            4. If the query needs both internal and external context, use multiple tools.
            5. Do not invent facts. If evidence is weak or missing, say so clearly.

            Response format:
            - Summary
            - Key findings
            - Sources used
            - Gaps or risks
            """

async def build_agent():
    load_dotenv()

    llm = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0,
        max_retries=2
    )

    hr_tool = build_hr_retriever()
    web_tool = build_web_search_tool()
    
    try:
        mcp_tools = await load_google_docs_mcp_tools()
        tools = [hr_tool, web_tool] + mcp_tools
    except Exception as e:
        print(f"\n Warning: Could not connect to Google Docs MCP server ({e}).")
        print("Starting agent with only HR RAG and Web Search tools...\n")
        tools = [hr_tool, web_tool]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent

async def main():
    agent = await build_agent()

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": query}]
        })

        final_message = result["messages"][-1].content
        print("\nFINAL ANSWER : ")
        print(final_message)

if __name__ == "__main__":
    asyncio.run(main())