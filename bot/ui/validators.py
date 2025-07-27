import re
from PySide6.QtGui import QValidator


class ValidateNumber(QValidator):
    def validate(self, num: str, index: int) -> tuple[QValidator.State, str, int]:
        pattern = re.compile("[0-9]{1,3}")

        if pattern.fullmatch(num):
            return QValidator.State.Acceptable, num, index

        return QValidator.State.Invalid, num, index


class ValidateRangeOrNumber:
    @staticmethod
    def validate(num: str) -> bool:
        pattern = re.compile(r"^\d+(-\d+)?$")

        if pattern.fullmatch(num):
            return True

        return False
