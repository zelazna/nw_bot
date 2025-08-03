import pickle
from unittest.mock import Mock

from PySide6.QtCore import QByteArray, QModelIndex, Qt

from bot.core.constants import MIME_TYPE
from bot.models import CommandListModel


def test_command_model(stroke_factory):
    first_record, last_record = [stroke_factory() for _ in range(2)]
    cmd_model = CommandListModel([first_record, last_record])
    index = Mock(spec=QModelIndex)
    index.row.return_value = 0
    assert cmd_model.data(index, Qt.ItemDataRole.DisplayRole) == "Shift+5 200"
    assert cmd_model.rowCount() == 2
    assert cmd_model.flags(QModelIndex()) == Qt.ItemFlag.NoItemFlags
    assert cmd_model.mimeTypes() == [
        "application/x-qabstractitemmodeldatalist",
        "application/vnd.text.list",
    ]
    mime_data = cmd_model.mimeData([QModelIndex()])
    data = QByteArray()
    data.append(pickle.dumps((0, first_record)))
    mime_data.setData(MIME_TYPE, data)
    assert (
        cmd_model.canDropMimeData(mime_data, Qt.DropAction.CopyAction, 1, 1, index)
        is False
    )
    assert (
        cmd_model.canDropMimeData(mime_data, Qt.DropAction.CopyAction, 1, -1, index)
        is True
    )
    assert cmd_model.rowCount() == 2
    assert cmd_model.dropMimeData(mime_data, Qt.DropAction.CopyAction, 1, -1, index)
    assert cmd_model.commands[0] == last_record

    assert (
        cmd_model.dropMimeData(mime_data, Qt.DropAction.CopyAction, 1, 1, index)
        is False
    )

    assert (
        cmd_model.dropMimeData(mime_data, Qt.DropAction.IgnoreAction, 1, -1, index)
        is True
    )

    mime_data.setData("truc", data)
    assert (
        cmd_model.dropMimeData(mime_data, Qt.DropAction.CopyAction, 1, 1, index)
        is False
    )
