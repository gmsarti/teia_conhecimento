from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from paths import TEMPLATES

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)  # Updated directory


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Added request argument
    return templates.TemplateResponse("under_construction.html", {"request": request})


@app.get("/status")
def get_status():
    # Add logic to check your application's health, e.g., database connection
    is_database_connected = True  # Replace with your actual check
    status = "ok" if is_database_connected else "database_error"

    s = {
        "status": status,
        "database": "connected" if is_database_connected else "not connected",
        "version": "1.0.0",  # Your API version
        # Add more status information as needed
    }
    return s
