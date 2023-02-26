from fastapi import APIRouter, BackgroundTasks, Request, status

from server.database.user import create_new_user
from server.models.base import MessageResponseSchema
from server.models.user import UserSignupRequest
from server.services.email import send_email
from server.services.validators import Tags

router = APIRouter(prefix="/auth", tags=[Tags.authentication])


@router.post(
    "/signup",
    name="auth:signup",
    summary="Create new user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(request: Request, user: UserSignupRequest, task: BackgroundTasks):
    created_user = await create_new_user(user)
    task.add_task(send_email, request=request, user=created_user)
    return MessageResponseSchema(msg="Confirm your email to activate your account")
