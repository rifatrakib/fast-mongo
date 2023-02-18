from fastapi import FastAPI

from server.config.factory import settings

app = FastAPI()


@app.get("/")
async def index():
    return settings
