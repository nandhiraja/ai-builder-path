import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

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

        Do not use emojis in your response. Keep the formatting clean, professional, and well-structured.
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
        print(f"\n[---] Warning: Could not connect to Google Docs MCP server ({e}).")
        print("Starting agent...\n")
        tools = [hr_tool, web_tool]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent


app = FastAPI(title="Presidio Internal Research Agent API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list

agent_instance = None

@app.on_event("startup")
async def startup_event():
    global agent_instance
    agent_instance = await build_agent()

@app.get("/")
async def read_index():

    return FileResponse("index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    global agent_instance
    if not agent_instance:
        agent_instance = await build_agent()
        
    result = await agent_instance.ainvoke({
        "messages": [{"role": "user", "content": request.query}]
    })
    
    final_message = result["messages"][-1].content
    
 
    sources = []
    for msg in result["messages"]:
        if getattr(msg, "type", None) == "tool":
            sources.append({
                "tool": getattr(msg, "name", "unknown_tool"),
                "content": str(msg.content)
            })
            
    return ChatResponse(
        answer=final_message,
        sources=sources
    )

if __name__ == "__main__":
    # Start web server on port 8030
    uvicorn.run(app, host="0.0.0.0", port=8030)