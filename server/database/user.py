from server.models.user import User, UserSignupRequest
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
