from fastapi import FastAPI

from arduino_backend.routers import user, auth

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(auth.router, prefix="/auth")
