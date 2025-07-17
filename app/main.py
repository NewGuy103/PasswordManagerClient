import sys
import traceback
import webbrowser

from PySide6.QtCore import QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from .config import AppSettings, setup_logger
from .controllers.apps import AppsController
from .ui.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app_ctrl: AppsController = None

        self.ui.mainStackedWidget.setCurrentIndex(1)
        self.ui.actionSource_Code.triggered.connect(
            lambda: webbrowser.open("https://github.com/NewGuy103/PasswordManagerClient")
        )

        self.setup_config()

    def reload_config(self):
        try:
            self.app_settings = AppSettings()
        except Exception as exc:
            tb: str = "".join(traceback.format_exception(exc, limit=1))

            QMessageBox.critical(
                self, "PasswordManager - Client", f"Could not load configuration, exiting.\nTraceback:\n\n{tb}"
            )

            self.close()

    def setup_config(self):
        try:
            self.app_settings = AppSettings()
        except Exception as exc:
            tb: str = "".join(traceback.format_exception(exc, limit=1))

            QMessageBox.critical(
                self, "PasswordManager - Client", f"Could not load configuration, exiting.\nTraceback:\n\n{tb}"
            )

            QTimer.singleShot(0, self.close)
            return

        setup_logger(self.app_settings.log_level)
        self.app_ctrl = AppsController(self)

    def closeEvent(self, event: QCloseEvent):
        if self.app_ctrl:
            if self.app_ctrl.pw_tab.db is not None:
                self.app_ctrl.pw_tab.db.close()

            if self.app_ctrl.pw_tab.client is not None:
                self.app_ctrl.pw_tab.client.close()

        event.accept()
        return super().closeEvent(event)


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()  # type: ignore
    mw.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
