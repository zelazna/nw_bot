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


def test_data_invalid_index():
    model = CommandListModel([DummyCommand("A")])
    assert model.data(QModelIndex()) is None


def test_data_out_of_bounds():
    model = CommandListModel([DummyCommand("A")])
    stale = model.index(0)
    model.commands.clear()
    assert model.data(stale) is None


def test_data_user_role():
    cmd = DummyCommand("X")
    model = CommandListModel([cmd])
    index = model.index(0)
    assert model.data(index, Qt.ItemDataRole.UserRole) is cmd


def test_data_unknown_role_returns_none():
    model = CommandListModel([DummyCommand("X")])
    index = model.index(0)
    assert model.data(index, Qt.ItemDataRole.DecorationRole) is None


def test_supported_drop_actions():
    model = CommandListModel()
    assert model.supportedDropActions() == Qt.DropAction.MoveAction


def test_flags_valid_index():
    model = CommandListModel([DummyCommand("A")])
    valid_index = model.index(0)
    assert model.flags(valid_index) & Qt.ItemFlag.ItemIsDragEnabled
    # Only the root (invalid) index accepts drops — individual items are drag sources only
    assert model.flags(QModelIndex()) & Qt.ItemFlag.ItemIsDropEnabled


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


def test_drop_mime_data_noop():
    cmds = [DummyCommand("A"), DummyCommand("B")]
    model = CommandListModel(cmds.copy())
    mime_data = QMimeData()
    mime_data.setData(MIME_TYPE, pickle.dumps((0, cmds[0])))
    result = model.dropMimeData(
        mime_data, Qt.DropAction.MoveAction, 0, 0, QModelIndex()
    )
    assert result is True
    assert [cmd.name for cmd in model.commands] == ["A", "B"]


def test_drop_mime_data_moves_item():
    cmds = [
        DummyCommand("One"),
        DummyCommand("Two"),
        DummyCommand("Three"),
    ]
    model = CommandListModel(cmds.copy())

    # Move "One" (index 0) after "Three" (index 2): row=3 means "insert before end"
    mime_data = QMimeData()
    mime_data.setData(MIME_TYPE, pickle.dumps((0, cmds[0])))

    model.dropMimeData(mime_data, Qt.DropAction.MoveAction, 3, 0, QModelIndex())
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
