import asyncio
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

@tool
def dummy_tool(x: str) -> str:
    """dummy"""
    return "dummy"

async def main():
    load_dotenv()
    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0, max_retries=2)
    tools = [dummy_tool]
    agent = create_agent(model=llm, tools=tools, system_prompt="you are helpful")
    print(type(agent))

if __name__ == "__main__":
    asyncio.run(main())
