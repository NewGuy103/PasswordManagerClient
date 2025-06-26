# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_sync_info_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_EditSyncInfoDialog(object):
    def setupUi(self, EditSyncInfoDialog):
        if not EditSyncInfoDialog.objectName():
            EditSyncInfoDialog.setObjectName(u"EditSyncInfoDialog")
        EditSyncInfoDialog.setWindowModality(Qt.WindowModality.WindowModal)
        EditSyncInfoDialog.resize(432, 327)
        self.verticalLayout = QVBoxLayout(EditSyncInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainDialogFrame = QFrame(EditSyncInfoDialog)
        self.mainDialogFrame.setObjectName(u"mainDialogFrame")
        self.mainDialogFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainDialogFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainDialogFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(8)
        self.serverURLLabel = QLabel(self.mainDialogFrame)
        self.serverURLLabel.setObjectName(u"serverURLLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.serverURLLabel)

        self.serverURLLineEdit = QLineEdit(self.mainDialogFrame)
        self.serverURLLineEdit.setObjectName(u"serverURLLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.serverURLLineEdit)

        self.usernameLabel = QLabel(self.mainDialogFrame)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.usernameLabel)

        self.usernameLineEdit = QLineEdit(self.mainDialogFrame)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        self.usernameLineEdit.setMaxLength(30)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.usernameLineEdit)

        self.passwordLabel = QLabel(self.mainDialogFrame)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.mainDialogFrame)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.passwordLineEdit)

        self.syncEnabledLabel = QLabel(self.mainDialogFrame)
        self.syncEnabledLabel.setObjectName(u"syncEnabledLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.syncEnabledLabel)

        self.syncEnabledCheckBox = QCheckBox(self.mainDialogFrame)
        self.syncEnabledCheckBox.setObjectName(u"syncEnabledCheckBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.syncEnabledCheckBox)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.testAuthButton = QPushButton(self.mainDialogFrame)
        self.testAuthButton.setObjectName(u"testAuthButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.testAuthButton.setIcon(icon)

        self.verticalLayout_2.addWidget(self.testAuthButton)


        self.verticalLayout.addWidget(self.mainDialogFrame)

        self.dialogButtonBox = QDialogButtonBox(EditSyncInfoDialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Orientation.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Discard|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout.addWidget(self.dialogButtonBox)

        QWidget.setTabOrder(self.serverURLLineEdit, self.usernameLineEdit)
        QWidget.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        QWidget.setTabOrder(self.passwordLineEdit, self.testAuthButton)

        self.retranslateUi(EditSyncInfoDialog)
        self.dialogButtonBox.accepted.connect(EditSyncInfoDialog.accept)
        self.dialogButtonBox.rejected.connect(EditSyncInfoDialog.reject)

        QMetaObject.connectSlotsByName(EditSyncInfoDialog)
    # setupUi

    def retranslateUi(self, EditSyncInfoDialog):
        EditSyncInfoDialog.setWindowTitle(QCoreApplication.translate("EditSyncInfoDialog", u"PasswordManager - Client - Edit sync info", None))
        self.serverURLLabel.setText(QCoreApplication.translate("EditSyncInfoDialog", u"Server URL:", None))
#if QT_CONFIG(tooltip)
        self.serverURLLineEdit.setToolTip(QCoreApplication.translate("EditSyncInfoDialog", u"Server where PasswordManager is running.\n"
"Must be a valid URL or the Test Authorization and Save buttons will be disabled.", None))
#endif // QT_CONFIG(tooltip)
        self.usernameLabel.setText(QCoreApplication.translate("EditSyncInfoDialog", u"Username:", None))
#if QT_CONFIG(tooltip)
        self.usernameLineEdit.setToolTip(QCoreApplication.translate("EditSyncInfoDialog", u"Username to login to. Max length of 30 characters.", None))
#endif // QT_CONFIG(tooltip)
        self.passwordLabel.setText(QCoreApplication.translate("EditSyncInfoDialog", u"Password:", None))
#if QT_CONFIG(tooltip)
        self.passwordLineEdit.setToolTip(QCoreApplication.translate("EditSyncInfoDialog", u"Password of the user.\n"
"Changing this from an empty field will require a login before saving.", None))
#endif // QT_CONFIG(tooltip)
        self.syncEnabledLabel.setText(QCoreApplication.translate("EditSyncInfoDialog", u"Sync enabled:", None))
        self.testAuthButton.setText(QCoreApplication.translate("EditSyncInfoDialog", u"Test Authorization", None))
    # retranslateUi

