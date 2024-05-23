from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.infra.database import query
from app.models.question_validation import Question
from app.services.ask_service import create_chain
from paths import TEMPLATES

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)  # Updated directory


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})


@app.get("/under-construction", response_class=HTMLResponse)
async def under_construction(request: Request):  # Added request argument
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


@app.get("/ask", response_class=HTMLResponse)
async def ask_question_form(request: Request):
    return templates.TemplateResponse("ask.html", {"request": request})


# @app.post("/ask")
# async def ask_question(question: Question):
# chain = create_chain()  # Create the chain
# result = chain.invoke({"input": question.question})  # Invoke the chain
# return {"answer": result}  # Return the answer text


@app.post("/ask", response_class=JSONResponse)
async def ask_question(request: Request):
    try:
        form_data = await request.json()
        print(f"Received form data: {form_data}")  # Log form data

        question_obj = Question(question=form_data["question"])
        print(f"Question object: {question_obj}")  # Log question object

        chain = create_chain()
        print(f"Chain created: {chain}")  # Log chain details

        result = chain.invoke({"input": question_obj.question})
        print(f"Result from chain: {result}")  # Log chain result

        return {"answer": result}
    except ValueError as ve:
        print(f"Value Error: {ve}")
        return JSONResponse(
            {"status": "ERROR", "msg": f"Invalid input: {ve}"}, status_code=400
        )  # Bad Request
    except KeyError as ke:
        print(f"Key Error: {ke}")
        return JSONResponse(
            {"status": "ERROR", "msg": f"Missing data: {ke}"}, status_code=400
        )
    except Exception as e:  # Catch-all for unexpected errors
        print(f"Error: {e}")
        return JSONResponse(
            {"status": "ERROR", "msg": "Internal Server Error"}, status_code=500
        )
