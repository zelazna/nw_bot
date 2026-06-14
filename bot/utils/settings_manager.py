from dataclasses import dataclass
from typing import ClassVar, final
from PySide6.QtCore import QSettings

from bot.core.constants import APP_NAME


class BaseSetting:
    settings: ClassVar[QSettings] = QSettings("Zelazna", APP_NAME)
    key: ClassVar[str]


@final
@dataclass
class RecentFileManager(BaseSetting):
    key: ClassVar[str] = "recents"
    max_items: ClassVar[int] = 5

    def load(self) -> list[dict[str, str]]:
        recents: list[dict[str, str]] = []
        size = self.settings.beginReadArray(self.key)
        for i in range(size):
            self.settings.setArrayIndex(i)
            recents.append({"path": self.settings.value("path")})
        self.settings.endArray()
        return recents

    def save(self, recents: list[dict[str, str]]) -> None:
        self.settings.beginWriteArray(self.key)
        for i, recent in enumerate(recents[: self.max_items]):
            self.settings.setArrayIndex(i)
            self.settings.setValue("path", recent["path"])
        self.settings.endArray()

    def add(self, path: str) -> None:
        recents = self.load()
        recents = [r for r in recents if r["path"] != path]
        recents.insert(0, {"path": path})
        self.save(recents)

    def remove(self, path: str) -> None:
        recents = self.load()
        recents = [r for r in recents if r["path"] != path]
        self.save(recents)

    def clear(self) -> None:
        self.save([])

    def exists(self, path: str) -> bool:
        return any(r["path"] == path for r in self.load())


@final
@dataclass
class SaveFolderManager(BaseSetting):
    key: ClassVar[str] = "bot/saveFolder"

    def get(self) -> str | None:
        return self.settings.value(self.key)  # pyright: ignore[reportAny]

    def save(self, folder_name: str) -> None:
        self.settings.setValue(self.key, folder_name)

    def clear(self) -> None:
        self.settings.remove(self.key)


saveFolderManager = SaveFolderManager()
recentFileManager = RecentFileManager()
