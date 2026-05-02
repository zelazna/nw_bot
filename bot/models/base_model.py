from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import ClassVar, Protocol

from pydantic import BaseModel, ConfigDict


class KeyboardExecutor(Protocol):
    def pressed(self, key: object) -> AbstractContextManager[None]: ...


class MouseExecutor(Protocol):
    def click(self, button: object) -> None: ...


class Command(ABC):
    is_reportable: ClassVar[bool] = True

    @abstractmethod
    def execute(self) -> None: ...


class BotBaseModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True, extra="forbid", frozen=True)
