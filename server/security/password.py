from server.security.hash import hasher


class PasswordManager:
    @property
    def generate_salt(self) -> str:
        return hasher.generate_salt_hash

    def generate_hashed_password(self, hash_salt: str, password: str) -> str:
        """two layer hashing on password with bcrypt algorithm."""
        return hasher.generate_password_hash(
            hash_salt=hash_salt,
            password=password,
        )

    def verify_password(self, hash_salt: str, password: str, hashed_password: str) -> bool:
        """verfiy stored password hash with two layer hashing of password."""
        return hasher.is_password_verified(
            password=hash_salt + password,
            hashed_password=hashed_password,
        )


def get_password_manager() -> PasswordManager:
    return PasswordManager()


password_manager: PasswordManager = get_password_manager()
