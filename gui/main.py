"""
Main GUI for the announce system
"""
import sys
import pprint   #pylint: disable=W0611
from PyQt5 import QtWidgets

import transitions
import mainWindowMain
import default

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)  #pylint: disable=I1101

    transitions.defaultSettings = default.getDefaults()

    transitions.mainWindow = mainWindowMain.mainWindow(app)
    transitions.mainWindow.listWidget.setMouseTracking(True)

    mainWindowMain.populateConfigList()

    transitions.mainWindow.showMaximized()
    app.exec()
