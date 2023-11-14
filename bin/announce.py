"""
 Announcing machine

 Input is a configuration file.
 See config.py for format.

   System will play background music until an announcement is
   schedule.  If the background audio is a song, it will be
   interrupted for the announcement.  Otherwise if the background
   is a safety or other non-scheduled announcement, it will wait
   for that announcement to finish, then play the scheduled
   announcement.

 Note: In the file any line beginning with "#" is a comment.

 File format: schedule.txt
   15:40    announce/thomas_last_15.mp3

 At 15:40 play the given announcement.
 File contains one line per announcement.,


 File format: background.txt

 m 00:00 00:00 cd/01.Track_1.mp3

 Music audio (m).  Can be played any time of the day
 (00:00 00:00).  The name of the song is cd/01.Track_1.mp3.

 a 08:00 10:00 general/safe.mp3

 Annulment (a).  Played between 8 am and 10 am (08:00 10:00).
 The name of the audio file follows.

"""
import sys
import re
import datetime
import time
import getopt
#import pprint
import select
import subprocess
import os
import signal

import config

bgHandler = None        # Handle the background work
logFile = None          # Log file handle
verbose = False         # Verbose output?
suspendFlag = False     # Are we suspended

def doCommand()->None:
    """
    Process command line options
    """
    global suspendFlag      # pylint: disable=global-statement
    command = sys.stdin.readline().rstrip()
    #v<n> -- Set background volume
    result = re.match(r'^v(\d+)', command)
    if result is not None:
        bgHandler.setVolume(int(result.group(1)))
        return

    #v+<n> -- Set background volume
    result = re.match(r'^v\+(\d+)', command)
    if result is not None:
        bgHandler.setVolume(bgHandler.getVolume() + int(result.group(1)))
        return

    #v-<n> -- Set background volume
    result = re.match(r'^v-(\d+)', command)
    if result is not None:
        bgHandler.setVolume(bgHandler.getVolume() - int(result.group(1)))
        return

    #p -- Pause
    result = re.match(r'^p', command)
    if result is not None:
        bgHandler.pause()
        input("Paused -- Press enter to continue")
        bgHandler.wait(1)
        return

    #s -- Suspend
    result = re.match(r'^s', command)
    if result is not None:
        suspendFlag = True
        print("Suspend set to %s" % suspendFlag)
        return

    #r -- Resume
    result = re.match(r'^s', command)
    if result is not None:
        suspendFlag = False
        print("Suspend set to %s" % suspendFlag)
        return

    #q -- Quit
    result = re.match(r'^q', command)
    if result is not None:
        Kill = subprocess.Popen(["/usr/bin/killall", "mpg123"])
        Kill.wait()
        sys.exit(0)

    print("Suspend set to %s" % suspendFlag)
    print("Commands:")
    print("v<n>  Set background volume (n is 0-100)")
    print("v+<n> Increase background volume (n is 0-100)")
    print("v-<n> Decrease background volume (n is 0-100)")
    print("p Pause background")
    print("s Suspend scheduled announcements")
    print("r Resume scheduled announcements")
    print("q Quit")


def getNowMinutes()->int:
    """
    Return current time in minutes
    """
    # Current time
    now = datetime.datetime.now()
    # Current time in minutes past midnight
    nowInMinutes = now.hour * 60 + now.minute
    return nowInMinutes

