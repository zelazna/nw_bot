from bot.ui.validators import ValidateNumber, ValidateRangeOrNumber
from PySide6.QtGui import QValidator
import pytest

test_cases = [
    (True, "5"),
    (True, "123"),
    (True, "5-10"),
    (True, "123-456"),
    (False, "12-"),
    (False, "-34"),
    (False, "abc"),
    (False, "12-34-56"),
]


@pytest.mark.parametrize(("expected", "input"), test_cases)
def test_validate_range(expected: QValidator.State, input: str):
    result = ValidateRangeOrNumber.validate(input)
    assert result == expected


test_cases = [
    (QValidator.State.Acceptable, "5"),
    (QValidator.State.Acceptable, "50"),
    (QValidator.State.Acceptable, "500"),
    (QValidator.State.Invalid, "abc"),
    (QValidator.State.Invalid, "1234"),
    (QValidator.State.Invalid, "12-34-56"),
]


@pytest.mark.parametrize(("expected", "input"), test_cases)
def test_validate_num(expected: QValidator.State, input: str):
    state, *_ = ValidateNumber().validate(input, 1)
    assert state == expected
