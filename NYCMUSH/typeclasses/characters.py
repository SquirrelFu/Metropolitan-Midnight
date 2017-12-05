"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from django.core.urlresolvers import reverse
from template import *
import commands.default_cmdsets
from merits import *
from evennia.contrib import gendersub
from django.template.loader import get_template
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import time
from evennia import create_channel
from world.textbox import StatBlock
from evennia.utils import search
from server.conf import settings
from evennia.utils import evtable
from evennia import DefaultCharacter
RSS_ENABLED = settings.RSS_ENABLED
if RSS_ENABLED:
    try:
        import feedparser
    except ImportError:
        raise ImportError("RSS requires python-feedparser to be installed. Install or set RSS_ENABLED=False.")

class Character(gendersub.GenderCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def return_appearance(self, looker):
        if (looker.db.template == "Changeling" or looker.db.template == "Fae-Touched") and self.db.template == "Changeling":
            if self.db.lingdesc:
                return self.name +"\n" + self.caller.db.lingdesc
            else:
                return self.name + "\nThis character seems particularly unremarkable."
        else:
            if self.db.desc:
                return self.name + "\n" + self.db.desc
            else:
                return self.name + "\nThis character seems particularly unremarkable."
    def at_post_puppet(self):
        super(Character, self).at_post_puppet()
        if self.db.last_login == "":
            self.db.last_login = datetime.now()
            if self.db.last_login.hour == 0 and self.db.approved:
                self.Refresh()
            elif not self.db.approved:
                pass
        else:
            if self.db.last_login.day < datetime.now().day:
                if self.db.approved:
                    self.Refresh()
                self.db.last_login = datetime.now()
    def at_object_creation(self):
        default_cmdsets = commands.default_cmdsets
        self.db.mundanestatus = ["Status (City Hall)","Status (Entertainment)","Status (Industry)","Status (Police)","Status (Street)","Status (Community)","Status (Internet)"
                              "Status (Organized Crime)","Status (Business)"]
        self.db.plusmerits = ["Damn Lucky","Subliminal Conditioning","Carrier","Plain Reader","The Protocol","Psychic Vampirism"]
        self.db.powerlist = [10,11,12,13,15,20,25,30,50,75]
        self.db.spendlist = [1,2,3,4,5,6,7,8,10,15]
        self.db.icname = "None"
        self.db.dob_day = 1
        self.db.dob_month = 1
        self.db.dob_year = 1
        self.db.meritlimit = 10
        self.db.doing = ""
        self.db.desclist = {}
        self.db.is_npc = False
        self.db.beatlog = []
        self.db.next_sate = ""
        self.db.xplog = []
        self.db.next_clear = ""
        #When the downtime log will be next cleared, just to be plain about what this does.
        self.db.next_lethal = ""
        self.db.next_agg = ""
        self.db.overview = ""
        self.db.last_login = ""
        self.db.readmessages = [[]]
        self.db.template = "Mortal"
        self.db.specialties = OrderedDict()
        self.db.attribbase = OrderedDict([('Intelligence',1),('Wits',1),('Resolve',1),('Strength',1),('Dexterity',1),('Stamina',1),('Presence',1),('Manipulation',1),('Composure',1)])
        self.db.attributes = OrderedDict([('Intelligence',1),('Wits',1),('Resolve',1),('Strength',1),('Dexterity',1),('Stamina',1),('Presence',1),('Manipulation',1),('Composure',1)])
        self.db.mentskills = {'Academics':0, 'Computer':0, 'Crafts':0, 'Investigation':0, 'Medicine':0, 'Occult':0, 'Politics':0, 'Science':0}
        self.db.physskills = {'Athletics':0, 'Brawl':0, 'Drive':0,'Firearms':0, 'Larceny':0, 'Stealth':0, 'Survival':0, 'Weaponry':0}
        self.db.socskills = {'Animal Ken':0, 'Empathy':0, 'Expression':0, 'Intimidation':0, 'Persuasion':0, 'Socialize':0, 'Streetwise':0, 'Subterfuge':0}
        attributes = self.db.attributes
        physskills = self.db.physskills
        self.db.mentskills = OrderedDict(sorted(self.db.mentskills.items()))
        self.db.physskills = OrderedDict(sorted(self.db.physskills.items()))
        self.db.socskills = OrderedDict(sorted(self.db.socskills.items()))
        self.db.mentkeys = self.db.mentskills.keys()
        self.db.physkeys = self.db.physskills.keys()
        self.db.sockeys = self.db.socskills.keys()
        self.db.downtime = 25
        self.db.size = 5
        self.db.timelog = []
        self.db.willpowerlog = []
        self.db.init_bonus = 0
        self.db.demeanor = ""
        self.db.nature = ""
        self.db.invitation = ""
        self.db.xsplat = ""
        self.db.ysplat = ""
        self.db.icname = ""
        self.db.conditions = []
        self.db.zsplat = ""
        self.db.tilts = []
        self.db.breaklog = []
        self.db.health_bonus = 0
        self.db.miscstats = []
        self.db.speed_bonus = 0
        self.db.beats = 0
        self.db.notes = {}
        self.db.background = []
        self.db.approved = False
        self.db.sanity = 7
        self.db.oldloc = ""
        self.db.dob_day = 1
        self.db.visibility = 0
        self.db.equipinv = []
        self.db.touchstones = {}
        self.db.dob_month = 1
        self.db.dob_year = 1
        self.db.dark = False
        self.db.harvest_amount = 0
        self.db.template = "Mortal"
        self.db.sanityname = "Integrity"
        self.db.demeanorname = "Virtue"
        self.db.naturename = "Vice"
        self.db.currentbreak = ""
        self.db.techniquelist = []
        self.db.pools = {'Willpower':str(attributes['Resolve']+attributes['Composure'])+","+str(attributes['Resolve']+attributes['Composure'])}
        self.db.powers = {}
        self.db.initiative = attributes['Dexterity'] + attributes['Composure'] + self.db.init_bonus
        self.db.defense = min(attributes['Dexterity'], attributes['Wits']) + physskills['Athletics']
        self.db.speed = attributes['Strength'] + attributes['Dexterity'] + self.db.size
        self.db.concept = "None"
        self.db.meritlist = []
        total_health = self.db.size + attributes['Stamina'] + self.db.health_bonus
        self.db.health_track = []
        counter = 0
        while counter < total_health:
            self.db.health_track.append(0)
            counter += 1
        self.db.tos_stage = 0
        if self.IsAdmin():
            self.cmdset.add(default_cmdsets.AdminSet(),permanent=True)
    def Resolve(self, cond):
        for item in self.db.conditions:
            if item.lower() == cond.lower():
                self.db.conditions.remove(item)
                return
    def Inflict(self,cond, *persist):
        conditions = self.db.conditions
        condref = search.scripts('ConditionReference')[0]
        for item in condref.db.conditionlist:
            if item[0].lower() == cond.lower():
                self.msg('Flag 1')
                if len(conditions) > 0:
                    self.msg('Flag 2')
                    for thing in conditions:
                        if cond in thing[0]:
                            return -1
                        #This section checks to see if the character already has a given condition.
                        if len(persist) == 0:
                            conditions.append(item[0])
                            return item[1]
                        elif persist[0] == True:
                            if item[1] == True:
                                conditions.append(item[0] + " (Persistent)")
                                return True
                            else:
                                if len(item) == 2:
                                    if item[2] == True:
                                        conditions.append(item[0] + " (Persistent)")
                                        return True
                        #This block is for conditions that by default, are persistent. A value of, 'True' as index 1 means that it is persistent by default.
                        #If a second boolean False is present that means that the condition may in fact, be taken as non-persistent.
                        elif persist[0] == False:
                            if item[1] == True:
                                return -1
                            else:
                                conditions.append(item[0])
                                return False
                else:
                    if len(persist) == 0:
                        conditions.append(item[0])
                        return item[1]
                    elif persist[0] == True:
                        if item[1] == True:
                            conditions.append(item[0] + " (Persistent)")
                            return True
                        else:
                            if len(item) == 2:
                                if item[2] == True:
                                    conditions.append(item[0] + " (Persistent)")
                                    return True
                        #This block is for conditions that by default, are persistent. A value of, 'True' as index 1 means that it is persistent by default.
                        #If a second boolean False is present that means that the condition may in fact, be taken as non-persistent.
                    elif persist[0] == False:
                        if item[1] == True:
                            return -1
                        else:
                            conditions.append(item[0])
                            return False
            elif item[0].lower() in cond.lower():
                if conditions:
                    for thing in condref.db.conditions:
                        if thing[0] == item[0]:
                            return -1
                        if len(persist) == 0:
                            conditions.append(item[0])
                            return item[1]
                        elif persist[0] == True:
                            if item[1] == True:
                                conditions.append(item[0] + " (Persistent)")
                                return True
                            else:
                                if len(item) == 3:
                                    if item[2] == True:
                                        conditions.append(item[0] + " (Persistent)")
                                        return True
                        elif persist[0] == False:
                            if item[1] == True:
                                if len(item) == 3:
                                    if item[2] == False:
                                        conditions.append(item[0])
                                        return False
                                return -1
                            else:
                                conditions.append(item[0])
                                return False
                
                
    def announce_move_from(self, destination):
        if self.account.db.dark:
            pass
        else:
            DefaultCharacter.announce_move_from(self, destination)
    def announce_move_to(self, source):
        if self.account.db.dark:
            pass
        else:
            DefaultCharacter.announce_move_to(self, source)
    def ShowAll(self):
        finalstring = ""
        if str(self.ShowEquip()) != "":
            finalstring += "/" + "-" * 34 + "Equipment" + "-" * 34 + "\\"
            finalstring += str(self.ShowEquip())
        if str(self.ShowArmor()) != "":
            if finalstring != "":
                finalstring += "\n"
            finalstring += "/" + "-" * 35 + "Armor" + "-" * 36 + "\\"
            finalstring += "\n" + str(self.ShowArmor())
        if str(self.ShowWeapon()) != "":
            if finalstring != "":
                finalstring += "\n"
            finalstring += "/" + "-" * 34 + "Weapons" + "-" * 35 + "\\"
            finalstring += "\n" + str(self.ShowWeapon())
        if str(self.ShowVehicles()) != "":
            if finalstring != "":
                finalstring += "\n"
            finalstring += "/" + "-" * 34 + "Vehicles" + "-" * 34 + "\\"
            finalstring += "\n" + str(self.ShowVehicles())
        if str(self.ShowExplosives()) != "":
            if finalstring != "":
                finalstring += "\n"
            finalstring += "/" + "-" * 34 + "Explosives" + "-" * 33 + "\\"
            finalstring += "\n" + str(self.ShowExplosives())
        return str(finalstring)
    def ShowEquip(self):
        equiptable = evtable.EvTable("Name","Dice Bonus",border="table",header_line_char="-")
        chargenref = search.objects("Chargen")[0]
        equiptable.hrules = 0
        equiptable.vrules = 0
        equipcount = 0
        for item in self.db.equipinv:
            for ref in chargenref.db.equip.db.equipment:
                if item[0] == ref[0]:
                    equiptable.add_row(item[0],item[1])
                    equipcount += 1
        equiptable.width = 78
        if equipcount == 0:
            equiptable = ""
        return equiptable
    def ShowArmor(self):
        armortable = evtable.EvTable("Name","Armor","Strength","Defense","Speed","Coverage",border="table",header_line_char="-")
        chargenref = search.objects("Chargen")[0]
        armorcount = 0
        for item in self.db.equipinv:
            for ref in chargenref.db.equip.db.armor:
                if item[0] == ref[0]:
                    armortable.add_row(item[0],item[1],item[2],item[3],item[4],item[5])
                    armorcount += 1
        armortable.width=78
        if armorcount == 0:
            armortable = ""
        return armortable
    def ShowWeapon(self):
        weapontable = evtable.EvTable("Name","Damage","Init","Strength","Size","Tags",border="table",header_line_char="-")
        chargenref = search.objects("Chargen")[0]
        weapontable.hrules = 0
        weapontable.vrules = 0
        weaponcount = 0
        for item in self.db.equipinv:
            for ref in chargenref.db.equip.db.weapons:
                if item[0].lower() == ref[0].lower():
                    weapontable.add_row(item[0],item[1],item[2],item[3],item[4],item[5])
                    weaponcount += 1
        weapontable.width = 78
        if weaponcount == 0:
            weapontable = ""
        return weapontable
    def ShowVehicles(self):
        vehicletable = evtable.EvTable("Name","Dice Modifier","Size","Speed","Special",border="table",header_line_char="-")
        chargenref = search.objects("Chargen")[0]
        vehicletable.hrules = 0
        vehicletable.vrules = 0
        vehiclecount = 0
        for item in self.db.equipinv:
            for ref in chargenref.db.equip.db.vehicles:
                if item[0] == ref[0]:
                    vehicletable.add_row(item[0],item[1],item[2],item[3],item[4])
                    vehiclecount += 1
        vehicletable.width=78
        if vehiclecount == 0:
            vehicletable = ""
        return vehicletable
    def ShowExplosives(self):
        explosivetable = evtable.EvTable("Name","Damage","Init","Area","Force","Strength","Size","Tags",header_line_char="-")
        chargenref = search.objects("Chargen")[0]
        explosivetable.hrules = 0
        explosivetable.vrules = 0
        explosivecount = 0
        for item in self.db.equipinv:
            for ref in chargenref.db.equip.db.explosives:
                if item[0] == ref[0]:
                    explosivetable.add_row(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
                    explosivecount += 1
        explosivetable.width=78
        if explosivecount == 0:
            explosivetable = ""
        return explosivetable
    def AddItem(self, item, *customname):
        inventory = self.db.equipinv
        if len(customname) == 1:
            item[0] = customname[0] + "(" + item[0] + ")"
        if len(inventory) > 0:
            for content in inventory:
                if item[0] in content:
                    return False
                else:
                    inventory.append(item)
                    return True
        else:
            inventory.append(item)
            return True
    def RemItem(self, item):
        inventory = self.db.equipinv
        if len(inventory) > 0:
            for content in inventory:
                if item[0] in content:
                    inventory.remove(content)
                else:
                    return False
        else:
            return False
    def IsAccountAdmin(self):
        if self.locks.check_lockstring(self, "dumm:pperm(Admin)") and self.dbid != 1:
            return True
        else:
            return False
    def AddBeat(self, source, reason):
        try:
            beatchannel = search.channels('Beats')[0]
        except IndexError:
            beatchannel = create_channel('Beats',desc='A log of all beats gained by players outside of daily gains',locks='control:perm(Immortals);listen:perm(Wizards);send:false()')
        self.db.beatlog.append("From |400"+source+"|n On |224"+ time.strftime("%b") + " "+ time.strftime("%d")+" "+ time.strftime("%Y")+"|n for |040"+reason + "|n")
        beatchannel.msg(self.name + " added a beat for |040" + reason + "|n from |400" + source)
    def ShowBeats(self):
        beatbox = StatBlock("Beat Log",False,list(self.db.beatlog))
        beatbox.SetColumns(1)
        return beatbox.Show() + beatbox.Footer()
    def Refresh(self):
        if self.db.template == "Werewolf":
            if 8 > self.db.sanity > 2:
                moonfeed = feedparser.parse(settings.MOON_PHASE)
                moonout = ""
                for item in moonfeed['entries']:
                    moonout += str(item['title'])
                moonout = moonout.lower()
                if "quarter" in moonout and self.db.xsplat == "Elodoth":
                    self.msg("As your auspice moon is in the sky and your harmony risks no kuruth regardless of whether it is a personal trigger or not, you gain 1 essence.")
                    self.PoolGain('Essence',1)
                    return
                elif 'gibbous' in moonout and self.db.xsplat == "Cahalith":
                    self.msg("As your auspice moon is in the sky and your harmony risks no kuruth regardless of whether it is a personal trigger or not, you gain 1 essence.")
                    self.PoolGain('Essence',1)
                    return
                elif 'crescent' in moonout and self.db.xsplat == "Ithaeur":
                    self.msg("As your auspice moon is in the sky and your harmony risks no kuruth regardless of whether it is a personal trigger or not, you gain 1 essence.")
                    self.PoolGain('Essence',1)
                elif 'full' in moonout and self.db.xsplat == "Rahu":
                    self.msg("As your auspice moon is in the sky and your harmony risks no kuruth regardless of whether it is a personal trigger or not, you gain 1 essence.")
                    self.PoolGain('Essence',1)
                elif 'new' or 'no' in moonout and self.db.xsplat == "Irraka":
                    self.msg("As your auspice moon is in the sky and your harmony risks no kuruth regardless of whether it is a personal trigger or not, you gain 1 essence.")
                    self.PoolGain('Essence',1)
        if self.db.template == "Vampire" or self.db.template == 'Mortal':
            if self.db.template == 'Vampire':
                self.PoolSpend('Vitae',1)
                self.msg("You spend a point of vitae for rising tonight.")
            elif self.db.template == 'Mortal':
                for merit in self.db.meritlist:
                    if merit[0] == "Psychic Vampirism":
                        self.PoolSpend('Ephemera',1)
                        self.caller.msg('You spend a point of ephemera to maintain yourself.')
        elif datetime.now() >= self.db.next_lethal:
            if self.db.template == "Werewolf":
                self.heal(2,len(self.db.health_track))
                self.msg("You heal all your lethal damage overnight due to werewolf regeneration.")
            else:
                self.Heal(2,1)
                self.msg("You heal a point of lethal damage from natural recovery.")
            self.db.next_lethal = datetime.now() + timedelta(days=2)
            for merit in self.db.meritlist:
                if merit[0] == "Biokinesis" and self.db.template == "Mortal":
                    self.db.next_lethal = datetime.now() + timedelta(days=1)
            if self.db.template == "Werewolf":
                self.db.next_lethal = datetime.now() + timedelta(days=1)
        if datetime.now() >= self.db.next_agg and self.db.template != "Vampire":
            if self.db.template == 'Werewolf':
                self.Heal(3,1)
                self.msg("You heal a point of aggravated damage from natural recovery.")
            self.db.next_agg = datetime.now() + timedelta(weeks=1)
            for merit in self.db.meritlist:
                if merit[0] == "Biokinesis" and self.db.template == "Mortal":
                    self.db.next_agg = datetime.now() + timedelta(days=3,hours=12)
            if self.db.template == 'Werewolf':
                self.db.next_agg = datetime.now() + timedelta(days=3, hours=12)
        if self.db.template == "Beast" and self.db.approved:
            if self.db.next_sate == "":
                self.msg("You don't have a time when you last spent satiety for upkeep on your character, despite being approved. Please contact staff.")
            elif datetime.now() >= self.db.next_sate:
                if 10 > self.db.sanity > 0:
                    self.db.sanity -= 1
                    self.msg("Your horror consumes a dot of satiety, as it does every so often.")
                    if self.db.powerstat < 4:
                        self.db.next_sate = datetime.now() + timedelta(weeks=1)
                    elif 7 > self.db.powerstat > 3:
                        self.db.next_sate = datetime.now() + timedelta(days=3)
                    elif 10 > self.db.powerstat > 6:
                        self.db.next_sate = datetime.now() + timedelta(days=2)
                    elif self.db.powerstat == 10:
                        self.db.next_sate = datetime.now() + timedelta(days=1)
        if self.db.template != "Vampire":
            self.PoolGain('Willpower',1)
            self.msg("You regain a point of willpower, and heal all bashing damage, as twenty-four hours have passed since your last refresh.")
            self.Heal(1,len(self.db.health_track) - 1)
        try:
            if time.strftime("%A").lower() == "Sunday" and self.db.last_login.day + 7 <= datetime.now().day:
                self.caller.db.timelog = []
                self.caller.msg("As a new week begins, your downtime log is cleared.")
                self.caller.db.downtime = 25
        except ValueError:
            pass
        
    def IsMortal(self):
        if self.db.template == "Mortal":
            return True
        else:
            return False
    def IsMortalPlus(self):
        for merit in self.db.meritlist:
            if merit[0] == "Damn Lucky":
                return "Atariya"
            elif merit[0] == "Subliminal Conditioning":
                return "Dreamer"
            elif merit[0] == "Carrier":
                return "Infected"
            elif merit[0] == "The Protocol":
                return "Lost Boy"
            elif merit[0] == "Plain Reader":
                return "Plain"
            elif merit[0] == "Psychic Vampirism":
                return "Psychic Vampire"
        return False
    def UpdateSatiety(self):
        if self.db.template == "Beast":
            if not ("Gorged (Satiety)" in self.db.conditionlist) or ("Ravenous (Satiety)" in self.db.conditionlist) or ("Sated (Satiety)" in self.db.conditionlist or
                    ("Slumbering (Satiety)" in self.db.conditionlist) or "Starving (Satiety)" in self.db.conditionlist):
                if self.db.sanity == 10:
                    self.db.conditionlist.append("Slumbering (Satiety)")
                elif 10 > self.db.sanity > 6:
                    self.db.conditionlist.append("Gorged (Satiety)")
                elif 7 > self.db.sanity > 3:
                    self.db.conditionlist.append("Sated (Satiety)")
                elif 4 > self.db.sanity > 0:
                    self.db.conditionlist.append("Starving (Satiety)")
                elif self.db.sanity == 0:
                    self.db.conditionlist.append("Ravenous (Satiety)")
            else:
                for condition in self.db.conditionlist:
                    if condition == "Gorged (Satiety)" or condition == "Ravenous (Satiety)" or condition == "Sated (Satiety)" or condition == "Slumbeing (Satiety)" or condition == "Starving (Satiety)":
                        oldcond = condition
                        self.db.conditionlist.remove(condition)
                if self.db.sanity == 10:
                    if oldcond != "Slumbering (Satiety)":
                        self.msg("Your new satiety condition is, 'Slumbering'. Better wake that horror up!")
                    self.db.conditionlist.append("Slumbering (Satiety)")
                elif 10 > self.db.sanity > 6:
                    self.db.conditionlist.append("Gorged (Satiety)")
                    if oldcond != "Gorged (Satiety)":
                        self.msg("Your new satiety condition is, 'Gorged'. Let's hope this doesn't turn into a food coma!")
                elif 7 > self.db.sanity > 3:
                    self.db.conditionlist.append("Sated (Satiety)")
                    if oldcond != "Sated":
                        self.msg("Your new satiety condition is, 'Sated'. Watch our for heroes!")
                elif 4 > self.db.sanity > 0:
                    self.db.conditionlist.append("Starving (Satiety)")
                    if oldcond != "Starving (Satiety)":
                        self.msg("Your new satiety condition is, 'Starving'. Better watch that hunger of yours!")
                elif self.db.sanity == 0:
                    self.db.conditionlist.append("Ravenous (Satiety)")
                    if oldcond != "Ravenous (Satiety)":
                        self.msg("Your new satiety condition is 'Ravenous'. Get that satiety up, and quick!")
        else:
            for condition in self.db.conditionlist:
                if condition == "Gorged (Satiety)" or condition == "Ravenous (Satiety)" or condition == "Sated (Satiety)" or condition == "Slumbeing (Satiety)" or condition == "Starving (Satiety)":
                    self.db.conditionlist.remove(condition)
                    
    def PoolGain(self, pool, amount):
        try:
            current = int(self.db.pools[pool].split(",")[0])
            maxpool = int(self.db.pools[pool].split(",")[1])
            if int(amount) + current > maxpool:
                self.db.pools[pool] = str(maxpool) + "," + str(maxpool)
            else:
                self.db.pools[pool] = str(int(amount) + int(current)) + "," + str(maxpool)
        except KeyError:
            return
    def PoolSpend(self, pool, amount):
        try:
            current = int(self.db.pools[pool].split(",")[0])
            maxpool = self.db.pools[pool].split(",")[1]
            if int(amount) - current < 0:
                return
            else:
                self.db.pools[pool] = str(int(amount) - int(current)) + "," + maxpool
        except KeyError:
            return
    def IsAdmin(self):
        if self.locks.check_lockstring(self, "dumm:perm(admin)") and self.id != 1:
            return True
        else:
            return False
    def AddPower(self, power, rank):
        self.db.powers[power] = rank
    def RemPower(self, power):
        del self.db.powers[power]
    def AddTech(self, name, *value):
        techniquelist = self.db.techniquelist
        if value:
            if len(value) == 2:
                value = value[0] + "," + value[1]
            else:
                value = value[0]
        for tech in techniquelist:
            if name in tech:
                return
        if value:
            techniquelist.append(name +","+value)
        else:
            techniquelist.append(name)
    def RemoveTech(self, name):
        for tech in self.db.techniquelist:
            for value in tech.split(","):
                if name.lower() in value.lower():
                    self.db.techniquelist.remove(tech)
    def Update(self):
        attributes = self.db.attributes
        physskills = self.db.physskills
        self.db.init_bonus = 0
        self.db.speed_bonus = 0
        self.db.size = 5
        self.db.visibility = 0
        for x in self.db.meritlist:
            if x[0] == "Fleet of Foot":
                self.db.speed_bonus = int(x[1])
            if x[0] == "Fast Reflexes":
                self.db.init_bonus = int(x[1])
            if x[0] == "Resources" or x[0] in self.db.mundanestatus or x[0] == "Allies" or x[0] == "Contacts":
                visibilitymargin = int(x[1]) - 3
                if visibilitymargin > 0:
                    self.db.visibility += visibilitymargin
            if x[0] == "Fame" or x[0] == "Fame Advanced":
                self.db.visibility += int(x[1])
            if x[0] == "Giant":
                self.db.size += 1
            if x[0] == "Psychic Vampirism":
                for y in self.db.meritlist:
                    if y[0] == "Ephemeral Battery":
                        self.db.pools["Ephemera"] = self.db.pools["Ephemera"].split(",")[0] + "," + str(self.db.attributes['Resolve']+ int(y[1]))
                if int(self.db.pools["Ephemera"].split(",")[1]) > self.db.attributes[5].effective_score:
                    pass
                else:
                    self.db.pools["Ephemera"] = self.db.pools["Ephemera"].split(",")[0] + "," + str(self.db.attributes['Resolve'])
            if x[0] == "Subliminal Conditioning":
                for y in self.db.meritlist:
                    if y[0] == "Memory Palace":
                        self.db.pools["Memory"] = self.db.pools["Memory"].split(",")[0] + "," + str(self.db.attributes['Resolve'] + int(y[1]))
                if int(self.db.pools["Memory"].split(",")[1]) > self.db.attributes['Resolve']:
                    pass
                else:
                    self.db.pools["Memory"] = self.db.pools["Memory"].split(",")[0] + "," + str(self.db.attributes['Resolve'])
        self.HealthCalc()
        self.db.initiative = attributes['Dexterity'] + attributes['Composure'] + self.db.init_bonus
        self.db.speed = attributes['Strength'] + attributes['Dexterity'] + self.db.size + self.db.speed_bonus
        self.db.defense = min(attributes['Dexterity'], attributes['Wits']) + physskills['Athletics']
        self.db.pools['Willpower'] = str(attributes['Resolve'] + attributes['Composure']) + "," + str(attributes['Resolve'] + attributes['Composure']) 
    def AddPlus(self, merit):
        if merit in self.db.plusmerits:
            if merit == "Subliminal Conditioning":
                try:
                    int(self.db.pools["Memory"].split(",")[0])
                    return
                except KeyError:
                    self.db.pools.update({"Memory":str(self.db.attributes['Resolve'])+","+str(self.db.attributes['Resolve'])})
            elif merit == "Psychic Vampirism":
                try:
                    int(self.db.pools["Ephemera"].split(",")[0])
                    return
                except KeyError:
                    self.db.pools.update({"Ephemera":str(self.db.attributes['Resolve'])+","+str(self.db.attributes['Resolve'])})
        self.Update()
    def RemPlus(self, merit):
        if merit == "Subliminal Conditioning":
            try:
                del self.db.pools["Memory"]
            except KeyError:
                return False
        elif merit == "Psychic Vampirism":
            try:
                del self.db.pools["Ephemera"]
            except KeyError:
                return False
    def AddMerit(self,name,rating, *note):
        if len(self.db.meritlist) == 0:
            self.db.meritlist.append(tuple([name,rating]))
            self.AddPlus(name)
            return
        for merit in self.db.meritlist:
            if name == merit[0]:
                if rating == merit[1]:
                    return
                else:
                    if len(note) != 0:
                        self.db.meritlist.remove(merit)
                        self.db.meritlist.append(tuple([name, rating, note]))
                        return
                    else:
                        self.db.meritlist.remove(merit)
                        self.db.meritlist.append(tuple([name, rating]))
                        return
        if len(note) != 0:
            for item in note:
                if item == note[0]:
                    noteout = note[0]
                else:
                    noteout += " " + item
            self.db.meritlist.append(tuple([name,rating,noteout]))
            self.AddPlus(name)
        else:
            self.db.meritlist.append(tuple([name,rating]))
            self.AddPlus(name)
    def RemMerit(self, name):
        for merit in self.db.meritlist:
            if merit[0] == name:
                self.db.meritlist.remove(merit)
                self.RemPlus(merit[0])
    def Damage(self, damagetype, value):
        counter = 0
        health = self.db.health_track
        damageleft = value
        wraparound = False
        while damageleft > 0:
            try:
                if health[counter] < damagetype:
                    health[counter] = damagetype
                    damageleft -= 1
                elif health[counter] == damagetype and wraparound != 0 and damagetype != 3:
                    health[counter] = damagetype + 1
                    damageleft -= 1
                    counter += 1
                if health[len(health) - 1] == damagetype + 1 and health[len(health) - 1] != 3:
                    health[counter] += 1
                    damageleft -= 1
                    counter += 1
                else:
                    counter += 1
                if wraparound == 3:
                    break
            except IndexError:
                counter = 0
                wraparound += 1
        temphealth = []
        for x in health:
            temphealth.append(x)
        temphealth.sort()
        temphealth.reverse()
        self.db.health_track = temphealth
    def Heal(self, damagetype, value):
        health = self.db.health_track
        counter = 0
        while counter < value:
            if damagetype >= health[counter]:
                health[counter] = 0
            counter += 1
        temphealth = []
        for x in health:
            temphealth.append(x)
        temphealth.sort()
        temphealth.reverse()
        self.db.health_track = temphealth
    def HealthCalc(self):
        new_health = self.db.size + self.db.attributes['Stamina'] + self.db.health_bonus
        new_track = []
        if len(self.db.health_track) > new_health:
            while len(new_track) < new_health:
                new_track.append(0)
            counter = 0
            while counter < len(new_track) - 1:
                new_track[counter] = self.db.health_track[counter]
                counter += 1
            new_track.sort()
            new_track.reverse()
            self.db.health_track = new_track
        if len(self.db.health_track) < new_health:
            for level in self.db.health_track:
                new_track.append(level)
            missing_amount = new_health - len(self.db.health_track)
            counter = 0
            while counter < missing_amount:
                new_track.append(0)
                counter += 1
            new_track.sort()
            new_track.reverse()
            self.db.health_track = new_track
    def get_absolute_url(self):
        return reverse('character:sheet', kwargs={'object_name':str(self).lower()})