class background:
    """
    Handle the background music
    """
    def __init__(self: object, volume: int) -> None:
        self.announce = False    # Are we doing an announcement?
        self.backgroundList = []     # List of things that are in background
        self.backgroundIndex = -1    # Current background item
        self.backgroundPlayer = None    # Background player
        self.volume = volume

    def setVolume(self: object, volume: int) -> None:
        """
        Set the volume

        :param self: -- us
        :param volume: -- volume to set
        """
        if volume < 0:
            volume = 0
        if volume > 100:
            volume = 100
        self.volume = volume
        print("Volume is %d" % volume)
        Mixer = subprocess.Popen(["/usr/bin/amixer", "-q", "set", "Master", "%d%%" % int(self.volume)])
        Mixer.wait()

    def getVolume(self: object) -> int:
        """
        Get the volume we are currently using

        :param self: -- us
        """
        return self.volume

    def readBackground(self, fileName: str) -> None:
        """
        Read the background play list
        """
        self.backgroundList = config.readBackgroundFile(fileName, False)

    def next(self) -> None:
        """ Advance the background music to the next song"""

        log("Start background.next")

        nowMinutes = getNowMinutes()
        while True:
            self.backgroundIndex = self.backgroundIndex + 1
            if self.backgroundIndex >= len(self.backgroundList):
                self.backgroundIndex = 0
            if self.backgroundList[self.backgroundIndex]['start_hour'] == 0:
                break
            startMinutes = (self.backgroundList[self.backgroundIndex]['start_hour'] * 60 +
                            self.backgroundList[self.backgroundIndex]['start_minute'])
            if startMinutes > nowMinutes:
                log("Skipping %s because before start time (%02d:%02d - %02d:%02d)" %
                    (self.backgroundList[self.backgroundIndex]['short_file'],
                     self.backgroundList[self.backgroundIndex]['start_hour'],
                     self.backgroundList[self.backgroundIndex]['start_minute'],
                     self.backgroundList[self.backgroundIndex]['end_hour'],
                     self.backgroundList[self.backgroundIndex]['end_minute']))
                continue
            endMinutes = (self.backgroundList[self.backgroundIndex]['end_hour'] * 60 +
                          self.backgroundList[self.backgroundIndex]['end_minute'])
            if endMinutes < nowMinutes:
                log("Skipping %s because after end time (%02d:%02d - %02d:%02d)" %
                    (self.backgroundList[self.backgroundIndex]['short_file'],
                     self.backgroundList[self.backgroundIndex]['start_hour'],
                     self.backgroundList[self.backgroundIndex]['start_minute'],
                     self.backgroundList[self.backgroundIndex]['end_hour'],
                     self.backgroundList[self.backgroundIndex]['end_minute']))
                continue
            break


        log("Background playing %s" % self.backgroundList[self.backgroundIndex]['short_file'])

        if self.backgroundPlayer is not None:
            log("Waiting for background player to finish")
            self.backgroundPlayer.wait()
            log("Waiting for background player to finish -- done")
            self.backgroundPlayer = None

        self.backgroundPlayer = \
                subprocess.Popen(["/usr/bin/mpg123", "-q", self.backgroundList[self.backgroundIndex]['file_name']], stdin=subprocess.DEVNULL)
        log("Background player started %d %s" % (self.backgroundPlayer.pid, self.backgroundList[self.backgroundIndex]['file_name']))
        Mixer = subprocess.Popen(["/usr/bin/amixer", "-q", "set", "Master", "%d%%" % int(self.volume)])
        log("Mixer set to %d" % int(self.volume))
        Mixer.wait()
        self.announce = (self.backgroundList[self.backgroundIndex]['type'] == 'a')
        log("End background.next")

    def wait(self: object, waitTime: int) -> None:
        """
        Wait until the specified time has passed

        :param self: This class
        :param waitTime: Time to wait in minutes

        @note If playing announcment, wait time may be longer
        """

        log("background.wait(%d, %d) -- sending SIGCONT" % (self.backgroundPlayer.pid, waitTime))
        try:
            os.kill(self.backgroundPlayer.pid, signal.SIGCONT)
        except ProcessLookupError:
            log("SIGCONT failed because background process done")
        Mixer = subprocess.Popen(["/usr/bin/amixer", "-q", "set", "Master", "%d%%" % int(self.volume)])
        log("Mixer set to %d" % int(self.volume))
        Mixer.wait()
        stopTime = getNowMinutes() + waitTime

        while True:
            while True:
                # Wait for command or 1 second to elapse
                if select.select([sys.stdin], [], [], 1.0)[0]:
                    doCommand()
                state = self.backgroundPlayer.poll()
                if (False):
                    if (state is not None):
                        stateString = "Done"
                    else:
                        stateString = "running"
                    log("background.poll(%d, %s)" % (self.backgroundPlayer.pid, stateString))
                if state is not None:
                    break

                # Break only if timeout and not in middle of announcement
                if (getNowMinutes() >= stopTime) and (not self.announce):
                    break

            if getNowMinutes() >= stopTime:
                break
            self.next()

        log("background.wait done")

    def playForever(self) -> None:
        """
        Play background music forever
        """
        while True:
            self.wait(99999)

    def pause(self) -> None:
        """
        Pause player 
        """
        log("background.pause(%d) -- sending SIGSTOP" % (self.backgroundPlayer.pid))
        try:
            os.kill(self.backgroundPlayer.pid, signal.SIGSTOP)
        except ProcessLookupError:
            log("Background process did not pause")


