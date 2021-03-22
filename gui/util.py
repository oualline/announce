"""
Utility functions and classes
"""

import pprint   # pylint: disable=W0611
import subprocess
from PyQt5 import QtWidgets

#pylint: disable=R0903
class genericListItem(QtWidgets.QListWidgetItem): #pylint: disable=I1101
    """
    Item for the main window configuration list.

    Includes the configuration property
    """
    def __init__(self: object, info: object, name: str) -> object:
        """
        Initialize the item

        :param info: Information about this item
        :param name: The name that's going into the selection list
        """

        self.info = info
        QtWidgets.QListWidgetItem.__init__(self, name)  #pylint: disable=I1101

def announceToString(announce: dict)->None:
    """
    Given announcement, turn it into a string

    :param announce: The announcment dictionary
    """
    if announce['comment']:
        if 'text' in announce:
            return announce['text']
        commentStr = "# "
    else:
        commentStr = ""

    return ("%s%02d:%02d  %s" % (commentStr,
                                 announce['start_hour'], announce['start_minute'],
                                 announce['short_file']))

def backgroundToString(background: dict)->None:
    """
    Given background, turn it into a string

    :param background: The background dictionary
    """
    if background['comment']:
        if 'text' in background:
            return background['text']
        commentStr = "# "
    else:
        commentStr = ""

    return ("%s%c %02d:%02d  %02d:%02d %s" % (commentStr, background['type'],
                                              background['start_hour'], background['start_minute'],
                                              background['end_hour'], background['end_minute'],
                                              background['short_file']))


def simpleEditor(fileName: str)-> None:
    """
    Run the simple editor
    """
    subprocess.run(['gedit', fileName])

def vimEditor(fileName: str)-> None:
    """
    Run the vim editor
    """
    subprocess.run(['gvim', fileName])

def fileManager(dirName: str)-> None:
    """
    Run the file manager for the given directory
    """
    subprocess.run(['thunar', dirName])

def playFile(fileName: str)-> None:
    """
    Play music file
    """
    subprocess.run(['smplayer', fileName])
