"""
Configuration file reader and writer.
Also searches the search path for
files.
"""
import os
import re
import pprint

# Master configuration
CONFIG_MASTER = "config.master"

# Foreground / background configuration
CONFIG_ANNOUNCE = "config.announce"
CONFIG_BACKGROUND = "config.background"

# Timed announcement
ANNOUNCE_DIR = "announce.d"
# General announcement (e.g. Be save)
GENERAL_DIR = "general.d"
# Songs
SONG_DIR = "songs.d"

CHECK_LIST = ["/media/sdo/GARDEN/announce/gui",
              "/mnt/usb/announce",
              "/home/user/announce",
              "/home/sdo/announce",
              os.getcwd(),
              "/media/user/GARDEN/announce",
              "/media/sdo/GARDEN/announce"]


def findFile(directory: str, theFile: str) -> str:
    """
    Look for a file in a set of standard places

    :param directory:  Directory to look for
    :param theFile: File to look for in the directory
    :returns: full path to the file or throw exception if not found
    """
    for check in CHECK_LIST:
        checkFile = os.path.join(check, directory, theFile)
        if os.path.isfile(checkFile):
            return checkFile
    raise FileNotFoundError(theFile)

def findDir(directory: str) -> str:
    """
    Look for a directory in a set of standard places
    :param directory: -- Directory to look for
    :returns: full path to the file or throw exception if not found
    """
    for check in CHECK_LIST:
        checkDir = os.path.join(check, directory)
        if os.path.isdir(checkDir):
            return checkDir
    raise FileNotFoundError(directory)

# Configuration file format
#       One line description of the config (description)
#       Foreground announcment list (foreground)
#       Background music list (background)
#       Background volume (volume)
#
#       other item is (name), the name of the file

def readConfigFile(currentFile: str):
    """
    Read configuration file, return dictionary containg
    the elements of the configuration.

    :param currentFile: File name to read

    description -- Description line
    announce -- Announcement list
    background -- Background music list
    volume -- Background volume
    """
    theFile = findFile(CONFIG_MASTER, currentFile)
    inFile = open(theFile, "r")
    result = {}
    result['description'] = inFile.readline().strip()
    result['announce'] = inFile.readline().strip()
    result['background'] = inFile.readline().strip()
    result['volume'] = inFile.readline().strip()
    result['name'] = currentFile
    inFile.close()
    return result

def writeConfigFile(config: dict, currentFile: str) -> None:
    """
    Write configuration file

    :param config: Configuration to write
    :param currentFile: File name to write

    """
    outFile = open(currentFile, "w")
    print("## config")
    pprint.pprint(config)
    outFile.write(config['description'])
    outFile.write('\n')
    outFile.write(config['announce'])
    outFile.write('\n')
    outFile.write(config['background'])
    outFile.write('\n')
    outFile.write("%d" % int(config['volume']))
    outFile.write('\n')
    outFile.close()

def readAnnounceFile(name: str, comment: bool):
    """
    Read an announcment file

    :param name: File name to read
    :param comment: Include comments

    Returns a list of announcment records

    Each record consists of

    comment(bool) -- Is this a comment
    text(str) -- The string for the comment

    start_hour -- Time of the announcement
    start_minute -- Time of the announcement

    short_file(str) -- Short file name
    file(str) -- The name of the music to play (if any) [full]
    """
    result = []

    theFile = findFile(CONFIG_ANNOUNCE, name)
    inFile = open(theFile)
    while True:
        line = inFile.readline()
        if line == '':
            break

        item = {}
        # Comment
        if re.match(r'^\s*#', line) is not None:
            item['comment'] = True
            item['text'] = line.rstrip()
            if not comment:
                continue

        # Blank line
        elif re.match(r'^\s*$', line) is not None:
            item['comment'] = True
            item['text'] = line.rstrip()
            if not comment:
                continue

        else:
            parsed = re.match(r'\s*(\d+):(\d+)\s+(\S.*)', line)
            if parsed is None:
                print("ERROR: Bad schedule line %s" % line)
                print(" -- Ignored")
                continue
            try:
                item = {'start_hour': int(parsed.group(1)),
                        'start_minute': int(parsed.group(2)),
                        'short_file': parsed.group(3),
                        'file_name': findFile(ANNOUNCE_DIR, parsed.group(3)),
                        'comment': False}
            except FileNotFoundError:
                print("WARNING: File %s not found.  Skipping" % parsed.group(3))
                continue
        result.append(item)
    inFile.close()
    return result

