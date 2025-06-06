import typing

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QMessageBox

from .tabs.passwords import PasswordsTabController

if typing.TYPE_CHECKING:
    from ..main import MainWindow


class AppsController(QObject):
    def __init__(self, mw_parent: 'MainWindow'):
        super().__init__(mw_parent)

        self.mw_parent = mw_parent
        self.ui = mw_parent.ui

        self.ui.appTabWidget.setCurrentIndex(0)  # passwords tab
        self.pw_tab = PasswordsTabController(self)
