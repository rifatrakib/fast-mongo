from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import parse_file_as

from server.config.factory import settings
from server.models.base import MapperSchema


def database_collection_mapper() -> MapperSchema:
    mapper = parse_file_as(
        type_=MapperSchema,
        path=settings.MONGO_MAPPER_PATH,
    )
    return mapper


async def create_database_clients():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    mapper = database_collection_mapper()
    for database in mapper.databases:
        await init_beanie(
            database=client[database.name],
            document_models=[database.collections],
        )
