"""
Edit a configuration file
"""
import sys
import os
import pprint   #pylint: disable=unused-import
from PyQt5 import QtWidgets

from configEdit import Ui_configEdit
import listEditMain
import transitions
import util

sys.path.append('../bin')
import config   # pylint: disable=C0413

editWindow = None       # Window we are editing in

def announceEdit(announce: object) -> None:
    """
    Edit or create an announcement list

    :param announce: The announcement information
    """
    editWindow.hide()
    fileName = announce.info['name']
    try:
        fullName = config.findFile(config.CONFIG_ANNOUNCE, fileName)
    except FileNotFoundError:
        #pylint: disable=c-extension-no-member
        errorDialog = QtWidgets.QErrorMessage()
        errorDialog.showMessage("Could not find file %s" % announce.info['name'])
        errorDialog.exec_()
    listEditMain.populateAnnounceEdit(fileName, fullName)

def backgroundEdit(background: object) -> None:
    """
    Edit a background list

    :param create: True if we are creating
    :param background: Background to create/edit
    """
    editWindow.hide()
    fileName = background.info['name']
    try:
        fullName = config.findFile(config.CONFIG_BACKGROUND, fileName)
    except FileNotFoundError:
        #pylint: disable=c-extension-no-member
        errorDialog = QtWidgets.QErrorMessage()
        errorDialog.showMessage("Could not find file %s" % background.info['name'])
        errorDialog.exec_()
    listEditMain.populateBackgroundEdit(fileName, fullName)

