from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from pydantic import EmailStr

from server.database.user import activate_user, create_new_user, verify_user_activation
from server.models.base import MessageResponseSchema
from server.security.dependencies import signup_email_field, signup_password_field, signup_username_field
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
async def create_user(
    request: Request,
    task: BackgroundTasks,
    username: str = Depends(signup_username_field),
    email: EmailStr = Depends(signup_email_field),
    password: str = Depends(signup_password_field),
):
    created_user = await create_new_user(username=username, email=email, password=password)
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
