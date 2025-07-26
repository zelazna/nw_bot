import logging
from typing import Any

from bot.core.constants import LOG_FILE, VERSION

extra = {"version": VERSION}
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(version)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    filename=LOG_FILE,
)
old_factory = logging.getLogRecordFactory()


def record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
    record = old_factory(*args, **kwargs)
    record.version = VERSION
    return record


logging.setLogRecordFactory(record_factory)
