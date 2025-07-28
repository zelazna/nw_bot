import functools
import os

from pynput.mouse import Button
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow

from bot.core.constants import VERSION
from bot.core.control import run
from bot.core.KeystrokeAdapter import match
from bot.core.recorder import Recorder
from bot.core.worker import Worker
from bot.models import CommandsModel, Keystroke, MouseClick, Params
from bot.ui.mainwindow import Ui_MainWindow
from bot.ui.modals import FileNameModal, LogViewerModal
from bot.ui.validators import ValidateNumber, ValidateRangeOrNumber
from bot.utils import loadConfig, logger, saveConfig


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.isRecording = False
        self.isRecordingOutside = False
        self.timeLeft = 0
        self.botTimer = QTimer(self)
        self.botTimer.timeout.connect(self.timerTick)
        self.validator = ValidateRangeOrNumber()

        self.recorder = Recorder()
        self.recorder.signals.interaction.connect(self.recordOutside)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.commandModel = CommandsModel()
        self.ui.keyListView.setModel(self.commandModel)
        self.ui.keyListView.setDragEnabled(True)
        self.ui.keyListView.setAcceptDrops(True)
        self.ui.keyListView.setDropIndicatorShown(True)

        self.ui.actionSaveConfig.triggered.connect(self.saveConfig)
        self.ui.actionLoadConfig.triggered.connect(self.loadConfig)
        self.ui.actionUnboundRecordToggle.triggered.connect(self.toggleOutsideRecord)

        self.ui.actionShowLogs.triggered.connect(self.showLogs)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.stopRecordButton.setVisible(False)
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.switchRecordKeystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.switchRecordKeystrokes, False)
        )
        self.ui.deleteKey.clicked.connect(self.deleteCommand)
        self.ui.deleteAll.clicked.connect(self.deleteAllKeys)

        self.interval = self.ui.interval
        self.interval.setClearButtonEnabled(True)

        self.limit = self.ui.limit
        self.limit.setClearButtonEnabled(True)
        self.limit.setValidator(ValidateNumber())

        self.ui.remainingTime.setVisible(False)

        self.ui.stopButton.setDisabled(True)
        self.ui.stopButton.clicked.connect(self.stopBot)
        self.ui.startButton.clicked.connect(self.startBot)

        self.ui.appVersion.setText(f"v{VERSION}")

    def switchRecordKeystrokes(self, state: bool):
        self.ui.startRecordButton.setVisible(not state)
        self.ui.stopRecordButton.setVisible(state)
        self.isRecording = state

        if self.isRecordingOutside:
            if state:
                self.recorder.start()
            else:
                self.recorder.stop()

    def deleteAllKeys(self):
        self.commandModel.commands.clear()
        self.commandModel.layoutChanged.emit()
        self.ui.keyListView.clearSelection()

    def deleteCommand(self):
        indexes = self.ui.keyListView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.commandModel.commands[index.row()]
            self.commandModel.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.ui.keyListView.clearSelection()

    def toggleOutsideRecord(self, checked: bool):
        self.isRecordingOutside = checked

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.isRecording and not self.isRecordingOutside:
            if stroke := match(event):
                self.commandModel.commands.append(stroke)
                self.commandModel.layoutChanged.emit()
        if event.key() == Qt.Key.Key_Delete:
            self.deleteCommand()

    def recordOutside(self, interaction: Keystroke | MouseClick):
        self.commandModel.commands.append(interaction)
        self.commandModel.layoutChanged.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.isRecording and not self.isRecordingOutside:
            print(event)
            button = event.button()
            kind = Button.right if button is Qt.MouseButton.RightButton else Button.left
            self.commandModel.commands.append(
                MouseClick(kind=kind, pos=(event.x(), event.y()))
            )
            self.commandModel.layoutChanged.emit()

    def botThreadComplete(self):
        logger.info("bot thread complete!")
        self.ui.startButton.setDisabled(False)
        self.ui.stopButton.setDisabled(True)
        self.ui.remainingTime.setVisible(False)

    @Slot()
    def startBot(self):
        params = self.dumpConfig()

        if ValidateRangeOrNumber.validate(params.interval):
            self.ui.remainingTime.setVisible(True)
            self.ui.stopButton.setDisabled(False)
            self.ui.startButton.setDisabled(True)

            self.startTimer(500)

            self.worker = Worker(run, params)
            self.worker.signals.finished.connect(self.botThreadComplete)
            self.worker.start()

    def startTimer(
        self, interval: int, /, timerType: Qt.TimerType = Qt.TimerType.CoarseTimer
    ) -> int:
        self.timeLeft = (
            int(self.limit.text()) * 60 * 1000
        )  # Convert minutes to milliseconds
        formatTime = self.formatTime(self.timeLeft)
        logger.info(f"Starting timer with {formatTime} minutes")
        self.ui.remainingTime.setText(formatTime)
        self.botTimer.start(interval)
        return 1

    def timerTick(self):
        self.timeLeft -= 1000  # Decrease by 1 second

        if self.timeLeft <= 0:
            self.stopBot()

        self.ui.remainingTime.setText(self.formatTime(self.timeLeft))

    @Slot()
    def stopBot(self):
        logger.info("Stopping bot")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.botThreadComplete()
        self.botTimer.stop()

    def saveConfig(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Sauvegarder le fichier de config"
        )
        if folder:
            dlg = FileNameModal()
            if dlg.exec():
                saveConfig(os.path.join(folder, dlg.filename), self.dumpConfig())

    def loadConfig(self):
        dialog = QFileDialog(self, "Choisir le fichier de config")
        filename, _ = dialog.getOpenFileName(self, filter="JSON files (*.json)")
        if filename:
            params = loadConfig(filename)
            self.commandModel.commands = params.commands
            self.interval.setText(params.interval)
            self.limit.setText(str(params.limit))
            self.ui.winNum.setCurrentText(str(params.winNum))
            self.commandModel.layoutChanged.emit()

    def dumpConfig(self) -> Params:
        return Params(
            commands=self.commandModel.commands,
            interval=self.interval.text(),
            limit=int(self.limit.text()),
            winNum=int(self.ui.winNum.currentText()),
        )

    def showLogs(self):
        with open("nw-bot.log", "r") as logFile:
            logs = logFile.read()
            logViewer = LogViewerModal(logs=logs)
            logViewer.exec()

    @functools.lru_cache
    def formatTime(self, milliseconds: int) -> str:
        secs = milliseconds / 1000
        secs = secs % (24 * 3600)
        hours = secs // 3600
        secs %= 3600
        mins = secs // 60
        secs %= 60
        return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
