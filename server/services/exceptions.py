class EntityDoesNotExist(Exception):
    """throw an exception when the data does not exist in the database."""


class EntityAlreadyExists(Exception):
    """throw an exception when the data already exist in the database."""


class PasswordDoesNotMatch(Exception):
    """throw an exception when the account password does not match the
    entitiy's hashed password from the database."""


class UserNotActive(Exception):
    """throw an exception when the account has not been activated through
    email."""
