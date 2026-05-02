import logging
from typing import final, override

from PySide6.QtCore import QObject, Signal

from bot.core.constants import APP_NAME, VERSION


@final
class QtLogHandler(logging.Handler, QObject):  # pyright: ignore[reportUnsafeMultipleInheritance]
    log_signal: Signal = Signal(str, int)

    def __init__(self) -> None:
        logging.Handler.__init__(self)
        QObject.__init__(self)

    @override
    def emit(self, record: logging.LogRecord) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        msg = self.format(record)
        self.log_signal.emit(msg, record.levelno)


formatter = logging.Formatter(f"{VERSION} - %(asctime)s - %(levelname)s - %(message)s")

qt_handler = QtLogHandler()
qt_handler.setFormatter(formatter)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(qt_handler)
