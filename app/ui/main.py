################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QAction, QCursor, QFont, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QMenu,
    QMenuBar,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 696)
        self.actionSource_Code = QAction(MainWindow)
        self.actionSource_Code.setObjectName("actionSource_Code")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.actionSource_Code.setIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainStackedWidget = QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setObjectName("mainStackedWidget")
        self.appPage = QWidget()
        self.appPage.setObjectName("appPage")
        self.verticalLayout_4 = QVBoxLayout(self.appPage)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.appTabWidget = QTabWidget(self.appPage)
        self.appTabWidget.setObjectName("appTabWidget")
        self.databasesTab = QWidget()
        self.databasesTab.setObjectName("databasesTab")
        self.horizontalLayout_9 = QHBoxLayout(self.databasesTab)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.databasesTabFrame = QFrame(self.databasesTab)
        self.databasesTabFrame.setObjectName("databasesTabFrame")
        self.databasesTabFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.databasesTabFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.databasesTabFrame)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.databasesTabInfoFrame = QFrame(self.databasesTabFrame)
        self.databasesTabInfoFrame.setObjectName("databasesTabInfoFrame")
        self.databasesTabInfoFrame.setMinimumSize(QSize(450, 400))
        self.databasesTabInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.databasesTabInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.databasesTabInfoFrame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_5)

        self.databasesTitleLabel = QLabel(self.databasesTabInfoFrame)
        self.databasesTitleLabel.setObjectName("databasesTitleLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.databasesTitleLabel.sizePolicy().hasHeightForWidth())
        self.databasesTitleLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        self.databasesTitleLabel.setFont(font)
        self.databasesTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.databasesTitleLabel)

        self.databasesTabButtonsWidget = QWidget(self.databasesTabInfoFrame)
        self.databasesTabButtonsWidget.setObjectName("databasesTabButtonsWidget")
        sizePolicy.setHeightForWidth(self.databasesTabButtonsWidget.sizePolicy().hasHeightForWidth())
        self.databasesTabButtonsWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_12 = QHBoxLayout(self.databasesTabButtonsWidget)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.databasesNewDatabaseButton = QPushButton(self.databasesTabButtonsWidget)
        self.databasesNewDatabaseButton.setObjectName("databasesNewDatabaseButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.databasesNewDatabaseButton.setIcon(icon1)

        self.horizontalLayout_12.addWidget(self.databasesNewDatabaseButton)

        self.databasesOpenDatabaseButton = QPushButton(self.databasesTabButtonsWidget)
        self.databasesOpenDatabaseButton.setObjectName("databasesOpenDatabaseButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.databasesOpenDatabaseButton.setIcon(icon2)

        self.horizontalLayout_12.addWidget(self.databasesOpenDatabaseButton)

        self.verticalLayout_9.addWidget(self.databasesTabButtonsWidget)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)

        self.databasesRecentlyOpenedLabel = QLabel(self.databasesTabInfoFrame)
        self.databasesRecentlyOpenedLabel.setObjectName("databasesRecentlyOpenedLabel")
        sizePolicy.setHeightForWidth(self.databasesRecentlyOpenedLabel.sizePolicy().hasHeightForWidth())
        self.databasesRecentlyOpenedLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_9.addWidget(self.databasesRecentlyOpenedLabel)

        self.recentlyOpenedDatabasesListView = QListView(self.databasesTabInfoFrame)
        self.recentlyOpenedDatabasesListView.setObjectName("recentlyOpenedDatabasesListView")

        self.verticalLayout_9.addWidget(self.recentlyOpenedDatabasesListView)

        self.horizontalLayout_11.addWidget(
            self.databasesTabInfoFrame, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_9.addWidget(self.databasesTabFrame)

        self.appTabWidget.addTab(self.databasesTab, "")
        self.passwordsTab = QWidget()
        self.passwordsTab.setObjectName("passwordsTab")
        self.verticalLayout_7 = QVBoxLayout(self.passwordsTab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.passwordsTabFrame = QFrame(self.passwordsTab)
        self.passwordsTabFrame.setObjectName("passwordsTabFrame")
        self.passwordsTabFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.passwordsTabFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.passwordsTabFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.passwordGroupsTreeView = QTreeView(self.passwordsTabFrame)
        self.passwordGroupsTreeView.setObjectName("passwordGroupsTreeView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.passwordGroupsTreeView.sizePolicy().hasHeightForWidth())
        self.passwordGroupsTreeView.setSizePolicy(sizePolicy1)
        self.passwordGroupsTreeView.header().setDefaultSectionSize(21)

        self.horizontalLayout_5.addWidget(self.passwordGroupsTreeView)

        self.passwordEntriesWidget = QWidget(self.passwordsTabFrame)
        self.passwordEntriesWidget.setObjectName("passwordEntriesWidget")
        self.verticalLayout_8 = QVBoxLayout(self.passwordEntriesWidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.passwordEntriesTableView = QTableView(self.passwordEntriesWidget)
        self.passwordEntriesTableView.setObjectName("passwordEntriesTableView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.passwordEntriesTableView.sizePolicy().hasHeightForWidth())
        self.passwordEntriesTableView.setSizePolicy(sizePolicy2)
        self.passwordEntriesTableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.passwordEntriesTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_8.addWidget(self.passwordEntriesTableView)

        self.passwordEntryInfoFrame = QFrame(self.passwordEntriesWidget)
        self.passwordEntryInfoFrame.setObjectName("passwordEntryInfoFrame")
        sizePolicy.setHeightForWidth(self.passwordEntryInfoFrame.sizePolicy().hasHeightForWidth())
        self.passwordEntryInfoFrame.setSizePolicy(sizePolicy)
        self.passwordEntryInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.passwordEntryInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.passwordEntryInfoFrame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.passwordEntryInfoWidget1 = QWidget(self.passwordEntryInfoFrame)
        self.passwordEntryInfoWidget1.setObjectName("passwordEntryInfoWidget1")
        self.horizontalLayout_7 = QHBoxLayout(self.passwordEntryInfoWidget1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.entryLabelsWidget = QWidget(self.passwordEntryInfoWidget1)
        self.entryLabelsWidget.setObjectName("entryLabelsWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.entryLabelsWidget.sizePolicy().hasHeightForWidth())
        self.entryLabelsWidget.setSizePolicy(sizePolicy3)
        self.gridLayout = QGridLayout(self.entryLabelsWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setVerticalSpacing(12)
        self.entryUsernameLabel = QLabel(self.entryLabelsWidget)
        self.entryUsernameLabel.setObjectName("entryUsernameLabel")
        sizePolicy.setHeightForWidth(self.entryUsernameLabel.sizePolicy().hasHeightForWidth())
        self.entryUsernameLabel.setSizePolicy(sizePolicy)
        self.entryUsernameLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout.addWidget(self.entryUsernameLabel, 0, 0, 1, 1)

        self.entryPasswordLabel = QLabel(self.entryLabelsWidget)
        self.entryPasswordLabel.setObjectName("entryPasswordLabel")
        sizePolicy.setHeightForWidth(self.entryPasswordLabel.sizePolicy().hasHeightForWidth())
        self.entryPasswordLabel.setSizePolicy(sizePolicy)
        self.entryPasswordLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout.addWidget(self.entryPasswordLabel, 1, 0, 1, 1)

        self.entryNotesLabel = QLabel(self.entryLabelsWidget)
        self.entryNotesLabel.setObjectName("entryNotesLabel")
        self.entryNotesLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignTrailing
        )

        self.gridLayout.addWidget(self.entryNotesLabel, 2, 0, 1, 1)

        self.horizontalLayout_7.addWidget(self.entryLabelsWidget)

        self.entryDataWidget = QWidget(self.passwordEntryInfoWidget1)
        self.entryDataWidget.setObjectName("entryDataWidget")
        self.gridLayout_2 = QGridLayout(self.entryDataWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.entryUsernameDataLabel = QLabel(self.entryDataWidget)
        self.entryUsernameDataLabel.setObjectName("entryUsernameDataLabel")
        sizePolicy.setHeightForWidth(self.entryUsernameDataLabel.sizePolicy().hasHeightForWidth())
        self.entryUsernameDataLabel.setSizePolicy(sizePolicy)
        self.entryUsernameDataLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_2.addWidget(self.entryUsernameDataLabel, 0, 0, 1, 1)

        self.entryPasswordWidget = QWidget(self.entryDataWidget)
        self.entryPasswordWidget.setObjectName("entryPasswordWidget")
        sizePolicy.setHeightForWidth(self.entryPasswordWidget.sizePolicy().hasHeightForWidth())
        self.entryPasswordWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_8 = QHBoxLayout(self.entryPasswordWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.entryPasswordShowHideButton = QPushButton(self.entryPasswordWidget)
        self.entryPasswordShowHideButton.setObjectName("entryPasswordShowHideButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.entryPasswordShowHideButton.sizePolicy().hasHeightForWidth())
        self.entryPasswordShowHideButton.setSizePolicy(sizePolicy4)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.entryPasswordShowHideButton.setIcon(icon3)

        self.horizontalLayout_8.addWidget(self.entryPasswordShowHideButton)

        self.entryPasswordDataLabel = QLabel(self.entryPasswordWidget)
        self.entryPasswordDataLabel.setObjectName("entryPasswordDataLabel")
        self.entryPasswordDataLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.horizontalLayout_8.addWidget(self.entryPasswordDataLabel)

        self.gridLayout_2.addWidget(self.entryPasswordWidget, 1, 0, 1, 1)

        self.entryNotesPlainTextEdit = QPlainTextEdit(self.entryDataWidget)
        self.entryNotesPlainTextEdit.setObjectName("entryNotesPlainTextEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.entryNotesPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.entryNotesPlainTextEdit.setSizePolicy(sizePolicy5)
        self.entryNotesPlainTextEdit.setReadOnly(True)
        self.entryNotesPlainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_2.addWidget(self.entryNotesPlainTextEdit, 3, 0, 1, 1)

        self.horizontalLayout_7.addWidget(self.entryDataWidget)

        self.horizontalLayout_6.addWidget(self.passwordEntryInfoWidget1)

        self.passwordEntryInfoWidget2 = QWidget(self.passwordEntryInfoFrame)
        self.passwordEntryInfoWidget2.setObjectName("passwordEntryInfoWidget2")
        self.horizontalLayout_10 = QHBoxLayout(self.passwordEntryInfoWidget2)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.entryLabelsWidget2 = QWidget(self.passwordEntryInfoWidget2)
        self.entryLabelsWidget2.setObjectName("entryLabelsWidget2")
        sizePolicy3.setHeightForWidth(self.entryLabelsWidget2.sizePolicy().hasHeightForWidth())
        self.entryLabelsWidget2.setSizePolicy(sizePolicy3)
        self.gridLayout_3 = QGridLayout(self.entryLabelsWidget2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(12)
        self.entryURLLabel = QLabel(self.entryLabelsWidget2)
        self.entryURLLabel.setObjectName("entryURLLabel")
        sizePolicy.setHeightForWidth(self.entryURLLabel.sizePolicy().hasHeightForWidth())
        self.entryURLLabel.setSizePolicy(sizePolicy)
        self.entryURLLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_3.addWidget(self.entryURLLabel, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.horizontalLayout_10.addWidget(self.entryLabelsWidget2)

        self.entryDataWidget2 = QWidget(self.passwordEntryInfoWidget2)
        self.entryDataWidget2.setObjectName("entryDataWidget2")
        self.gridLayout_4 = QGridLayout(self.entryDataWidget2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.entryURLDataLabel = QLabel(self.entryDataWidget2)
        self.entryURLDataLabel.setObjectName("entryURLDataLabel")
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
        self.settingsTab.setObjectName("settingsTab")
        self.horizontalLayout = QHBoxLayout(self.settingsTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.databaseSettingsGroupBox = QGroupBox(self.settingsTab)
        self.databaseSettingsGroupBox.setObjectName("databaseSettingsGroupBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.databaseSettingsGroupBox.sizePolicy().hasHeightForWidth())
        self.databaseSettingsGroupBox.setSizePolicy(sizePolicy6)
        self.verticalLayout_5 = QVBoxLayout(self.databaseSettingsGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QWidget(self.databaseSettingsGroupBox)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.syncInfoGroupBox = QGroupBox(self.widget)
        self.syncInfoGroupBox.setObjectName("syncInfoGroupBox")
        sizePolicy.setHeightForWidth(self.syncInfoGroupBox.sizePolicy().hasHeightForWidth())
        self.syncInfoGroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.syncInfoGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.syncInfoServerURLLabel = QLabel(self.syncInfoGroupBox)
        self.syncInfoServerURLLabel.setObjectName("syncInfoServerURLLabel")
        font1 = QFont()
        font1.setPointSize(12)
        self.syncInfoServerURLLabel.setFont(font1)
        self.syncInfoServerURLLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.verticalLayout_3.addWidget(self.syncInfoServerURLLabel)

        self.syncInfoUsernameLabel = QLabel(self.syncInfoGroupBox)
        self.syncInfoUsernameLabel.setObjectName("syncInfoUsernameLabel")
        self.syncInfoUsernameLabel.setFont(font1)

        self.verticalLayout_3.addWidget(self.syncInfoUsernameLabel)

        self.syncInfoEditButton = QPushButton(self.syncInfoGroupBox)
        self.syncInfoEditButton.setObjectName("syncInfoEditButton")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.syncInfoEditButton.sizePolicy().hasHeightForWidth())
        self.syncInfoEditButton.setSizePolicy(sizePolicy7)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.syncInfoEditButton.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.syncInfoEditButton)

        self.verticalLayout_2.addWidget(self.syncInfoGroupBox)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.verticalLayout_5.addWidget(self.widget)

        self.horizontalLayout.addWidget(self.databaseSettingsGroupBox)

        self.appConfigGroupBox = QGroupBox(self.settingsTab)
        self.appConfigGroupBox.setObjectName("appConfigGroupBox")
        sizePolicy6.setHeightForWidth(self.appConfigGroupBox.sizePolicy().hasHeightForWidth())
        self.appConfigGroupBox.setSizePolicy(sizePolicy6)
        self.verticalLayout_6 = QVBoxLayout(self.appConfigGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.clientInfoWidget = QWidget(self.appConfigGroupBox)
        self.clientInfoWidget.setObjectName("clientInfoWidget")
        sizePolicy4.setHeightForWidth(self.clientInfoWidget.sizePolicy().hasHeightForWidth())
        self.clientInfoWidget.setSizePolicy(sizePolicy4)
        self.gridLayout_10 = QGridLayout(self.clientInfoWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.clientVersionLabel = QLabel(self.clientInfoWidget)
        self.clientVersionLabel.setObjectName("clientVersionLabel")
        sizePolicy3.setHeightForWidth(self.clientVersionLabel.sizePolicy().hasHeightForWidth())
        self.clientVersionLabel.setSizePolicy(sizePolicy3)
        self.clientVersionLabel.setFont(font1)
        self.clientVersionLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.clientVersionLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.gridLayout_10.addWidget(self.clientVersionLabel, 0, 0, 1, 1)

        self.verticalLayout_6.addWidget(self.clientInfoWidget)

        self.logLevelWidget = QWidget(self.appConfigGroupBox)
        self.logLevelWidget.setObjectName("logLevelWidget")
        sizePolicy4.setHeightForWidth(self.logLevelWidget.sizePolicy().hasHeightForWidth())
        self.logLevelWidget.setSizePolicy(sizePolicy4)
        self.horizontalLayout_3 = QHBoxLayout(self.logLevelWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.logLevelLabel = QLabel(self.logLevelWidget)
        self.logLevelLabel.setObjectName("logLevelLabel")
        sizePolicy3.setHeightForWidth(self.logLevelLabel.sizePolicy().hasHeightForWidth())
        self.logLevelLabel.setSizePolicy(sizePolicy3)
        self.logLevelLabel.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_3.addWidget(self.logLevelLabel)

        self.logLevelComboBox = QComboBox(self.logLevelWidget)
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setObjectName("logLevelComboBox")
        sizePolicy3.setHeightForWidth(self.logLevelComboBox.sizePolicy().hasHeightForWidth())
        self.logLevelComboBox.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.logLevelComboBox)

        self.verticalLayout_6.addWidget(self.logLevelWidget)

        self.logFileWidget = QWidget(self.appConfigGroupBox)
        self.logFileWidget.setObjectName("logFileWidget")
        sizePolicy3.setHeightForWidth(self.logFileWidget.sizePolicy().hasHeightForWidth())
        self.logFileWidget.setSizePolicy(sizePolicy3)
        self.horizontalLayout_4 = QHBoxLayout(self.logFileWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.logFilePathLabel = QLabel(self.logFileWidget)
        self.logFilePathLabel.setObjectName("logFilePathLabel")
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
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 20))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.actionSource_Code)

        self.retranslateUi(MainWindow)

        self.mainStackedWidget.setCurrentIndex(0)
        self.appTabWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "PasswordManager - Client", None))
        self.actionSource_Code.setText(QCoreApplication.translate("MainWindow", "Source Code", None))
        self.databasesTitleLabel.setText(
            QCoreApplication.translate("MainWindow", "PasswordManager - Client: {version}", None)
        )
        self.databasesNewDatabaseButton.setText(QCoreApplication.translate("MainWindow", "New database", None))
        self.databasesOpenDatabaseButton.setText(QCoreApplication.translate("MainWindow", "Open database", None))
        self.databasesRecentlyOpenedLabel.setText(
            QCoreApplication.translate("MainWindow", "Recently opened databases:", None)
        )
        self.appTabWidget.setTabText(
            self.appTabWidget.indexOf(self.databasesTab), QCoreApplication.translate("MainWindow", "Databases", None)
        )
        self.entryUsernameLabel.setText(QCoreApplication.translate("MainWindow", "Username:", None))
        self.entryPasswordLabel.setText(QCoreApplication.translate("MainWindow", "Password:", None))
        self.entryNotesLabel.setText(QCoreApplication.translate("MainWindow", "Notes:", None))
        self.entryUsernameDataLabel.setText("")
        self.entryPasswordDataLabel.setText("")
        self.entryURLLabel.setText(QCoreApplication.translate("MainWindow", "URL:", None))
        self.entryURLDataLabel.setText("")
        self.appTabWidget.setTabText(
            self.appTabWidget.indexOf(self.passwordsTab), QCoreApplication.translate("MainWindow", "Passwords", None)
        )
        self.databaseSettingsGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Database Settings", None))
        self.syncInfoGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Sync Info", None))
        self.syncInfoServerURLLabel.setText(QCoreApplication.translate("MainWindow", "Server URL: {server_url}", None))
        self.syncInfoUsernameLabel.setText(QCoreApplication.translate("MainWindow", "Username: {username}", None))
        self.syncInfoEditButton.setText(QCoreApplication.translate("MainWindow", "Edit Sync Info", None))
        self.appConfigGroupBox.setTitle(QCoreApplication.translate("MainWindow", "App Config", None))
        self.clientVersionLabel.setText(QCoreApplication.translate("MainWindow", "Client version: {version}", None))
        self.logLevelLabel.setText(QCoreApplication.translate("MainWindow", "Log Level:", None))
        self.logLevelComboBox.setItemText(0, QCoreApplication.translate("MainWindow", "Debug", None))
        self.logLevelComboBox.setItemText(1, QCoreApplication.translate("MainWindow", "Info", None))
        self.logLevelComboBox.setItemText(2, QCoreApplication.translate("MainWindow", "Warning", None))
        self.logLevelComboBox.setItemText(3, QCoreApplication.translate("MainWindow", "Error", None))
        self.logLevelComboBox.setItemText(4, QCoreApplication.translate("MainWindow", "Critical", None))

        self.logFilePathLabel.setText(QCoreApplication.translate("MainWindow", "Log File: {file_path}", None))
        self.appTabWidget.setTabText(
            self.appTabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", "About", None))

    # retranslateUi
