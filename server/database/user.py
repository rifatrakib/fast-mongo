from pydantic import EmailStr

from server.models.user import Activation, User, UserSignupRequest
from server.security.password import password_manager


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


async def create_new_user_activation(username: str, email: EmailStr) -> Activation:
    activation_record = Activation(
        username=username,
        email=email,
    )
    new_record = await activation_record.insert()
    return new_record
