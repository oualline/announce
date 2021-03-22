"""
Dialog for editing a single announcement
"""
import sys
import pprint   # pylint: disable=unused-import
import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QDialog   #pylint: disable=unused-import, no-name-in-module
from PyQt5.QtCore import QTime  #pylint: disable=no-name-in-module

import announceEdit
import util
import transitions

sys.path.append('../bin')
import config   #pylint: disable=wrong-import-position

#pylint: disable=c-extension-no-member
class announceEditWindow(QtWidgets.QMainWindow, announceEdit.Ui_announceEdit):
    """
    Editing announcement window
    """
    def __init__(self, announce, insertSlot, insertFlag, *args, obj=None, **kwargs):
        #pylint: disable=unused-argument
        self.announce = announce
        self.insertSlot = insertSlot
        self.insertFlag = insertFlag
        super(announceEditWindow, self).__init__(*args, **kwargs)
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)

    def validateFile(self: object)->bool:
        """
        Validate the file selected currently

        Returns true if good, false if bad
        """
        try:
            config.findFile(config.ANNOUNCE_DIR, self.announce['short_file'])
            return True
        except FileNotFoundError:
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("Could not find file %s" % self.announce['name'])
            errorDialog.exec_()
            return False

    def selectFileButtonClicked(self) -> None:
        """
        Callback for the "select" button.
        """
        # Get the directory we are going to use
        theDir = config.findDir(config.ANNOUNCE_DIR)
        # Get the file
        fileName = QFileDialog.getOpenFileName(self,
                                               "Select File", theDir,
                                               "Announcements (*.mp3)")
        # Do we have the file?
        if fileName[0] != '':
            # Set the name to the name only
            self.announce['short_file'] = fileName[0][len(theDir)+1:]
            # Set the label
            self.fileNameLabel.setText(self.announce['short_file'])

    def applyButtonClicked(self):
        """
        Apply the changes
        """
        self.hide()
        self.announce['comment'] = self.radioComment.isChecked()
        if self.announce['comment']:
            self.announce['text'] = self.commentText.text()
        else:
            self.announce['start_hour'] = self.timeSelection.time().hour()
            self.announce['start_minute'] = self.timeSelection.time().minute()

        if self.validateFile():
            transitions.announceEditToListEdit(self.announce, self.insertSlot, self.insertFlag)

    def cancelButtonClicked(self):
        """
        Cancel button, just hide window and go away
        """
        self.hide()

    def playButtonClicked(self):
        """
        The play button has been clicked.  Play the file
        """
        if not self.validateFile():
            return
        util.playFile(config.findFile(config.ANNOUNCE_DIR,
                                      self.announce['short_file']))

    def enableParts(self):
        """
        Depending on which radio button is enabled
        enable or disable widgets
        """
        if self.radioComment.isChecked():
            self.commentText.setEnabled(True)
            self.timeSelection.setEnabled(False)
            self.selectFileButton.setEnabled(False)
            self.fileNameLabel.setEnabled(False)
            self.playButton.setEnabled(False)

            self.announce['comment'] = True
            if self.commentText.text() == '':
                self.commentText.setText(util.announceToString(self.announce))
        else:
            self.commentText.setEnabled(False)
            self.timeSelection.setEnabled(True)
            self.selectFileButton.setEnabled(True)
            self.fileNameLabel.setEnabled(True)
            self.playButton.setEnabled(True)
            self.announce['comment'] = False

            if ('short_name' in self.announce) and (self.announce['short_name'] != ''):
                theText = self.commentText.text()
                if theText[0] == '#':
                    theText = theText[1:]
                parsed = re.match(r'*(d+):(d+)+(S.*)', theText)
                if parsed is None:
                    return
                self.announce['start_hour'] = int(parsed.group(1))
                self.announce['start_minute'] = int(parsed.group(2))
                self.announce['short_file'] = parsed.group(3)
                theTime = QTime(
                    int(self.announce['start_hour']),
                    int(self.announce['start_minute']))
                self.timeSelection.setTime(theTime)
                self.fileNameLabel.setText(self.announce['short_file'])

def announceEditMain(announce: dict, insertSlot: int, insertFlag: bool) -> None:
    """
    Popup the announce editing / create menu

    :param Announce: The annoncement to edit
    :param insertSlot: Where it is located
    :param insertFlag: if true, insert above this one
    """
    global announceEdit #pylint: disable=global-statement

    announceEdit = announceEditWindow(announce, insertSlot, insertFlag)

    if announce['comment']:
        announceEdit.radioComment.setChecked(True)
        announceEdit.radioAnnounce.setChecked(False)
        theText = announce['text']
        # Get time into something QT understands
        theTime = QTime(0, 0)
    else:
        announceEdit.radioComment.setChecked(False)
        announceEdit.radioAnnounce.setChecked(True)
        theText = ''
        # Get time into something QT understands
        theTime = QTime(
            int(announce['start_hour']),
            int(announce['start_minute']))

    announceEdit.enableParts()

    announceEdit.commentText.setText(theText)
    if 'short_file' in announce:
        announceEdit.fileNameLabel.setText(announce['short_file'])
    else:
        announceEdit.fileNameLabel.setText("")

    announceEdit.timeSelection.setTime(theTime)

    announceEdit.show()
