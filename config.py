import sys

from aqt import mw
from aqt.utils import showWarning

# to be configured by Dev
############################
addonName = "Copy notes"
version = 2


def newVersion():
    pass


"""A string stating what could occurs with a wrong configuration file"""
otherwise = ""


# end configuration

userOption = None


def _getUserOption():
    global userOption
    if userOption is None:
        userOption = mw.addonManager.getConfig(__name__)


def getUserOption(key=None, default=None):
    _getUserOption()
    if key is None:
        return userOption
    if key in userOption:
        return userOption[key]
    else:
        return default


lastVersion = getUserOption(version, 0)
if lastVersion < version:
    newVersion()
    pass
if lastVersion > version:
    t = f"Please update add-on {addonName}. It seems that your configuration file is made for a more recent version of the add-on."
    if otherwise:
        t += "\n"+otherwise
    showWarning(t)


def writeConfig():
    mw.addonManager.writeConfig(__name__, userOption)


def update(_):
    global userOption, fromName
    userOption = None
    fromName = None


mw.addonManager.setConfigUpdatedAction(__name__, update)

fromName = None


def getFromName(name):
    global fromName
    if fromName is None:
        fromName = dict()
        for dic in getUserOption("columns"):
            fromName[dic["name"]] = dic
    return fromName.get(name)


def setUserOption(key, value):
    _getUserOption()
    userOption[key] = value
    writeConfig()
