from typing import Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt


class KeysModel(QAbstractListModel):
    def __init__(self, keys: list[tuple[int, str]] | None = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.keys: list[tuple[int, str]] = keys if keys else []

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = 0
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            _, key = self.keys[index.row()]
            return key

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self.keys)
