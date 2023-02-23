from fastapi import APIRouter

from server.database.user import create_new_user
from server.models.user import UserResponse, UserSignupRequest
from server.services.validators import Tags

router = APIRouter(prefix="/auth", tags=[Tags.authentication])


@router.post("/signup", response_model=UserResponse)
async def create_user(user: UserSignupRequest):
    created_user = await create_new_user(user)
    return UserResponse(**created_user.dict())
