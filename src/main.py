from fastapi import FastAPI
from src.routers import items, hello, user, auth

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(auth.router, prefix="/auth")
app.include_router(hello.router)
app.include_router(items.router, prefix="/items")
