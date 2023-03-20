from fastapi import HTTPException, status


async def http_exc_400_credentials_bad_signin_request() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Signin failed! Recheck all your credentials!"},
    )


async def http_exc_401_inactive_user() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "User not active. Please reactive account!"},
    )


async def http_exc_401_unverified_user() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "User not verified. Please verify your phone number!"},
    )


async def http_exc_403_credentials_exception() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"msg": "Refused access to the requested resource!"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def http_exc_404_key_expired() -> Exception:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Provided key has expired! Please validate before expiration."},
    )


async def http_exc_404_not_found() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Requested resource does not exist!"},
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
