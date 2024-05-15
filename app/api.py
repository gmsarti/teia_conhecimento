# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")


# # @app.get("/")
# # async def root():
# #     return {"race": "half-orc"}


# @app.get("/", response_class=HTMLResponse)
# async def root(request: Request):
#     return templates.TemplateResponse("under_construction.html", {"request": request})


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")  # Updated directory


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Added request argument
    return templates.TemplateResponse("under_construction.html", {"request": request})
