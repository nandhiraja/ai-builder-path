import os
import re
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from bedrock_service import BedrockAgentService

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="AWS Bedrock Web Crawler Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


class CrawlRequest(BaseModel):
    url: str = Field(..., min_length=10, max_length=2048)
    session_id: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=5000)
    session_id: str | None = None


def validate_http_url(url: str):
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"

    if not re.match(pattern, url, re.IGNORECASE):
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid HTTP or HTTPS website URL."
        )


def get_agent_service():
    try:
        return BedrockAgentService()
    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Server configuration error: {str(error)}"
        )


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "running",
        "service": "AWS Bedrock Web Crawler Agent"
    }


@app.post("/api/crawl")
def crawl_website(request: CrawlRequest):
    validate_http_url(request.url)

    message = f"Crawl this URL: {request.url}"

    service = get_agent_service()

    result = service.invoke_agent(
        user_message=message,
        session_id=request.session_id or str(uuid.uuid4())
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unable to invoke the Bedrock Agent.")
        )

    return result


@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
    service = get_agent_service()

    result = service.invoke_agent(
        user_message=request.message,
        session_id=request.session_id or str(uuid.uuid4())
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unable to invoke the Bedrock Agent.")
        )

    return result