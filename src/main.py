from fastapi import FastAPI
from src.routers import items, hello, user

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(hello.router)
app.include_router(items.router, prefix="/items")
