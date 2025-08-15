import logging

from PySide6.QtCore import QObject, Signal

from bot.core.constants import APP_NAME, VERSION


class QtLogHandler(logging.Handler, QObject):
    log_signal = Signal(str, int)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record: logging.LogRecord) -> None:  # type: ignore
        msg = self.format(record)
        self.log_signal.emit(msg, record.levelno)


formatter = logging.Formatter(f"{VERSION} - %(asctime)s - %(levelname)s - %(message)s")

# Handler Qt
qt_handler = QtLogHandler()
qt_handler.setFormatter(formatter)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(qt_handler)
