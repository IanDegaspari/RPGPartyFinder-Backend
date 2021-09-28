from fastapi import FastAPI
from routes import app

@app.post("/create")
async def root():
    return {"message": "Hello World"}