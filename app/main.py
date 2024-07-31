from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts,users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def get_message():
    return {"message": "hello"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)









