import pickle

from PySide6.QtCore import QMimeData, QModelIndex, Qt
import pytest

from bot.core.constants import MIME_TYPE
from bot.models.command_list import CommandListModel


class DummyCommand:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"DummyCommand({self.name})"

    def execute(self): ...


def test_row_count():
    model = CommandListModel([DummyCommand("A"), DummyCommand("B")])
    assert model.rowCount() == 2


def test_data_display_role():
    cmd = DummyCommand("Test")
    model = CommandListModel([cmd])
    index = model.index(0)
    assert model.data(index, Qt.ItemDataRole.DisplayRole) == repr(cmd)


def test_flags_valid_index():
    model = CommandListModel([DummyCommand("A")])
    index = model.index(0)
    flags = model.flags(index)
    assert flags & Qt.ItemFlag.ItemIsDragEnabled
    assert flags & Qt.ItemFlag.ItemIsDropEnabled


def test_mime_types_contains_custom_type():
    model = CommandListModel()
    assert MIME_TYPE in model.mimeTypes()


def test_mime_data_serialization():
    cmd = DummyCommand("Serialized")
    model = CommandListModel([cmd])
    index = model.index(0)
    mime_data = model.mimeData([index])

    assert mime_data.hasFormat(MIME_TYPE)
    bytes_array = mime_data.data(MIME_TYPE)
    idx, loaded_cmd = pickle.loads(bytes(bytes_array.data()))
    assert idx == 0
    assert repr(loaded_cmd) == repr(cmd)


def test_can_drop_mime_data_valid():
    model = CommandListModel()
    mime_data = QMimeData()
    mime_data.setData(MIME_TYPE, pickle.dumps((0, DummyCommand("DropMe"))))
    assert model.canDropMimeData(
        mime_data, Qt.DropAction.MoveAction, 0, 0, QModelIndex()
    )


def test_can_drop_mime_data_invalid():
    model = CommandListModel()
    mime_data = QMimeData()
    mime_data.setData("Hello", pickle.dumps((0, DummyCommand("DropMe"))))
    assert (
        model.canDropMimeData(mime_data, Qt.DropAction.MoveAction, 0, 0, QModelIndex())
        is False
    )

    mime_data.setData(MIME_TYPE, pickle.dumps((0, DummyCommand("DropMe"))))
    assert (
        model.canDropMimeData(mime_data, Qt.DropAction.MoveAction, 0, 15, QModelIndex())
        is False
    )


def test_drop_mime_data_moves_item():
    cmds = [
        DummyCommand("One"),
        DummyCommand("Two"),
        DummyCommand("Three"),
    ]
    model = CommandListModel(cmds.copy())

    # Move "One" (index 0) after "Three" (index 2)
    mime_data = QMimeData()
    mime_data.setData(MIME_TYPE, pickle.dumps((0, cmds[0])))

    model.dropMimeData(mime_data, Qt.DropAction.MoveAction, 1, 0, QModelIndex())
    assert [cmd.name for cmd in model.commands] == ["Two", "Three", "One"]  # type: ignore


@pytest.mark.parametrize(
    ("params", "expected"),
    [
        ((Qt.DropAction.IgnoreAction, 1, 0, QModelIndex()), True),
        ((Qt.DropAction.MoveAction, 1, 15, QModelIndex()), False),
    ],
)
def test_drop_mime_data_returns(params, expected):
    model = CommandListModel()
    mime_data = QMimeData()
    mime_data.setData(MIME_TYPE, pickle.dumps((0, "")))
    assert model.dropMimeData(mime_data, *params) is expected
