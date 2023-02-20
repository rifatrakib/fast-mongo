from server.models.user import User, UserRequest, UserResponse


async def create_new_user(user: UserRequest):
    new_user = User(**user.dict())
    await new_user.insert()
    created_user = UserResponse(**new_user.dict())
    return created_user
