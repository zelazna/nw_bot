from typing import Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt


class KeysModel(QAbstractListModel):
    def __init__(self, keys: list[str] | None = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.keys: list[str] = keys if keys else []

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = 0
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.keys[index.row()]

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self.keys)
