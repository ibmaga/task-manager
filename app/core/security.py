import jwt
from passlib.hash import scrypt
from datetime import datetime, timedelta
from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.api.schemes.user import UserFromDB, User, Tokens
from app.core.configs import settings
from app.exc.exception import AuthenticationError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/log-in/")

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_hash(password: str) -> str:
    return scrypt.hash(password)


def verify_pass(password: str, hash_pass: str) -> bool:
    return scrypt.verify(secret=password, hash=hash_pass)


def get_user_view(user: UserFromDB) -> User:
    return User(username=user.username, password=user.password, role=user.role)


def authentication(userdata: OAuth2PasswordRequestForm, user: UserFromDB) -> User:
    if verify_pass(userdata.password, user.password):
        return get_user_view(user)
    raise AuthenticationError


def encode_jwt(
    token_type: str,
    token_data: dict,
    private_key=settings.SECRETKEY,
    algorithm=settings.ALGORITHM,
    expire_minutes: int = settings.EXP_ACCESS,
    expire_timedelta: timedelta | None = None,
) -> str:
    now = datetime.now()
    if expire_timedelta:
        exp = now + expire_timedelta
    else:
        exp = now + timedelta(minutes=expire_minutes)

    jwt_payload = {TOKEN_TYPE_FIELD: token_type, "exp": exp, "iat": now}
    jwt_payload.update(token_data)

    return jwt.encode(payload=jwt_payload, key=private_key, algorithm=algorithm)


def create_access_token(user: User) -> str:
    jwt_payload = {"sub": user.username, "role": user.role}
    return encode_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload)


def create_refresh_token(user: User):
    jwt_payload = {"sub": user.username}
    return encode_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.EXP_REFRESH),
    )


def decode_jwt(token: str):
    return jwt.decode(jwt=token, key=settings.SECRETKEY, algorithms=settings.ALGORITHM)


def is_jwt(token: str = Depends(oauth_scheme)):
    return decode_jwt(token)


def set_token_to_cookie(response: Response, token: Tokens):
    response.set_cookie("access_token", token.access_token, httponly=True)
    response.set_cookie("refresh_token", token.refresh_token, httponly=True)
