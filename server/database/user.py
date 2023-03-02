from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pydantic import EmailStr

from server.models.user import Activation, User, UserSignupRequest
from server.security.password import password_manager
from server.services.exceptions import EntityDoesNotExist


async def is_username_available(username: str) -> bool:
    user = await User.find(User.username == username).first_or_none()
    return False if user else True


async def is_email_available(email: EmailStr) -> bool:
    user = await User.find(User.email == email).first_or_none()
    return False if user else True


async def create_new_user(user: UserSignupRequest) -> User:
    hash_salt = password_manager.generate_salt
    new_user = User(
        **user.dict(),
        hash_salt=hash_salt,
        hashed_password=password_manager.generate_hashed_password(
            hash_salt=hash_salt,
            password=user.password,
        )
    )
    created_user = await new_user.insert()
    return created_user


async def activate_user(username: str) -> bool:
    user = await User.find(User.username == username).first_or_none()

    if not user:
        raise EntityDoesNotExist("No such user exists!")

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
