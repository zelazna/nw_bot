import functools
from typing import TYPE_CHECKING, final

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QErrorMessage, QFileDialog, QMainWindow
from pydantic import ValidationError

from bot.core.constants import APP_NAME
from bot.models import Params
from bot.ui.modals import FileNameModal
from bot.utils import recentFileManager, saveFolderManager
from bot.utils.config import ConfigService
from bot.utils.logger import logger

if TYPE_CHECKING:
    from bot.models.command_list import CommandListModel
    from bot.ui.main_window_ui import Ui_MainWindow


@final
class ConfigHandler:
    _ui: "Ui_MainWindow"
    _model: "CommandListModel"
    _window: QMainWindow
    _service: ConfigService

    def __init__(
        self,
        ui: "Ui_MainWindow",
        model: "CommandListModel",
        window: QMainWindow,
    ) -> None:
        self._ui = ui
        self._model = model
        self._window = window
        self._service = ConfigService()
        self.current_file: str | None = None

        ui.actionSaveConfig.triggered.connect(self.save)
        ui.actionSaveAs.triggered.connect(self.save_as)
        ui.actionLoadConfig.triggered.connect(self.load)

        for r in recentFileManager.load():
            action = QAction(r["path"], window)
            action.triggered.connect(functools.partial(self.load_file, r["path"]))
            ui.menuRecent.addAction(action)

    def load_file(self, filepath: str) -> None:
        logger.info(f"Loading config from {filepath}")
        try:
            if result := self._service.load(filepath):
                self._model.commands = list(result.commands)
                self._ui.interval.setText(result.interval)
                self._ui.limit.setText(str(result.limit))
                self._ui.winNum.setCurrentText(str(result.winNum))
                self._model.layoutChanged.emit()
                self._window.setWindowTitle(f"{APP_NAME} {filepath}")
                recentFileManager.add(filepath)
                self.current_file = filepath
        except FileNotFoundError:
            logger.exception("File not found")
            self.show_error(
                f"Une erreur c'est produite lors du chargement de la config: le fichier {filepath} n'a pas ete trouve"
            )
            recentFileManager.remove(filepath)
        except ValidationError as exc:
            logger.exception(f"Invalid config: {exc}")
            self.show_error(
                f"Une erreur c'est produite lors du chargement de la config: {exc!r}"
            )

    def save(self) -> None:
        cfg = self.dump()
        if self.current_file:
            self._service.save(self.current_file, cfg)
            return
        folder_name = saveFolderManager.get()

        if not folder_name:
            folder_name = QFileDialog.getExistingDirectory(
                self._window, "Sauvegarder le fichier de config"
            )
            logger.info(f"{folder_name} is chosen for saving files")
            saveFolderManager.save(folder_name)
        if folder_name:
            dlg = FileNameModal()
            if dlg.exec():
                recent = f"{folder_name}/{dlg.filename}"
                logger.info(f"Saving config to {recent}")
                self._service.save(recent, cfg)
                self._add_recent_menu_item(recent)
                self._window.setWindowTitle(f"{APP_NAME} {recent}")
                recentFileManager.add(recent)
                self.current_file = recent

    def save_as(self) -> None:
        saveFolderManager.clear()
        self.current_file = None
        self.save()

    def load(self) -> None:
        dialog = QFileDialog(self._window, "Choisir le fichier de config")
        filepath, _ = dialog.getOpenFileName(self._window, filter="JSON files (*.json)")
        if filepath:
            self.load_file(filepath)
            self._add_recent_menu_item(filepath)
            self._window.setWindowTitle(f"{APP_NAME} {filepath}")

    def dump(self) -> Params:
        return Params(
            commands=tuple(self._model.commands),
            interval=self._ui.interval.text() or "1",
            limit=int(self._ui.limit.text()),
            winNum=int(self._ui.winNum.currentText()),
        )

    def show_error(self, message: str) -> None:
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec_()

    def _add_recent_menu_item(self, path: str) -> None:
        action = QAction(path, self._window)
        action.triggered.connect(lambda: self.load_file(path))
        self._ui.menuRecent.addAction(action)
