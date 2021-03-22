# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'announceEdit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_announceEdit(object):
    def setupUi(self, announceEdit):
        announceEdit.setObjectName("announceEdit")
        announceEdit.resize(800, 217)
        self.centralwidget = QtWidgets.QWidget(announceEdit)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioComment = QtWidgets.QRadioButton(self.centralwidget)
        self.radioComment.setObjectName("radioComment")
        self.verticalLayout.addWidget(self.radioComment)
        self.commentText = QtWidgets.QLineEdit(self.centralwidget)
        self.commentText.setText("")
        self.commentText.setObjectName("commentText")
        self.verticalLayout.addWidget(self.commentText)
        self.radioAnnounce = QtWidgets.QRadioButton(self.centralwidget)
        self.radioAnnounce.setObjectName("radioAnnounce")
        self.verticalLayout.addWidget(self.radioAnnounce)
        self.timeSelection = QtWidgets.QTimeEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeSelection.sizePolicy().hasHeightForWidth())
        self.timeSelection.setSizePolicy(sizePolicy)
        self.timeSelection.setObjectName("timeSelection")
        self.verticalLayout.addWidget(self.timeSelection)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selectFileButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectFileButton.sizePolicy().hasHeightForWidth())
        self.selectFileButton.setSizePolicy(sizePolicy)
        self.selectFileButton.setObjectName("selectFileButton")
        self.horizontalLayout_2.addWidget(self.selectFileButton)
        self.fileNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.horizontalLayout_2.addWidget(self.fileNameLabel)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.appluButton = QtWidgets.QPushButton(self.centralwidget)
        self.appluButton.setObjectName("appluButton")
        self.horizontalLayout.addWidget(self.appluButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        announceEdit.setCentralWidget(self.centralwidget)

        self.retranslateUi(announceEdit)
        self.radioAnnounce.toggled['bool'].connect(announceEdit.enableParts)
        self.selectFileButton.clicked.connect(announceEdit.selectFileButtonClicked)
        self.playButton.clicked.connect(announceEdit.playButtonClicked)
        self.appluButton.clicked.connect(announceEdit.applyButtonClicked)
        self.cancelButton.clicked.connect(announceEdit.cancelButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(announceEdit)

    def retranslateUi(self, announceEdit):
        _translate = QtCore.QCoreApplication.translate
        announceEdit.setWindowTitle(_translate("announceEdit", "Edit/Create Announcement"))
        self.radioComment.setText(_translate("announceEdit", "Comment"))
        self.radioAnnounce.setText(_translate("announceEdit", "Announcement"))
        self.timeSelection.setDisplayFormat(_translate("announceEdit", "hh:mm"))
        self.selectFileButton.setText(_translate("announceEdit", "Select File"))
        self.fileNameLabel.setText(_translate("announceEdit", "<file-name>"))
        self.playButton.setText(_translate("announceEdit", "Play"))
        self.appluButton.setText(_translate("announceEdit", "Apply"))
        self.cancelButton.setText(_translate("announceEdit", "Cancel"))
