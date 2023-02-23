from fastapi import APIRouter

from server.services.validators import Tags

router = APIRouter(prefix="/users", tags=[Tags.users])
