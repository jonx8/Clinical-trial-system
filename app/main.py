from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def api_hello():
    return {"Clinical trial API is running"}
