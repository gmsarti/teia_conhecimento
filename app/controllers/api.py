from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from paths import TEMPLATES

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)  # Updated directory


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Added request argument
    return templates.TemplateResponse("under_construction.html", {"request": request})
