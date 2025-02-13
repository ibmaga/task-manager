# import logging
import logfire

# FORMAT = "%(levelname)s:     %(filename)s:%(lineno)s - %(message)s [%(asctime)s]"
# DATE_FMT = "%H:%M:%S %d-%m-%Y"
# logging.basicConfig(
#     level=logging.INFO,
#     format=FORMAT,
#     datefmt=DATE_FMT,
# )
#
# logger = logging.getLogger(__name__)


def log(app):
    logfire.configure(token="sR4RftrwQgRHMQPXJjt0QlMHy7WfktdMYWzm708YCX33")
    logfire.instrument_fastapi(app=app, capture_headers=True)
    logfire.instrument_asyncpg()
