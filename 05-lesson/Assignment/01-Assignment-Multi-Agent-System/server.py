import os
import sys
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages

from multi_agent_support import compiled_system




class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    routed_to: str

app = FastAPI(title="Presidio Multi-Agent Support")


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_ui():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    state = {"messages": [HumanMessage(content=req.message)]}
    routed_to = "unknown"

    async for output in compiled_system.astream(state, stream_mode="updates"):
        for node_name, node_update in output.items():


            if node_name in ("it_agent", "finance_agent"):
                routed_to = node_name.replace("_agent", "").upper()
            if "messages" in node_update:
                state["messages"] = add_messages(
                    state["messages"],
                    node_update["messages"],
                )

    last_msg = state["messages"][-1] if state["messages"] else None

    if last_msg and isinstance(last_msg, AIMessage):
        final = last_msg.content
    else:
        final = "I can help with **IT** or **Finance** queries. Could you provide more details?"

    return ChatResponse(reply=final, routed_to=routed_to)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8501, reload=False)
