import typing

from PySide6.QtCore import QAbstractListModel, QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QDialog, QHeaderView, QMenu, QMessageBox

from ...models import AddPasswordEntryData
from ...ui.add_password_entry_dialog import Ui_AddPasswordEntryDialog
from ...workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..apps import AppsController


class PasswordEntriesModel(QAbstractListModel):
    def __init__(self, /, parent: 'PasswordsTabController' = None):
        super().__init__(parent)
        self.pw_ctrl = parent

        self.entries: list = []
    
    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.entries[index.row()]
            return text
    
    def rowCount(self, /, index):
        return len(self.entries)
    
    def add_data(self, data: AddPasswordEntryData) -> None:
        # TODO: Format this properly
        self.entries.append(f"Entry name: {data.entry_name} - {data.username} | {data.password} | {data.url}")

    
class PasswordsTabController(QObject):
    def __init__(self, app_parent: 'AppsController'):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        self.ui_setup()

        # Controllers
        self.entries_view_ctrl = PasswordEntriesViewController(self)

    def ui_setup(self):
        self.ui.passwordGroupsTreeWidget.header().setStretchLastSection(False)

        for column in range(self.ui.passwordGroupsTreeWidget.model().columnCount()):
            self.ui.passwordGroupsTreeWidget.header().setSectionResizeMode(
                column, QHeaderView.ResizeMode.ResizeToContents
            )
            
        self.ui.passwordGroupsTreeWidget.expandAll()


class PasswordEntriesViewController(QObject):
    def __init__(self, pw_parent: PasswordsTabController):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui
    
        self.entries_model = PasswordEntriesModel(parent=self)
        self.ui.passwordEntriesListView.setModel(self.entries_model)

        self.ui.passwordEntriesListView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.passwordEntriesListView.customContextMenuRequested.connect(self.context_menu_event)
    
    @Slot()
    def context_menu_event(self, pos):
        context = QMenu(self.mw_parent)

        list_add_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        add_entry_action = QAction("Add entry", self, icon=list_add_icon)

        add_entry_action.triggered.connect(self.add_password_entry)

        context.addAction(add_entry_action)
        context.exec(self.ui.passwordEntriesListView.mapToGlobal(pos))

    @Slot()
    def add_password_entry(self):
        dialog = AddPasswordEntryDialog(self)

        @Slot(AddPasswordEntryData)
        def dialog_accepted(data: AddPasswordEntryData):
            self.entries_model.add_data(data)
            self.entries_model.layoutChanged.emit()
        
        dialog.dataComplete.connect(dialog_accepted)
        dialog.exec()

        dialog.deleteLater()


class AddPasswordEntryDialog(QDialog):
    dataComplete = Signal(AddPasswordEntryData)
    def __init__(self, /, parent: PasswordEntriesViewController):
        super().__init__(parent.mw_parent)
        self.ui = Ui_AddPasswordEntryDialog()
        
        self.pw_parent = parent
        self.ui.setupUi(self)
    
    def accept(self):
        entry_name = self.ui.entryNameLineEdit.text()
        username = self.ui.usernameLineEdit.text()

        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()

        data = AddPasswordEntryData(
            entry_name=entry_name,
            username=username,
            password=password,
            url=url
        )

        self.dataComplete.emit(data)
        return super().accept()
