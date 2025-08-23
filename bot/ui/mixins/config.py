import functools
from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QErrorMessage, QFileDialog, QMainWindow

from bot.core.constants import APP_NAME
from bot.models import Params
from bot.ui.modals import FileNameModal
from bot.utils import recentFileManager, saveFolderManager
from bot.utils.config import loadConfig, saveConfig
from bot.utils.logger import logger

if TYPE_CHECKING:
    from bot.core.keystroke_adapter import QtKeystrokeAdapter
    from bot.core.mouse_adapter import MouseAdapter
    from bot.core.recorder import Recorder
    from bot.models.command_list import CommandListModel
    from bot.ui.main_window_ui import Ui_MainWindow


class ConfigMixin(QMainWindow):
    ui: "Ui_MainWindow"
    recorder: "Recorder"
    commandModel: "CommandListModel"
    key_stroke_adapter: "QtKeystrokeAdapter"
    mouse_adapter: "MouseAdapter"
    isRecording: bool

    def setupConfig(self):
        self.ui.actionSaveConfig.triggered.connect(self.saveConfig)
        self.ui.actionSaveAs.triggered.connect(self.saveConfigAs)
        self.ui.actionLoadConfig.triggered.connect(self.loadConfig)

        for r in recentFileManager.load():
            action = QAction(r["path"], self)
            action.triggered.connect(functools.partial(self.loadConfigFile, r["path"]))
            self.ui.menuRecent.addAction(action)

    def loadConfigFile(self, filepath: str):
        logger.info(f"Loading config from {filepath}")
        try:
            result = loadConfig(filepath)
            if isinstance(result, Params):
                self.commandModel.commands = result.commands
                self.ui.interval.setText(result.interval)
                self.ui.limit.setText(str(result.limit))
                self.ui.winNum.setCurrentText(str(result.winNum))
                self.commandModel.layoutChanged.emit()
                self.setWindowTitle(f"{APP_NAME} {filepath}")
                recentFileManager.add(filepath)
                self.currentFile = filepath
        except FileNotFoundError:
            logger.exception("Error loading config", exc_info=True)
            self._showErrorModal(
                "Une erreur c'est produite lors du chargement de la config: "
                f"le fichier {filepath} n'a pas ete trouve"
            )
            recentFileManager.remove(filepath)
        except Exception as exc:
            logger.exception("Error loading config", exc_info=True)
            self._showErrorModal(
                f"Une erreur c'est produite lors du chargement de la config: {exc!r}"
            )

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
            interval=self.ui.interval.text(),
            limit=int(self.ui.limit.text()),
            winNum=int(self.ui.winNum.currentText()),
        )

    def addRecentMenuItem(self, path: str):
        action = QAction(path, self)
        action.triggered.connect(lambda: self.loadConfigFile(path))
        self.ui.menuRecent.addAction(action)

    def _showErrorModal(self, message: str):
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec_()
