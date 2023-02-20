from fastapi import FastAPI

from server.config.factory import settings
from server.database.manager import create_database_clients
from server.routes.user import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def initialize_app():
    await create_database_clients()


@app.get("/")
async def index():
    return settings
