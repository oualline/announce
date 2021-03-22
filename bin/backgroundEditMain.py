"""
Dialog for editing a single background entry
"""
import sys
import re
import pprint       #pylint: disable=unused-import

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QDialog   # pylint: disable=no-name-in-module, unused-import
from PyQt5.QtCore import QTime  # pylint: disable=no-name-in-module

import backgroundEdit
import util
import transitions

sys.path.append('../bin')
import config       # pylint: disable=wrong-import-position

# pylint: disable=c-extension-no-member
class backgroundEditWindow(QtWidgets.QMainWindow, backgroundEdit.Ui_backgroundEdit):
    """
    Editing background window
    """
    def __init__(self, background, insertSlot, insertFlag, *args, obj=None, **kwargs):
        #pylint: disable=unused-argument
        self.background = background
        self.insertSlot = insertSlot
        self.insertFlag = insertFlag
        super(backgroundEditWindow, self).__init__(*args, **kwargs)
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        if self.background['comment']:
            self.radioComment.setChecked(True)
            self.radioAnnounce.setChecked(False)
            self.radioMusic.setChecked(False)
        elif self.background['type'] == 'a':
            self.radioComment.setChecked(False)
            self.radioAnnounce.setChecked(True)
            self.radioMusic.setChecked(False)
        else:
            self.radioComment.setChecked(False)
            self.radioAnnounce.setChecked(False)
            self.radioMusic.setChecked(True)
        self.enableParts()


    def selectFileButtonClicked(self):
        """
        Callback for the "select" button.
        """
        # Get the directory we are going to use
        if self.background['type'] == 'a':
            theDir = config.findDir(config.ANNOUNCE_DIR)
        else:
            theDir = config.findDir(config.SONG_DIR)
        # Get the file
        fileName = QFileDialog.getOpenFileName(self,
                                               "Select File", theDir, "Background Music (*.mp3)")
        # Do we have the file?
        if fileName[0] != '':
            # Set the name to the name only
            self.background['short_file'] = fileName[0][len(theDir)+1:]
            # Set the label
            self.fileNameLabel.setText(self.background['short_file'])

    def applyButtonClicked(self):
        """
        Apply the changes
        """
        self.hide()
        self.background['comment'] = self.radioComment.isChecked()
        if self.background['comment']:
            self.background['text'] = self.commentText.text()
        else:
            if self.anyTimeCheckbox.isChecked():
                self.background['start_hour'] = 0
                self.background['start_minute'] = 0
                self.background['end_hour'] = 0
                self.background['end_minute'] = 0
            else:
                self.background['start_hour'] = self.startTime.time().hour()
                self.background['start_minute'] = self.startTime.time().minute()
                self.background['end_hour'] = self.endTime.time().hour()
                self.background['end_minute'] = self.endTime.time().minute()

        try:
            if self.background['type'] == 'a':
                config.findFile(config.GENERAL_DIR, self.background['short_file'])
            else:
                config.findFile(config.SONG_DIR, self.background['short_file'])
        except FileNotFoundError:
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("ERROR: File not found %s" % self.background['short_file'])
            errorDialog.exec_()

        transitions.backgroundEditToListEdit(self.background, self.insertSlot, self.insertFlag)

    def cancelButtonClicked(self):
        """
        Cancel button, just hide window and go away
        """
        self.hide()

    def playButtonClicked(self):
        """
        The play button has been clicked.  Play the file
        """
        try:
            if self.background['type'] == 'a':
                util.playFile(config.findFile(config.ANNOUNCE_DIR,
                                              self.background['short_file']))
            else:
                util.playFile(config.findFile(config.SONG_DIR,
                                              self.background['short_file']))
        except FileNotFoundError:
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("ERROR: File not found %s" % self.background['short_file'])
            errorDialog.exec_()

    def repeatButtonClicked(self):
        """
        The repeat button has been clicked
        """

        repeatCount = self.repeatCount.value()
        fileName = self.background['short_file']
        try:
            config.findFile(config.ANNOUNCE_DIR, fileName)
        except FileNotFoundError:
            errorDialog = QtWidgets.QErrorMessage()
            errorDialog.showMessage("ERROR: Could not find announcement file %s" %
                                    fileName)
            errorDialog.exec_()
            return

        label = util.backgroundToString(self.background)
        newItem = util.genericListItem(self.background, label)

        transitions.backgroundEdit.hide()
        transitions.backgroundInsertRepeat(newItem, repeatCount)

    def loadAllButtonClicked(self):
        """
        The "load all" button has been clicked
        """
        # Directory containing top level songs
        songDir = config.findDir(config.SONG_DIR)
        # Directory selected
        theDir = QFileDialog.getExistingDirectory(self,
                                                  "Select Directory to import",
                                                  songDir)
        if not theDir.startswith(songDir):
            print("Directory (%s) not sub-directory of %s" % (theDir, songDir))
            return

        transitions.backgroundLoadAllToListEdit(theDir)
        transitions.backgroundEdit.hide()


    def enableParts(self):
        """
        Depending on which radio button is enabled
        enable or disable widgets
        """
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-statements
        if self.radioComment.isChecked():
            self.commentText.setEnabled(True)
            self.startTime.setEnabled(False)
            self.endTime.setEnabled(False)
            self.selectFileButton.setEnabled(False)
            self.fileNameLabel.setEnabled(False)
            self.playButton.setEnabled(False)

            self.background['comment'] = True
            if self.commentText.text() == '':
                self.commentText.setText(util.backgroundToString(self.background))

            self.startTime.setEnabled(False)
            self.endTime.setEnabled(False)
        else:
            self.commentText.setEnabled(False)
            self.startTime.setEnabled(True)
            self.endTime.setEnabled(True)
            self.selectFileButton.setEnabled(True)
            self.fileNameLabel.setEnabled(True)
            self.playButton.setEnabled(True)

            if self.anyTimeCheckbox.isChecked():
                self.startTime.setEnabled(False)
                self.endTime.setEnabled(False)
            else:
                self.startTime.setEnabled(True)
                self.endTime.setEnabled(True)

            self.background['comment'] = False
            if self.radioMusic.isChecked():
                self.background['type'] = 'm'
            else:
                self.background['type'] = 'a'

            if ('short_name' in self.background) and (self.background['short_name'] != ''):
                theText = self.commentText.text()
                if theText[0] == '#':
                    theText = theText[1:]
                parsed = re.match(r'([am])\s+(\d+):(\d+)\s+(\d+):(\d+)\s+(\S.*)', theText)
                if parsed is None:
                    self.background['short_file'] = "Select a file"
                    self.background['start_hour'] = 0
                    self.background['start_minute'] = 0
                    self.background['end_hour'] = 0
                    self.background['end_minute'] = 0
                    self.background['comment'] = False
                    if self.radioMusic.checked():
                        self.background['type'] = 'm'
                    else:
                        self.background['type'] = 'a'
                    self.setValues()
                    return
                try:
                    fileName = parsed.group(6)
                    self.background['short_file'] = fileName
                    if self.background['type'] == 'a':
                        self.background['file_name'] = config.findFile(config.GENERAL_DIR, fileName)
                    else:
                        self.background['file_name'] = config.findFile(config.SONG_DIR, fileName)
                except FileNotFoundError:
                    self.background['file_name'] = ''
                    self.background['short_file'] = 'Select a file'

                self.setValues()

    def setValues(self: object) -> None:
        """
        Set the values of the various controls
        """
        if self.background['comment']:
            self.commentText.setText(self.background['text'])
            self.radioComment.setChecked(True)
            self.radioAnnounce.setChecked(False)
            self.radioMusic.setChecked(False)
        elif self.background['type'] == 'a':
            self.radioComment.setChecked(False)
            self.radioAnnounce.setChecked(True)
            self.radioMusic.setChecked(False)
            self.setTime()
            self.fileNameLabel.setText(self.background['short_file'])
        else:
            self.radioComment.setChecked(False)
            self.radioAnnounce.setChecked(False)
            self.radioMusic.setChecked(True)
            self.setTime()
            self.fileNameLabel.setText(self.background['short_file'])

    def setTime(self: object) -> None:
        """
        Set start and end time
        """
        startTime = QTime(
            int(self.background['start_hour']),
            int(self.background['start_minute']))
        endTime = QTime(
            int(self.background['end_hour']),
            int(self.background['end_minute']))
        self.startTime.setTime(startTime)
        self.endTime.setTime(endTime)
        anyTime = (int(self.background['start_hour']) == 0) and     \
                  (int(self.background['start_minute']) == 0) and   \
                  (int(self.background['end_hour']) == 0) and       \
                  (int(self.background['end_minute']) == 0)
        self.anyTimeCheckbox.setChecked(anyTime)

