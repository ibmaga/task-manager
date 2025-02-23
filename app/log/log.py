from logfire import configure
from functools import lru_cache

from app.db.database import engine
from app.core.configs import settings


def _log():
    logg = configure(token=settings.LOG_TOKEN)
    logg.instrument_asyncpg()
    logg.instrument_sqlalchemy(engine=engine)
    return logg


@lru_cache
def get_logger():
    return _log()


logger = get_logger()
