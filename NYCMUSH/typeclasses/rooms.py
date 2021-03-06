"""
Room

Rooms are simple containers that has no location of their own.

"""
from datetime import datetime
from datetime import timedelta
from evennia import DefaultCharacter
from evennia import DefaultRoom
from evennia import create_script
from evennia import default_cmds
from evennia.objects.objects import DefaultObject
from evennia.utils import inherits_from
from textwrap import wrap
from dateutil.relativedelta import relativedelta
from threading import Timer

import commands.default_cmdsets
from typeclasses.exits import Exit

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_creation(self):
        self.db.features = {}
        self.db.envirotilts = []
        self.db.shadowdesc = ""
        self.db.morningdesc = ""
        self.db.afternoondesc = ""
        self.db.eveningdesc = ""
        self.db.nightdesc = ""
    def return_appearance(self, looker):
        sorted(self.contents)
        currenttime = datetime.now() - timedelta(hours=5)
        currenthour = currenttime.hour
        try:
            if looker.account.sessions.get()[0].protocol_flags['SCREENWIDTH'][0] >= 156:
                screenwidth = looker.account.sessions.get()[0].protocol_flags['SCREENWIDTH'][0]
            else:
                screenwidth = 156
        except (AttributeError, IndexError, KeyError) as e:
            screenwidth = 156
        
        leftmargin = (screenwidth/4) - 1 - len(self.name)/2
        if len(self.name) % 2 == 0:
            rightmargin = leftmargin
        else:
            rightmargin = leftmargin - 1
        outputstring = "|115/" + "-" * leftmargin + "|n|555" + self.name + "|115" + "-" * rightmargin + "\\\n"
        wrapstring = ""
        if self.db.desc:
            if looker.db.hisil:
                if looker.db.hisil == False:
                    wrapstring = wrap(self.db.desc,(screenwidth/2) - 3)
                else:
                    wrapstring = wrap(self.db.shadowdesc,(screenwidth/2) - 3)
            else:
                wrapstring = wrap(self.db.desc,(screenwidth/2) - 3)
        if wrapstring != "":
            for text in wrapstring:
                outputstring += "|115|||n " + text + " " * ((screenwidth/2) - 1 - len("| " + text)) + "|115|||n\n"
        if 6 > currenthour > 0:
            if self.db.nightdesc:
                if self.db.nightdesc != "":
                    nightwrap = wrap(self.db.nightdesc, (screenwidth/2) - 3)
                    outputstring += "|115|||n" + " " * ((screenwidth/2) - 2) + "|115|||n\n"
                    for dark in nightwrap:
                        outputstring += "|115|||n " + dark + " " * ((screenwidth/2) - 1 - len("| " + dark)) + "|115|||n\n"
        elif 12 > currenthour > 5:
            if self.db.morningdesc:
                if self.db.morningdesc != "":
                    morningwrap = wrap(self.db.morningdesc,(screenwidth/2) - 3)
                    outputstring += "|115|||n" + " " * ((screenwidth/2) - 2) + "|115|||n\n"
                    for sun in morningwrap:
                        outputstring += "|115|||n " + sun + " " * ((screenwidth/2) - 1 - len("| " + sun)) + "|115|||n\n"
        elif 18 > currenthour > 11 :
            if self.db.afternoondesc:
                if self.db.afternoondesc != "":
                    noonwrap = wrap(self.db.afternoondesc,(screenwidth/2) - 3)
                    outputstring += "|115|||n" + " " * ((screenwidth/2) - 2) +"|115|||n\n"
                    for heat in noonwrap:
                        outputstring += "|115|||n " + heat + " " * ((screenwidth/2) - 1 - len("| " + heat)) + "|115|||n\n"
        elif 24 > currenthour > 17:
            if self.db.eveningdesc:
                if self.db.eveningdesc != "":
                    eveningwrap = wrap(self.db.eveningdesc,(screenwidth/2) - 3)
                    outputstring += "|115|||n" + " " * ((screenwidth/2) - 2) + "|115|||n\n"
                    for moon in eveningwrap:
                        outputstring += "|115|||n " + moon + " " *((screenwidth/2) - 1 - len("| " + moon)) + "|115|||n\n"
        try:
            if len(self.db.envirotilts) > 0:
                outputstring += "|115+" + "-" * 48 + "|555Environmental Tilts|115" + "-" * 49 + "+\n"
                for tilt in self.db.envirotilts:
                    outputstring += "|||n " + tilt + " " * ((screenwidth/2) - 1 - len("| " + tilt)) + "|115||\n"
        except TypeError:
            pass
        outputstring += "|115+" + "-" * (screenwidth/4 - len("Characters")/2 - 1) + "|555Characters|115" + "-" * (screenwidth/4 - len("Characters")/2 - 1) + "+\n"
        for char in self.contents:
            if inherits_from(char, DefaultCharacter):
                if char.db.hidden:
                    if char.db.hidden == True and char != looker:
                        continue
                if char.db.shortdesc:
                    if char.db.shortdesc != "" and char.has_account:
                        outputstring += "|115|||n " + char.name + ": " + char.db.shortdesc + " " * ((screenwidth/2) - 1 - len("| " + char.name + ": "+ char.db.shortdesc)) + "|115||\n"
                    elif char.has_account:
                        outputstring += "|115|||n " + char.name + " " * ((screenwidth)/2 - 1 - len("| " + char.name )) + "|115||\n" 
                elif char == looker:
                    outputstring += "|115|||n " + char.name + ": |111Set your short description with +shortdesc!" + " " * ((screenwidth)/2 - 1 - len("| " + char.name + ": Set your short description with +shortdesc!")) + "|115||\n" 
                elif char.has_account:
                    outputstring += "|115|||n " + char.name + " " * ((screenwidth)/2 - 1 - len("| " + char.name )) + "|115||\n" 
        if len(self.exits) > 0:
            outputstring += "|115+" + "-" * (screenwidth/4 - len("Characters")/2 + 2) + "|555Exits|115" + "-" * (screenwidth/4 - len("Characters")/2 + 1) + "+\n"
            exitstring = ""
            exitlist = sorted(self.exits)
            for exititer in exitlist:
                if exitstring == "":
                    outputstring += "|115|||n "
                if isinstance(exititer.aliases.get(),str):
                    if isinstance(exititer.destination, Location):
                        exitstring += exititer.name + " |222<" + exititer.aliases.get().upper() + ">|n   "
                    else:
                        exitstring+= exititer.name + " <" + exititer.aliases.get().upper() + ">   "
                    if exititer == exitlist[-1] or ((exitlist.index(exititer) % 3) == 0 and exitlist.index(exititer) != 0):
                        outputstring += exitstring
                        outputstring += " " * ((screenwidth/2) - 3 - len(exitstring.replace("|222","").replace("|n",""))) + "|115|||n\n"
                        exitstring = ""
                elif isinstance(exititer.aliases.get(),list):
                    if isinstance(exititer.destination, Location):
                        exitstring += exititer.name + " |222<" + exititer.aliases.get()[0].upper() + ">|n   "
                    else:
                        exitstring += exititer.name + " <" + exititer.aliases.get()[0].upper() + ">   "
                    if exititer == exitlist[-1] or ((exitlist.index(exititer) % 3) == 0 and exitlist.index(exititer) != 0):
                        outputstring += exitstring
                        outputstring += " " * ((screenwidth/2) - 3 - len(exitstring.replace("|222","").replace("|n",""))) + "|115|||n\n"
                        exitstring = ""
                else:
                    exitstring += exititer.name + "   "        
                    if exititer == exitlist[-1] or ((exitlist.index(exititer) % 3 )== 0 and exitlist.index(exititer) != 0):
                        outputstring += exitstring
                        outputstring += " " * ((screenwidth/2) - 3 - len(exitstring.replace("|222","").replace("|n",""))) + "|115||\n"
                        exitstring = ""
        outputstring += "|115\\" + "-" * ((screenwidth/2) - 2) + "/"
        return outputstring
        
