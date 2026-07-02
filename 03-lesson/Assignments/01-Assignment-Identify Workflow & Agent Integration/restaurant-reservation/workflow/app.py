from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from booking import reserve_table

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {"request": request}
    )


@app.post("/reserve", response_class=HTMLResponse)
def reserve(
    request: Request,
    name: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    guests: int = Form(...)
    ):
    result = reserve_table(guests)

    return templates.TemplateResponse(
        "response.html",
        {
            "request": request,
            "result": result,
            "name": name,
            "date": date,
            "time": time,
            "guests": guests
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)