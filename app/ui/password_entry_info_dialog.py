# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'password_entry_info_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QLabel, QLineEdit,
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_PasswordEntryInfoDialog(object):
    def setupUi(self, PasswordEntryInfoDialog):
        if not PasswordEntryInfoDialog.objectName():
            PasswordEntryInfoDialog.setObjectName(u"PasswordEntryInfoDialog")
        PasswordEntryInfoDialog.setWindowModality(Qt.WindowModality.WindowModal)
        PasswordEntryInfoDialog.resize(409, 376)
        self.verticalLayout = QVBoxLayout(PasswordEntryInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainDialogFrame = QFrame(PasswordEntryInfoDialog)
        self.mainDialogFrame.setObjectName(u"mainDialogFrame")
        self.mainDialogFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainDialogFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainDialogFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.titleLabel = QLabel(self.mainDialogFrame)
        self.titleLabel.setObjectName(u"titleLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.titleLabel)

        self.titleLineEdit = QLineEdit(self.mainDialogFrame)
        self.titleLineEdit.setObjectName(u"titleLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.titleLineEdit)

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

        self.urlLabel = QLabel(self.mainDialogFrame)
        self.urlLabel.setObjectName(u"urlLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.urlLabel)

        self.urlLineEdit = QLineEdit(self.mainDialogFrame)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.urlLineEdit)

        self.notesLabel = QLabel(self.mainDialogFrame)
        self.notesLabel.setObjectName(u"notesLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.notesLabel)

        self.notesPlainTextEdit = QPlainTextEdit(self.mainDialogFrame)
        self.notesPlainTextEdit.setObjectName(u"notesPlainTextEdit")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.notesPlainTextEdit)


        self.verticalLayout_2.addLayout(self.formLayout)


        self.verticalLayout.addWidget(self.mainDialogFrame)

        self.dialogButtonBox = QDialogButtonBox(PasswordEntryInfoDialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Orientation.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.dialogButtonBox)

        QWidget.setTabOrder(self.titleLineEdit, self.usernameLineEdit)
        QWidget.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        QWidget.setTabOrder(self.passwordLineEdit, self.urlLineEdit)

        self.retranslateUi(PasswordEntryInfoDialog)
        self.dialogButtonBox.accepted.connect(PasswordEntryInfoDialog.accept)
        self.dialogButtonBox.rejected.connect(PasswordEntryInfoDialog.reject)

        QMetaObject.connectSlotsByName(PasswordEntryInfoDialog)
    # setupUi

    def retranslateUi(self, PasswordEntryInfoDialog):
        PasswordEntryInfoDialog.setWindowTitle(QCoreApplication.translate("PasswordEntryInfoDialog", u"PasswordManager - Password entry info", None))
        self.titleLabel.setText(QCoreApplication.translate("PasswordEntryInfoDialog", u"Title:", None))
        self.usernameLabel.setText(QCoreApplication.translate("PasswordEntryInfoDialog", u"Username:", None))
        self.passwordLabel.setText(QCoreApplication.translate("PasswordEntryInfoDialog", u"Password:", None))
        self.urlLabel.setText(QCoreApplication.translate("PasswordEntryInfoDialog", u"URL:", None))
        self.urlLineEdit.setPlaceholderText(QCoreApplication.translate("PasswordEntryInfoDialog", u"https://example.com", None))
        self.notesLabel.setText(QCoreApplication.translate("PasswordEntryInfoDialog", u"Notes:", None))
    # retranslateUi

