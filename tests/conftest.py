import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    return application
