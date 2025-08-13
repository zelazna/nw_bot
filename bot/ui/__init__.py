import functools

from PySide6.QtCore import Qt, QTimerEvent, Slot
from PySide6.QtGui import QAction, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QErrorMessage, QFileDialog, QMainWindow

from bot.core.constants import APP_NAME, PADDING_IN_S, TIMER_TIMEOUT_MILLISEC, VERSION
from bot.core.control import run
from bot.core.keystroke_adapter import QtKeystrokeAdapter
from bot.core.mouse_adapter import MouseAdapter
from bot.core.recorder import Recorder
from bot.core.worker import Worker
from bot.models import CommandListModel, Params
from bot.ui.main_window import Ui_MainWindow
from bot.ui.modals import FileNameModal, LogViewerModal
from bot.ui.validators import ValidateNumber, ValidateRangeOrNumber
from bot.utils import format_time, recentFileManager, saveFolderManager
from bot.utils.config import loadConfig, saveConfig
from bot.utils.logger import logger

OUTSIDE_BUTTON_STYLE = "background-color: #0067c0; color:white;"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.isRecording = False
        self.timeLeft = 0
        self.timer_id = 0
        self.validator = ValidateRangeOrNumber()
        self.currentFile = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.commandModel = CommandListModel()
        self.ui.keyListView.setModel(self.commandModel)
        self.ui.keyListView.setDragEnabled(True)
        self.ui.keyListView.setAcceptDrops(True)
        self.ui.keyListView.setDropIndicatorShown(True)

        self.recorder = Recorder(self.commandModel)
        self.key_stroke_adapter = QtKeystrokeAdapter(self.commandModel)
        self.mouse_adapter = MouseAdapter(self.commandModel)

        self.ui.actionSaveConfig.triggered.connect(self.saveConfig)
        self.ui.actionSaveAs.triggered.connect(self.saveConfigAs)
        self.ui.actionLoadConfig.triggered.connect(self.loadConfig)
        self.ui.actionUnboundRecordToggle.triggered.connect(self.toggleOutsideRecord)

        for r in recentFileManager.load():
            action = QAction(r["path"], self)
            action.triggered.connect(lambda: self.loadConfigFile(r["path"]))
            self.ui.menuRecent.addAction(action)

        self.ui.actionShowLogs.triggered.connect(self.showLogs)

        for i in range(1, 10):
            self.ui.winNum.addItem(str(i))

        self.ui.stopRecordButton.setVisible(False)
        self.ui.startRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, True)
        )
        self.ui.stopRecordButton.clicked.connect(
            functools.partial(self.toggleRecordKeystrokes, False)
        )

        self.ui.startRecordOutsideButton.clicked.connect(self.startRecordOutside)
        self.ui.stopRecordOutsideButton.clicked.connect(self.stopRecordOutside)
        self.ui.startRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
        self.ui.stopRecordOutsideButton.setStyleSheet(OUTSIDE_BUTTON_STYLE)
        self.ui.startRecordOutsideButton.setVisible(False)
        self.ui.stopRecordOutsideButton.setVisible(False)

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

    def toggleRecordKeystrokes(self, state: bool):
        self.ui.startRecordButton.setVisible(not state)
        self.ui.stopRecordButton.setVisible(state)
        self.isRecording = state

    def startRecordOutside(self):
        self.recorder.start()
        self.isRecording = False
        self.ui.startRecordOutsideButton.setVisible(False)
        self.ui.stopRecordOutsideButton.setVisible(True)

    def stopRecordOutside(self):
        self.ui.startRecordOutsideButton.setVisible(True)
        self.ui.stopRecordOutsideButton.setVisible(False)
        self.recorder.stop()

    def toggleOutsideRecord(self, checked: bool):
        if self.isRecording:
            self.toggleRecordKeystrokes(False)
        self.ui.startRecordButton.setVisible(not checked)
        self.ui.startRecordOutsideButton.setVisible(checked)

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

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.isRecording:
            self.key_stroke_adapter.on_key_release(event)
        if event.key() == Qt.Key.Key_Delete:
            self.deleteCommand()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.isRecording:
            self.mouse_adapter.on_click(event.x(), event.y(), event.button(), True)

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

            self.timeLeft = int(self.limit.text()) * 60 * 1000 + (
                PADDING_IN_S * 1000
            )  # Convert minutes to milliseconds
            self.timer_id = self.startTimer(TIMER_TIMEOUT_MILLISEC)
            logger.info(f"Starting timer with {format_time(self.timeLeft)} minutes")

            self.worker = Worker(run, params)
            self.worker.signals.finished.connect(self.botThreadComplete)
            self.worker.start()

    def timerEvent(self, event: QTimerEvent) -> None:
        self.timeLeft -= TIMER_TIMEOUT_MILLISEC  # Decrease by 0.5 second
        self.ui.remainingTime.setText(format_time(self.timeLeft))

    @Slot()
    def stopBot(self):
        logger.info("Stopping bot")
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
            self.worker.terminate()
        self.botThreadComplete()
        self.killTimer(self.timer_id)

    def addRecentMenuItem(self, path: str):
        action = QAction(path, self)
        action.triggered.connect(lambda: self.loadConfigFile(path))
        self.ui.menuRecent.addAction(action)

    def loadConfigFile(self, filepath: str):
        logger.info(f"Loading config from {filepath}")
        try:
            result = loadConfig(filepath)
            if isinstance(result, Params):
                self.commandModel.commands = result.commands
                self.interval.setText(result.interval)
                self.limit.setText(str(result.limit))
                self.ui.winNum.setCurrentText(str(result.winNum))
                self.commandModel.layoutChanged.emit()
                self.setWindowTitle(f"{APP_NAME} {filepath}")
                recentFileManager.add(filepath)
                self.currentFile = filepath
        except FileNotFoundError:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                "Une erreur c'est produite lors du chargement de la config: "
                f"le fichier {filepath} n'a pas ete trouve"
            )
            error_dialog.exec_()
            recentFileManager.remove(filepath)

    def saveConfig(self):
        cfg = self.dumpConfig()
        if self.currentFile:
            saveConfig(self.currentFile, cfg)
            return
        folder_name = saveFolderManager.get()

        if not folder_name:
            folder_name = QFileDialog.getExistingDirectory(
                self, "Sauvegarder le fichier de config"
            )
            logger.info(f"{folder_name} is chosen for saving files")
            saveFolderManager.save(folder_name)
        if folder_name:
            dlg = FileNameModal()
            if dlg.exec():
                recent = f"{folder_name}/{dlg.filename}"
                logger.info(f"Saving config to {recent}")
                saveConfig(recent, cfg)
                self.addRecentMenuItem(recent)
                self.setWindowTitle(f"{APP_NAME} {recent}")
                recentFileManager.add(recent)
                self.currentFile = recent

    def saveConfigAs(self):
        saveFolderManager.clear()
        self.currentFile = None
        self.saveConfig()

    def loadConfig(self):
        dialog = QFileDialog(self, "Choisir le fichier de config")
        filepath, _ = dialog.getOpenFileName(self, filter="TXT files (*.txt)")
        if filepath:
            self.loadConfigFile(filepath)
            self.addRecentMenuItem(filepath)
            self.setWindowTitle(f"{APP_NAME} {filepath}")

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
