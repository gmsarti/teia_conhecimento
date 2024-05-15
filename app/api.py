from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Root"])
def hello():
    return {"Hello!": "We're working to deploy."}
