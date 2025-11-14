from datetime import datetime, timedelta, timezone
from app.core.config import settings
from jose import jwt, JWTError
from typing import Optional
from app.core.redis_client import redis_client

def _expire(delta) -> int:
    return int((datetime.now(tz=timezone.utc) + delta).timestamp())

def create_access_token(subject: str) -> str:
    payload = {"sub":subject, "exp": _expire(timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(subject: str) -> str:
    payload = {"sub": subject, "exp": _expire(timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))}
    return jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token:str) -> Optional[str]:
    try:
        data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return data.get("sub")
    except JWTError:
        return None
    
def decode_refresh_token(token: str) -> Optional[str]:
    try:
        data = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return data.get("sub")
    except JWTError:
        return None

def blacklist_token(token: str, expires_in: int):
    redis_client.setex(f"blacklist:{token}", expires_in, "true")

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}")