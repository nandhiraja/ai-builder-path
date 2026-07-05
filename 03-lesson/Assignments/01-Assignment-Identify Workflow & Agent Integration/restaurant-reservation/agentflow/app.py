from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from agent import run_agent

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory conversation history (list of ollama-format messages)
# Each entry: {"role": "user"|"assistant", "content": "..."}
conversation: list = []

# Display history for the UI (simpler format)
chat_display: list = []


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "chat": chat_display}
    )


@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, message: str = Form(...)):
    global conversation, chat_display


    reply = run_agent(user_message=message, history=conversation)

    conversation.append({"role": "user",      "content": message})
    conversation.append({"role": "assistant",  "content": reply})

    chat_display.append({"role": "user",  "content": message})
    chat_display.append({"role": "agent", "content": reply})

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "chat": chat_display}
    )


@app.post("/reset", response_class=HTMLResponse)
def reset(request: Request):
    global conversation, chat_display
    conversation = []
    chat_display = []
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "chat": chat_display}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)