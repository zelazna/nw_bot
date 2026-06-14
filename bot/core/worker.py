from typing import Callable, final

from PySide6.QtCore import QObject, QThread, Signal, Slot

from bot.models import Params
from bot.utils.logger import logger


@final
class WorkerSignals(QObject):
    finished: Signal = Signal()
    error: Signal = Signal(tuple)
    result: Signal = Signal(object)
    current_command: Signal = Signal(int)


@final
class Worker(QThread):
    fn: Callable[["Params", WorkerSignals], None]
    params: Params
    signals: WorkerSignals

    def __init__(self, fn: Callable[["Params", WorkerSignals], None], params: Params):
        super(Worker, self).__init__()
        self.fn = fn
        self.params = params
        self.signals = WorkerSignals()

    @Slot()  # pyright: ignore[reportAny]
    def run(self) -> None:
        try:
            result = self.fn(self.params, self.signals)
        except Exception:
            logger.error("Something went wrong", exc_info=True)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
