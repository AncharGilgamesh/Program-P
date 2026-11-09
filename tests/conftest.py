import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Одно приложение Qt на прогон. Окно не показывается."""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    return application
