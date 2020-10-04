from fastapi import FastAPI
from src.routers import user, auth

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(auth.router, prefix="/auth")
