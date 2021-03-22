"""
Handle the writing and reading of defaults
and a other utility functions
"""
import json
import os

def saveDefaults(defaultSettings: dict)->None:
    """
    Save the defaults

    :param defaultSettings: The settings to save
    """
    jsonString = json.dumps(defaultSettings)
    jsonFile = open(os.path.join(os.environ['HOME'], "announce.json"), "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def getDefaults()->dict:
    """
    Get the default

    Returns the defaults
    """
    jsonFileName = os.path.join(os.environ['HOME'], "announce.json")
    if not os.path.isfile(jsonFileName):
        return {}
    jsonFile = open(jsonFileName, "r")
    result = json.loads(jsonFile.read())
    jsonFile.close()
    return result
