from typing import Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt

from bot.core import Keystroke


class KeysModel(QAbstractListModel):
    def __init__(self, keys: list[Keystroke] | None = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.keys: list[Keystroke] = keys if keys else []

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = 0
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            stroke = self.keys[index.row()]
            return repr(stroke)

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self.keys)
