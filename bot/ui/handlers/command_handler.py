from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from bot.models.command_list import CommandListModel
    from bot.ui.main_window_ui import Ui_MainWindow


@final
class CommandHandler:
    _ui: "Ui_MainWindow"
    _model: "CommandListModel"

    def __init__(self, ui: "Ui_MainWindow", model: "CommandListModel") -> None:
        self._ui = ui
        self._model = model

        ui.deleteKey.clicked.connect(self.delete)
        ui.deleteAll.clicked.connect(self.delete_all)
        ui.remainingTime.setVisible(False)

    def delete(self) -> None:
        indexes = self._ui.keyListView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self._model.commands[index.row()]
            self._model.layoutChanged.emit()
            self._ui.keyListView.clearSelection()

    def delete_all(self) -> None:
        self._model.commands.clear()
        self._model.layoutChanged.emit()
        self._ui.keyListView.clearSelection()