def log(msg: str) -> str:
    """ Log a message to the console

        :param str: What to log
    """
    # When did this occur
    now = datetime.datetime.now()
    if verbose:
        print("%02d:%02d:%02d %s" % (now.hour, now.minute, now.second, msg))
    logFile.write("%02d:%02d:%02d %s\n" % (now.hour, now.minute, now.second, msg))

class foreground:
    """
    Handle all the foreground announcements
    """
    def __init__(self: object) -> None:
        self.scheduleList = []       # List of things that are scheduled
        self.scheduleNext = 0

    def readSchedule(self: object, fileName: str) -> None:
        """
        Read list of scheduled items.

        :param fileName: The name of the file to read
        """
        self.scheduleList = config.readAnnounceFile(fileName, False)
        for i in range(len(self.scheduleList)-1, -1, -1):
            itemMinutes = (self.scheduleList[i]['start_hour']*60 +
                           self.scheduleList[i]['start_minute'])

            if itemMinutes < getNowMinutes():
                log("Removing item because it is in the past %02d:%02d %s" %
                    (self.scheduleList[i]['start_hour'],
                     self.scheduleList[i]['start_minute'],
                     self.scheduleList[i]['short_file']))
                self.scheduleList.remove(self.scheduleList[i])

    def computeDiff(self: object) -> int:
        """
        Compute the difference between now and next announcement
        """

        scheduleMinute = (self.scheduleList[self.scheduleNext]['start_hour']*60 +
                          self.scheduleList[self.scheduleNext]['start_minute'])

        # Compute the time difference
        theTimeDiff = scheduleMinute - getNowMinutes()
        log("Foreground wait %d minutes until %02d:%02d %s" %
            (theTimeDiff,
             self.scheduleList[self.scheduleNext]['start_hour'],
             self.scheduleList[self.scheduleNext]['start_minute'],
             self.scheduleList[self.scheduleNext]['short_file']))
        return theTimeDiff

    def checkEndOfDay(self: object) -> bool:
        """
        If end of the day, play music forever.
        """
        return self.scheduleNext >= len(self.scheduleList)

    def announce(self: object) -> None:
        """
        Play announcment
        """
        log("Announce %s" % self.scheduleList[self.scheduleNext]['short_file'])
        if suspendFlag:
            print("Suspend in effect.  Skipped")
        else:
            foregroundPlayer =  \
                subprocess.Popen(["/usr/bin/mpg123", "-q", self.scheduleList[self.scheduleNext]['file_name'] ], stdin=subprocess.DEVNULL)
            log("Foreground player started (%d %s)" % (foregroundPlayer.pid, self.scheduleList[self.scheduleNext]['file_name']))
            log("Volume set to 100%")
            Mixer = subprocess.Popen(["/usr/bin/amixer", "-q", "set", "Master", "100%"])
            Mixer.wait()

            foregroundPlayer.wait()
            log("Foreground player done")

        self.scheduleNext = self.scheduleNext + 1

(options, args) = getopt.getopt(sys.argv[1:], 'v')

if len(args) != 1:
    print("Usage is announce.py [-v] <config-file>")
    sys.exit(8)

verbose = False
for currentOption in options:
    if currentOption[0] == '-v':
        verbose = True

logFile = open("/tmp/announce.log", "w")

configFile = config.findFile(config.CONFIG_MASTER, args[0])
configParam = config.readConfigFile(configFile)

bgHandler = background(int(configParam['volume']))
bgHandler.readBackground(config.findFile(config.CONFIG_BACKGROUND, configParam['background']))

fgHandler = foreground()
fgHandler.readSchedule(config.findFile(config.CONFIG_ANNOUNCE, configParam['announce']))
log("Initialization done")

log("Starting background")
bgHandler.next()

while True:
    if fgHandler.checkEndOfDay():
        bgHandler.playForever()

    timeDiff = fgHandler.computeDiff()
    if timeDiff > 0:
        bgHandler.wait(timeDiff)

    bgHandler.pause()
    fgHandler.announce()
