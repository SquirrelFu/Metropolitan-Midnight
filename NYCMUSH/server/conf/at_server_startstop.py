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
import os
from evennia.utils import search
from evennia import create_script
from evennia import DefaultCharacter
import commands
def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    if os.path.isfile(r'.\spherestatus\v_status.txt'):
        settings.VAMP_STATUS = open(r'.\spherestatus\v_status.txt').read()
    if os.path.isfile('.\spherestatus\ww_status.txt'):
        settings.WOLF_STATUS = open('.\spherestatus\ww_status.txt').read()
    if os.path.isfile('.\spherestatus\ma_status.txt'):
        settings.MAGE_STATUS = open('.\spherestatus\ma_status.txt').read()
    if os.path.isfile('.\spherestatus\ch_status.txt'):
        settings.LING_STATUS = open('.\spherestatus\ch_status.txt').read()
    if os.path.isfile('.\spherestatus\hn_status.txt'):
        settings.HUNTER_STATUS = open('.\spherestatus\hn_status.txt').read()
    if os.path.isfile(r'.\spherestatus\bt_status.txt'):
        settings.BEAST_STATUS = open(r'.\spherestatus\bt_status.txt').read()
    if os.path.isfile('.\spherestatus\mm_status.txt'):
        settings.MUMMY_STATUS = open('.\spherestatus\mm_status.txt').read()
    if os.path.isfile('.\spherestatus\pm_status.txt'):
        settings.PROMETHEAN_STATUS = open('.\spherestatus\pm_status.txt').read()
    if os.path.isfile('.\spherestatus\dm_status.txt'):
        settings.DEMON_STATUS = open('.\spherestatus\dm_status.txt').read()
    if os.path.isfile(".\spherestatus\pv_status.txt"):
        settings.PSYVAMP_STATUS = open('.\spherestatus\pv_status.txt').read()
    if os.path.isfile(r".\spherestatus\at_status.txt"):
        settings.ATARIYA_STATUS = open(r'.\spherestatus\at_status.txt').read()
    if os.path.isfile(".\spherestatus\dr_status.txt"):
        settings.DREAMER_STATUS = open('.\spherestatus\dr_status.txt').read()
    if os.path.isfile(".\spherestatus\if_status.txt"):
        settings.INFECTED_STATUS = open('.\spherestatus\if_status.txt').read()
    if os.path.isfile(".\spherestatus\pl_status.txt"):
        settings.PLAIN_STATUS = open('.\spherestatus\pl_status.txt').read()
    if os.path.isfile(".\spherestatus\lb_status.txt"):
        settings.LOSTBOYS_STATUS = open('.\spherestatus\lb_status.txt').read()
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
    if settings.VAMP_STATUS != "???":
        v_status = open(r'.\spherestatus\v_status.txt','w')
        v_status.write(str(settings.VAMP_STATUS))
    if settings.WOLF_STATUS != "???":
        ww_status = open('.\spherestatus\ww_status.txt','w')
        ww_status.write(str(settings.WOLF_STATUS))
    if settings.MAGE_STATUS != "???":
        ma_status = open('.\spherestatus\ma_status.txt','w')
        ma_status.write(str(settings.MAGE_STATUS))
    if settings.LING_STATUS != "???":
        ch_status = open('.\spherestatus\ch_status.txt','w')
        ch_status.write(str(settings.LING_STATUS))
    if settings.HUNTER_STATUS != "???":
        hn_status = open('.\spherestatus\hn_status.txt','w')
        hn_status.write(str(settings.HUNTER_STATUS))
    if settings.BEAST_STATUS != "???":
        bt_status = open(r'.\spherestatus\bt_status.txt','w')
        bt_status.write(str(settings.BEAST_STATUS))
    if settings.MUMMY_STATUS != "???":
        mm_status = open('.\spherestatus\mm_status.txt','w')
        mm_status.write(str(settings.MUMMY_STATUS))
    if settings.PROMETHEAN_STATUS != "???":
        pm_status = open('.\spherestatus\pm_status.txt','w')
        pm_status.write(str(settings.PROMETHEAN_STATUS))
    if settings.DEMON_STATUS != "???":
        dm_status = open('.\spherestatus\dm_status.txt','w')
        dm_status.write(str(settings.DEMON_STATUS))
    if settings.ATARIYA_STATUS != "???":
        at_status = open(r'.\spherestatus\at_status.txt','w')
        at_status.write(str(settings.ATARIYA_STATUS))
    if settings.DREAMER_STATUS != "???":
        dr_status = open('.\spherestatus\dr_status.txt','w')
        dr_status.write(str(settings.DREAMER_STATUS))
    if settings.INFECTED_STATUS != "???":
        if_status = open('.\spherestatus\if_status.txt','w')
        if_status.write(str(settings.INFECTED_STATUS))
    if settings.LOSTBOYS_STATUS != "???":
        lb_status = open('.\spherestatus\lb_status.txt','w')
        lb_status.write(str(settings.LOSTBOYS_STATUS))
    if settings.PLAIN_STATUS != "???":
        pl_status = open('.\spherestatus\pl_status.txt','w')
        pl_status.write(str(settings.PLAIN_STATUS))
    if settings.PSYVAMP_STATUS != "???":
        pv_status = open('.\spherestatus\pv_status.txt','w')
        pv_status.write(str(settings.PSYVAMP_STATUS))


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
