from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from arduino_backend.user import router as user_router
from arduino_backend.auth import router as auth_router

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(user_router.router, prefix="/user")
app.include_router(auth_router.router, prefix="/auth")
