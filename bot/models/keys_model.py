import logging
import pickle
from typing import TYPE_CHECKING, Any, List, Sequence

from PySide6.QtCore import (
    QAbstractListModel,
    QMimeData,
    Qt,
    QModelIndex,
    QPersistentModelIndex,
    QByteArray,
)

from bot.core.constants import MIME_TYPE

if TYPE_CHECKING:
    from bot.models import Keystroke


Index = QModelIndex | QPersistentModelIndex


class KeysModel(QAbstractListModel):
    def __init__(
        self, keys: list["Keystroke"] | None = None, *args: Any, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.keys: list["Keystroke"] = keys if keys else []

    def data(self, index: Index, role: int = 0) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            stroke = self.keys[index.row()]
            return repr(stroke)

    def rowCount(self, parent: Index = QModelIndex()) -> int:
        return len(self.keys)

    def flags(self, index: Index) -> Qt.ItemFlag:
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled
        return flags

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
                data.append(pickle.dumps((idx, self.keys[idx])))

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

        if row != -1:
            after_index = row
        elif parent.isValid():
            after_index = parent.row()
        else:
            after_index = self.rowCount(QModelIndex())
        before_index, stroke = pickle.loads(data.data(MIME_TYPE).data())

        logging.debug(f"Item {stroke} from idx {before_index} to idx {after_index}")

        self.beginResetModel()
        item = self.keys.pop(before_index)
        self.keys.insert(after_index + 1, item)
        self.endResetModel()

        return True