def writeAnnounceFile(name: str, announce) -> None:
    """
    Write an announcment file

    :param name: Name (short name) of the file
    :param announce: The data to write
    """

    theFile = os.path.join(findDir(CONFIG_ANNOUNCE), name)
    outFile = open(theFile, "w")
    for item in announce:
        if item.info['comment']:
            outFile.write(item.info['text'])
            outFile.write('\n')
        else:
            outFile.write("%02d:%02d %s\n" %
                          (item.info['start_hour'],
                           item.info['start_minute'],
                           item.info['short_file']))

    outFile.close()

def readBackgroundFile(name: str, comment: bool):
    """
    Read an backgound file

    :param name: The name of the file to read
    :param comment: If true, include comments

    Returns a list of backgound records

    Each record consists of

    comment(bool) -- Is this a comment
    text(str) -- The string for the comment

    kind --     a or m
                a -- Announcment
                m -- Music

    start_hour -- When we can first run the musci
    start_minute -- When we can first run the musci

    end_hour -- When we can last run the musci
    end_minute -- When we can last run the musci

    short_file(str) -- Short file name
    file(str) -- The name of the music to play (if any) [full]
    """
    result = []

    theFile = findFile(CONFIG_BACKGROUND, name)
    inFile = open(theFile)
    while True:
        line = inFile.readline()
        if line == '':
            break

        item = {}
        # Comment
        if re.match(r'^\s*#', line) is not None:
            item['comment'] = True
            item['text'] = line.rstrip()
            if not comment:
                continue

        # Blank line
        elif re.match(r'^\s*$', line) is not None:
            item['comment'] = True
            item['text'] = line.rstrip()
            if not comment:
                continue

        else:
            parsed = re.match(r'([am])\s+(\d+):(\d+)\s+(\d+):(\d+)\s+(\S.*)', line)
            if parsed is None:
                print("ERROR: Bad background line %s" % line)
                print(" -- Ignored")
                input("Press <enter> to continue")
                continue
            item = {
                'comment': False,
                'type': parsed.group(1),
                'start_hour': int(parsed.group(2)),
                'start_minute': int(parsed.group(3)),
                'end_hour': int(parsed.group(4)),
                'end_minute': int(parsed.group(5))}
            fileName = parsed.group(6)
            item['short_file'] = fileName
            try:
                if item['type'] == 'a':
                    item['file_name'] = findFile(GENERAL_DIR, fileName)
                else:
                    item['file_name'] = findFile(SONG_DIR, fileName)
            except FileNotFoundError:
                item['comment'] = True
                item['text'] = "#<no-file>" + line.rstrip()
                print("Missing file %s" % line.rstrip())
                if not comment:
                    continue

        result.append(item)
    inFile.close()
    return result

def writeBackgroundFile(name: str, background) -> None:
    """
    Write a background file

    :param name: Name (short name) of the file
    :param background: The data to write
    """

    theFile = os.path.join(findDir(CONFIG_BACKGROUND), name)
    outFile = open(theFile, "w")
    for item in background:
        if item.info['comment']:
            outFile.write(item.info['text'])
            outFile.write('\n')
        else:
            outFile.write("%c %02d:%02d %02d:%02d %s\n" %
                          (item.info['type'],
                           item.info['start_hour'], item.info['start_minute'],
                           item.info['end_hour'], item.info['end_minute'],
                           item.info['short_file']))

    outFile.close()
