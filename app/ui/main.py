# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 696)
        self.actionSource_Code = QAction(MainWindow)
        self.actionSource_Code.setObjectName(u"actionSource_Code")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.actionSource_Code.setIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName(u"mainStackedWidget")
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.verticalLayout_2 = QVBoxLayout(self.loginPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainLoginFrame = QFrame(self.loginPage)
        self.mainLoginFrame.setObjectName(u"mainLoginFrame")
        self.mainLoginFrame.setMinimumSize(QSize(350, 250))
        self.mainLoginFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainLoginFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.mainLoginFrame)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(12, -1, 12, -1)
        self.loginLabel = QLabel(self.mainLoginFrame)
        self.loginLabel.setObjectName(u"loginLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginLabel.sizePolicy().hasHeightForWidth())
        self.loginLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(18)
        self.loginLabel.setFont(font)
        self.loginLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.loginLabel)

        self.serverURILineEdit = QLineEdit(self.mainLoginFrame)
        self.serverURILineEdit.setObjectName(u"serverURILineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.serverURILineEdit.sizePolicy().hasHeightForWidth())
        self.serverURILineEdit.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(12)
        self.serverURILineEdit.setFont(font1)

        self.verticalLayout_3.addWidget(self.serverURILineEdit)

        self.usernameLineEdit = QLineEdit(self.mainLoginFrame)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        sizePolicy1.setHeightForWidth(self.usernameLineEdit.sizePolicy().hasHeightForWidth())
        self.usernameLineEdit.setSizePolicy(sizePolicy1)
        self.usernameLineEdit.setFont(font1)

        self.verticalLayout_3.addWidget(self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(self.mainLoginFrame)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        sizePolicy1.setHeightForWidth(self.passwordLineEdit.sizePolicy().hasHeightForWidth())
        self.passwordLineEdit.setSizePolicy(sizePolicy1)
        self.passwordLineEdit.setFont(font1)
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_3.addWidget(self.passwordLineEdit)

        self.loginButton = QPushButton(self.mainLoginFrame)
        self.loginButton.setObjectName(u"loginButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy2)
        self.loginButton.setFont(font1)

        self.verticalLayout_3.addWidget(self.loginButton)


        self.verticalLayout_2.addWidget(self.mainLoginFrame, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.mainStackedWidget.addWidget(self.loginPage)
        self.appPage = QWidget()
        self.appPage.setObjectName(u"appPage")
        self.verticalLayout_4 = QVBoxLayout(self.appPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.appTabWidget = QTabWidget(self.appPage)
        self.appTabWidget.setObjectName(u"appTabWidget")
        self.databasesTab = QWidget()
        self.databasesTab.setObjectName(u"databasesTab")
        self.horizontalLayout_9 = QHBoxLayout(self.databasesTab)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.databasesTabFrame = QFrame(self.databasesTab)
        self.databasesTabFrame.setObjectName(u"databasesTabFrame")
        self.databasesTabFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.databasesTabFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.databasesTabFrame)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.databasesTabInfoFrame = QFrame(self.databasesTabFrame)
        self.databasesTabInfoFrame.setObjectName(u"databasesTabInfoFrame")
        self.databasesTabInfoFrame.setMinimumSize(QSize(450, 400))
        self.databasesTabInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.databasesTabInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.databasesTabInfoFrame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_5)

        self.databasesTitleLabel = QLabel(self.databasesTabInfoFrame)
        self.databasesTitleLabel.setObjectName(u"databasesTitleLabel")
        sizePolicy.setHeightForWidth(self.databasesTitleLabel.sizePolicy().hasHeightForWidth())
        self.databasesTitleLabel.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(14)
        self.databasesTitleLabel.setFont(font2)
        self.databasesTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.databasesTitleLabel)

        self.databasesTabButtonsWidget = QWidget(self.databasesTabInfoFrame)
        self.databasesTabButtonsWidget.setObjectName(u"databasesTabButtonsWidget")
        sizePolicy.setHeightForWidth(self.databasesTabButtonsWidget.sizePolicy().hasHeightForWidth())
        self.databasesTabButtonsWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_12 = QHBoxLayout(self.databasesTabButtonsWidget)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.databasesNewDatabaseButton = QPushButton(self.databasesTabButtonsWidget)
        self.databasesNewDatabaseButton.setObjectName(u"databasesNewDatabaseButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.databasesNewDatabaseButton.setIcon(icon1)

        self.horizontalLayout_12.addWidget(self.databasesNewDatabaseButton)

        self.databasesOpenDatabaseButton = QPushButton(self.databasesTabButtonsWidget)
        self.databasesOpenDatabaseButton.setObjectName(u"databasesOpenDatabaseButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.databasesOpenDatabaseButton.setIcon(icon2)

        self.horizontalLayout_12.addWidget(self.databasesOpenDatabaseButton)


        self.verticalLayout_9.addWidget(self.databasesTabButtonsWidget)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)

        self.databasesRecentlyOpenedLabel = QLabel(self.databasesTabInfoFrame)
        self.databasesRecentlyOpenedLabel.setObjectName(u"databasesRecentlyOpenedLabel")
        sizePolicy.setHeightForWidth(self.databasesRecentlyOpenedLabel.sizePolicy().hasHeightForWidth())
        self.databasesRecentlyOpenedLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_9.addWidget(self.databasesRecentlyOpenedLabel)

        self.recentlyOpenedDatabasesListView = QListView(self.databasesTabInfoFrame)
        self.recentlyOpenedDatabasesListView.setObjectName(u"recentlyOpenedDatabasesListView")

        self.verticalLayout_9.addWidget(self.recentlyOpenedDatabasesListView)


        self.horizontalLayout_11.addWidget(self.databasesTabInfoFrame, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.horizontalLayout_9.addWidget(self.databasesTabFrame)

        self.appTabWidget.addTab(self.databasesTab, "")
        self.passwordsTab = QWidget()
        self.passwordsTab.setObjectName(u"passwordsTab")
        self.verticalLayout_7 = QVBoxLayout(self.passwordsTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.passwordsTabFrame = QFrame(self.passwordsTab)
        self.passwordsTabFrame.setObjectName(u"passwordsTabFrame")
        self.passwordsTabFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.passwordsTabFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.passwordsTabFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.passwordGroupsTreeView = QTreeView(self.passwordsTabFrame)
        self.passwordGroupsTreeView.setObjectName(u"passwordGroupsTreeView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.passwordGroupsTreeView.sizePolicy().hasHeightForWidth())
        self.passwordGroupsTreeView.setSizePolicy(sizePolicy3)
        self.passwordGroupsTreeView.header().setDefaultSectionSize(21)

        self.horizontalLayout_5.addWidget(self.passwordGroupsTreeView)

        self.passwordEntriesWidget = QWidget(self.passwordsTabFrame)
        self.passwordEntriesWidget.setObjectName(u"passwordEntriesWidget")
        self.verticalLayout_8 = QVBoxLayout(self.passwordEntriesWidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.passwordEntriesTableView = QTableView(self.passwordEntriesWidget)
        self.passwordEntriesTableView.setObjectName(u"passwordEntriesTableView")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.passwordEntriesTableView.sizePolicy().hasHeightForWidth())
        self.passwordEntriesTableView.setSizePolicy(sizePolicy4)
        self.passwordEntriesTableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.passwordEntriesTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_8.addWidget(self.passwordEntriesTableView)

        self.passwordEntryInfoFrame = QFrame(self.passwordEntriesWidget)
        self.passwordEntryInfoFrame.setObjectName(u"passwordEntryInfoFrame")
        sizePolicy.setHeightForWidth(self.passwordEntryInfoFrame.sizePolicy().hasHeightForWidth())
        self.passwordEntryInfoFrame.setSizePolicy(sizePolicy)
        self.passwordEntryInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.passwordEntryInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.passwordEntryInfoFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.passwordEntryInfoWidget1 = QWidget(self.passwordEntryInfoFrame)
        self.passwordEntryInfoWidget1.setObjectName(u"passwordEntryInfoWidget1")
        self.horizontalLayout_7 = QHBoxLayout(self.passwordEntryInfoWidget1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.entryLabelsWidget = QWidget(self.passwordEntryInfoWidget1)
        self.entryLabelsWidget.setObjectName(u"entryLabelsWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.entryLabelsWidget.sizePolicy().hasHeightForWidth())
        self.entryLabelsWidget.setSizePolicy(sizePolicy5)
        self.gridLayout = QGridLayout(self.entryLabelsWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(12)
        self.entryUsernameLabel = QLabel(self.entryLabelsWidget)
        self.entryUsernameLabel.setObjectName(u"entryUsernameLabel")
        sizePolicy.setHeightForWidth(self.entryUsernameLabel.sizePolicy().hasHeightForWidth())
        self.entryUsernameLabel.setSizePolicy(sizePolicy)
        self.entryUsernameLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.entryUsernameLabel, 0, 0, 1, 1)

        self.entryPasswordLabel = QLabel(self.entryLabelsWidget)
        self.entryPasswordLabel.setObjectName(u"entryPasswordLabel")
        sizePolicy.setHeightForWidth(self.entryPasswordLabel.sizePolicy().hasHeightForWidth())
        self.entryPasswordLabel.setSizePolicy(sizePolicy)
        self.entryPasswordLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.entryPasswordLabel, 1, 0, 1, 1)

        self.entryNotesLabel = QLabel(self.entryLabelsWidget)
        self.entryNotesLabel.setObjectName(u"entryNotesLabel")
        self.entryNotesLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)

        self.gridLayout.addWidget(self.entryNotesLabel, 2, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.entryLabelsWidget)

        self.entryDataWidget = QWidget(self.passwordEntryInfoWidget1)
        self.entryDataWidget.setObjectName(u"entryDataWidget")
        self.gridLayout_2 = QGridLayout(self.entryDataWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.entryUsernameDataLabel = QLabel(self.entryDataWidget)
        self.entryUsernameDataLabel.setObjectName(u"entryUsernameDataLabel")
        sizePolicy.setHeightForWidth(self.entryUsernameDataLabel.sizePolicy().hasHeightForWidth())
        self.entryUsernameDataLabel.setSizePolicy(sizePolicy)
        self.entryUsernameDataLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_2.addWidget(self.entryUsernameDataLabel, 0, 0, 1, 1)

        self.entryPasswordWidget = QWidget(self.entryDataWidget)
        self.entryPasswordWidget.setObjectName(u"entryPasswordWidget")
        sizePolicy.setHeightForWidth(self.entryPasswordWidget.sizePolicy().hasHeightForWidth())
        self.entryPasswordWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_8 = QHBoxLayout(self.entryPasswordWidget)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.entryPasswordShowHideButton = QPushButton(self.entryPasswordWidget)
        self.entryPasswordShowHideButton.setObjectName(u"entryPasswordShowHideButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.entryPasswordShowHideButton.sizePolicy().hasHeightForWidth())
        self.entryPasswordShowHideButton.setSizePolicy(sizePolicy6)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.entryPasswordShowHideButton.setIcon(icon3)

        self.horizontalLayout_8.addWidget(self.entryPasswordShowHideButton)

        self.entryPasswordDataLabel = QLabel(self.entryPasswordWidget)
        self.entryPasswordDataLabel.setObjectName(u"entryPasswordDataLabel")
        self.entryPasswordDataLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.horizontalLayout_8.addWidget(self.entryPasswordDataLabel)


        self.gridLayout_2.addWidget(self.entryPasswordWidget, 1, 0, 1, 1)

        self.entryNotesPlainTextEdit = QPlainTextEdit(self.entryDataWidget)
        self.entryNotesPlainTextEdit.setObjectName(u"entryNotesPlainTextEdit")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.entryNotesPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.entryNotesPlainTextEdit.setSizePolicy(sizePolicy7)
        self.entryNotesPlainTextEdit.setReadOnly(True)
        self.entryNotesPlainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_2.addWidget(self.entryNotesPlainTextEdit, 3, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.entryDataWidget)


        self.horizontalLayout_6.addWidget(self.passwordEntryInfoWidget1)

        self.passwordEntryInfoWidget2 = QWidget(self.passwordEntryInfoFrame)
        self.passwordEntryInfoWidget2.setObjectName(u"passwordEntryInfoWidget2")
        self.horizontalLayout_10 = QHBoxLayout(self.passwordEntryInfoWidget2)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.entryLabelsWidget2 = QWidget(self.passwordEntryInfoWidget2)
        self.entryLabelsWidget2.setObjectName(u"entryLabelsWidget2")
        sizePolicy5.setHeightForWidth(self.entryLabelsWidget2.sizePolicy().hasHeightForWidth())
        self.entryLabelsWidget2.setSizePolicy(sizePolicy5)
        self.gridLayout_3 = QGridLayout(self.entryLabelsWidget2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(12)
        self.entryURLLabel = QLabel(self.entryLabelsWidget2)
        self.entryURLLabel.setObjectName(u"entryURLLabel")
        sizePolicy.setHeightForWidth(self.entryURLLabel.sizePolicy().hasHeightForWidth())
        self.entryURLLabel.setSizePolicy(sizePolicy)
        self.entryURLLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.entryURLLabel, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 1, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.entryLabelsWidget2)

        self.entryDataWidget2 = QWidget(self.passwordEntryInfoWidget2)
        self.entryDataWidget2.setObjectName(u"entryDataWidget2")
        self.gridLayout_4 = QGridLayout(self.entryDataWidget2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.entryURLDataLabel = QLabel(self.entryDataWidget2)
        self.entryURLDataLabel.setObjectName(u"entryURLDataLabel")
        sizePolicy.setHeightForWidth(self.entryURLDataLabel.sizePolicy().hasHeightForWidth())
        self.entryURLDataLabel.setSizePolicy(sizePolicy)
        self.entryURLDataLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_4.addWidget(self.entryURLDataLabel, 0, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 1, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.entryDataWidget2)


        self.horizontalLayout_6.addWidget(self.passwordEntryInfoWidget2)


        self.verticalLayout_8.addWidget(self.passwordEntryInfoFrame)


        self.horizontalLayout_5.addWidget(self.passwordEntriesWidget)


        self.verticalLayout_7.addWidget(self.passwordsTabFrame)

        self.appTabWidget.addTab(self.passwordsTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.horizontalLayout = QHBoxLayout(self.settingsTab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.availableLoginsGroupbox = QGroupBox(self.settingsTab)
        self.availableLoginsGroupbox.setObjectName(u"availableLoginsGroupbox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.availableLoginsGroupbox.sizePolicy().hasHeightForWidth())
        self.availableLoginsGroupbox.setSizePolicy(sizePolicy8)
        self.verticalLayout_5 = QVBoxLayout(self.availableLoginsGroupbox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.availableLoginsListWidget = QListWidget(self.availableLoginsGroupbox)
        self.availableLoginsListWidget.setObjectName(u"availableLoginsListWidget")
        sizePolicy7.setHeightForWidth(self.availableLoginsListWidget.sizePolicy().hasHeightForWidth())
        self.availableLoginsListWidget.setSizePolicy(sizePolicy7)

        self.verticalLayout_5.addWidget(self.availableLoginsListWidget)

        self.accountButtonFrame = QFrame(self.availableLoginsGroupbox)
        self.accountButtonFrame.setObjectName(u"accountButtonFrame")
        self.accountButtonFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.accountButtonFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.accountButtonFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.addAccountButton = QPushButton(self.accountButtonFrame)
        self.addAccountButton.setObjectName(u"addAccountButton")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.addAccountButton.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.addAccountButton)

        self.removeAccountButton = QPushButton(self.accountButtonFrame)
        self.removeAccountButton.setObjectName(u"removeAccountButton")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.removeAccountButton.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.removeAccountButton)


        self.verticalLayout_5.addWidget(self.accountButtonFrame)


        self.horizontalLayout.addWidget(self.availableLoginsGroupbox)

        self.appConfigGroupBox = QGroupBox(self.settingsTab)
        self.appConfigGroupBox.setObjectName(u"appConfigGroupBox")
        sizePolicy8.setHeightForWidth(self.appConfigGroupBox.sizePolicy().hasHeightForWidth())
        self.appConfigGroupBox.setSizePolicy(sizePolicy8)
        self.verticalLayout_6 = QVBoxLayout(self.appConfigGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.clientInfoWidget = QWidget(self.appConfigGroupBox)
        self.clientInfoWidget.setObjectName(u"clientInfoWidget")
        sizePolicy6.setHeightForWidth(self.clientInfoWidget.sizePolicy().hasHeightForWidth())
        self.clientInfoWidget.setSizePolicy(sizePolicy6)
        self.gridLayout_10 = QGridLayout(self.clientInfoWidget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.serverUrlLabel = QLabel(self.clientInfoWidget)
        self.serverUrlLabel.setObjectName(u"serverUrlLabel")
        self.serverUrlLabel.setFont(font1)
        self.serverUrlLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.serverUrlLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.serverUrlLabel, 2, 0, 1, 1)

        self.clientVersionLabel = QLabel(self.clientInfoWidget)
        self.clientVersionLabel.setObjectName(u"clientVersionLabel")
        sizePolicy5.setHeightForWidth(self.clientVersionLabel.sizePolicy().hasHeightForWidth())
        self.clientVersionLabel.setSizePolicy(sizePolicy5)
        self.clientVersionLabel.setFont(font1)
        self.clientVersionLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.clientVersionLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.clientVersionLabel, 0, 0, 1, 1)

        self.appCurrentUsernameLabel = QLabel(self.clientInfoWidget)
        self.appCurrentUsernameLabel.setObjectName(u"appCurrentUsernameLabel")
        self.appCurrentUsernameLabel.setFont(font1)
        self.appCurrentUsernameLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.appCurrentUsernameLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.appCurrentUsernameLabel, 1, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.clientInfoWidget)

        self.logLevelWidget = QWidget(self.appConfigGroupBox)
        self.logLevelWidget.setObjectName(u"logLevelWidget")
        sizePolicy6.setHeightForWidth(self.logLevelWidget.sizePolicy().hasHeightForWidth())
        self.logLevelWidget.setSizePolicy(sizePolicy6)
        self.horizontalLayout_3 = QHBoxLayout(self.logLevelWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.logLevelLabel = QLabel(self.logLevelWidget)
        self.logLevelLabel.setObjectName(u"logLevelLabel")
        sizePolicy5.setHeightForWidth(self.logLevelLabel.sizePolicy().hasHeightForWidth())
        self.logLevelLabel.setSizePolicy(sizePolicy5)
        self.logLevelLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.logLevelLabel)

        self.logLevelComboBox = QComboBox(self.logLevelWidget)
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setObjectName(u"logLevelComboBox")
        sizePolicy5.setHeightForWidth(self.logLevelComboBox.sizePolicy().hasHeightForWidth())
        self.logLevelComboBox.setSizePolicy(sizePolicy5)

        self.horizontalLayout_3.addWidget(self.logLevelComboBox)


        self.verticalLayout_6.addWidget(self.logLevelWidget)

        self.logFileWidget = QWidget(self.appConfigGroupBox)
        self.logFileWidget.setObjectName(u"logFileWidget")
        sizePolicy5.setHeightForWidth(self.logFileWidget.sizePolicy().hasHeightForWidth())
        self.logFileWidget.setSizePolicy(sizePolicy5)
        self.horizontalLayout_4 = QHBoxLayout(self.logFileWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.logFilePathLabel = QLabel(self.logFileWidget)
        self.logFilePathLabel.setObjectName(u"logFilePathLabel")
        self.logFilePathLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.horizontalLayout_4.addWidget(self.logFilePathLabel)


        self.verticalLayout_6.addWidget(self.logFileWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.appConfigGroupBox)

        self.appTabWidget.addTab(self.settingsTab, "")

        self.verticalLayout_4.addWidget(self.appTabWidget)

        self.mainStackedWidget.addWidget(self.appPage)

        self.verticalLayout.addWidget(self.mainStackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 20))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.actionSource_Code)

        self.retranslateUi(MainWindow)

        self.mainStackedWidget.setCurrentIndex(1)
        self.appTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PasswordManager - Client", None))
        self.actionSource_Code.setText(QCoreApplication.translate("MainWindow", u"Source Code", None))
        self.loginLabel.setText(QCoreApplication.translate("MainWindow", u"PasswordManager Login", None))
        self.serverURILineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter server URL", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter username", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter password", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.databasesTitleLabel.setText(QCoreApplication.translate("MainWindow", u"PasswordManager - Client: {version}", None))
        self.databasesNewDatabaseButton.setText(QCoreApplication.translate("MainWindow", u"New database", None))
        self.databasesOpenDatabaseButton.setText(QCoreApplication.translate("MainWindow", u"Open database", None))
        self.databasesRecentlyOpenedLabel.setText(QCoreApplication.translate("MainWindow", u"Recently opened databases:", None))
        self.appTabWidget.setTabText(self.appTabWidget.indexOf(self.databasesTab), QCoreApplication.translate("MainWindow", u"Databases", None))
        self.entryUsernameLabel.setText(QCoreApplication.translate("MainWindow", u"Username:", None))
        self.entryPasswordLabel.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.entryNotesLabel.setText(QCoreApplication.translate("MainWindow", u"Notes:", None))
        self.entryUsernameDataLabel.setText("")
        self.entryPasswordDataLabel.setText("")
        self.entryURLLabel.setText(QCoreApplication.translate("MainWindow", u"URL:", None))
        self.entryURLDataLabel.setText("")
        self.appTabWidget.setTabText(self.appTabWidget.indexOf(self.passwordsTab), QCoreApplication.translate("MainWindow", u"Passwords", None))
        self.availableLoginsGroupbox.setTitle(QCoreApplication.translate("MainWindow", u"Available Logins", None))
        self.addAccountButton.setText(QCoreApplication.translate("MainWindow", u"Add Login", None))
        self.removeAccountButton.setText(QCoreApplication.translate("MainWindow", u"Remove Login", None))
        self.appConfigGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"App Config", None))
        self.serverUrlLabel.setText(QCoreApplication.translate("MainWindow", u"Server URL: {server_url}", None))
        self.clientVersionLabel.setText(QCoreApplication.translate("MainWindow", u"Client version: {version}", None))
        self.appCurrentUsernameLabel.setText(QCoreApplication.translate("MainWindow", u"User: {username}", None))
        self.logLevelLabel.setText(QCoreApplication.translate("MainWindow", u"Log Level:", None))
        self.logLevelComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Debug", None))
        self.logLevelComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Info", None))
        self.logLevelComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Warning", None))
        self.logLevelComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Error", None))
        self.logLevelComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Critical", None))

        self.logFilePathLabel.setText(QCoreApplication.translate("MainWindow", u"Log File: {file_path}", None))
        self.appTabWidget.setTabText(self.appTabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

