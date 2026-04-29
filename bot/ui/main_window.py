from functools import partial
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QAbstractItemView, QMainWindow

from bot.core.constants import PADDING_IN_S, TIMER_TIMEOUT_MILLISEC, VERSION
from bot.core.control import run
from bot.core.keystroke_adapter import QtKeystrokeAdapter
from bot.core.mouse_adapter import MouseAdapter
from bot.core.recorder import Recorder
from bot.core.worker import Worker, WorkerSignals
from bot.models import CommandListModel
from bot.ui.delegates import CommandDelegate
from bot.ui.main_window_ui import Ui_MainWindow
from bot.ui.mixins import ConfigMixin, RecordMixin, EventMixin
from bot.ui.mixins.record import RecordingMode
from bot.ui.modals import LogDialog
from bot.ui.validators import ValidateNumber, ValidateRangeOrNumber
from bot.utils import format_time
from bot.utils.logger import logger, qt_handler


class MainWindow(ConfigMixin, EventMixin, RecordMixin, QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker: Optional[Worker] = None
        self.recording_mode = RecordingMode.IDLE
        self.timeLeft = 0
        self.timer_id = 0
        self.validator = ValidateRangeOrNumber()
        self.currentFile: str | None = None
        self.logs: list[tuple[str, int]] = []
        self.commandModel = CommandListModel()
        self.recorder = Recorder(self.commandModel)
        self.key_stroke_adapter = QtKeystrokeAdapter(self.commandModel)
        self.mouse_adapter = MouseAdapter(self.commandModel)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore
        self.setupRecording()
        self.setupConfig()
        self.setupEvents()

        self.ui.keyListView.setModel(self.commandModel)
        self.ui.keyListView.setItemDelegate(CommandDelegate(self.ui.keyListView))
        self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ui.keyListView.setDropIndicatorShown(True)

        self.ui.actionUnboundRecordToggle.triggered.connect(self.toggleOutsideRecord)

        self.ui.actionShowLogs.triggered.connect(self.showLogs)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.interval.setClearButtonEnabled(True)

        self.ui.limit.setClearButtonEnabled(True)
        self.ui.limit.setValidator(ValidateNumber())

        self.ui.stopButton.setDisabled(True)
        self.ui.stopButton.clicked.connect(self.stopBot)
        self.ui.startButton.clicked.connect(self.startBot)

        self.ui.appVersion.setText(f"v{VERSION}")

        qt_handler.log_signal.connect(self.storeLog)

    ## Bot Control
    @Slot()
    def startBot(self):
        params = self.dumpConfig()

        if ValidateRangeOrNumber.validate(params.interval):
            self.ui.remainingTime.setVisible(True)
            self.ui.stopButton.setDisabled(False)
            self.ui.startButton.setDisabled(True)

            self.timeLeft = int(self.ui.limit.text()) * 60 * 1000 + (
                PADDING_IN_S * 1000
            )  # Convert minutes to milliseconds
            self.timer_id = self.startTimer(TIMER_TIMEOUT_MILLISEC)
            logger.info(f"Starting timer with {format_time(self.timeLeft)} minutes")

            self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
            signals = WorkerSignals()
            self.worker = Worker(partial(run, on_command=signals.current_command.emit), params)
            self.worker.signals = signals
            self.worker.signals.finished.connect(self.botThreadComplete)
            self.worker.signals.current_command.connect(self.setCurrentCommand)
            self.worker.start()
        else:
            self._showErrorModal("Configuration invalide!")

    @Slot()
    def stopBot(self):
        logger.info("Stopping bot")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.botThreadComplete()
        self.killTimer(self.timer_id)

    def botThreadComplete(self):
        logger.info("bot thread complete!")
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)
        self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ui.keyListView.clearSelection()

    @Slot(int)
    def setCurrentCommand(self, index: int):
        self.ui.keyListView.setCurrentIndex(self.commandModel.index(index, 0))

    ## LOGS
    def storeLog(self, message: str, level: int):
        self.logs.append((message, level))

    def showLogs(self):
        logViewer = LogDialog(self.logs, self)
        logViewer.exec()
