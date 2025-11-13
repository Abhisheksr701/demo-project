# app/main.py
from fastapi import FastAPI
import logging
from . import models
from .database import engine, Base

app = FastAPI(title="FastAPI Railway MySQL Example")

# include your routers here (example)
from .routes.user import router as user_router
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.on_event("startup")
def startup_event():
    if engine is None:
        logging.error("Database engine not configured. Skipping Base.metadata.create_all().")
        return
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created or already exist.")
    except Exception as e:
        logging.exception("Failed to create tables on startup: %s", e)
