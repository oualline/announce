# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(602, 387)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonPlay = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPlay.setObjectName("buttonPlay")
        self.horizontalLayout.addWidget(self.buttonPlay)
        self.buttonEdit = QtWidgets.QPushButton(self.centralwidget)
        self.buttonEdit.setObjectName("buttonEdit")
        self.horizontalLayout.addWidget(self.buttonEdit)
        self.fileManager = QtWidgets.QPushButton(self.centralwidget)
        self.fileManager.setObjectName("fileManager")
        self.horizontalLayout.addWidget(self.fileManager)
        self.buttonRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.horizontalLayout.addWidget(self.buttonRefresh)
        self.buttonShutdown = QtWidgets.QPushButton(self.centralwidget)
        self.buttonShutdown.setObjectName("buttonShutdown")
        self.horizontalLayout.addWidget(self.buttonShutdown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.buttonPlay.clicked.connect(MainWindow.buttonPlayClicked)
        self.buttonEdit.clicked.connect(MainWindow.buttonEditClicked)
        self.buttonShutdown.clicked.connect(MainWindow.buttonShutdownClicked)
        self.fileManager.clicked.connect(MainWindow.buttonOpenFileManagerClicked)
        self.listWidget.currentItemChanged['QListWidgetItem*','QListWidgetItem*'].connect(MainWindow.listEntryChanged)
        self.buttonRefresh.clicked.connect(MainWindow.buttonRefreshClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Select a configuration to use"))
        self.listWidget.setSortingEnabled(True)
        self.buttonPlay.setText(_translate("MainWindow", "Play"))
        self.buttonEdit.setText(_translate("MainWindow", "Edit"))
        self.fileManager.setText(_translate("MainWindow", "Open File Manager"))
        self.buttonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.buttonShutdown.setText(_translate("MainWindow", "Shutdown"))
