"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""
import settings
import os.path as path
import os
from evennia.utils import search
from evennia import create_script
from evennia import DefaultCharacter
def Load_Status(inString):
    loadstring = "./spherestatus/" + inString + "status.txt"
    if path.exists(loadstring):
        if inString.lower() == "vampire":
            settings.VAMPIRE_STATUS = open(loadstring).read()
        elif inString.lower() == "hunter":
            settings.HUNTER_sTATUS = open(loadstring).read()
        elif inString.lower() == "werewolf":
            settings.WOLF_STATUS = open(loadstring).read()
        elif inString.lower() == "mage":
            settings.MAGE_STATUS = open(loadstring).read()
        elif inString.lower() == "beast":
            settings.BEAST_STATUS = open(loadstring).read()
        elif inString.lower() == "changeling":
            settings.CHANGELING_STATUS = open(loadstring).read()
        elif inString.lower() == "geist":
            settings.GEIST_STATUS = open(loadstring).read()
        elif inString.lower() == "mummy":
            settings.MUMMY_STATUS = open(loadstring).read()
        elif inString.lower() == "atariya":
            settings.ATARIYA_STATUS = open(loadstring).read()
        elif inString.lower() == "dreamer":
            settings.DREAMER_STATUS = open(loadstring).read()
        elif inString.lower() == "infected":
            settings.INFECTED_STATUS = open(loadstring).read()
        elif inString.lower() == "lostboy":
            settings.LOSTBOYS_STATUS = open(loadstring).read()
        elif inString.lower() == "plain":
            settings.PLAIN_STATUS = open(loadstring).read()
        elif inString.lower() == "psyvamp":
            settings.PSYVAMP_STATUS = open(loadstring).read()
        elif inString.lower() == "demon":
            settings.DEMON_STATUS = open(loadstring).read()
        elif inString.lower() == "promethean":
            settings.PROMETHEAN_STATUS = open(loadstring).read()
def Save_Status(sphereIn):
    savestring = "./spherestatus/" + sphereIn + "status.txt"
    spherelist = ["vampire","werewolf","hunter","mage","beast",
                  "promethean","demon","changeling","geist","mummy","atariya","dreamer","infected","lostboy","plain","psyvamp"]
    if not path.exists(savestring) and sphereIn in spherelist:
        if not path.isdir("./spherestatus/"):
            os.makedirs("./spherestatus/")
        open(savestring,'w').close()
    with open(savestring,"r+") as stat:
        if sphereIn.lower() == "vampire":
            stat.write(settings.VAMPIRE_STATUS)
        elif sphereIn.lower() == "hunter":
            stat.write(settings.HUNTER_STATUS)
        elif sphereIn.lower() == "werewolf":
            stat.write(settings.WEREWOLF_STATUS)
        elif sphereIn.lower() == "mage":
            stat.write(settings.MAGE_STATUS)
        elif sphereIn.lower() == "beast":
            stat.write(settings.BEAST_STATUS)
        elif sphereIn.lower() == "changeling":
            stat.write(settings.CHANGELING_STATUS)
        elif sphereIn.lower() == "geist":
            stat.write(settings.GEIST_STATUS)
        elif sphereIn.lower() == "mummy":
            stat.write(settings.MUMMY_STATUS)
        elif sphereIn.lower() == "atariya":
            stat.write(settings.ATARIYA_STATUS)
        elif sphereIn.lower() == "dreamer":
            stat.write(settings.DREAMER_STATUS)
        elif sphereIn.lower() == "infected":
            stat.write(settings.INFECTED_STATUS)
        elif sphereIn.lower() == "lostboy":
            stat.write(settings.LOSTBOYS_STATUS)
        elif sphereIn.lower() == "plain":
            stat.write(settings.PLAIN_STATUS)
        elif sphereIn.lower() == "psyvamp":
            stat.write(settings.PSYVAMP_STATUS)
        elif sphereIn.lower() == "demon":
            stat.write(settings.DEMON_STATUS)
        elif sphereIn.lower() == "promethean":
            stat.write(settings.PROMETHEAN_STATUS)
def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    Load_Status("vampire")
    Load_Status("werewolf")
    Load_Status("mage")
    Load_Status("beast")
    Load_Status("changeling")
    Load_Status("geist")
    Load_Status("mummy")
    Load_Status("atariya")
    Load_Status("dreamer")
    Load_Status("infected")
    Load_Status("lostboy")
    Load_Status("plain")
    Load_Status("psyvamp")
    Load_Status("hunter")
    Load_Status('demon')
    Load_Status('promethean')
    try:
        beatsearch = search.scripts('BeatHandler')[0]
    except IndexError:
        beatsearch = create_script('world.beats.BeatAwarder',key='BeatHandler',persistent=True)
    charbase = DefaultCharacter.objects.filter_family()
def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    Save_Status("vampire")
    Save_Status("werewolf")
    Save_Status("mage")
    Save_Status("beast")
    Save_Status("changeling")
    Save_Status("geist")
    Save_Status("mummy")
    Save_Status("atariya")
    Save_Status("dreamer")
    Save_Status("lostboy")
    Save_Status("plain")
    Save_Status("psyvamp")
    Save_Status("hunter")
    Save_Status('demon')
    Save_Status('promethean')



def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
