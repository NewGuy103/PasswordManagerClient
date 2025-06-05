# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_password_entry_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_AddPasswordEntryDialog(object):
    def setupUi(self, AddPasswordEntryDialog):
        if not AddPasswordEntryDialog.objectName():
            AddPasswordEntryDialog.setObjectName(u"AddPasswordEntryDialog")
        AddPasswordEntryDialog.setWindowModality(Qt.WindowModality.WindowModal)
        AddPasswordEntryDialog.resize(409, 184)
        self.verticalLayout = QVBoxLayout(AddPasswordEntryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainDialogFrame = QFrame(AddPasswordEntryDialog)
        self.mainDialogFrame.setObjectName(u"mainDialogFrame")
        self.mainDialogFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainDialogFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainDialogFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.usernameLabel = QLabel(self.mainDialogFrame)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.usernameLabel)

        self.usernameLineEdit = QLineEdit(self.mainDialogFrame)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.usernameLineEdit)

        self.passwordLabel = QLabel(self.mainDialogFrame)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.mainDialogFrame)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.passwordLineEdit)

        self.entryNameLabel = QLabel(self.mainDialogFrame)
        self.entryNameLabel.setObjectName(u"entryNameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.entryNameLabel)

        self.entryNameLineEdit = QLineEdit(self.mainDialogFrame)
        self.entryNameLineEdit.setObjectName(u"entryNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.entryNameLineEdit)

        self.urlLabel = QLabel(self.mainDialogFrame)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.urlLabel)

        self.urlLineEdit = QLineEdit(self.mainDialogFrame)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.urlLineEdit)


        self.verticalLayout_2.addLayout(self.formLayout)


        self.verticalLayout.addWidget(self.mainDialogFrame)

        self.dialogButtonBox = QDialogButtonBox(AddPasswordEntryDialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Orientation.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.dialogButtonBox)

        QWidget.setTabOrder(self.entryNameLineEdit, self.usernameLineEdit)
        QWidget.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        QWidget.setTabOrder(self.passwordLineEdit, self.urlLineEdit)

        self.retranslateUi(AddPasswordEntryDialog)
        self.dialogButtonBox.accepted.connect(AddPasswordEntryDialog.accept)
        self.dialogButtonBox.rejected.connect(AddPasswordEntryDialog.reject)

        QMetaObject.connectSlotsByName(AddPasswordEntryDialog)
    # setupUi

    def retranslateUi(self, AddPasswordEntryDialog):
        AddPasswordEntryDialog.setWindowTitle(QCoreApplication.translate("AddPasswordEntryDialog", u"PasswordManager - Add password entry", None))
        self.usernameLabel.setText(QCoreApplication.translate("AddPasswordEntryDialog", u"Username:", None))
        self.passwordLabel.setText(QCoreApplication.translate("AddPasswordEntryDialog", u"Password:", None))
        self.entryNameLabel.setText(QCoreApplication.translate("AddPasswordEntryDialog", u"Entry Name:", None))
        self.urlLabel.setText(QCoreApplication.translate("AddPasswordEntryDialog", u"URL:", None))
        self.urlLineEdit.setPlaceholderText(QCoreApplication.translate("AddPasswordEntryDialog", u"https://example.com", None))
    # retranslateUi

