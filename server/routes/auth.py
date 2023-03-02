from fastapi import APIRouter, BackgroundTasks, Request, status

from server.database.user import activate_user, create_new_user, verify_user_activation
from server.models.base import MessageResponseSchema
from server.models.user import UserSignupRequest
from server.services.email import send_email
from server.services.exceptions import EntityDoesNotExist
from server.services.messages import http_exc_404_key_expired
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


@router.get(
    "/activate-account/{activation_key}",
    name="auth:activation",
    summary="Activate user account with random activation key",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def activation_key(activation_key: str):
    try:
        username = await verify_user_activation(activation_key)
        await activate_user(username)
    except EntityDoesNotExist:
        await http_exc_404_key_expired()
    return MessageResponseSchema(msg="Your account has been activated")
