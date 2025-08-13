from typing import Callable

from PySide6.QtCore import QObject, QThread, Signal, Slot

from bot.models import Params
from bot.utils.logger import logger


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QThread):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function

    """

    def __init__(self, fn: Callable[[Params], None], *args: Params):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args)
        except Exception:
            logger.error("Something went wrong: \n", exc_info=True)
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
