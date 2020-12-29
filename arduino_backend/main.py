from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from arduino_backend.settings import config
from arduino_backend.user import router as user_router
from arduino_backend.auth import router as auth_router
from arduino_backend.token import router as token_router
from arduino_backend.controller import router as controller_router
from arduino_backend.clientsocket.router import router as clientsocket_router
from arduino_backend import database
import logging
from pyfiglet import Figlet
from sentry_sdk import init
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware



f = Figlet(font="slant")
gunicorn_logger = logging.getLogger('gunicorn.error')
gunicorn_logger.info("\n" + f.renderText("arduino-cloud"))

app = FastAPI()

if config.SENTRY == "True":
    init(
        dsn=config.SENTRY_URL,
        traces_sample_rate=1.0)
    app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/user")
app.include_router(auth_router.router, prefix="/auth")
app.include_router(controller_router.router, prefix="/controller")
app.include_router(token_router.router, prefix="/token")
app.include_router(clientsocket_router, prefix="/socket")
