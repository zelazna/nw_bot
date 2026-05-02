import logging
import pickle
from collections.abc import Sequence
from typing import final, override

from PySide6.QtCore import (
    QAbstractListModel,
    QByteArray,
    QMimeData,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
)

from bot.core.constants import MIME_TYPE
from bot.models.keyboard import DirectionalKeystroke, Keystroke
from bot.models.mouse import MouseClick

Index = QModelIndex | QPersistentModelIndex


@final
class CommandListModel(QAbstractListModel):
    commands: list[Keystroke | DirectionalKeystroke | MouseClick]

    def __init__(
        self,
        commands: list[Keystroke | DirectionalKeystroke | MouseClick] | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.commands = commands if commands else []

    @override
    def data(self, index: Index, role: int = 0) -> object:
        if not index.isValid():
            return None
        if not (0 <= index.row() < len(self.commands)):
            return None
        command = self.commands[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return repr(command)
        if role == Qt.ItemDataRole.UserRole:
            return command
        return None

    @override
    def rowCount(self, parent: Index = QModelIndex()) -> int:  # pyright: ignore[reportCallInDefaultInitializer]
        return len(self.commands)

    @override
    def flags(self, index: Index) -> Qt.ItemFlag:
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemFlag.ItemIsDragEnabled
        else:
            flags |= Qt.ItemFlag.ItemIsDropEnabled
        return flags

    @override
    def supportedDropActions(self) -> Qt.DropAction:
        return Qt.DropAction.MoveAction

    @override
    def mimeTypes(self) -> list[str]:
        types = super().mimeTypes()
        types.append(MIME_TYPE)
        return types

    @override
    def mimeData(self, indexes: Sequence[QModelIndex]) -> QMimeData:
        mimeData = QMimeData()
        data = QByteArray()

        for idx in indexes:
            if idx.isValid():
                row = idx.row()
                data.append(pickle.dumps((row, self.commands[row])))

        mimeData.setData(MIME_TYPE, data)
        return mimeData

    def add_command(
        self, command: Keystroke | DirectionalKeystroke | MouseClick
    ) -> None:
        self.commands.append(command)
        self.layoutChanged.emit()

    @override
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

    @override
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
        before_index, command = pickle.loads(data.data(MIME_TYPE).data())  # pyright: ignore[reportAny]

        logging.debug(f"Item {command} from idx {before_index} to idx {insert_at}")

        if before_index == insert_at or before_index + 1 == insert_at:
            return True

        root = QModelIndex()
        if not self.beginMoveRows(root, before_index, before_index, root, insert_at):  # pyright: ignore[reportAny]  # pragma: no cover
            return True  # pragma: no cover
        item = self.commands.pop(before_index)  # pyright: ignore[reportAny]
        if before_index < insert_at:
            insert_at -= 1
        self.commands.insert(insert_at, item)
        self.endMoveRows()

        return True