class Chargen(Room):
    def at_object_creation(self):
        default_cmdsets = commands.default_cmdsets
        super(Chargen, self).at_object_creation()
        
        self.cmdset.add(default_cmdsets.ChargenCmdSet(), permanent=True)
        if self.db.contracts:
            self.db.contracts.stop()
        self.db.contracts = create_script("changelingstats.ChangelingStatHandler",obj=self,key="ChangelingStats",persistent=True)
        if self.db.embeds:
            self.db.embeds.stop()
        self.db.embeds = create_script("demonstats.DemonStatHandler",obj=self,key="DemonStats",persistent=True)
        if self.db.transmutations:
            self.db.transmutations.stop()
        self.db.transmutations = create_script("prometheanstats.PrometheanStatHandler",obj=self,key="PrometheanStats",persistent=True)
        if self.db.disciplines:
            self.db.disciplines.stop()
        self.db.disciplines = create_script("vampirestats.VampireStatHandler",obj=self,key="VampireStats",persistent=True)
        if self.db.endowments:
            self.db.endowments.stop()
        self.db.endowments = create_script("hunterstats.HunterHandler",obj=self,key="HunterStats",persistent=True)
        if self.db.gifts:
            self.db.gifts.stop()
        self.db.gifts = create_script("werewolfstats.WerewolfStatHandler", obj=self, key="WerewolfStats", persistent=True)
        if self.db.arcana:
            self.db.arcana.stop()
        self.db.arcana = create_script("magestats.MageStatHandler",obj=self,key="MageStats",persistent=True)
        if self.db.atavisms:
            self.db.atavisms.stop()
        self.db.atavisms = create_script("beaststats.BeastStatHandler",obj=self,key="BeastStats",persistent=True)
        if self.db.merits:
            self.db.merits.stop()
        self.db.merits = create_script("merits.MeritHandler",obj=self,key="MeritList",persistent=True)
        if self.db.affinities:
            self.db.affinities.stop()
        self.db.affinities = create_script("mummystats.MummyHandler",obj=self,key="MummyStats",persistent=True)
        if self.db.equip:
            self.db.equip.stop()
        self.db.equip = create_script("world.inventory.EquipmentList",obj=self,key="EquipmentHandler",persistent=True)
