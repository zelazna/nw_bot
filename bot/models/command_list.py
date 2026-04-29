import logging
import pickle
from typing import Any, List, Sequence

from PySide6.QtCore import (
    QAbstractListModel,
    QByteArray,
    QMimeData,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from bot.core.constants import MIME_TYPE
from bot.models.keyboard import DirectionalKeystroke, Keystroke
from bot.models.mouse import MouseClick

Index = QModelIndex | QPersistentModelIndex


class CommandListModel(QAbstractListModel):
    def __init__(
        self,
        commands: list[Keystroke | DirectionalKeystroke | MouseClick] | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.commands = commands if commands else []

    def data(self, index: Index, role: int = 0):
        if not index.isValid():
            return None
        command = self.commands[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return repr(command)
        if role == Qt.ItemDataRole.UserRole:
            return command

    def rowCount(self, parent: Index = QModelIndex()) -> int:
        return len(self.commands)

    def flags(self, index: Index) -> Qt.ItemFlag:
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemFlag.ItemIsDragEnabled
        else:
            flags |= Qt.ItemFlag.ItemIsDropEnabled
        return flags

    def supportedDropActions(self) -> Qt.DropAction:
        return Qt.DropAction.MoveAction

    def mimeTypes(self) -> List[str]:
        types = super().mimeTypes()
        types.append(MIME_TYPE)
        return types

    def mimeData(self, indexes: Sequence[QModelIndex]) -> QMimeData:
        mimeData = QMimeData()
        data = QByteArray()

        for idx in indexes:
            if idx.isValid():
                idx = idx.row()
                data.append(pickle.dumps((idx, self.commands[idx])))

        mimeData.setData(MIME_TYPE, data)
        return mimeData

    def canDropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Index,
    ) -> bool:
        if not data.hasFormat(MIME_TYPE):
            return False
        if column > 0:
            return False
        return True

    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Index,
    ) -> bool:
        if not self.canDropMimeData(data, action, row, column, parent):
            return False
        if action is Qt.DropAction.IgnoreAction:
            return True
        insert_at = row if row != -1 else self.rowCount(QModelIndex())
        before_index, command = pickle.loads(data.data(MIME_TYPE).data())

        logging.debug(f"Item {command} from idx {before_index} to idx {insert_at}")

        if before_index == insert_at or before_index + 1 == insert_at:
            return True

        self.beginResetModel()
        item = self.commands.pop(before_index)
        if before_index < insert_at:
            insert_at -= 1
        self.commands.insert(insert_at, item)
        self.endResetModel()

        return True
