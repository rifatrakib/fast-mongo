from fastapi import APIRouter

from server.database.user import create_new_user
from server.models.user import UserRequest, UserResponse

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse)
async def create_user(user: UserRequest):
    created_user = await create_new_user(user)
    return created_user
