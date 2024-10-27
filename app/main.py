from fastapi import FastAPI
from app.routes import router
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI()

app.include_router(router)
