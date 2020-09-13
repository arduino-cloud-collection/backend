from typing import Optional
from fastapi import FastAPI
from src.routers import items, hello

app = FastAPI()

app.include_router(hello.router)
app.include_router(items.router, prefix="/items")
