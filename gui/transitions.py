"""
Transition from one window to another
"""
import pprint           # pylint: disable=unused-import
import subprocess
import os

import configEditMain
import listEditMain
import util
import config
import mainWindowMain

mainWindow = None       # main window
backgroundEdit = None   # Edit background window
defaultSettings = {}    # Defaults

def runAnnounce(configName: str) -> None:
    """
    Run the announce program

    :param configName: Configuration to use for the announce program
    """
    mainWindow.hide()
    subprocess.run(["python3", "announce.py", configName])
    mainWindow.show()

def mainToConfigEdit(window: object, configInfo: dict) -> None:
    """
    We are in main and wish to edit/create a configuration.

    :param window: Main editing window
    :param configInfo: The configuration
    """
    window.hide()
    configEditMain.configEditMain(configInfo)
    configEditMain.editWindow.showMaximized()

def configEditToMain() -> None:
    """
    We are in the edit configuration window.
    Go to main window
    """
    configEditMain.editWindow.hide()
    mainWindowMain.populateConfigList()

    mainWindow.showMaximized()

def announceEditToListEdit(announce: dict, insertSlot: int, insertFlag: bool) -> None:
    """
    Announce edit is done, do an insert or update

    :param announce: Announcement information
    :param insertSlot: where to insert if inserting
    :param insertFlag: are we inserting
    """
    if insertSlot > (listEditMain.listEditWindow.listWidget.count()-1):
        listEditMain.listEditWindow.listWidget.setCurrentRow(insertSlot)

    currentRow = listEditMain.listEditWindow.listWidget.currentRow()

    label = util.announceToString(announce)
    if insertFlag:
        newItem = util.genericListItem(announce, label)
        listEditMain.listEditWindow.listWidget.insertItem(currentRow, newItem)
        listEditMain.listEditWindow.listWidget.setCurrentRow(currentRow)
    else:
        item = listEditMain.listEditWindow.listWidget.item(currentRow)
        item.setText(label)
        item.info = announce

    listEditMain.listEditWindow.show()

def backgroundInsertRepeat(info: dict, repeatCount: int) -> None:
    """
    Do an repeated insertion

    :param info: The stuff to insert
    :param repeatCount: Number of songs between repeats
    """
    currentIndex = 0
    label = util.backgroundToString(info.info)

    while currentIndex < listEditMain.listEditWindow.listWidget.count()-1:
        announceCount = 0
        while announceCount < repeatCount:
            if listEditMain.listEditWindow.listWidget.item(currentIndex).info['type'] == 'm':
                announceCount += 1
            currentIndex += 1
            if currentIndex >= listEditMain.listEditWindow.listWidget.count()-1:
                break
        if currentIndex >= listEditMain.listEditWindow.listWidget.count()-1:
            break
        newItem = util.genericListItem(info.info, label)
        listEditMain.listEditWindow.listWidget.insertItem(currentIndex, newItem)
        currentIndex += 1

    listEditMain.listEditWindow.show()


def backgroundEditToListEdit(background: dict, insertSlot: int, insertFlag: bool) -> None:
    """
    Background edit is done, do an insert or update

    :param background: Background information
    :param insertSlot: where to insert if inserting
    :param insertFlag: are we inserting
    """
    if insertSlot > (listEditMain.listEditWindow.listWidget.count()-1):
        listEditMain.listEditWindow.listWidget.setCurrentRow(insertSlot)

    currentRow = listEditMain.listEditWindow.listWidget.currentRow()

    label = util.backgroundToString(background)
    if insertFlag:
        newItem = util.genericListItem(background, label)
        listEditMain.listEditWindow.listWidget.insertItem(currentRow, newItem)
        listEditMain.listEditWindow.listWidget.setCurrentRow(currentRow)
    else:
        item = listEditMain.listEditWindow.listWidget.item(currentRow)
        item.setText(label)
        item.info = background

    listEditMain.listEditWindow.show()

def backgroundLoadAllToListEdit(directory: str):
    """
    Background edit is done, do an insert or update

    :param directory: Directory to use for loading
    """

    songDir = config.findDir(config.SONG_DIR)
    for theFile in os.scandir(directory):
        if not theFile.is_file():
            print("%s is not a file.  Skipping" % theFile.name)
            continue
        if not theFile.name.endswith(".mp3"):
            print("%s is not a music file.  Skipping" % theFile.name)
            continue

        fileName = os.path.join(directory, theFile.name)
        fileName = fileName[len(songDir)+1:]
        label = "m 00:00 00:00 %s" % fileName
        background = {
            'comment': False,
            'type': 'm',
            'start_hour': 0,
            'start_minute': 0,
            'end_hour': 0,
            'end_minute': 0,
            'short_file': fileName}
        newItem = util.genericListItem(background, label)
        listEditMain.listEditWindow.listWidget.insertItem(
            listEditMain.listEditWindow.listWidget.count()-1, newItem)

##@@    for i in range(listEditMain.listEditWindow.listWidget.count()):
##@@        print("### item %d" % i)
##@@        pprint.pprint(listEditMain.listEditWindow.listWidget.item(i).info)

    listEditMain.listEditWindow.show()

def listEditToConfig() -> None:
    """
    We are in the list editor
    Go to config window
    """
    listEditMain.listEditWindow.hide()
    configEditMain.populateLists()
    configEditMain.editWindow.showMaximized()
