from fastapi import APIRouter, BackgroundTasks, Depends, Path, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from server.database.user import activate_user, authenticate_user, create_new_user, read_user_by_id, update_password, verify_user_activation
from server.models.database.user import User
from server.models.helpers.base import MessageResponseSchema
from server.models.response.user import TokenResponseSchema, UserResponse
from server.security.dependencies import (
    get_current_active_user,
    new_password_form,
    password_form_field,
    signup_email_field,
    signup_username_field,
)
from server.security.token import jwt_engine
from server.services.email import send_email
from server.services.exceptions import EntityDoesNotExist, PasswordDoesNotMatch, UserNotActive
from server.services.messages import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_401_inactive_user,
    http_exc_401_not_authorized,
    http_exc_404_key_expired,
    http_exc_404_not_found,
)
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
    password: str = Depends(new_password_form),
):
    created_user = await create_new_user(username=username, email=email, password=password)
    task.add_task(send_email, request=request, user=created_user)
    return MessageResponseSchema(msg="Confirm your email to activate your account")


@router.post(
    "/signin",
    name="auth:signin",
    summary="Authenticate user for token",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = await authenticate_user(
            username=form_data.username,
            password=form_data.password,
        )
    except EntityDoesNotExist or PasswordDoesNotMatch:
        raise await http_exc_400_credentials_bad_signin_request()
    except UserNotActive:
        raise await http_exc_401_inactive_user()

    access_token = jwt_engine.generate_access_token(user=user)
    return TokenResponseSchema(token_type="Bearer", access_token=access_token)


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


@router.get(
    "/accounts/me",
    name="user:info",
    summary="Fetch information about current user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def read_current_user(user: User = Depends(get_current_active_user)):
    return user.dict()


@router.get(
    "/accounts/{user_id}",
    name="user:info",
    summary="Fetch information about an active or non active user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def read_user(
    user_id: str = Path(
        title="user ID",
        decription="Unique ID that can be used to distinguish between users.",
    ),
):
    try:
        user = await read_user_by_id(user_id)
        return user.dict()
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()


@router.patch(
    "/password/update",
    name="account:password-update",
    summary="Update password of the current active user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    current_password: str = Depends(password_form_field),
    new_password: str = Depends(new_password_form),
    current_user: User = Depends(get_current_active_user),
):
    try:
        await update_password(
            user_id=current_user.id,
            current_password=current_password,
            new_password=new_password,
        )
        return MessageResponseSchema(msg="Password updated successfully!")
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()
    except PasswordDoesNotMatch:
        raise await http_exc_401_not_authorized(problem="password")
