"""
Edit a configuration file
"""
import sys

import pprint   #pylint: disable=W0611

from PyQt5 import QtWidgets
#from PyQt5 import Qt
from PyQt5 import QtCore
from listEdit import Ui_listEdit

import announceEditMain
import backgroundEditMain
import util
import transitions

sys.path.append('../bin')
import config   # pylint: disable=C0413

listEditWindow = None

class listEditGUI(QtWidgets.QMainWindow, Ui_listEdit):  #pylint: disable=c-extension-no-member
    """
    Class that defines the editing window for the configuration file
    """
    def buttonMoveUpPressed(self: object, notUsed: bool) -> None:
        """
        Move current entry up

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        currentRow = self.listWidget.currentRow()
        if currentRow < 1:
            return
        currentItem = self.listWidget.takeItem(currentRow)
        self.listWidget.insertItem(currentRow - 1, currentItem)
        self.listWidget.setCurrentRow(currentRow-1)

    def buttonMoveDownPressed(self: object, notUsed: bool) -> None:
        """
        Move item down

        :param self: Ourselves
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        currentRow = self.listWidget.currentRow()
        # -1 because of blank line
        # -1 because numbering starts at 0
        if currentRow >= (self.listWidget.count()-2):
            return
        currentItem = self.listWidget.takeItem(currentRow)
        self.listWidget.insertItem(currentRow + 1, currentItem)
        self.listWidget.setCurrentRow(currentRow+1)

    def buttonEditPressed(self: object, notUsed: bool) -> None:
        """
        Edit the current item

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument

        if self.listWidget.count() < 2:
            self.buttonInsertAbovePressed(False)
            return

        if self.theType == 'A':
            announceEditMain.announceEditMain(self.listWidget.currentItem().info,
                                              self.listWidget.currentRow(), False)
        else:
            currentBackground = self.listWidget.currentItem().info
            backgroundEditMain.backgroundEditMain(currentBackground,
                                                  self.listWidget.currentRow(), False)

    def buttonInsertAbovePressed(self: object, notUsed: bool) -> None:
        """
        Insert item before current item

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument

        if self.listWidget.count() < 2:
            info = {
                'comment':True,
                'text': '# '
                }
        else:
            info = self.listWidget.currentItem().info

        if self.theType == 'A':
            announceEditMain.announceEditMain(info,
                                              self.listWidget.currentRow(), True)
        else:
            backgroundEditMain.backgroundEditMain(info,
                                                  self.listWidget.currentRow(), True)

    def checkRemoveAll(self: object, shortName: str) -> None:
        """
        We are deleting a announcement from the background
        See if we delete all

        :param self: Ourselves
        :param shortName: Short file name of the announcement
        """
        msgBox = QtWidgets.QMessageBox()    #pylint: disable=c-extension-no-member
        msgBox.setText('Removing announcement')
        msgBox.setInformativeText('Remove single entry, or all entries for this announcement')
        allButton = msgBox.addButton('All', QtWidgets.QMessageBox.ResetRole)    #pylint: disable=c-extension-no-member
        cancelButton = msgBox.addButton('Cancel', QtWidgets.QMessageBox.AcceptRole) #pylint: disable=c-extension-no-member
        thisButton = msgBox.addButton('This only', QtWidgets.QMessageBox.RejectRole)    #pylint: disable=c-extension-no-member
        ret = msgBox.exec_()

        if msgBox.clickedButton() == thisButton:
            return False
        if msgBox.clickedButton() == cancelButton:
            return True
        if msgBox.clickedButton() == allButton:
            index = 0
            while index < self.listWidget.count():
                info = self.listWidget.item(index).info
                if 'short_file' not in info:
                    index += 1
                    continue
                if info['short_file'] == shortName:
                    self.listWidget.takeItem(index)
                else:
                    index += 1
            return True
        print("INTERNAL ERROR: Got %d from message box" % ret)
        pprint.pprint(msgBox.clickedButton())
        return True


    def buttonDeletePressed(self: object, notUsed: bool) -> None:
        """
        Delete the current row

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        if self.theType != 'A':
            item = self.listWidget.item(self.listWidget.currentRow())
            if item.info['type'] == 'a':
                if self.checkRemoveAll(item.info['short_file']):
                    return
        self.listWidget.takeItem(self.listWidget.currentRow())

    def buttonSavePressed(self: object, notUsed: bool) -> None:
        """
        Save the current file

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        allItems = self.listWidget.findItems('*', QtCore.Qt.MatchWildcard)  #pylint: disable=c-extension-no-member
        allItems.pop(-1)    # Remove the blank line we added

        if self.theType == 'A':
            config.writeAnnounceFile(self.fullName, allItems)
        else:
            config.writeBackgroundFile(self.fullName, allItems)

        transitions.listEditToConfig()

    def buttonSaveAsPressed(self: object, notUsed: bool) -> None:
        """
        Save the current file under a new name

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        # Get the directory we are going to use
        if self.theType == 'A':
            theDir = config.findDir(config.CONFIG_ANNOUNCE)
            #pylint: disable=c-extension-no-member
            fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enter file to save",
                                                             theDir,
                                                             "Announcement configurations (*.txt)")
        else:
            theDir = config.findDir(config.CONFIG_BACKGROUND)
            #pylint: disable=c-extension-no-member
            fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Enter file to save",
                                                             theDir,
                                                             "Background configurations (*.txt)")

        # Do we have the file?
        if fileName[0] != '':
            # Set the name to the name only
            shortName = fileName[0][len(theDir)+1:]
            allItems = self.listWidget.findItems('*', QtCore.Qt.MatchWildcard)  #pylint: disable=c-extension-no-member
            allItems.pop(-1)    # Remove the blank line we added

            # Write out the file
            if self.theType == 'A':
                config.writeAnnounceFile(shortName, allItems)
            else:
                config.writeBackgroundFile(shortName, allItems)

            transitions.listEditToConfig()

    # pylint: disable=no-self-use
    def buttonCancelPressed(self: object, notUsed: bool) -> None:
        """
        Save the current file

        :param self: Us
        :param notUsed: Not used
        """
        #pylint: disable=unused-argument
        transitions.listEditToConfig()

    def __init__(self, *args, obj=None, **kwargs):
        """
        Initialize the main window
        """
        #pylint: disable=unused-argument
        super(listEditGUI, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.theType = '?'
        self.fileName = None
        self.fullName = None

    def setType(self: object, theType: str) -> None:
        """
        Set the type to A (announce) or B (background)

        :param self: this class instance
        :param theType: A or B depending on type
        """
        self.theType = theType

    def setFileName(self: object, name: str, fullName: str) -> None:
        """
        Set the file name to be used to save this list

        :param self: Ourselves
        :param name: The name of the file (short)
        :param fullName: Full name of the file
        """
        self.fileName = name
        self.fullName = fullName

    def setTitle(self: object, titleText: str):
        """
        Set the text for the label at the top

        :param self: Ourselves
        :param titleText: The text for the title
        """
        self.editWhatLabel.setText(titleText)


def populateAnnounceEdit(name: str, fileName: str)->None:
    """
    Populate the announceEdit window (listEdit)
    and show it

    :param name: The name of the file
    :param fullName: The full name of the file
    """

    global listEditWindow   #pylint: disable=global-statement

    if listEditWindow is None:
        listEditWindow = listEditGUI()

    listEditWindow.setType('A')
    listEditWindow.setFileName(name, fileName)

    announceList = config.readAnnounceFile(name, True)
    listEditWindow.listWidget.clear()

    if announceList[0]['comment']:
        titleText = "Editing announcement: " + announceList[0]['text'][1:] + " File: " + name
    else:
        titleText = "Editing announcement file " + name
    listEditWindow.setWindowTitle(titleText)
    listEditWindow.editWhatLabel.setText(titleText)

    for currentAnnouncement in announceList:
        label = util.announceToString(currentAnnouncement)
        newItem = util.genericListItem(currentAnnouncement, label)
        listEditWindow.listWidget.addItem(newItem)

    newItem = util.genericListItem("", "")
    listEditWindow.listWidget.addItem(newItem)
    listEditWindow.showMaximized()
    listEditWindow.listWidget.setCurrentRow(1)

def populateBackgroundEdit(name: str, fullName: str)->None:
    """
    Populate the announceEdit window (listEdit)
    and show it

    :param name: The name of the file
    :param fullName: The full name of the file
    """

    global listEditWindow   #pylint: disable=global-statement

    if listEditWindow is None:
        listEditWindow = listEditGUI()

    listEditWindow.setType('B')
    listEditWindow.setFileName(name, fullName)

    backgroundList = config.readBackgroundFile(fullName, True)
    listEditWindow.listWidget.clear()

    if len(backgroundList) > 0:
        if backgroundList[0]['comment']:
            titleText = "Editing background: " + backgroundList[0]['text'][1:] + " File: " + name
        else:
            titleText = "Editing background file " + name
    else:
        titleText = "Editing background file " + name
    listEditWindow.setWindowTitle(titleText)
    listEditWindow.editWhatLabel.setText(titleText)

    for currentBackground in backgroundList:
        label = util.backgroundToString(currentBackground)
        newItem = util.genericListItem(currentBackground, label)
        listEditWindow.listWidget.addItem(newItem)

    newItem = util.genericListItem("", "")
    listEditWindow.listWidget.addItem(newItem)
    listEditWindow.showMaximized()
    listEditWindow.listWidget.setCurrentRow(1)
