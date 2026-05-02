from typing import final, override

from PySide6.QtCore import Qt, QTimerEvent, Slot
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QAbstractItemView, QMainWindow

from bot.core.constants import PADDING_IN_S, TIMER_TIMEOUT_MILLISEC, VERSION
from bot.core.control import run
from bot.core.keystroke_adapter import QtKeystrokeAdapter
from bot.core.mouse_adapter import MouseAdapter
from bot.core.recorder import Recorder
from bot.core.worker import Worker
from bot.models import CommandListModel
from bot.ui.delegates import CommandDelegate
from bot.ui.handlers import CommandHandler, ConfigHandler, RecordHandler, RecordingMode
from bot.ui.main_window_ui import Ui_MainWindow
from bot.ui.modals import LogDialog
from bot.ui.validators import ValidateNumber, ValidateRangeOrNumber
from bot.utils import format_time
from bot.utils.logger import logger, qt_handler


@final
class MainWindow(QMainWindow):
    worker: Worker | None
    timeLeft: int
    timer_id: int
    logs: list[tuple[str, int]]
    _command_model: CommandListModel
    _key_adapter: QtKeystrokeAdapter
    _mouse_adapter: MouseAdapter
    ui: Ui_MainWindow
    config: ConfigHandler
    record: RecordHandler
    commands: CommandHandler

    def __init__(self) -> None:
        super().__init__()

        self.worker = None
        self.timeLeft = 0
        self.timer_id = 0
        self.logs = []

        self._command_model = CommandListModel()
        recorder = Recorder(self._command_model)
        self._key_adapter = QtKeystrokeAdapter(self._command_model)
        self._mouse_adapter = MouseAdapter(self._command_model)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.config = ConfigHandler(self.ui, self._command_model, self)
        self.record = RecordHandler(self.ui, recorder)
        self.commands = CommandHandler(self.ui, self._command_model)

        self.ui.keyListView.setModel(self._command_model)
        self.ui.keyListView.setItemDelegate(CommandDelegate(self.ui.keyListView))
        self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ui.keyListView.setDropIndicatorShown(True)

        self.ui.actionUnboundRecordToggle.triggered.connect(self.record.toggle_outside)
        self.ui.actionShowLogs.triggered.connect(self.showLogs)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.interval.setClearButtonEnabled(True)
        self.ui.limit.setClearButtonEnabled(True)
        self.ui.limit.setValidator(ValidateNumber())

        self.ui.stopButton.setDisabled(True)
        self.ui.stopButton.clicked.connect(self.stopBot)  # pyright: ignore[reportAny]
        self.ui.startButton.clicked.connect(self.startBot)  # pyright: ignore[reportAny]

        self.ui.appVersion.setText(f"v{VERSION}")
        qt_handler.log_signal.connect(self.storeLog)

    # Qt event overrides: delegate to handlers / adapters

    @override
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.record.mode is RecordingMode.INSIDE:
            self._key_adapter.on_key_release(event)  # pyright: ignore[reportArgumentType]
        if event.key() == Qt.Key.Key_Delete:
            self.commands.delete()

    @override
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.record.mode is RecordingMode.INSIDE:
            self._mouse_adapter.on_click(event.x(), event.y(), event.button(), True)

    @override
    def timerEvent(self, event: QTimerEvent) -> None:
        self.timeLeft -= TIMER_TIMEOUT_MILLISEC
        self.ui.remainingTime.setText(format_time(self.timeLeft))

    # Bot control

    @Slot()  # pyright: ignore[reportAny]
    def startBot(self) -> None:
        params = self.config.dump()

        if ValidateRangeOrNumber.validate(params.interval):
            self.ui.remainingTime.setVisible(True)
            self.ui.stopButton.setDisabled(False)
            self.ui.startButton.setDisabled(True)

            self.timeLeft = int(self.ui.limit.text()) * 60 * 1000 + (PADDING_IN_S * 1000)
            self.timer_id = self.startTimer(TIMER_TIMEOUT_MILLISEC)
            logger.info(f"Starting timer with {format_time(self.timeLeft)} minutes")

            self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
            self.worker = Worker(run, params)
            self.worker.signals.finished.connect(self.botThreadComplete)
            self.worker.signals.current_command.connect(self.setCurrentCommand)  # pyright: ignore[reportAny]
            self.worker.start()
        else:
            self.config.show_error("Configuration invalide!")

    @Slot()  # pyright: ignore[reportAny]
    def stopBot(self) -> None:
        logger.info("Stopping bot")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.botThreadComplete()
        self.killTimer(self.timer_id)

    def botThreadComplete(self) -> None:
        logger.info("bot thread complete!")
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)
        self.ui.keyListView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ui.keyListView.clearSelection()

    @Slot(int)  # pyright: ignore[reportAny]
    def setCurrentCommand(self, index: int) -> None:
        self.ui.keyListView.setCurrentIndex(self._command_model.index(index, 0))

    # Logs

    def storeLog(self, message: str, level: int) -> None:
        self.logs.append((message, level))

    def showLogs(self) -> None:
        logViewer = LogDialog(self.logs, self)
        logViewer.exec()
