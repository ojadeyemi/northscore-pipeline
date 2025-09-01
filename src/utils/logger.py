import logging

from src.config.settings import LOG_LEVEL

FORMAT = "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"

if LOG_LEVEL == "DEBUG":
    FORMAT = "[%(asctime)s] %(levelname)-8s [%(name)s] %(filename)s:%(lineno)d in %(funcName)s(): %(message)s"
else:
    FORMAT = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"

logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

logger_blocklist = ["hpack", "httpcore", "urllib3"]

for module in logger_blocklist:
    logging.getLogger(module).setLevel(logging.WARNING)

log = logging.getLogger("pipeline")
