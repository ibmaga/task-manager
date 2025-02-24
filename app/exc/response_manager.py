from fastapi import status

from app.exc.models import ErrorResponse


class AuthResponses:
    reg_responses = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad request",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "User already exists",
        },
    }

    login_responses = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        },
    }

    refresh_responses = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid token",
        },
    }


class TaskResponses:
    task_responses = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad request",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid token",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Task not found",
        },
    }
