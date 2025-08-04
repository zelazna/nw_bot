import pytest
from bot.utils.settings_manager import RecentFileManager, SaveFolderManager


@pytest.fixture
def recent_manager():
    manager = RecentFileManager()
    manager.max_items = 3
    yield manager
    manager.clear()
    return manager


@pytest.fixture
def save_folder_manager():
    manager = SaveFolderManager()
    yield manager
    manager.clear()
    return manager


def test_add_and_load_recent(recent_manager):
    path = "/tmp/test.txt"
    recent_manager.add(path)
    recents = recent_manager.load()
    assert len(recents) == 1
    assert recents[0]["path"] == path


def test_no_duplicates(recent_manager):
    path = "/tmp/unique.txt"
    recent_manager.add(path)
    recent_manager.add(path)
    recents = recent_manager.load()
    assert len(recents) == 1


def test_ordering_recent(recent_manager):
    recent_manager.add("/tmp/1.txt")
    recent_manager.add("/tmp/2.txt")
    recent_manager.add("/tmp/3.txt")
    recents = recent_manager.load()
    assert recents[0]["path"] == "/tmp/3.txt"
    assert recents[1]["path"] == "/tmp/2.txt"
    assert recents[2]["path"] == "/tmp/1.txt"


def test_max_items_recent(recent_manager):
    recent_manager.add("/tmp/1.txt")
    recent_manager.add("/tmp/2.txt")
    recent_manager.add("/tmp/3.txt")
    recent_manager.add("/tmp/4.txt")
    recents = recent_manager.load()
    assert len(recents) == 3
    assert "/tmp/1.txt" not in [r["path"] for r in recents]


def test_remove_recent(recent_manager):
    recent_manager.add("/tmp/delete.txt")
    recent_manager.remove("/tmp/delete.txt")
    assert not recent_manager.exists("/tmp/delete.txt")


def test_save_and_get_folder(save_folder_manager):
    path = "/home/test/folder"
    save_folder_manager.save(path)
    assert save_folder_manager.get() == path


def test_clear_folder(save_folder_manager):
    save_folder_manager.save("/tmp/some_folder")
    save_folder_manager.clear()
    assert save_folder_manager.get() is None
