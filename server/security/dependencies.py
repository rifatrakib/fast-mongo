from fastapi import Depends, Form
from pydantic import EmailStr

from server.database.user import is_email_available, is_username_available
from server.services.exceptions import EntityAlreadyExists
from server.services.messages import http_exc_409_conflict, http_exc_412_password_mismatch


async def signup_username_field(
    username: str = Form(
        title="username",
        decription="""
            Unique username containing letters, numbers, and
            any of (., _, -, @) in between 6 to 32 characters.
        """,
        regex=r"^[\w.@_-]{6,32}$",
        min_length=6,
        max_length=32,
    ),
):
    try:
        await is_username_available(username)
    except EntityAlreadyExists as e:
        await http_exc_409_conflict(e.args[0])
    return username


async def signup_email_field(
    email: EmailStr = Form(
        title="email",
        decription="Unique email that can be used for user account activation.",
    ),
):
    try:
        await is_email_available(email)
    except EntityAlreadyExists as e:
        await http_exc_409_conflict(e.args[0])
    return email


async def password_form_field(
    password: str = Form(
        title="Password",
        alias="password",
        description="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    ),
    repeat_password: str = Form(
        title="Repeat Password",
        alias="repeatPassword",
        description="Repeat the same password.",
    ),
):
    if password != repeat_password:
        await http_exc_412_password_mismatch()
    return password


def signup_password_field(password: str = Depends(password_form_field)):
    return password
