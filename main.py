from fastapi import FastAPI

from app.log.log import logger
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.users import router as user_router
from app.api.endpoints.tasks import router as task_router


app = FastAPI(title="Task manager API")
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)

logger.instrument_fastapi(app=app)
