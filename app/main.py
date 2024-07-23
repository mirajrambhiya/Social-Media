from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg
import time
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine,get_db
from .routers import posts,users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def get_message():
    return {"message": "hello"}



# while True:
#     try:
#         correct_password = input("Enter the correct password: ")
#         conn = psycopg.connect(dbname="Social Media", user="postgres", password=correct_password)
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Failed to connect to database with the new password")
#         print("Error:", error)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)









