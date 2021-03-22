"""
Main GUI for the announce system
"""
import sys
import os
import pprint       # pylint: disable=unused-import
from PyQt5 import QtWidgets

from MainWindow import Ui_MainWindow

import default
import transitions
import util

sys.path.append('../bin')
import config   #pylint: disable=wrong-import-position

class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow): #pylint: disable=I1101
    """
    The top level window
    """

    #pylint: disable=no-self-use
    def buttonRefreshClicked(self, notUsed):
        """
        Called when the "Refresh" button is clicked

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        populateConfigList()

    #pylint: disable=no-self-use
    def buttonPlayClicked(self, notUsed):
        """
        Called when the "Play" button is clicked

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        configName = transitions.mainWindow.listWidget.currentItem().info['name']
        transitions.defaultSettings['currentConfig'] = configName
        default.saveDefaults(transitions.defaultSettings)
        transitions.runAnnounce(configName)

    def buttonEditClicked(self: object, notUsed: bool) -> None:
        """
        Called when the "Edit" button is clicked

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        configName = transitions.mainWindow.listWidget.currentItem().info['name']
        transitions.defaultSettings['currentConfig'] = configName
        transitions.mainToConfigEdit(transitions.mainWindow,
                                     self.listWidget.currentItem().info)

    #pylint: disable=no-self-use
    def buttonOpenFileManagerClicked(self: object, notUsed: bool) -> None:
        """
        Called when the "Open file manager" button is clicked

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        configName = transitions.mainWindow.listWidget.currentItem().info['name']
        transitions.defaultSettings['currentConfig'] = configName
        util.fileManager(config.findDir(config.CONFIG_MASTER))


    def buttonShutdownClicked(self: object, notUsed: bool)->None:
        """
        Called when the "Shutdown" button is clicked

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        transitions.mainWindow.hide()
        self.app.quit()

    def listEntryChanged(self: object, old: object, new: object) -> None:
        """
        List entry has changed.  Update items.

        :param self: Ourselves
        :param old: Old item (not used)
        :param new: New item (not used)
        """
        #pylint: disable=unused-argument
        currentItem = transitions.mainWindow.listWidget.currentItem()
        if currentItem is not None:
            configName = currentItem.info['name']
            transitions.defaultSettings['currentConfig'] = configName

    def __init__(self, app, *args, obj=None, **kwargs):
        """
        Initialize the main window

        :param self: ourselves
        :param app: Main application
        """
        #pylint: disable=unused-argument
        super(mainWindow, self).__init__(*args, **kwargs)
        self.app = app
        self.setupUi(self)

def populateConfigList():
    """
    Populate the list of configurations in the main window
    """

    transitions.mainWindow.listWidget.clear()
    configFiles = os.listdir(config.findDir(config.CONFIG_MASTER))
    if 'currentConfig' not in transitions.defaultSettings:
        transitions.defaultSettings['currentConfig'] = configFiles[0]

    for currentFile in configFiles:
        aConfig = config.readConfigFile(currentFile)
        newItem = util.genericListItem(aConfig, aConfig['description'])
        newItem.setToolTip(aConfig['description'])
        newItem.setStatusTip(aConfig['description'])

        transitions.mainWindow.listWidget.addItem(newItem)
        if transitions.defaultSettings['currentConfig'] == currentFile:
            transitions.mainWindow.listWidget.setCurrentItem(newItem)
