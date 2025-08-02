from unittest.mock import Mock
from bot.models import CommandsModel
from PySide6.QtCore import Qt, QModelIndex


# TODO: https://pytest-qt.readthedocs.io/en/4.5.0/index.html
def test_command_model(stroke_factory):
    cmd_model = CommandsModel([stroke_factory()])
    index = Mock(spec=QModelIndex)
    index.row.return_value = 0
    assert cmd_model.data(index, Qt.ItemDataRole.DisplayRole) == "Shift+5"
    assert cmd_model.rowCount() == 1
    assert cmd_model.flags(QModelIndex()) == Qt.ItemFlag.NoItemFlags
    assert cmd_model.mimeTypes() == [
        "application/x-qabstractitemmodeldatalist",
        "application/vnd.text.list",
    ]
    mime_data = cmd_model.mimeData([QModelIndex()])
    assert mime_data.data("application/vnd.text.list") == ""
    assert (
        cmd_model.canDropMimeData(mime_data, Qt.DropAction.CopyAction, 1, 1, index)
        is False
    )
    assert (
        cmd_model.canDropMimeData(mime_data, Qt.DropAction.CopyAction, 1, -1, index)
        is True
    )