def backgroundEditMain(background: dict, insertSlot: int, insertFlag: bool) -> None:
    """
    Popup the background editing / create menu

    :param background: Background to edit
    :param insertSlot: If inserting, slot to insert before
    :param insertFlag: If true, we are inserting
    """

    workingBackground = background.copy()
    transitions.backgroundEdit = backgroundEditWindow(workingBackground, insertSlot, insertFlag)

    if workingBackground['comment']:
        transitions.backgroundEdit.radioComment.setChecked(True)
        transitions.backgroundEdit.radioAnnounce.setChecked(False)
        transitions.backgroundEdit.radioMusic.setChecked(False)
        theText = workingBackground['text']
        # Get time into something QT understands
        startTime = QTime(0, 0)
        endTime = QTime(0, 0)
    else:
        transitions.backgroundEdit.radioComment.setChecked(False)
        if workingBackground['type'] == 'a':
            transitions.backgroundEdit.radioAnnounce.setChecked(True)
            transitions.backgroundEdit.radioMusic.setChecked(False)
        else:
            transitions.backgroundEdit.radioAnnounce.setChecked(False)
            transitions.backgroundEdit.radioMusic.setChecked(True)

        theText = ''
        # Get time into something QT understands
        startTime = QTime(
            int(workingBackground['start_hour']),
            int(workingBackground['start_minute']))
        endTime = QTime(
            int(workingBackground['end_hour']),
            int(workingBackground['end_minute']))

    pprint.pprint(workingBackground)
    if int(workingBackground['start_hour']) == 0 and \
       int(workingBackground['start_minute']) == 0:
        transitions.backgroundEdit.anyTimeCheckbox.setChecked(True)
    else:
        transitions.backgroundEdit.anyTimeCheckbox.setChecked(False)

    transitions.backgroundEdit.enableParts()

    transitions.backgroundEdit.commentText.setText(theText)
    if 'short_file' in workingBackground:
        transitions.backgroundEdit.fileNameLabel.setText(workingBackground['short_file'])
    else:
        transitions.backgroundEdit.fileNameLabel.setText("")

    transitions.backgroundEdit.startTime.setTime(startTime)
    transitions.backgroundEdit.endTime.setTime(endTime)

    transitions.backgroundEdit.show()