class configEditWindow(QtWidgets.QMainWindow, Ui_configEdit):   #pylint: disable=c-extension-no-member
    """
    Class that defines the editing window for the configuration file
    """
    def configSaveClicked(self: object, notUsed: bool) -> None:
        """
        Save the current file

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        self.guiToConfig()
        try:
            config.writeConfigFile(self.config,
                                   config.findFile(config.CONFIG_MASTER, self.config['name']))
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['name'])
            errorDialog.exec_()
        transitions.configEditToMain()

    def editEditorAnnounceClicked(self: object, notUsed: bool) -> None:
        """
        Save and edit the file using the system editor

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            util.simpleEditor(config.findFile(config.CONFIG_ANNOUNCE, self.config['announce']))
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['announce'])
            errorDialog.exec_()

    def editVimAnnounceClicked(self: object, notUsed: bool) -> None:
        """
        Save and edit the file using the VIM editor

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            util.vimEditor(config.findFile(config.CONFIG_ANNOUNCE, self.config['announce']))
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['announce'])
            errorDialog.exec_()

    def fileManagerAnnounceButtonClicked(self: object, notUsed: bool) -> None:
        """
        Open the file in the file manager

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            fullName = config.findFile(config.CONFIG_ANNOUNCE, self.config['announce'])
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['announce'])
            errorDialog.exec_()
        fullName = os.path.dirname(fullName)
        util.fileManager(fullName)

    #pylint: disable=no-self-use
    def refreshAnnounceClicked(self: object, notused: bool) -> None:
        """
        Refresh button for announcements

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        populateAnnounce(editWindow.config['announce'])

    def editEditorBackgroundClicked(self: object, notUsed: bool) -> None:
        """
        Save and edit the file using the GUI editor

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            util.simpleEditor(config.findFile(config.CONFIG_BACKGROUND, self.config['background']))
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['background'])
            errorDialog.exec_()

    def editVimBackgroundClicked(self: object, notUsed: bool) -> None:
        """
        Save and edit the file using the GUI editor

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            util.vimEditor(config.findFile(config.CONFIG_BACKGROUND, self.config['background']))

        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['background'])
            errorDialog.exec_()

    def fileManagerBackgroundButtonClicked(self: object, notUsed: bool) -> None:
        """
        Open the file manager with the indicated file

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        try:
            fullName = config.findFile(config.CONFIG_BACKGROUND, self.config['background'])
        except FileNotFoundError:
            #pylint: disable=c-extension-no-member
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.config['background'])
            errorDialog.exec_()
        fullName = os.path.dirname(fullName)
        util.fileManager(fullName)

    #pylint: disable=no-self-use
    def refreshBackgroundClicked(self: object, notused: bool) -> None:
        """
        Refresh button for background

        :param self: Us
        :param notUsed: Unused
        """
        #pylint: disable=unused-argument
        populateBackground(editWindow.config['announce'])

    def guiToConfig(self: object) -> None:
        """
        Take GUI and stick it in our local configuration
        """
        self.config['description'] = self.description.text()
        self.config['announce'] = self.announceList.currentItem().info['name']
        self.config['background'] = self.backgroundList.currentItem().info['name']
        try:
            self.config['volume'] = int(self.backgroundVolume.text())
        except ValueError:
            self.config['volume'] = 98

    def saveAsButtonClicked(self: object, notUsed: bool) -> None:
        """
        Save the current file

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        self.guiToConfig()

        # pylint: disable=c-extension-no-member
        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File",
            os.path.join(config.findDir(config.CONFIG_MASTER),
                         self.config['name']),
            "Configuration (*.txt)")

        if fileName[0] == '':
            return

        try:
            theDir = config.findDir(config.CONFIG_MASTER)
        except FileNotFoundError:
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find configuration directory")
            return

        if not fileName[0].startswith(theDir):
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("File (%s) outside of parent (%s)" %
                                    (fileName[0], theDir))
            errorDialog.exec_()
            return

        newConfig = self.config.copy()
        newConfig['name'] = fileName[0][len(theDir)+1:]

        config.writeConfigFile(newConfig, fileName[0])

        transitions.configEditToMain()

    #pylint: disable=no-self-use
    def cancelClicked(self: object, notUsed: bool) -> None:
        """
        Cancel configuration edit, return to main menu

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        transitions.configEditToMain()

    #pylint: disable=no-self-use
    def editGUIBackgroundClicked(self: object, notUsed: bool) -> None:
        """
        Background list item, edit

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        backgroundEdit(editWindow.backgroundList.currentItem())

    #pylint: disable=no-self-use
    def editGUIAnnounceClicked(self: object, notUsed: bool) -> None:
        """
        Announce list item, edit

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        announceEdit(editWindow.announceList.currentItem())

    def __init__(self, *args, obj=None, **kwargs):
        """
        Initialize the main window
        """
        #pylint: disable=unused-argument
        super(configEditWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.config = None

def populateAnnounce(name: str) -> None:
    """
    Populate the list of announcement in the config edit window

    :param name: Name of the file containing the announcements
    """

    editWindow.announceList.clear()
    announceFiles = os.listdir(config.findDir(config.CONFIG_ANNOUNCE))

    # Loop through all the announce file and display them
    for currentFile in announceFiles:
        announceInfo = config.readAnnounceFile(currentFile, True)

        # Decide if we're going to use the first line of the announcment
        # as the title
        useComment = len(announceInfo) > 0
        if useComment:
            useComment = useComment and (announceInfo[0]['comment'])
        if useComment:
            useComment = useComment and (len(announceInfo[0]['text']) > 0)
        if useComment:
            announceLine = announceInfo[0]['text'][1:]
        else:
            announceLine = currentFile
        newItem = util.genericListItem({'name': currentFile}, announceLine)

        editWindow.announceList.addItem(newItem)
        if name == currentFile:
            editWindow.announceList.setCurrentItem(newItem)

def populateBackground(name: str) -> None:
    """
    Populate the list of background songs in the config edit window

    :param name: Name of the background spec
    """

    editWindow.backgroundList.clear()
    backgroundFiles = os.listdir(config.findDir(config.CONFIG_BACKGROUND))
    backgroundFiles.sort()

    for currentFile in backgroundFiles:
        backgroundInfo = config.readBackgroundFile(currentFile, True)
        if len(backgroundInfo) > 0:
            if backgroundInfo[0]['comment']:
                backgroundLine = backgroundInfo[0]['text'][1:]
            else:
                backgroundLine = currentFile
        else:
            backgroundLine = currentFile
        newItem = util.genericListItem({'name': currentFile}, backgroundLine)

        editWindow.backgroundList.addItem(newItem)
        if name == currentFile:
            editWindow.backgroundList.setCurrentItem(newItem)

def configEditMain(configInfo: dict) -> None:
    """
    ConfigEdit/Create main window

    :param configInfo: The configuration to edit
    :param window: The main window
    """

    #pylint: disable=global-statement
    global editWindow

    if editWindow is None:
        editWindow = configEditWindow()
    editWindow.config = configInfo.copy()

    editWindow.fileNameLabel.setText("File name %s" % configInfo['name'])
    editWindow.description.setText(configInfo['description'])
    editWindow.backgroundVolume.setText(configInfo['volume'])
    editWindow.backgroundVolume.setInputMask('009')
    populateLists()

def populateLists():
    """
    Populate the two lists
    """
    populateAnnounce(editWindow.config['announce'])
    populateBackground(editWindow.config['background'])
