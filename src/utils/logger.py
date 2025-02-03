import logging

FORMAT = "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

logger_blocklist = [
    "hpack",
    "httpcore",
]

for module in logger_blocklist:
    logging.getLogger(module).setLevel(logging.WARNING)

log = logging.getLogger("usports-data-pipeline")
