from fastapi import FastAPI
from . import models
from .database import engine
from .routes import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Railway MySQL Example")

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI on Railway with MySQL!"}
