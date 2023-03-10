from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pydantic import EmailStr

from server.models.user import Activation, User
from server.security.password import password_manager
from server.services.exceptions import EntityAlreadyExists, EntityDoesNotExist, PasswordDoesNotMatch, UserNotActive


async def read_user_by_username(username: str) -> User:
    user = await User.find(User.username == username).first_or_none()
    if not user:
        raise EntityDoesNotExist("No such user exists!")
    return user


async def is_username_available(username: str) -> bool:
    await read_user_by_username(username=username)
    return True


async def is_email_available(email: EmailStr) -> bool:
    user = await User.find(User.email == email).first_or_none()
    if user:
        raise EntityAlreadyExists(f"email {email} has already been used!")
    return True


async def create_new_user(username: str, email: EmailStr, password: str) -> User:
    hash_salt = password_manager.generate_salt
    new_user = User(
        username=username,
        email=email,
        hash_salt=hash_salt,
        hashed_password=password_manager.generate_hashed_password(
            hash_salt=hash_salt,
            password=password,
        ),
    )
    created_user = await new_user.insert()
    return created_user


async def authenticate_user(username: str, password: str) -> User:
    user = await read_user_by_username(username=username)

    if not user.is_active:
        raise UserNotActive("Account is not active! please activate through email.")

    if not password_manager.verify_password(
        hash_salt=user.hash_salt,
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise PasswordDoesNotMatch("wrong username or password!")

    return user


async def activate_user(username: str) -> bool:
    user = await read_user_by_username(username=username)
    await user.set({User.is_active: True, User.updated_at: datetime.utcnow()})
    return True


async def create_new_user_activation(username: str, email: EmailStr) -> Activation:
    activation_record = Activation(
        username=username,
        email=email,
    )
    new_record = await activation_record.insert()
    return new_record


async def verify_user_activation(activation_key: str) -> str:
    stored_record = await Activation.find(
        Activation.id == ObjectId(activation_key),
        Activation.created_at >= datetime.utcnow() - timedelta(minutes=5),
    ).first_or_none()

    if not stored_record:
        raise EntityDoesNotExist("No such activation key or key expired!")

    username = stored_record.username
    await stored_record.delete()
    return username
