from fastapi import APIRouter, Depends, status, Response

from app.api.schemes.user import UserRegistration, Tokens
from app.exc.models import ErrorResponseModel
from app.api.dependencies import user_crud_dep, check_user
from app.core.security import (
    create_access_token,
    set_token_to_cookie,
    create_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth & reg"])


@router.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponseModel}},
)
async def sign_up(user: UserRegistration, crud: user_crud_dep):
    result = await crud.add_user(user)
    return result


@router.post("/log-in/", status_code=status.HTTP_200_OK)
async def log_in(response: Response, user=Depends(check_user)) -> Tokens:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    tokens = Tokens(access_token=access_token, refresh_token=refresh_token)
    set_token_to_cookie(response, tokens)
    return tokens


"""написать исключение на все случаи, использовать refresh_token,
расширить crud в dao: отдельно для user и tasks, использовать роли, написать модели почти для всего,
закрепить jwt токен на cookie, реализовать автоматическую замену просроченного jwt"""
