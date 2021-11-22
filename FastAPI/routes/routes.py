from fastapi import FastAPI
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from routes.user import user_router
from routes.login import login_router
from routes.user_preferences import pref_router
from routes.user_relations import relations_router
from routes.party import party_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user_router, tags=["user"])
app.include_router(login_router, tags=["login"])
app.include_router(pref_router, tags=["preferences"])
app.include_router(relations_router, tags=["relations"])
app.include_router(party_router, tags=["party"])