class Welcome(Room):
    def at_object_creation(self):
        super(Welcome, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.WelcomeCmdSet(), permanent=True)
class GridSpace(Room):
    def at_object_creation(self):
        super(GridSpace, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.GridCmdSet(), permanent=True)
class Borough(Room):
    def at_object_creation(self):
        super(Borough, self).at_object_creation()
class Location(Room):
    def at_object_creation(self):
        super(Location, self).at_object_creation()
        self.cmdset.add(commands.default_cmdsets.LocationCmdSet(), permanent=True)
class Node(DefaultObject):
    
    def __init__(self, name, rank):
        self.db.rank = rank
        self.db.capacity = rank * 3
        self.db.name = name
        self.db.current = self.db.capacity
    def Drain(self, amount):
        capacity = self.db.capacity
        if capacity >= amount:
            capacity -= amount
            return amount
        elif capacity < amount:
            return capacity
    def Update(self):
        self.db.current += self.db.rank
        if self.db.current > self.db.capacity:
            self.db.current = self.db.capacity
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        midnight = datetime(year=tomorrow.year,month=tomorrow.month,day=tomorrow.day,hour=0,minute=0,second=0)
        interval = (midnight - datetime.now()).seconds
        t = Timer(interval, self.Update)
    def ChangeRank(self, rank):
        self.db.rank = rank