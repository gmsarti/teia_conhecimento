from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.infra.database import query
from paths import TEMPLATES

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)  # Updated directory


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Added request argument
    return templates.TemplateResponse("under_construction.html", {"request": request})


@app.get(
    "/api/v1/status",
    summary="Get API status",
    response_description="API health and status details",
)
def get_status():
    """
    Checks and returns the current status and health information of the API.
    """

    # 1. Database Connection Check (More Robust)
    try:
        # Replace with your actual database connection and a simple query (e.g., SELECT 1)
        database_status = "connected"
    except Exception as e:  # Catch any database-related exceptions
        database_status = "connection error"
        print(f"Database error: {e}")  # Log the error for debugging
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,  # 503 for database issue
            detail="Database connection error",
        )

    s = {
        "updated_at": datetime.now(),
        "status": "ok" if database_status == "connected" else "error",
        "database": database_status,
        "version": "0.1.0",  # Your API version
        "dependencies": {
            "database": {
                "version": query("SHOW server_version;")[0][0],
                "max_connections": int(query("SHOW max_connections;")[0][0]),
                "opened_connections": int(
                    query(
                        "SELECT COUNT(*) FROM pg_stat_activity WHERE datname = 'local_db';"
                    )[0][0]
                ),
            }
        },
        # Add more status information as needed
    }

    return s
