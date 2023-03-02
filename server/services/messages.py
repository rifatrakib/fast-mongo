from fastapi import HTTPException, status


async def http_exc_404_key_expired() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Provided key has expired! Please validate before expiration."},
    )


async def http_exc_409_conflict(message: str) -> Exception:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"msg": message},
    )


async def http_exc_412_password_mismatch() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail={"msg": "Passwords does not match!"},
    )
