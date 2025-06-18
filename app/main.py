import sys
import traceback
import webbrowser

from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from .config import AppSettings, setup_logger
from .controllers.apps import AppsController
from .localdb.database import database
from .workers import make_worker_thread
from .ui.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app_ctrl: AppsController = None

        self.ui.mainStackedWidget.setCurrentIndex(1)
        self.ui.actionSource_Code.triggered.connect(
            lambda: webbrowser.open('https://github.com/NewGuy103/PasswordManagerClient')
        )

        self.setup_config()
    
    def reload_config(self):
        try:
            self.app_settings = AppSettings()
        except Exception as exc:
            tb: str = ''.join(traceback.format_exception(exc, limit=1))

            QMessageBox.critical(
                self, 'PasswordManager - Client',
                f"Could not load configuration, exiting.\nTraceback:\n\n{tb}"
            )

            self.close()

    def setup_config(self):
        try:
            self.app_settings = AppSettings()
        except Exception as exc:
            tb: str = ''.join(traceback.format_exception(exc, limit=1))

            QMessageBox.critical(
                self, 'PasswordManager - Client',
                f"Could not load configuration, exiting.\nTraceback:\n\n{tb}"
            )

            QTimer.singleShot(0, self.close)
            return
        
        setup_logger(self.app_settings.log_level)
        make_worker_thread(database.setup, self.app_loaded, self.app_load_failed)

    @Slot()
    def app_loaded(self):
        self.app_ctrl = AppsController(self)
    
    @Slot(Exception)
    def app_load_failed(self, exc: Exception):
        tb: str = ''.join(traceback.format_exception(exc, limit=1))

        QMessageBox.critical(
            self, 'PasswordManager - Client',
            f"Local database could not be loaded, exiting.\nTraceback:\n\n{tb}"
        )

        QTimer.singleShot(0, self.close)
    
    def closeEvent(self, event: QCloseEvent):
        event.accept()
        return super().closeEvent(event)


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()  # type: ignore
    mw.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
