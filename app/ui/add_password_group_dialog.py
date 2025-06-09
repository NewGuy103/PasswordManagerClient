# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_password_group_dialog.ui'
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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_AddPasswordGroupDialog(object):
    def setupUi(self, AddPasswordGroupDialog):
        if not AddPasswordGroupDialog.objectName():
            AddPasswordGroupDialog.setObjectName(u"AddPasswordGroupDialog")
        AddPasswordGroupDialog.setWindowModality(Qt.WindowModality.WindowModal)
        AddPasswordGroupDialog.resize(409, 184)
        self.verticalLayout = QVBoxLayout(AddPasswordGroupDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainDialogFrame = QFrame(AddPasswordGroupDialog)
        self.mainDialogFrame.setObjectName(u"mainDialogFrame")
        self.mainDialogFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainDialogFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainDialogFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.groupNameLabel = QLabel(self.mainDialogFrame)
        self.groupNameLabel.setObjectName(u"groupNameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.groupNameLabel)

        self.groupNameLineEdit = QLineEdit(self.mainDialogFrame)
        self.groupNameLineEdit.setObjectName(u"groupNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.groupNameLineEdit)


        self.verticalLayout_2.addLayout(self.formLayout)


        self.verticalLayout.addWidget(self.mainDialogFrame)

        self.dialogButtonBox = QDialogButtonBox(AddPasswordGroupDialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Orientation.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.dialogButtonBox)


        self.retranslateUi(AddPasswordGroupDialog)
        self.dialogButtonBox.accepted.connect(AddPasswordGroupDialog.accept)
        self.dialogButtonBox.rejected.connect(AddPasswordGroupDialog.reject)

        QMetaObject.connectSlotsByName(AddPasswordGroupDialog)
    # setupUi

    def retranslateUi(self, AddPasswordGroupDialog):
        AddPasswordGroupDialog.setWindowTitle(QCoreApplication.translate("AddPasswordGroupDialog", u"PasswordManager - Add password group", None))
        self.groupNameLabel.setText(QCoreApplication.translate("AddPasswordGroupDialog", u"Group Name:", None))
    # retranslateUi

