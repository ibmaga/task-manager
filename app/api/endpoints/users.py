from fastapi import APIRouter, Depends, status

from app.api.schemes.user import UserReg, UserOut
from app.api.schemes.other import Tokens
from app.exc.models import ErrorResponseModel
from app.api.dependencies import user_crud_dep, check_user, get_user_by_payload
from app.core.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["auth & reg"])


@router.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponseModel}},
)
async def sign_up(user: UserReg, crud: user_crud_dep) -> UserOut:
    result = await crud.add_user(user)
    return UserOut.model_validate(result)


@router.post(
    "/log-in/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseModel}},
)
async def log_in(user=Depends(check_user)) -> Tokens:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/")
async def refresh(user=Depends(get_user_by_payload)) -> Tokens:
    access_token = create_access_token(user)
    return Tokens(access_token=access_token)


"""
реализовать автоматическую замену просроченного jwt
"""
