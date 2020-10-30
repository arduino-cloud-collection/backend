from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from arduino_backend.user import router as user_router
from arduino_backend.auth import router as auth_router
from arduino_backend.controller import router as controller_router
from arduino_backend import database

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(user_router.router, prefix="/user")
app.include_router(auth_router.router, prefix="/auth")
app.include_router(controller_router.router, prefix="/controller")

database.DatabaseBase.metadata.create_all(bind=database.engine)
