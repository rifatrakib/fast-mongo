from passlib.context import CryptContext

from server.config.factory import settings


class HashGenerator:
    def __init__(self):
        self._password_hash: CryptContext = CryptContext(
            schemes=[settings.PASSWORD_HASH_ALGORITHM],
            deprecated="auto",
        )
        self._salt_hash: CryptContext = CryptContext(
            schemes=[settings.SALT_HASH_ALGORITHM],
            deprecated="auto",
        )
        self._salt: str = settings.HASH_SALT

    @property
    def _get_hashing_salt(self) -> str:
        return self._salt

    @property
    def generate_salt_hash(self) -> str:
        """generate a hash from bcrypt to append to the user password."""
        return self._salt_hash.hash(secret=self._get_hashing_salt)

    def generate_password_hash(self, hash_salt: str, password: str) -> str:
        """add the password with the first layer bcrypt hash, before the second
        layer hash using bcrypt algorithm."""
        return self._password_hash.hash(secret=hash_salt + password)

    def is_password_verified(self, password: str, hashed_password: str) -> bool:
        """decode password and verify whether it is the correct."""
        return self._password_hash.verify(secret=password, hash=hashed_password)


def get_hash_generator() -> HashGenerator:
    return HashGenerator()


hasher: HashGenerator = get_hash_generator()
