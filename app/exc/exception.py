from fastapi.exceptions import HTTPException
from fastapi import status


class UserNotFoundError(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail="User not found"):
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFoundError(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsError(HTTPException):
    def __init__(
        self, status_code=status.HTTP_409_CONFLICT, detail="User already exists"
    ):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login or password is not valid",
    ):
        super().__init__(status_code=status_code, detail=detail)


class TokenError(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Token error"):
        super().__init__(status_code=status_code, detail=detail)


class PermissionsError(HTTPException):
    def __init__(
        self, status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission"
    ):
        super().__init__(status_code=status_code, detail=detail)
