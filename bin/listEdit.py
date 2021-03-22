# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listEdit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_listEdit(object):
    def setupUi(self, listEdit):
        listEdit.setObjectName("listEdit")
        listEdit.resize(800, 668)
        self.centralwidget = QtWidgets.QWidget(listEdit)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editWhatLabel = QtWidgets.QLabel(self.centralwidget)
        self.editWhatLabel.setObjectName("editWhatLabel")
        self.verticalLayout.addWidget(self.editWhatLabel)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.moveUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveUpButton.setObjectName("moveUpButton")
        self.horizontalLayout_2.addWidget(self.moveUpButton)
        self.moveDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveDownButton.setObjectName("moveDownButton")
        self.horizontalLayout_2.addWidget(self.moveDownButton)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_2.addWidget(self.editButton)
        self.insertAboveButton = QtWidgets.QPushButton(self.centralwidget)
        self.insertAboveButton.setObjectName("insertAboveButton")
        self.horizontalLayout_2.addWidget(self.insertAboveButton)
        self.deletebutton = QtWidgets.QPushButton(self.centralwidget)
        self.deletebutton.setObjectName("deletebutton")
        self.horizontalLayout_2.addWidget(self.deletebutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.saveAsButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAsButton.setObjectName("saveAsButton")
        self.horizontalLayout_3.addWidget(self.saveAsButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        listEdit.setCentralWidget(self.centralwidget)

        self.retranslateUi(listEdit)
        self.moveUpButton.clicked.connect(listEdit.buttonMoveUpPressed)
        self.moveDownButton.clicked.connect(listEdit.buttonMoveDownPressed)
        self.editButton.clicked.connect(listEdit.buttonEditPressed)
        self.insertAboveButton.clicked.connect(listEdit.buttonInsertAbovePressed)
        self.deletebutton.clicked.connect(listEdit.buttonDeletePressed)
        self.saveButton.clicked.connect(listEdit.buttonSavePressed)
        self.saveAsButton.clicked.connect(listEdit.buttonSaveAsPressed)
        self.cancelButton.clicked.connect(listEdit.buttonCancelPressed)
        QtCore.QMetaObject.connectSlotsByName(listEdit)

    def retranslateUi(self, listEdit):
        _translate = QtCore.QCoreApplication.translate
        listEdit.setWindowTitle(_translate("listEdit", "ListEdit"))
        self.editWhatLabel.setText(_translate("listEdit", "TextLabel"))
        self.listWidget.setSortingEnabled(False)
        self.moveUpButton.setText(_translate("listEdit", "Move Up"))
        self.moveDownButton.setText(_translate("listEdit", "Move Down"))
        self.editButton.setText(_translate("listEdit", "Edit"))
        self.insertAboveButton.setText(_translate("listEdit", "Insert Above"))
        self.deletebutton.setText(_translate("listEdit", "Delete"))
        self.saveButton.setText(_translate("listEdit", "Save"))
        self.saveAsButton.setText(_translate("listEdit", "Save As"))
        self.cancelButton.setText(_translate("listEdit", "Cancel"))
