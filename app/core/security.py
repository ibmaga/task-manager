import jwt
from fastapi import Depends, Response
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from passlib.hash import scrypt

from app.api.schemes.other import Payload, Tokens
from app.api.schemes.user import UserFromDB, User, UserOut
from app.core.configs import settings
from app.exc.exception import AuthenticationError, TokenError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/log-in/")
http_bearer = HTTPBearer(auto_error=False)

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_hash(password: str) -> str:
    return scrypt.hash(password)


def verify_pass(password: str, hash_pass: str) -> bool:
    return scrypt.verify(secret=password, hash=hash_pass)


def get_user_view(user: UserFromDB) -> User:
    return User(username=user.username, password=user.password, role=user.role)


async def authentication(
    userdata: OAuth2PasswordRequestForm, user: UserFromDB, user_crud
) -> UserOut:
    if verify_pass(userdata.password, user.password):
        """Изменение роли пользователя при авторизации на user"""
        if user.role != "user":
            user.role = "user"
            await user_crud.update_user(user_id=user.id, user=user)
        return UserOut.model_validate(user)
    raise AuthenticationError


def encode_jwt(
    token_type: str,
    token_data: dict,
    private_key=settings.SECRETKEY,
    algorithm=settings.ALGORITHM,
    expire_minutes: int = settings.EXP_ACCESS,
    expire_timedelta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        exp = now + expire_timedelta
    else:
        exp = now + timedelta(minutes=expire_minutes)

    jwt_payload = {TOKEN_TYPE_FIELD: token_type, "exp": exp, "iat": now}
    jwt_payload.update(token_data)

    return jwt.encode(payload=jwt_payload, key=private_key, algorithm=algorithm)


def create_access_token(user: UserFromDB) -> str:
    jwt_payload = {"sub": user.username, "id": user.id, "role": user.role}
    return encode_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload)


def create_refresh_token(user: UserFromDB):
    jwt_payload = {"sub": user.username, "id": user.id}
    return encode_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.EXP_REFRESH),
    )


def decode_jwt(token: str) -> dict:
    return jwt.decode(jwt=token, key=settings.SECRETKEY, algorithms=settings.ALGORITHM)


def check_payload_token(token: str, type_token: str):
    try:
        payload = decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise TokenError(detail="Token has expired")

    if payload[TOKEN_TYPE_FIELD] != type_token:
        raise TokenError(
            detail=f"Invalid token type {payload[TOKEN_TYPE_FIELD]!r} expected {type_token!r}"
        )
    return payload


class CheckToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, token: str = Depends(oauth_scheme)):
        payload = check_payload_token(token, self.token_type)
        return Payload(**payload)


def set_token_to_cookie(response: Response, token: Tokens):
    response.set_cookie("access_token", token.access_token, httponly=True)
    response.set_cookie("refresh_token", token.refresh_token, httponly=True)
