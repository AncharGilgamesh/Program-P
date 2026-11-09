"""Дата собрания без показа окна. Фикстура qapp уже поднимает QApplication."""

import re

import pytest

from View.meetingdatedialog import MeetingDateDialog

pytestmark = pytest.mark.usefixtures("qapp")


def test_meeting_date_is_day_month_year():
    dialog = MeetingDateDialog(["4411 – Учебная практика"])
    date_str = dialog.get_results()[1]
    assert re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", date_str)
