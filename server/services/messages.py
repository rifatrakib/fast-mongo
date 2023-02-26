from fastapi import HTTPException, status


async def http_exc_404_key_expired() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Provided key has expired! Please validate before expiration."},
    )
