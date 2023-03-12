from datetime import datetime, timedelta
from typing import Union

from beanie import Document, Insert, Update, before_event
from pydantic import Field

from server.models.helpers.user import UserBase


class User(Document, UserBase):
    hashed_password: str = Field(
        title="hashed password",
        decription="Generated hash for the user provided password string.",
    )
    hash_salt: str = Field(
        title="hashed salt",
        decription="A mark for increasing security on password hash.",
    )
    is_active: bool = Field(
        default=False,
        title="active status",
        decription="Whether user is active, determined via email confirmation.",
    )
    is_verified: bool = Field(
        default=False,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="time of insert",
        decription="Exact time when the user information was first saved.",
    )
    updated_at: Union[datetime, None] = Field(
        default=None,
        title="time of last update",
        decription="Exact time when the user information was last updated.",
    )

    class Settings:
        name = "users"
        indexes = ["username", "email"]

    @before_event(Insert)
    def nullify_update_time_on_create(self):
        """set time of update as None before inserting user data."""
        self.updated_at = None

    @before_event(Update)
    def time_of_last_update(self):
        """set time of update as current UTC time before updating user data."""
        self.updated_at = datetime.utcnow()


class Activation(Document, UserBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="time of insert",
        decription="Exact time when the user information was first saved.",
    )

    class Settings:
        name = "user_activations"
        indexes = ["username", "email", "created_at"]

    @before_event(Insert)
    async def clear_expired(self):
        """remove any expired document before inserting any new document."""
        threshold = datetime.utcnow() - timedelta(minutes=5)
        await self.find({"created_at": {"$lt": threshold}}).delete()
