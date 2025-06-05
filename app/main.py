import sys
import traceback
import webbrowser

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
            lambda: webbrowser.open('https://github.com/NewGuy103/PasswordManagerClient')
        )

        self.setup_config()
    
    def reload_config(self):
        try:
            self.app_settings = AppSettings()
        except Exception as exc:
            self.config_load_failed(exc)

    def setup_config(self):
        try:
            self.app_settings = AppSettings()
            self.config_loaded()
        except Exception as exc:
            self.config_load_failed(exc)

    def config_loaded(self):
        setup_logger(self.app_settings.log_level)        
        self.app_ctrl = AppsController(self)

    def config_load_failed(self, exc: Exception):
        tb: str = ''.join(traceback.format_exception(exc))

        QMessageBox.critical(
            self,
            'PasswordManager - Client',
            f"Could not load configuration, exiting.\nTraceback:\n\n{tb}"
        )
        self.close()
    
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
