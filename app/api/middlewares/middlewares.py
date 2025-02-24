from fastapi import Request

from app.api.dependencies import check_access_dep
from app.exc.exception import PermissionsError


class CheckPermission:

    def __init__(self, role: str = "admin"):
        self.role = role

    async def __call__(
        self,
        request: Request,
        call_next,
        jwt_payload: check_access_dep,
    ):
        if jwt_payload.role != self.role:
            raise PermissionsError
        return await call_next(request)
