# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configEdit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_configEdit(object):
    def setupUi(self, configEdit):
        configEdit.setObjectName("configEdit")
        configEdit.resize(800, 767)
        configEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(configEdit)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.fileNameLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.horizontalLayout.addWidget(self.fileNameLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.description = QtWidgets.QLineEdit(self.centralwidget)
        self.description.setObjectName("description")
        self.horizontalLayout_2.addWidget(self.description)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.backgroundVolume = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgroundVolume.sizePolicy().hasHeightForWidth())
        self.backgroundVolume.setSizePolicy(sizePolicy)
        self.backgroundVolume.setObjectName("backgroundVolume")
        self.horizontalLayout_6.addWidget(self.backgroundVolume)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.announceList = QtWidgets.QListWidget(self.centralwidget)
        self.announceList.setObjectName("announceList")
        self.horizontalLayout_5.addWidget(self.announceList)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.editGUIAnnounce = QtWidgets.QPushButton(self.centralwidget)
        self.editGUIAnnounce.setObjectName("editGUIAnnounce")
        self.verticalLayout_2.addWidget(self.editGUIAnnounce)
        self.editEditorAnnounce = QtWidgets.QPushButton(self.centralwidget)
        self.editEditorAnnounce.setObjectName("editEditorAnnounce")
        self.verticalLayout_2.addWidget(self.editEditorAnnounce)
        self.editVimAnnounce = QtWidgets.QPushButton(self.centralwidget)
        self.editVimAnnounce.setObjectName("editVimAnnounce")
        self.verticalLayout_2.addWidget(self.editVimAnnounce)
        self.fileManagerAnnounceButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileManagerAnnounceButton.setObjectName("fileManagerAnnounceButton")
        self.verticalLayout_2.addWidget(self.fileManagerAnnounceButton)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.backgroundList = QtWidgets.QListWidget(self.centralwidget)
        self.backgroundList.setObjectName("backgroundList")
        self.horizontalLayout_4.addWidget(self.backgroundList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.editGUIBackground = QtWidgets.QPushButton(self.centralwidget)
        self.editGUIBackground.setObjectName("editGUIBackground")
        self.verticalLayout.addWidget(self.editGUIBackground)
        self.editEditorBackground = QtWidgets.QPushButton(self.centralwidget)
        self.editEditorBackground.setObjectName("editEditorBackground")
        self.verticalLayout.addWidget(self.editEditorBackground)
        self.editVimBackground = QtWidgets.QPushButton(self.centralwidget)
        self.editVimBackground.setObjectName("editVimBackground")
        self.verticalLayout.addWidget(self.editVimBackground)
        self.fileManagerBackgroundButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileManagerBackgroundButton.setObjectName("fileManagerBackgroundButton")
        self.verticalLayout.addWidget(self.fileManagerBackgroundButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.configSave = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configSave.sizePolicy().hasHeightForWidth())
        self.configSave.setSizePolicy(sizePolicy)
        self.configSave.setObjectName("configSave")
        self.horizontalLayout_3.addWidget(self.configSave)
        self.saveAsButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveAsButton.sizePolicy().hasHeightForWidth())
        self.saveAsButton.setSizePolicy(sizePolicy)
        self.saveAsButton.setObjectName("saveAsButton")
        self.horizontalLayout_3.addWidget(self.saveAsButton)
        self.cancel = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_3.addWidget(self.cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        configEdit.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(configEdit)
        self.statusbar.setObjectName("statusbar")
        configEdit.setStatusBar(self.statusbar)

        self.retranslateUi(configEdit)
        self.saveAsButton.clicked.connect(configEdit.saveAsButtonClicked)
        self.configSave.clicked.connect(configEdit.configSaveClicked)
        self.cancel.clicked.connect(configEdit.cancelClicked)
        self.fileManagerBackgroundButton.clicked.connect(configEdit.fileManagerBackgroundButtonClicked)
        self.editVimBackground.clicked.connect(configEdit.editVimBackgroundClicked)
        self.editEditorBackground.clicked.connect(configEdit.editEditorBackgroundClicked)
        self.editGUIBackground.clicked.connect(configEdit.editGUIBackgroundClicked)
        self.fileManagerAnnounceButton.clicked.connect(configEdit.fileManagerAnnounceButtonClicked)
        self.editVimAnnounce.clicked.connect(configEdit.editVimAnnounceClicked)
        self.editEditorAnnounce.clicked.connect(configEdit.editEditorAnnounceClicked)
        self.editGUIAnnounce.clicked.connect(configEdit.editGUIAnnounceClicked)
        QtCore.QMetaObject.connectSlotsByName(configEdit)

    def retranslateUi(self, configEdit):
        _translate = QtCore.QCoreApplication.translate
        configEdit.setWindowTitle(_translate("configEdit", "Edit Configuration"))
        self.fileNameLabel.setText(_translate("configEdit", "File name:"))
        self.label_2.setText(_translate("configEdit", "Description"))
        self.label_5.setText(_translate("configEdit", "Background Volume"))
        self.label_3.setText(_translate("configEdit", "Announcements"))
        self.announceList.setSortingEnabled(True)
        self.editGUIAnnounce.setText(_translate("configEdit", "Edit"))
        self.editEditorAnnounce.setText(_translate("configEdit", "Edit with\n"
"Editor"))
        self.editVimAnnounce.setText(_translate("configEdit", "Edit with \n"
"Vim"))
        self.fileManagerAnnounceButton.setText(_translate("configEdit", "Open in\n"
"File Manager"))
        self.label_4.setText(_translate("configEdit", "Background specification"))
        self.backgroundList.setSortingEnabled(True)
        self.editGUIBackground.setText(_translate("configEdit", "Edit"))
        self.editEditorBackground.setText(_translate("configEdit", "Edit with\n"
"Editor"))
        self.editVimBackground.setText(_translate("configEdit", "Edit with\n"
"Vim"))
        self.fileManagerBackgroundButton.setText(_translate("configEdit", "Open in\n"
"File Manager"))
        self.configSave.setText(_translate("configEdit", "Save"))
        self.saveAsButton.setText(_translate("configEdit", "SaveAs"))
        self.cancel.setText(_translate("configEdit", "Cancel"))
