"""
Commands

Commands describe the input the player can do to the game.

"""
from datetime import date
from evennia import Command as BaseCommand
from evennia import default_cmds
import os
import random
from server.conf import settings
from textwrap import wrap
from evennia.utils.evmenu import get_input
import re
from typeclasses import merits
from string import capwords
import datetime
from exceptions import NameError
from world.textbox import StatBlock
from evennia.utils import search
from evennia import DefaultCharacter
import time
from evennia import create_channel
from itertools import izip
from evennia.utils import evtable
from evennia.utils import inherits_from
from evennia.utils import utils
from evennia import create_script
# from evennia import default_cmds

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_command(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_command(): Extra actions, often things done after
            every command, like prompts.

    """
    pass
class ChargenItems(default_cmds.MuxCommand):
    """
    This command requires a switch, and will either add or remove an item from your inventory.
    It must match an item found in either the core Chronicles of Darkness book, or in Hurt Locker.
    An equals sign may be placed after the name in order to provide an alias for the item itself,
    such as a named sword or a specific model of car.
    Syntax:
        +item/add <Item>
        +item/rem <Item>
    """
    key = "+item"
    help_category = "Chargen"
    lock = "cmd:inside(Chargen)"
    def func(self):
        if len(self.switches) > 0:
            switch = self.switches[0]
            lhs = self.lhs
            rhs = self.rhs
            if switch == "add":
            #Given that this format is used in both the adding and removal sections,
            #only one set of comments will be present for both.
                for gear in self.caller.location.db.equip.db.equipment:
                #Iterates through the chargen room's list of equipment, specifically miscellaneous
                #forms of equipment. This is anything that isn't armor, a weapon, a vehicle, or
                #An explosive. As such, these are mostly skill-boosting tools.
                    if lhs.lower() == gear[0].lower():
                    #Checks to see if the argument is found in the equipment listing.
                    #Within the listing, the first AKA zeroth element is the name.
                    #The .lower() part is to allow for case-insensitive checking.
                        if rhs:
                        #Checks to see if the user specified an alternate name to be used for the equipment.
                            self.caller.AddItem(gear,rhs)
                            self.caller.msg(gear[0] + " added to your inventory as " + rhs)
                            #Of course, actually adds the gear itself. It's based on the equipment list
                            #in the chargen room instead of the user's input for standardization purposes.
                        else:
                            self.caller.AddItem(gear)
                            self.caller.msg(gear[0] + " added to your inventory")
                        return
                for tank in self.caller.location.db.equip.db.armor:
                    if lhs.lower() == tank[0].lower():
                        if rhs:
                            self.caller.AddItem(tank, rhs)
                            self.caller.msg(tank[0] + " added to your inventory as " + rhs)
                        else:
                            self.caller.AddItem(tank)
                            self.caller.msg(tank[0] + " added to your inventory")
                        return
                for harm in self.caller.location.db.equip.db.weapons:
                    if lhs.lower() == harm[0].lower():
                        if rhs:
                            self.caller.AddItem(harm, rhs)
                            self.caller.msg(harm[0] + " added to your inventory as " + rhs)
                        else:
                            self.caller.AddItem(harm)
                            self.caller.msg(harm[0] + " added to your inventory")
                        return
                for boom in self.caller.location.db.equip.db.explosives:
                    if lhs.lower() == boom[0].lower():
                        if rhs:
                            self.caller.AddItem(boom, rhs)
                            self.caller.msg(boom[0] + " added to your inventory as " + rhs)
                        else:
                            self.caller.AddItem(boom)
                            self.caller.msg(boom[0] + " added to your inventory")
                        return
                for zoom in self.caller.location.db.equip.db.vehicles:
                    if lhs.lower() == zoom[0].lower():
                        if rhs:
                            self.caller.AddItem(zoom,rhs)
                            self.caller.msg(zoom[0] + " added to your inventory as " + rhs)
                        else:
                            self.caller.AddItem(zoom)
                            self.caller.msg(zoom[0] + " added to your inventory")
                        return
                self.caller.msg("Invalid item!")
                return
            elif switch == "rem":
                for gear in self.caller.location.db.equip.db.equipment:
                    if lhs.lower() == gear[0].lower():
                        self.caller.RemItem(gear)
                        self.caller.msg(gear[0] + " removed from your inventory")
                        return
                for tank in self.caller.location.db.equip.db.armor:
                    if lhs.lower() == tank[0].lower():
                        self.caller.RemItem(tank)
                        self.caller.msg(tank[0] + " removed from your inventory")
                        return
                for harm in self.caller.location.db.equip.db.weapons:
                    if lhs.lower() == harm[0].lower():
                        self.caller.RemItem(harm)
                        self.caller.msg(harm[0] + " removed from your inventory")
                        return
                for boom in self.caller.location.db.equip.db.explosives:
                    if lhs.lower() == boom[0].lower():
                        self.caller.RemItem(boom)
                        self.caller.msg(boom[0] + " removed from your inventory")
                        return
                for zoom in self.caller.location.db.equip.db.vehicles:
                    if lhs.lower() == zoom[0].lower():
                        self.caller.RemItem(zoom)
                        self.caller.msg(zoom[0] + " removed from your inventory")
                        return
                self.caller.msg("Invalid item!")
                return
        else:
            self.caller.msg("Please select whether you are going to add or remove an item.")
class MarkNPC(Command):
    """
    Only useable by wizards, this command allows the admin to mark a specific character as an NPC,
    or remove it and designate them as a player character.
    """
    key = "+NPC"
    aliases = "+npc"
    lock = "cmd:(Wizards)"
    help_category="Admin"
    def func(self):
        if self.caller.db.is_npc == False:
            self.caller.db.is_npc = True
            self.locks.add('puppet:pperm(Wizards)')
            #This bit might seem odd. What it does is allows the NPC to be puppeted by any wizard.
            #As multiple locks can coexist, this is more or less just an extra parameter that
            #allows wizards to puppet it in addition to allowing the basic player to puppet the
            #character. 
            self.caller.msg("Character marked as an NPC.")
        elif self.caller.db.is_npc == True:
            self.caller.db.is_npc = False
            self.locks.remove('puppet:pperm(Wizards)')
            #As implied, removes the ability for any and every wizard to puppet the character.
            self.caller.msg("Character marked as a PC")
class CensusCommand(Command):
    """
    This command allows you to see a census of all the characters on the MUSH. The
    number not in parentheses is the number of approved characters, the number in
    parentheses is the number of unapproved characters.
    """
    key = "+census"
    lock = "cmd:all()"
    help_category = "OOC"
    def parse(self):
        self.args = self.args.strip()
    def func(self):
        charlist = DefaultCharacter.objects.filter_family()
        #Gets every character that inherits from, "DefaultCharacter".
        chargenref = search.objects("Chargen")[0]
        #Searches for the Chargen room, mostly for purposes of identifying
        #psychic characters by comparing all the merits on the character's
        #sheet to the list of supernatural merits, and consequently saying
        #whether or not they qualify as a psychic. It only does this for
        #those with a template string of, "Mortal" so it doesn't identify
        #vampires using the Coil of Zirnitra as M+ psychics erroneously.
        approvelist = []
        tentativelist = []
        mortalcount = 0
        unappmortal = 0
        vampcount = 0
        ghoulcount = 0
        unappvamp = 0
        unappghoul = 0
        wolfcount = 0
        bloodcount = 0
        unappwolf = 0
        unappblood = 0
        magecount = 0
        proxcount = 0
        unappmage = 0
        unappprox = 0
        lingcount = 0
        faecount = 0
        unappling = 0
        unappfae = 0
        beastcount = 0
        unappbeast = 0
        demoncount = 0
        unappdemon = 0
        mummycount = 0
        unappmummy = 0
        prommiecount = 0
        unappprommie = 0
        huntercount = 0
        unapphunter = 0
        psyvampcount = 0
        unapppsyvamp = 0
        infectedcount = 0
        unappinfected = 0
        atariyacount = 0
        unappatariya = 0
        dreamercount = 0
        unappdreamer = 0
        plaincount = 0
        unappplain = 0
        psicount = 0
        unapppsi = 0
        lostboycount = 0
        unapplostboy = 0
        marker = 0
        malecount = 0
        unappmale = 0
        femalecount = 0
        unappfemale = 0
        neutcount = 0
        unappneut = 0
        censusout = []
        demographics = []
        self.superplayer = None
        for character in charlist:
            if character.db.approved:
                cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
                if character.db.last_login <= cutoff:
                    continue
                approvelist.append(character)
            #This bit checks to see if the character is approved and what's more,
            #only uses the characters that have been active within the last 30 days.
            else:
                tentativelist.append(character)
        for entry in approvelist:
            if entry.is_superuser or entry.player == self.superplayer:
                self.superplayer = entry.player
                continue
                #Makes sure that the superuser isn't added for security reasons.
            record = ""
            if entry.db.is_npc:
                continue
                #Makes sure that NPCs aren't added to the census, what with them being plot characters.
            if entry.db.gender == "male":
                malecount += 1
            elif entry.db.gender == "female":
                femalecount += 1
            else:
                neutcount += 1
            #Obviously, these three branches check the gender of the character being scanned for
            #demographic purposes.
            if entry.db.template == "Mortal":
                for merit in entry.db.meritlist:
                    if merit[0].lower() == "psychic vampirism" and record == "":
                        psyvampcount += 1
                        record = "psychic vampire"
                    elif merit[0].lower() == "carrier" and record == "":
                        infectedcount += 1
                        record = "infected"
                    elif merit[0].lower() == "damn lucky" and record == "":
                        atariyacount += 1
                        record = "atariya"
                    elif merit[0].lower() == "plain reader" and record == "":
                        plaincount += 1
                        record = "plain"
                    elif merit[0].lower() == "subliminal conditioning" and record == "":
                        dreamercount += 1
                        record = "dreamer"
                    elif merit[0].lower() == "the protocol":
                        lostboycount += 1
                        record = "lostboy"
                    for merit in entry.db.meritlist:
                        for psi in chargenref.db.merits.supernatural:
                            if merit[0] == psi[0] and record == "":
                                psicount += 1
                                record = "psychic"
                    #This whole segment iterates through the list of merits the individual character
                    #that's being scanned has. 'Record' is set to the M+ variety of course, and the
                    #evaluating segments don't search for other types if they already have one merit.
                if record == "":
                    mortalcount += 1
            if entry.db.template == "Vampire":
                vampcount += 1
            if entry.db.template == "Ghoul":
                ghoulcount += 1
            if entry.db.template == "Werewolf":
                wolfcount += 1
            if entry.db.template == "Wolfblood":
                bloodcount += 1
            if entry.db.template == "Mage":
                magecount += 1
            if entry.db.template == "Proximus":
                proxcount += 1
            if entry.db.template == "Changeling":
                lingcount += 1
            if entry.db.template == "Fae-Touched":
                faecount += 1
            if entry.db.template == "Beast":
                beastcount += 1
            if entry.db.template == "Mummy":
                mummycount += 1
            if entry.db.template == "Demon":
                demoncount += 1
            if entry.db.template == "Promethean":
                prommiecount += 1
            if entry.db.template == "Hunter":
                huntercount += 1
            marker += 1
        marker = 0
        for entry in tentativelist:
            if entry.is_superuser or entry.player == self.superplayer:
                self.superplayer = entry.player
                continue
            record = ""
            if entry.db.is_npc:
                continue
            if entry.db.gender == "male":
                unappmale += 1
            elif entry.db.gender == "female":
                unappfemale += 1
            else:
                unappneut += 1
            if entry.db.template == "Mortal":
                for merit in entry.db.meritlist:
                    if merit[0].lower() == "psychic vampirism":
                        unapppsyvamp += 1
                        record = "psychic vampire"
                    elif merit[0].lower() == "carrier":
                        unappinfected += 1
                        record = "infected"
                    elif merit[0].lower() == "damn lucky":
                        unappatariya += 1
                        record = "atariya"
                    elif merit[0].lower() == "plain reader":
                        unappplain += 1
                        record = "plain"
                    elif merit[0].lower() == "subliminal conditioning":
                        unappdreamer += 1
                        record = "dreamer"
                    elif merit[0].lower() == "the protocol":
                        unapplostboy += 1
                        record = "lost boy"
                    for merit in entry.db.meritlist:
                        for psi in chargenref.db.merits.supernatural:
                            if merit[0] == psi[0] and record == "":
                                unapppsi += 1
                                record = "psychic"
                if record == "":
                    unappmortal += 1
            if entry.db.template == "Vampire":
                unappvamp += 1
            if entry.db.template == "Ghoul":
                unappghoul += 1
            if entry.db.template == "Werewolf":
                unappwolf += 1
            if entry.db.template == "Wolfblood":
                unappblood += 1
            if entry.db.template == "Mage":
                unappmage += 1
            if entry.db.template == "Proximus":
                unappprox += 1
            if entry.db.template == "Changeling":
                unappling += 1
            if entry.db.template == "Fae-Touched":
                unappfae += 1
            if entry.db.template == "Beast":
                unappbeast += 1
            if entry.db.template == "Mummy":
                unappmummy += 1
            if entry.db.template == "Demon":
                unappdemon += 1
            if entry.db.template == "Promethean":
                unappprommie += 1
            if entry.db.template == "Hunter":
                unapphunter += 1
            marker += 1
        if mortalcount > 0 and unappmortal > 0:
            censusout.append("Mortals,"+str(mortalcount)+" ("+str(unappmortal)+")")
        elif mortalcount > 0:
            censusout.append("Mortals,"+str(mortalcount))
        elif unappmortal > 0:
            censusout.append("Mortals,"+"("+str(unappmortal)+")")
        if psicount > 0 and unapppsi > 0:
            censusout.append('Psychics,' + str(psicount) + " (" + str(unapppsi) + ")")
        elif psicount > 0:
            censusout.append('Psychics,' + str(psicount))
        elif unapppsi > 0:
            censusout.append('Psychics,' + "(" + str(unapppsi) + ")")
        if atariyacount > 0 and unappatariya > 0:
            censusout.append("Atariya,"+str(atariyacount)+" ("+str(unappatariya)+")")
        elif atariyacount > 0:
            censusout.append("Atariya,"+str(atariyacount))
        elif unappatariya > 0:
            censusout.append("Atariya,"+"("+str(unappatariya)+")")
        if dreamercount > 0 and unappdreamer > 0:
            censusout.append("Dreamers,"+str(dreamercount) + " ("+str(unappdreamer)+")")
        if infectedcount > 0 and unappinfected > 0:
            censusout.append("Infected,"+str(infectedcount) +" ("+str(unappinfected)+")")
        elif infectedcount > 0:
            censusout.append("Infected,"+str(infectedcount))
        elif unappinfected > 0:
            censusout.append("Infected,"+"("+str(unappinfected)+")")
        if lostboycount > 0 and unapplostboy > 0:
            censusout.append("Lost Boys,"+str(lostboycount) + " (" + str(unapplostboy) + ")")
        elif lostboycount > 0:
            censusout.append('Lost Boys,'+str(lostboycount))
        elif unapplostboy > 0:
            censusout.append('Lost Boys,' +"(" + str(unapplostboy) + ")")
        if plaincount > 0 and unappplain > 0:
            censusout.append("Plain,"+str(plaincount) + " (" + str(unappplain) + ")")
        elif plaincount > 0:
            censusout.append("Plain,"+str(plaincount))
        elif unappplain > 0:
            censusout.append('Plain', "(" + str(unappplain) + ")")
        if psyvampcount > 0 and unapppsyvamp > 0:
            censusout.append("Psychic Vampires,"+str(psyvampcount) + " (" + str(unapppsyvamp) + ")" )
        elif psyvampcount > 0:
            censusout.append('Psychic Vampires,'+str(psyvampcount))
        elif unapppsyvamp > 0:
            censusout.append('Psychic Vampires,' + "("+str(unapppsyvamp)+")")
        if vampcount > 0 and unappvamp > 0:
            censusout.append("Vampires,"+str(vampcount) + " (" + str(unappvamp) +")")
        elif vampcount > 0:
            censusout.append('Vampires,'+str(vampcount))
        elif unappvamp > 0:
            censusout.append('Vampires,' + "(" + str(unappvamp) + ")")
        if ghoulcount > 0 and unappghoul > 0:
            censusout.append('Ghouls, ' + str(ghoulcount) + " (" + str(unappghoul) + ")")
        elif ghoulcount > 0:
            censusout.append('Ghouls,' + str(ghoulcount))
        elif unappghoul > 0:
            censusout.append('Ghouls,' + "(" + str(unappghoul) + ")")
        if wolfcount > 0 and unappwolf > 0:
            censusout.append("Werewolves,"+str(wolfcount)  + " ( " + str(unappwolf) + ")")
        elif wolfcount > 0:
            censusout.append('Werewolves,'+str(wolfcount))
        elif unappwolf > 0:
            censusout.append('Werewolves,' + "(" + str(unappwolf) + ")")
        if bloodcount > 0 and unappblood > 0:
            censusout.append('Wolfblooded,' + str(bloodcount) + " (" + str(unappblood) + ")")
        elif bloodcount > 0:
            censusout.append('Wolfblooded,' + str(bloodcount))
        elif unappblood > 0:
            censusout.append('Wolfblooded,' + "(" + str(unappblood) + ")")
        if magecount > 0:
            censusout.append("Mages,"+str(magecount))
        if lingcount > 0:
            censusout.append("Changelings,"+str(lingcount))
        if beastcount > 0:
            censusout.append("Beasts,"+str(beastcount))
        if mummycount > 0:
            censusout.append("Mummies,"+str(mummycount))
        if demoncount > 0:
            censusout.append("Demons,"+str(demoncount))
        if prommiecount > 0:
            censusout.append("Prometheans,"+str(prommiecount))
        if huntercount > 0:
            censusout.append("Hunters,"+str(huntercount))
        if malecount > 0 and unappmale > 0:
            demographics.append('Male,'+str(malecount) + " (" + str(unappmale) +")")
        elif malecount > 0:
            demographics.append('Male,'+str(malecount))
        elif unappmale > 0:
            demographics.append('Male,' + "(" + str(unappmale) + ")")
        if femalecount > 0 and unappfemale > 0:
            demographics.append('Female,'+str(femalecount) + " (" + str(unappfemale) +")")
        elif unappfemale > 0:
            demographics.append('Female,' + "(" + str(unappfemale) + ")")
        elif femalecount > 0:
            demographics.append('Female,' + str(femalecount))
        if neutcount > 0 and unappneut > 0:
            demographics.append('Neutral,'+str(neutcount) + " (" + str(unappneut) + ")")
        elif unappneut > 0:
            demographics.append('Neutral,' + "(" + str(unappneut) + ")")
        elif neutcount > 0:
            demographics.append('Neutral,' + str(neutcount))
        censusbox = StatBlock("Templates",False,censusout)
        demobox = StatBlock('Demographics',demographics)
        self.caller.msg(censusbox.Show()+demobox.Show() + demobox.Footer())
class GenPage(Command):
    key = "+step"
    lock = 'cmd:all()'
    def func(self):
        caller = self.caller
        args = self.args
        self.args = self.args.strip()
        try:
            pass
        except ValueError:
            pass
        
class PowerList(Command):
    """
    This command allows you to see a list of powers available to your template. Mortals of course, have no powers.
    Powers are defined as non-merit abilities, such as gifts, disciplines, arcana, and so on that supernatural
    creatures possess. Without input, it will show a certain type of powers that is the most simple.
    For vampires this is disciplines, for werewolves this is gifts, for mages this is arcana, and so on. With
    input, it will show that kind of power such as vampire devotions, mage rotes, and the like.
    
    Syntax
    +powers
    """
    #This method returns a list of powers available to the individual character's template. Vampires will see all disciplines, werewolves all gifts and facets, and so on.
    #Support has yet to be added for secondary powers such as rotes, rites, devotions, and so on.
    key = "+powers"
    lock = "cmd:all()"
    help_category = "Gameplay"
    def parse(self):
        self.args = self.args.strip()
        #Just removing whitespace from the arguments, really arguments are only used for mages anyway and in single numbers or words so it's not a big deal.
    def func(self):
        caller = self.caller
        outputstring = ""
        #This string is going to be used as the final message. Everything on the list is added onto this string, so it's just defined as empty for now.
        args = self.args
        if caller.db.template == "Mortal":
            self.caller.msg("Mortals don't have powers. For psychic abilities and M+ templates, please use +stat.")
            return
        if caller.db.template == "Vampire":
        #Checks to see if the character is a vampire or not.
            if not args:
                disclist = []
                for x in caller.location.db.disciplines.db.disciplines:
                    disclist.append(x[0])
                discblock = StatBlock("Disciplines",False,disclist)
                discblock.SetWidth(78)
                outputstring += discblock.Show()
                outputstring += discblock.Footer()
            elif args.lower() == "devotions":
                devlist = []
                devstring = ""
                devotions = caller.location.db.disciplines.db.devotions
                for x in devotions:
                    for y in x:
                        if y == x[1]:
                            continue
                        elif y == x[0]:
                            devstring += y + ",("
                        else:
                            if "/" in y.split(",")[0]:
                                devstring += y.split(",")[0].split("/")[0] + " or " + y.split(",")[0].split("/")[1] + " "+ y.split(",")[1]
                                if y == x[len(x) - 1]:
                                    devstring += ")"
                                else:
                                    devstring += " "
                            else:
                                if y == x[len(x) - 1]:
                                    devstring += y.split(",")[0] + " " + y.split(",")[1] + ")"
                                else:
                                    devstring += y.split(",")[0] + " " + y.split(",")[1] + " "
                    devlist.append(devstring)
                    devstring = ""
                devblock = StatBlock("Devotions",False,devlist)
                devblock.SetWidth(78)
                devblock.SetColumns(1)
                devblock.SetColor("300")
                outputstring += devblock.Show()
                outputstring += devblock.Footer()
        if self.caller.db.template == "Werewolf":
            giftlist = []
            giftcounter = 0
            facetcounter = 0
            subcounter = 0
            rowcounter = 0
            giftdata = self.caller.location.db.gifts.db.gifts
            while giftcounter < (len(giftdata)):
                giftlist.append(giftdata[giftcounter][facetcounter])
                giftcounter += 1
                if (giftcounter)%3 == 0 and facetcounter != 5 and rowcounter != 5:
                    while facetcounter < 5:
                        oldsub = subcounter
                        while subcounter < giftcounter:
                            giftlist.append(giftdata[subcounter][facetcounter+4])
                            subcounter += 1
                        subcounter = oldsub
                        facetcounter += 1
                    facetcounter = 0
                    subcounter = giftcounter
            giftbox = StatBlock("Gifts",False,giftlist)
            giftbox.SetWidth(78)
            giftbox.SetHeaderInterval(6)
            giftbox.SetColor("320")
            outputstring += giftbox.Show()
            outputstring += giftbox.Footer()
        if caller.db.template == "Mage":
        #This section is devoted to displaying mage arcana and rotes. Rotes are organized like gift facets are, but there's a LOT more of them. Such as it is, they're split up
        #into different pages accessible by the command, '+powers <arcanum>' or '+powers <rank>'. If nothing is provided, it will give a massive three-column list of every rote.
            outputstring += "|235/" + "-" * 35 + "|nRotes|235" + "-" * 36 + "\\|n\n"
            #Just the header.
            rotes = self.caller.location.db.arcana.db.rotes
            #Sets an alias to the mage power handler's list of rotes.
            args = self.args
            if not args:
                oldrote = ""
                for rote in rotes:
                    if oldrote != "":
                        if oldrote[0] != rote[0]:
                            leftpad = 38 - int(float(len(rote[0]))/2)
                            if (len(rote[0]) % 2) == 0:
                                rightpad = leftpad
                            else:
                                rightpad = leftpad - 1
                            outputstring += "|235+|n" + "|235-|n" * leftpad + rote[0] + "|235-|n" * rightpad + "|235+|n\n"
                        if int(oldrote[2]) != int(rote[2]):
                            leftpad = 38 - (len("Rank 1 rotes")/2)
                            rightpad = leftpad
                            outputstring += "|235+|n" + "|235-|n" * leftpad + "Rank " + rote[2] + " rotes" + "|235-|n" * rightpad + "|235+|n\n"
                    else:
                        leftpad = 38 - int(float(len("Death"))/2)
                        if (len("Death") % 2) == 0:
                            rightpad = leftpad
                        else:
                            rightpad = leftpad - 1
                        outputstring += "|235+|n" + "|235-|n" * leftpad + "Death" + "|235-|n" * rightpad + "|235+|n\n"
                    outputstring += "|235|||n" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")"
                    endpad = 77 - len("|" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")")
                    outputstring += " " * (endpad) + "|235|||n\n"
                    oldrote = rote
            else:
                for x,y,z in izip(self.caller.db.physskills.keys(),self.caller.db.mentskills.keys(),self.caller.db.socskills.keys()):
                    oldrote = ""
                    if args.lower().replace("_"," ") == x.lower() or args.lower().replace("_"," ") == y.lower() or args.lower().replace("_"," ") == z.lower() or args.lower == "animalken":
                        for rote in rotes:
                            if not (args.lower() in rote[3].lower().split(",")):
                                continue
                            if oldrote != "":
                                if oldrote[0] != rote[0]:
                                    leftpad = 38 - int(float(len(rote[0]))/2)
                                    if (len(rote[0]) % 2) == 0:
                                        rightpad = leftpad
                                    else:
                                        rightpad = leftpad - 1
                                    outputstring += "|235+|n" + "|235-|n" * leftpad + rote[0] + "|235-|n" * rightpad + "|235+|n\n"
                                if int(oldrote[2]) != int(rote[2]) or (oldrote[0] != rote[0]):
                                    leftpad = 38 - (len("Rank 1 rotes")/2)
                                    rightpad = leftpad
                                    outputstring += "|235+|n" + "|235-|n" * leftpad + "Rank " + rote[2] + " rotes" + "|235-|n" * rightpad + "|235+|n\n"
                            else:
                                leftpad = 38 - int(float(len("Death"))/2)
                                if (len("Death") % 2) == 0:
                                    rightpad = leftpad
                                else:
                                    rightpad = leftpad - 1
                                outputstring += "|235+|n" + "|235-|n" * leftpad + "Death" + "|235-|n" * rightpad + "|235+|n\n"
                                outputstring += "|235+|n" + "|235-|n" * 32 + "Rank " +rote[2] + " rotes" + "|235-|n" * 32 + "|235+|n\n"
                            outputstring += "|235|||n" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")"
                            endpad = 77 - len("|" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")")
                            outputstring += " " * (endpad) + "|235|||n\n"
                            oldrote = rote
                if self.IsInt(args):
                    oldrote = ""
                    for rote in rotes:
                        if not (args.lower() in rote[2]):
                            continue
                        if oldrote != "":
                            if oldrote[0] != rote[0]:
                                leftpad = 38 - int(float(len(rote[0]))/2)
                                if (len(rote[0]) % 2) == 0:
                                    rightpad = leftpad
                                else:
                                    rightpad = leftpad - 1
                                outputstring += "|235+|n" + "|235-|n" * leftpad + rote[0] + "|235-|n" * rightpad + "|235+|n\n"
                            if int(oldrote[2]) != int(rote[2]):
                                leftpad = 38 - (len("Rank 1 rotes")/2)
                                rightpad = leftpad
                                outputstring += "|235+|n" + "|235-|n" * leftpad + "Rank " + rote[2] + " rotes" + "|235-|n" * rightpad + "|235+|n\n"
                        else:
                            leftpad = 38 - int(float(len("Death"))/2)
                            if (len("Death") % 2) == 0:
                                rightpad = leftpad
                            else:
                                rightpad = leftpad - 1
                            outputstring += "|235+|n" + "|235-|n" * leftpad + "Death" + "|235-|n" * rightpad + "|235+|n\n"
                        outputstring += "|235|||n" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")"
                        endpad = 77 - len("|" + rote[1] + " (" + rote[3].split(",")[0] + " " + rote[3].split(",")[1] + " " + rote[3].split(",")[2] + ")")
                        outputstring += " " * (endpad) + "|235|||n\n"
                        oldrote = rote
            outputstring += "|235\\" + "-" * 76 + "/|n"
            #Mage footer here.
        elif self.caller.db.template == "Changeling":
            colorcode = "020"
            outputstring += "|" + colorcode + "/" + "-" * 33 + "|nContracts|" + colorcode +"-" * 34 + "\\\n"
            for contract in self.caller.location.db.contracts.db.contracts:
                if contract == self.caller.location.db.contracts.db.contracts[0]:
                    oldrank = 1
                    outputstring += "+" + "-" * 30 + "|nRank 1 Contracts|" + colorcode + "-" * 30 + "+\n"
                elif int(contract[1][0]) > oldrank:
                    oldrank = int(contract[1][0])
                    outputstring += "+" + "-" * 30 + "|nRank " + contract[1][0]+ " Contracts|" + colorcode + "-" * 30 + "+\n"
                outputstring += "|||n " + contract[0] + " ("+contract[2].replace(",",", ") + ")" + " " * (76 - len("| "+contract[0] + "("+contract[2].replace(",",", ") + ")")) + "|" + colorcode +"||\n"
            outputstring += "\\" + "-" * 76 + "/"
        elif self.caller.db.template == "Hunter":
            colorcode = "121"
            outputstring += "|" + colorcode + "/" + "-" * 33 + "|nEndowments|" + colorcode + "-" * 33 + "\\\n"
            outputstring += "+" + "-" * 30 + "|nAdvanced Armory|" + colorcode + "-" * 31 + "+\n"
            for gear in self.caller.location.db.endowments.db.advarmory:
                if len(gear[1]) > 1:
                    outputstring += "|||n " + gear[0] + " " + "("+ gear[1].replace(",",", ") + ")" + " " * (76 - len("|" + gear[0] + " " + "("+ gear[1].replace(",",", ") + ")")) + "|" + colorcode + "||\n"
                else:
                    outputstring += "|||n " + gear[0] + " " + gear[1] + " " * (76 - len("|" + gear[0] + " " + gear[1])) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 32 + "|nBenedictions|" + colorcode + "-" * 32 + "+\n"
            for bless in self.caller.location.db.endowments.db.benediction:
                outputstring += "|||n " + bless[0] + " " * (76 - len(" "+bless[0])) +"|" + colorcode + "||\n"
            outputstring += "+" + "-" * 33 + "|nCastigation|"  + colorcode + "-" * 32 + "+\n"
            for burn in self.caller.location.db.endowments.db.castigation:
                outputstring += "|||n " + burn[0] + " " * (76 - len(" "+burn[0])) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 35 +"|nElixir|" + colorcode + "-" * 35 + "||\n"
            for potion in self.caller.location.db.endowments.db.elixir:
                outputstring += "|||n " + potion[0] + " (" + potion[1].replace(",",", ")+ ")" + " " * (76 - len(" " + potion[0] + " (" + potion[1].replace(",",", ")+ ")")) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 37 + "|nInk|" + colorcode + "-" * 36 + "+\n"
            for dot in self.caller.location.db.endowments.db.ink:
                outputstring += "|||n " + dot[0] + " " * (76 - len(" " + dot[0])) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 35 + "|nRelics|" + colorcode + "-" * 35 + "+\n" 
            for old in self.caller.location.db.endowments.db.relic:
                outputstring += "|||n " + old[0] + " (" + old[1].replace(",",", ") + ")" + " " * (76 - len(" " + old[0] + " (" + old[1].replace(",",", ") + ")"))  + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 30 + "|nThaumatechnology|" + colorcode + "-" * 30 + "+\n"
            for bio in self.caller.location.db.endowments.db.thaumatechnology:
                outputstring += "|||n " + bio[0] + " (" + bio[1].replace(",",", ") + ")" + " " * (76 - len(" " + bio[0] + " (" + bio[1].replace(",",", ") + ")")) + "|" + colorcode + "||\n"
            outputstring += "\\" + "-" * 76  + "/"
        elif self.caller.db.template == "Beast":
            colorcode = "212"
            outputstring += "|" + colorcode + "/" + "-" * 34 + "|nAtavisms|" + colorcode + "-" * 34 + "\\\n"
            for atavism in self.caller.location.db.atavisms.db.atavisms:
                outputstring += "|||n " + atavism[0] + " (" + atavism[1] + ")" + " " * (76 - len(" " + atavism[0] + " (" + atavism[1] + ")")) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 33 + "|nNightmares|" + colorcode + "-" * 33 + "+\n"
            for scare in self.caller.location.db.atavisms.db.nightmares:
                outputstring += "|||n " + scare[0] + " ("
                if "," in scare[1]:
                    outputstring += scare[1].split(",")[1] + " " + scare[1].split(",")[0] + ")" + " " * (76 - len(" " + scare[0] + " (" + scare[1].split(",")[1] + " " + scare[1].split(",")[0] + ")")) + "|" + colorcode + "||\n"
                else:
                    outputstring += scare[1] + ")" + " " * (76 - len(" " + scare[0] + " (" + scare[1] + ")")) + "|" + colorcode + "||\n"
            outputstring += "\\" + "-" * 76 + "/"
        elif self.caller.db.template == "Mummy":
            colorcode = "330"
            outputstring += "|" + colorcode + "/" + "-" * 33 + "|nAffinities|" + colorcode + "-" * 33 + "\\\n"
            outputstring += "+" + "-" * 35 + "|nGuild|" + colorcode + "-" * 36 + "+\n"
            guildaff = False
            for aff in self.caller.location.db.affinities.db.affinities:
                if len(aff) == 3 and not guildaff:
                    guildaff = True
                    outputstring += "+" + '-' * 35 + "|nPillar|" + colorcode + "-" * 35 + "+\n"
                if not guildaff or len(aff) == 2:
                    outputstring += "|||n " + aff[0] + " (" + aff[1] + ")" + " " * (76 - len(" " + aff[0] + " (" + aff[1] + ")")) + "|" + colorcode + "||\n"
                else:
                    outputstring += "|||n " + aff[0] + " (" + aff[1] + " " + aff[2] + ")" + " " * (76 - len(" " + aff[0] + " (" + aff[1] + " " + aff[2] + ")")) + "|" + colorcode + "||\n"
            outputstring += "+" + "-" * 33 + "|nUtterances|" + colorcode + "-" * 33 + "+\n"
            for utt in self.caller.location.db.affinities.db.utterances:
                outputstring += "|||n " + utt[0] + " (" + utt[1].split(",")[0] + " " + utt[2].split(",")[0] + ", " + utt[1].split(",")[1] + " " + utt[2].split(",")[1] + ", " + utt[1].split(",")[2] + " " + utt[2].split(",")[2]+ ")" + " " * (76 - len(" " + utt[0] + " (" + utt[1].split(",")[0] + " " + utt[2].split(",")[0] + ", " + utt[1].split(",")[1] + " " + utt[2].split(",")[1] + ", " + utt[2].split(",")[2] + " " + utt[1].split(",")[2] + ")")) + "|" + colorcode + "||\n"
            outputstring += "\\" + "-" * 76 + "/"
        elif self.caller.db.template == "Promethean":
            color = "313"
            outputstring += "|" + color + "/" + "-" * 31 + "|nTransmutations|" + color + "-" * 31 + "\\\n"
            for change in self.caller.location.db.transmutations.db.transmutations:
                outputstring += "|||n " + change[0] + " (" + change[1] + ")" + " " * (76 - len(change[0] + " (" + change[1] + ")" + " ")) + "|" + color + "||\n"
            outputstring += "+" + "-" * 31 + "|nDistillations|" + color + "-" * 32 + "+\n"
            for change2 in self.caller.location.db.transmutations.db.transmutations:
                if change2[0] == "Saturninus":
                    outputstring += "|||n"
                    distillrow = change2[2] + ", " + change2[3] + ", " + change2[4] + ", " + change2[5]
                    distillrow += " " * (76 - len(distillrow)) +"|" + color + "||\n"
                    distillrow += "|" + color + "|||n" + "(Saturninus)"
                    distillrow += " " * (76 - len("|(Saturninus)")+1)
                    outputstring += distillrow + "|" + color + "||\n"
                else:
                    outputstring += "|||n"
                    distillrow = change2[2] + ", " + change2[3] + ", " + change2[4] + ", " + change2[5] + " (" + change2[0] + ")"
                    distillrow += " " * (76 - len(distillrow))
                    outputstring += distillrow + "|" + color + "||\n"
            outputstring += "\\" + "-" * 76 + "/"
        elif self.caller.db.template == "Demon":
            color = "223"
            if not args:
                outputstring += "|" + color + "/" + "-" * 35 + "|nEmbeds|" + color + "-" * 35 +"\\\n"
                oldembed = ""
                for embed in self.caller.location.db.embeds.db.embeds:
                    if embed[0] != oldembed:
                        leftmargin = 37 - len(embed[0])/2
                        if len(embed[0]) % 2 == 0:
                            rightmargin = leftmargin + 2
                        else:
                            rightmargin = leftmargin + 1
                        outputstring += "+" + "-" * leftmargin + "|n" + embed[0] + "|" + color + "-" * rightmargin + "+\n"
                    outputstring += "|||n " + embed[2] + " " * (76 - len(embed[2] + " ")) + "|" + color + "||\n"
                    oldembed = embed[0]
                outputstring += "+" + "-" * 34 + "|nExploits|" + color + "-" * 34 + "+\n"
                for exploit in self.caller.location.db.embeds.db.exploits:
                    outputstring += "|||n " + exploit[0] + " (" + exploit[2] + ")" + " " * (76 - len("| " + exploit[0] + " (" + exploit[2] + ")")+1) + "|" + color + "||\n"
                outputstring += "+" + "-" * 28 + "|nDemonic Form Traits|" + color + "-" * 29 + "+\n"
                outputstring += "+" + "-" * 31 + "|nModifications|" + color + "-" * 32 + "+\n"
                for mod in self.caller.location.db.embeds.db.modifications:
                    outputstring += "|||n " + mod[0] + " " * (76 - len(" " + mod[0])) + "|" + color + "||\n"
                outputstring += "+" + "-" * 32 + "|nTechnologies|" + color + "-" * 32 + "+\n"
                for tech in self.caller.location.db.embeds.db.technologies:
                    outputstring += "|||n " + tech[0] + " " * (76 - len(" " + tech[0])) + "|" + color + "||\n"
                outputstring += "+" + "-" * 32 + "|nPropulsions|" + color + "-" * 33 + "+\n"
                for prop in self.caller.location.db.embeds.db.propulsion:
                    outputstring += "|||n " + prop[0] + " " * (76 - len(" " + prop[0])) + "|" + color + "||\n" 
                outputstring += "+" + "-" * 33 + "|nProcesses|" + color + "-" * 34 + "+\n"
                for proc in self.caller.location.db.embeds.db.processes:
                    outputstring += "|||n " + proc[0] + " " * (76 - len(" " + proc[0])) + "|" + color + "||\n"
            if args.lower() == "embeds":
                outputstring += "|" + color + "/" + "-" * 35 + "|nEmbeds|" + color + "-" * 35 +"\\\n"
                oldembed = ""
                for embed in self.caller.location.db.embeds.db.embeds:
                    if embed[0] != oldembed:
                        leftmargin = 37 - len(embed[0])/2
                        if len(embed[0]) % 2 == 0:
                            rightmargin = leftmargin + 2
                        else:
                            rightmargin = leftmargin + 1
                        outputstring += "+" + "-" * leftmargin + "|n" + embed[0] + "|" + color + "-" * rightmargin + "+\n"
                    outputstring += "|||n " + embed[2] + " " * (76 - len(embed[2] + " ")) + "|" + color + "||\n"
                    oldembed = embed[0]
            elif args.lower() == "exploits":
                outputstring += "|" + color + "/" + "-" * 34 + "|nExploits|" + color + "-" * 34 + "\\\n"
                for exploit in self.caller.location.db.embeds.db.exploits:
                    outputstring += "|||n " + exploit[0] + " (" + exploit[2] + ")" + " " * (76 - len("| " + exploit[0] + " (" + exploit[2] + ")")+1) + "|" + color + "||\n"
            elif args.lower() == "traits":
                outputstring += "|" + color + "/" + "-" * 28 + "|nDemonic Form Traits|" + color + "-" * 29 + "\\\n"
                outputstring += "+" + "-" * 31 + "|nModifications|" + color + "-" * 32 + "+\n"
                for mod in self.caller.location.db.embeds.db.modifications:
                    outputstring += "|||n " + mod[0] + " " * (76 - len(" " + mod[0])) + "|" + color + "||\n"
                outputstring += "+" + "-" * 32 + "|nTechnologies|" + color + "-" * 32 + "+\n"
                for tech in self.caller.location.db.embeds.db.technologies:
                    outputstring += "|||n " + tech[0] + " " * (76 - len(" " + tech[0])) + "|" + color + "||\n"
                outputstring += "+" + "-" * 32 + "|nPropulsions|" + color + "-" * 33 + "+\n"
                for prop in self.caller.location.db.embeds.db.propulsion:
                    outputstring += "|||n " + prop[0] + " " * (76 - len(" " + prop[0])) + "|" + color + "||\n" 
                outputstring += "+" + "-" * 33 + "|nProcesses|" + color + "-" * 34 + "+\n"
                for proc in self.caller.location.db.embeds.db.processes:
                    outputstring += "|||n " + proc[0] + " " * (76 - len(" " + proc[0])) + "|" + color + "||\n"
            elif args.lower() == "modifications":
                outputstring += "|" + color + "/" + "-" * 31 + "|nModifications|" + color + "-" * 32 + "\\\n"
                for mod in self.caller.location.db.embeds.db.modifications:
                    outputstring += "|||n " + mod[0] + " " * (76 - len(" " + mod[0])) + "|" + color + "||\n"
            elif args.lower() == "technologies":
                outputstring += "|" + color + "/" + "-" * 32 + "|nTechnologies|" + color + "-" * 32 + "\\\n"
                for tech in self.caller.location.db.embeds.db.technologies:
                    outputstring += "|||n " + tech[0] + " " * (76 - len(" " + tech[0])) + "|" + color + "||\n"
            elif args.lower() == "propulsion" or args.lower() == "propulsions":
                outputstring += "|" + color + "/" + "-" * 32 + "|nPropulsions|" + color + "-" * 33 + "\\\n"
                for prop in self.caller.location.db.embeds.db.propulsion:
                    outputstring += "|||n " + prop[0] + " " * (76 - len(" " + prop[0])) + "|" + color + "||\n" 
            elif args.lower() == "processes":
                outputstring += "|" + color + "/" + "-" * 33 + "|nProcesses|" + color + "-" * 34 + "\\\n"
                for proc in self.caller.location.db.embeds.db.processes:
                    outputstring += "|||n " + proc[0] + " " * (76 - len(" " + proc[0])) + "|" + color + "||\n"
            outputstring += "\\" + "-" * 76 + "/"
        self.caller.msg(outputstring)
        #Send the actual power list to the player.
    def AddRote(self, x, *skillin):
    #Made this method, 'cause screw adding the same code over and over. If it's re-used, it should be a method. Sadly while a good axiom, one I do not always
    #follow myself. The x argument is the rote this method is actually processing in list form. The skillin optional method is passed when searching for rotes
    #by skill, and removes it from the list of skills displayed on the basis that such information is redundant. It wouldn't be on the list if it didn't have
    #that skill, after all.
        roteskills = x[2].split(",")
        #Splits the skills into their own list.
        roteskills.sort()
        #Sorts the skills alphabetically.
        rotestring = ""
        #The rotestring is the string to be rerturned.
        try:
            skillin = skillin[0]
        except IndexError:
            skillin = "None"
        #Basically, this sets the skillin variable to, "None" if there wasn't a skillin argument passed.
        if "AnimalKen" in roteskills:
            roteskills[roteskills.index("AnimalKen")] = "Animal Ken"
        #Just prettying up any instances where the animal ken skill is used.
        for y in roteskills:
            if y == skillin:
                roteskills.remove(y)
        if y != "None":
            rotestring += "|| " + x[0] + " (" + roteskills[0] + ", " + roteskills[1] + ")"
        else:
            rotestring += "|| " + x[0] + " (" + roteskills[0] + ", " + roteskills[1] + ", " + roteskills[2] + ")"
        rotestring += " " * (78 - len(rotestring)) + "||\n"
        #A minor quirk, and the reason why I'm making two instances of adding to rotestring instead of one. If you were to add the final rote entry and
        #then add the padding immediately after, it would only count the first two rote entries. It executes the entire string, concatenates it all, THEN
        #adds it to the rotestring variable. Hence, I have to wait until it's added the final entry for it to be able to catch what I want.
        return rotestring
    def IsInt(self, x):
        try:
            int(x)
            return True
        except ValueError:
            return False
        #A pretty simple checker for if something is an integer or not.
class SpendPool(default_cmds.MuxCommand):
    """
    This command is used to spend and add to a pool freely. It can be a willpower pool,
    or it can be a pool used by a given supernatural type. Please note that not all
    supernatural creatures can regain their expendable pool at will, on an out of character
    basis. Even in-character, regaining one's expendable pool is a matter of some effort
    at the least.
    
    What the command is depends on your template. For vampires and ghouls it's +vitae,
    for werewolves it's +essence, for mages and proximi it's +mana, and so on.
    
    Syntax:
    +<pool>/spend <Amount> (Spend a given amount of a pool)
    +<pool>/gain <Amount> (Gain a given amount of a pool, if your template allows free recovery)
    +willpower/virtue <Reason> (Recover all your willpower, due to your virtue being acted upon)
    +willpower/vice <Reason> (Recover one point of willpower, due to your vice being acted upon)
    """
    #This command is used for EVERY pool, whether it's willpower or a supernatural pool.
    key = "+willpower"
    aliases = ["+vitae","+essence","+mana","+glamour","+pyros","+satiety","+aether","+ab","+ba","+ka","+ren","+sheut","+ephemera","+memory"]
    help_category = "Gameplay"
    def func(self):
        modaction = ""
        #This stores the string used in the final output, saying whether the character is spending or gaining an expendable resource.
        cmdstring = self.cmdstring
        #Just a small alias for the original command string. This doesn't include switches, or arguments, or the slash delimiter for arguments.
        arglist = self.arglist
        #Alias for the arguments.
        switches = self.switches
        #Alias for the switches.
        if len(switches) == 0:
            self.caller.msg("Please select whether you are gaining or spending.")
            return
        if cmdstring == "+willpower":
        #This branch goes off if you're spending or gaining willpower.
            if switches[0].lower() == "spend":
            #Here's the thing. It looks at the first element, because you should never try to spend and gain at the same time. That's just a recipe for errors.
                if self.caller.db.pools['Willpower'].split(",")[1] == 0:
                #Technically the spending method own't let you spend if you have nothing in that pool, but it's good to be doubly sure.
                    self.caller.msg("You have no willpower remaining.")
                    #Giving the user feedback helps them know what's going on.
                    return
                modaction = " spends "
                #Sets the modaction variable as noted before.
                if self.isint(arglist[0]):
                #Checks to make sure someone is spending numerically, not in words. Also just to be sure nothing was input that would crash the command.
                    if int(arglist[0]) >= 1:
                        self.caller.spend('Willpower',arglist[0])
                        #Call the method for spending, with the argument in question.
                    else:
                        self.caller.msg("Please enter a value greater than zero.")
                        #Pretty self-explanatory, but a little bit of a thing here. This NEEDS to be in the code, as gaining or spending a positive
                        #value ignores your minimum of 0, and maximum limit. If so desired, this may be fixed in the pool handler.
                        return
            if switches[0].lower() == "virtue":
                if self.caller.db.demeanorname == "Virtue":
                    self.caller.PoolGain('Willpower',int(self.caller.db.pools['Willpower'].split(",")[1]))
                    self.caller.db.willpowerlog.append("On "+time.strftime("%b")+" "+time.strftime("%d")+time.strftime("%Y")+"you exercised your virtue to restore your willpower. Reason: "+self.args)
            elif switches[0].lower() == "vice" and self.caller.db.naturename == "Vice":
                self.caller.PoolGain('Willpower',1)
                self.caller.db.willpowerlog.append("On "+time.strftime("%b")+" "+time.strftime("%d")+time.strftime("%Y")+"you exercised your vice to restore your willpower. Reason: "+self.args)
        if cmdstring in self.aliases:
        #This branch is called if the person is spending something other than willpower.
            if self.caller.db.template != "Mortal" and self.caller.db.template != "Hunter" and self.caller.db.template != "Beast":
            #Just a small thing to make sure people aren't trying to modify resources they don't have.
                if self.caller.db.pools[0].split(",")[0] == 0 and switches[0] == "spend":
                #Checking if someone is trying to spend on empty.
                    self.caller.msg("You have nothing to spend!")
                    return
                if self.caller.db.pools[0].split(",")[0] == self.caller.db.pools[0].split(",")[1] and switches[0] == "gain":
                #Checking if someone is trying to gain a resource that is currently full.
                    self.caller.msg("The resource you're trying to gain is full!")
                    return
            if cmdstring == "+vitae":
            #Checking to see if someone is trying to spend vitae.
                if self.caller.db.template == "Vampire" or self.caller.db.template == "Ghoul":
                #As is ever prudent, making sure that those attempting to spend vitae are in fact, vampires.
                    if switches[0].lower() == "spend":
                    #Checking to see that the individual is spending.
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.Spend('Vitae',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a value greater than zero.")
                                return
                        else:
                            self.caller.msg("Please enter a valid value to spend.")
                            return
                else:
                    self.caller.msg("As you are not a vampire or ghoul, you have no vitae to spend.")
                    return
            if cmdstring == "+essence":
            #Checking to see if someone is trying to spend essence
                if self.caller.db.template == "Werewolf":
                #Checks to see that the caller is the proper splat.
                    if switches[0].lower() == "spend":
                    #Checking to see if the werewolf is spending essence.
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.Spend('Essence',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a value greater than zero.")
                                return
                        else:
                            self.caller.msg("Please enter a valid value to spend.")
                            return
                    else:
                        self.caller.msg("That's not a valid switch. Only spending is supported.")
                        return
                else:
                    self.caller.msg("Only werewolves have essence to spend.")
                    return
            if cmdstring == "+mana":
                if self.caller.db.template == "Mage" or self.caller.db.template == "Proximus":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.spend('Mana',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a value greater than zero.")
                                return
                        else:
                            self.caller.msg("Please enter a valid value to spend.")
                            return
                    else:
                        self.caller.msg("That switch is not supported.")
                        return
                else:
                    self.caller.msg("Only mages and proximi have mana to spend!")
                    return
            if cmdstring == "+glamour":
                if self.caller.db.template == "Changeling" or self.caller.db.template == "Fae-Touched":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >=1:
                                self.caller.Spend('Glamour',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Plaase enter a valid value to spend.")
                            return
                else:
                    self.caller.msg("Only changelings and fae-touched have glamour to spend!")
                    return
            if cmdstring == "+pyros":
                if self.caller.db.template == "Promethean":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.Spend('Pyros',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Invalid spending value.")
                            return
                    elif switches[0].lower() == "gain":
                        modaction = " gains "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolGain('Pyros',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value.")
                                return
                        else:
                            self.caller.msg("Invalid value.")
                            return
                    else:
                        self.caller.msg("Invalid switch.")
                        return
                else:
                    self.caller.msg("Only prometheans have pyros to spend!")
                    return
            if cmdstring == "+satiety":
                if self.caller.db.template == "Beast":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                if int(arglist[0]) > self.caller.db.sanity:
                                    self.caller.msg("You can't spend that much satiety!")
                                    return
                                else:
                                    self.caller.db.sanity -= int(arglist[0])
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Invalid value.")
                            return
                    else:
                        self.caller.msg("Invalid switch.")
                        return
                else:
                    self.caller.msg("Only Beasts have satietiy to expend!")
                    return
            if cmdstring == "+aether":
                if self.caller.db.template == "Demon":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolSpend('Aether',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Invalid value, numbers only please.")
                            return
                    elif switches[0].lower() == "gain":
                        modaction = " gains "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolGain('Aether',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to gain.")
                                return
                        else:
                            self.caller.msg("Please enter a number to spend, rather than something else.")
                            return
                    else:
                        self.caller.msg("Only spending and gaining are supported.")
                        return
                else:
                    self.caller.msg("Only demons have aether to spend!")
            if cmdstring == "+ab" or cmdstring == "+ba" or cmdstring == "+ka" or cmdstring == "+ren" or cmdstring == "+sheut":
                if self.caller.db.template == "Mummy":
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolSpend(cmdstring.replace("+","").title(),int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Please enter a valid value to spend.")
                            return
                    elif switches[0].lower() == "gain":
                        modaction = " gains "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolGain(cmdstring.replace("+","").title(),int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to gain.")
                                return
                        else:
                            self.caller.msg("Please enter a valid value to spend.")
                            return
                    else:
                        self.caller.msg("Invalid switch.")
                        return
                else:
                    self.caller.msg("Only mummies can spend from pillars!")
                    return
            if cmdstring == "+ephemera":
                for merit in self.caller.db.meritlist:
                    if merit[0].lower() == "psychic vampirism":
                        isvamp = True
                if isvamp:
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1:
                                self.caller.PoolSpend('Ephemera',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Please enter a number when spending.")
                            return
                    else:
                        self.caller.msg("Invalid switch.")
                        return
                else:
                    self.caller.msg("Only psychic vampires have ephemera to spend!")
                    return
            if cmdstring == "+memory":
                for merit in self.caller.db.meritlist:
                    if merit[0].lower() == "subliminal conditioning":
                        isdreamer = True
                if isdreamer:
                    if switches[0].lower() == "spend":
                        modaction = " spends "
                        if self.isint(arglist[0]):
                            if int(arglist[0]) >= 1 or int(self.lhs) >= 1:
                                if self.lhs != "":
                                    self.caller.PoolSpend('Memory',int(self.lhs))
                                else:
                                    self.caller.PoolSpend('Memory',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        elif self.isint(self.lhs):
                            if int(self.lhs) >= 1:
                                if self.lhs != "":
                                    self.caller.PoolSpend('Memory',int(self.lhs))
                                else:
                                    self.caller.PoolSpend('Memory',int(arglist[0]))
                            else:
                                self.caller.msg("Please enter a positive value to spend.")
                                return
                        else:
                            self.caller.msg("Please enter a number when spending.")
                            return
                    else:
                        self.caller.msg("Invalid switch.")
                        return
                else:
                    self.caller.msg("Only dreamers may use memory!")
                    return
        if cmdstring[1:len(cmdstring)] == "willpower":
            if switches[0].lower() == "virtue" and self.caller.db.demeanorname == "Virtue":
                stringout = self.caller.name + " gains " + str(int(self.caller.db.pools['Willpower'].split(",")[1]) - int(self.caller.db.pools['Willpower'.split(",")[0]])) +" willpower."
            elif switches[0].lower() == "vice" and self.caller.db.naturename == "Vice":
                stringout = self.caller.name + " gains " + str(1) +" willpower."
            else:
                stringout = self.caller.name + modaction +arglist[0] + " " + cmdstring[1:len(cmdstring)]
                #Of course, this is concatenating all the other strings that indicate what the person was doing.
        else:
            if self.lhs != "":
                stringout = self.caller.name + modaction + self.lhs + " " + cmdstring[1:len(cmdstring)]
        if len(switches) > 0:
            if switches[0].lower() == "virtue" or switches[0].lower() == "vice":
                pass
        elif self.rhs:
        #Check to see if the player provided a reason for the expenditure
            stringout += " for " + self.rhs
        for character in self.caller.location.contents:
        #Iterate through the location's contents.
            if character.player:
            #Check to see if the character has a player. That is to say, see if they are in fact a character whose player is not AFK.
                character.msg(stringout)
    def isint(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

class HealthManage(default_cmds.MuxCommand):
    """
    This command is used to heal and damage your character both, while two commands are used they are both the same piece
    of health management code.
    
    Syntax:
    +damage <Bashing/Lethal/Aggravated>=<Amount> (Take 'Amount' points of the damage type selected)
    +heal <Bashing/Lethal/Aggravated>=<Amount> (Heal 'Amount' points of the damage type selected)
    """
    #Used for damaging and healing the character controlled by the player who calls this command. Despite the key being +damage, +heal is an alias, so it does both.
    key = "+damage"
    lock = "cmd:all()"
    aliases = ["+heal"]
    help_category = "Gameplay"
    def func(self):
        lhs = self.lhs
        #The lhs variable in this case, stores the damage type that is being dealt or healed.
        rhs = self.rhs
        #The rhs variable stores the amount of damage that is in fact, being dealt or healed. Bear in mind, integers passed as arguments are /strings/, so they have to be
        #converted to integers to be used as such.
        cmdstring = self.cmdstring
        if cmdstring == "+damage":
        #Checks to see if the character is being damaged. A minor thing to note for health and related commands, the health track is a list of integers.
        #A 0 means the health box is undamaged, a 1 means it has bashing damage, a 2 means it has lethal damage, a 3 means it has aggravated damage.
            if lhs.lower() == "bashing":
                self.caller.Damage(1,int(rhs))
            elif lhs.lower() == "lethal":
                self.caller.Damage(2,int(rhs))
            elif lhs.lower() == "aggravated":
                self.caller.Damage(3,int(rhs))
            for person in self.caller.location.contents:
                if person.player:
                    person.msg(self.caller.name + " took " + str(rhs) + " " + lhs.lower() + " damage!")
        elif cmdstring == "+heal":
            if lhs.lower() == "bashing":
                self.caller.Heal(1,int(rhs))
            elif lhs.lower() == "lethal":
                self.caller.Heal(2,int(rhs))
            elif lhs.lower() == "aggravated":
                self.caller.Heal(3,int(rhs))
            for person in self.caller.location.contents:
                if person.player:
                    person.msg(self.caller.name + " healed for " +str(rhs+" " + lhs.lower() + " damage!"))
class BreakCommand(default_cmds.MuxCommand):
    """
    This command is used to automatically roll for breaking points, detachment, and other similar concepts where the character's
    integrity equivalent changes. It automatically gives a beat for facing a breaking point, but a reason must also be provided
    to prevent abuse for infinite beats, or in the case of Dreamers, infinite memory. Use of this command is announced to a
    wizards-only channel, and the reason for the breaking point is logged so that the character may be awarded beats later.
    
    Certain intrinsic modifiers such as the ventrue clan's weakness, as well as the level of integrity for mortals, and the
    level of harmony for werewolves are all automatically incorporated.
    
    Syntax:
    +break <Modifier>=<Reason> (Rolls a breaking point with modifiers based on the situation, for a given reason. Mortals, also works
    for Demons making a compromise check.)
    +break/<Condition> (Choose an appropriate condition for going through a breaking point or equivalent, regardless of template.)
    +break <Modifiers>=<Reason>/<Level> (Rolls for detachment with situational modifiers, for a given reason, at a given level of
    infringement. Vampires only.)
    +break <Modifiers>=<Reason>/<Flesh or Spirit> (Rolls a breaking point towards flesh or spirit, with certain modifiers. Werewolves
    only.)
    +break <Modifiers>=<Reason>/<Enlightened, Understanding, or Falling> (Rolls for hubris with a reason, at a given level of act
    of hubris. Mages only.)
    """
    key = "+break"
    lock = "cmd:all()"
    help_category = "Gameplay"
    def func(self):
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        template = self.caller.db.template
        caller = self.caller
        attributes = caller.db.attrstats
        sanity = caller.db.sanity
        dramafail = False
        dreamer = False
        if caller.db.approved == False:
            caller.msg("You can't roll breaking points unless you're approved.")
            return
        if len(switches) == 0:
            if "=" in self.args:
                try:
                    notices = search.channels('Breaking Points')[0]
                except IndexError:
                    notices = create_channel('Breaking Points',alias='break',desc='Breaking point notices',locks='control:perm(Immortals);listen:perm(Wizards);send:false()')
                if self.caller.db.sanityname == "Integrity":
                    if self.caller.db.currentbreak == "":
                        for merit in self.caller.db.meritlist:
                            if merit[0].lower() == "subliminal conditioning":
                                dreamer = True
                        breakpool = attributes['Resolve'] + attributes['Composure']
                        try:
                            breakpool += int(lhs)
                        except ValueError:
                            self.caller.msg("Invalid modiifer.")
                            return
                        breakcount = 0
                        successes = 0
                        if sanity >= 8:
                            breakpool += 2
                        elif sanity >= 6:
                            breakpool += 1
                        elif sanity >= 4:
                            pass
                        elif sanity >= 2:
                            breakpool -= 1
                        elif sanity == 1:
                            breakpool -= 2
                        dramafail = False
                        if breakpool > 0:
                            while breakcount < breakpool:
                                breakdie = random.randint(1,10)
                                if breakdie >= 8:
                                    successes += 1
                                    if breakdie == 10:
                                        breakcount -= 1
                                breakcount += 1
                        else:
                            alldice = False
                            while alldice == False:
                                breakdie = random.randint(1,10)
                                if breakdie == 10:
                                    successes += 1
                                elif breakdie == 1 and successes == 0:
                                    dramafail = True
                                    alldice = True
                                else:
                                    alldice = True
                                    
                        if 5 > successes > 0:
                            self.caller.msg("Breaking point passed, dot of integrity retained. Please use +break/guilty, +break/shaken, or +break/spooked to accept a condition.")
                            self.caller.db.currentbreak = "Success," + rhs
                            self.caller.AddBeat("Breaking Point",rhs)
                            notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " with a modifier of " + lhs + " and got a success.")
                            if dreamer:
                                self.caller.PoolGain('Memory',successes)
                            return
                        elif successes >= 5:
                            self.caller.msg("Breaking point passed with an exceptional success. No need to select a condition, two beats added to your log and a point of willpower gained.")
                            self.caller.db.beats.AddBeat("Breaking Point",rhs)
                            self.caller.db.beats.AddBeat("Breaking Point",rhs)
                            self.caller.PoolGain('Willpower',1)
                            self.caller.db.breaklog.append("Exceptional success. Reason: "+rhs+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                            notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+ lhs + " and got an exceptional success.")
                            if dreamer:
                                self.caller.PoolGain('Memory',successes)
                            return
                        elif successes == 0 and not dramafail:
                            self.caller.msg("Breaking point failed, please use +break/guilty, +break/shaken, or +break/spooked to accept a condition.")
                            self.caller.db.currentbreak = "Failure," + rhs
                            self.caller.AddBeat("Breaking Point",rhs)
                            notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " with a modifier of "+ lhs + "and got a failure.")
                        elif successes == 0 and dramafail:
                            self.caller.msg("Breaking point dramatically failed, please use +break/madness, +break/fugue, or +break/broken to accept a condition.")
                            self.caller.db.currentbreak = "Dramatic Failure," + rhs
                            self.caller.AddBeat("Breaking Point",rhs)
                            notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+lhs+" and got a dramatic failure.")
                            return
                    else:
                        self.caller.msg("You still need to accept a condition from your previous breaking point!")
                        return
                elif template == "Mage":
                    if self.caller.db.currentbreak == "":
                        if "/" in rhs:
                            if rhs.split("/")[1].lower() == "enlightened" or rhs.split("/")[1] == "5":
                                dicepool = 5
                            elif rhs.split("/")[1].lower() == "understanding" or rhs.split("/")[1] == "3":
                                dicepool = 3
                            elif rhs.split("/")[1].lower() == "falling" or rhs.split("/")[1] == "1":
                                dicepool = 1
                            try:
                                dicepool += int(lhs)
                            except ValueError:
                                self.caller.msg("That's not a avalid modifier for a breaking point.")
                                return
                            counter = 0
                            success = 0
                            if dicepool > 0:
                                while counter < dicepool:
                                    die = random.randint(1,10)
                                    if die >= 8:
                                        success += 1
                                        if die == 10:
                                            counter -= 1
                                    counter += 1
                            else:
                                alldice = False
                                while not alldice:
                                    die = random.randint(1,10)
                                    if die == 10:
                                        success += 1
                                    if die == 1 and success == 0:
                                        alldice = True
                                        dramafail = True
                                    else:
                                        alldice = True
                            if 5 > success > 0:
                                self.caller.msg("Breaking point succeeded, dot of wisdom retained and beat added.")
                                self.caller.AddBeat('Breaking Point',rhs)
                                notices.msg(self.caller.name + " just rolled for an act of hubris with a modifier of " + lhs + " and succeeded.")
                                return
                            elif successes >= 5:
                                self.caller.msg("Breaking point passed with an exceptional success, extra beat and point of temporary willpower added.")
                                self.caller.AddBeat('Breaking Point',rhs)
                                self.caller.AddBeat('Breaking Point',rhs)
                                notices.msg(self.caller.name + " just rolled for an act of hubris with a modifier of " + lhs + " and got an exceptional success.")
                                self.caller.PoolGain('Willpower',1)
                                self.caller.db.breaklog.append("Exceptional success. Reason: "+rhs+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                return
                            elif successes == 0 and not dramafail:
                                self.caller.msg("Breaking point failed, dot of wisdom removed. Please use +break/rampant or +break/megalomaniacal to select a condition as a result.")
                                self.caller.AddBeat('Breaking Point',rhs)
                                notices.msg(self.caller.name + " just rolled for an act of hubris with a modifier of " + lhs + " and got a failure.")
                                self.caller.db.currentbreak = "Failure," + rhs
                                self.caller.db.breaklog.append("Failure. Reason: "+rhs+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                return
                            elif successes == 0 and dramafail:
                                self.caller.msg("Breaking point dramatically failed, dot of wisdom removed. Please use +break/rampant or +break/megalomaniacal to select a condition as a result. You are not to resolve these conditions until your character gains another dot of wisdom.")
                                self.caller.AddBeat('Breaking Point',rhs)
                                self.caller.AddBeat('Breaking Point',rhs)
                                notices.msg(self.caller.name + " just rolled for an act of hubris with a modifier of " + lhs + " and got a failure.")
                                self.caller.db.breaklog.append("Failure. Reason: "+rhs+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                self.caller.db.currentbreak = "Dramatic Failure," +rhs
                                return
                                
                        else:
                            self.caller.msg("You need to provide both a reason and a level of hubris to roll for a breaking point.")
                    else:
                        self.caller.msg("You still need to resolve your previous breaking point with +break/rampant or +break/megalomaniacal first.")
                        return
                elif template == "Vampire":
                    if self.caller.db.currentbreak == "":
                        breakpool = 0
                        for merit in self.caller.db.meritlist:
                            if merit[0] == "Touchstone":
                                touchstones = int(merit[1])
                            if self.caller.db.xsplat != "Ventrue":
                                if (7 - touchstones) < sanity:
                                    breakpool += 3
                                elif (7 - touchstones) == sanity:
                                    breakpool += 2
                                else:
                                    breakpool -= 2
                            else:
                                if (8 - touchstones) < sanity:
                                    breakpool += 3
                                elif (8 - touchstones) == sanity:
                                    breakpool += 2
                                else:
                                    breakpool -= 2
                            try:
                                breakpool += int(self.lhs)
                            except ValueError:
                                self.caller.msg("Invalid modifier.")
                                return
                        if self.rhs:
                            if "/" in self.rhs:
                                reason = self.rhs.split("/")[0]
                                try:
                                    rank = int(self.rhs.split("/")[1])
                                except ValueError:
                                    self.caller.msg("That's not a valid rank of breaking point.")
                                    return
                                if rank > sanity:
                                    self.caller.msg("You don't have to roll for detachment for an action of that tier.")
                                    return
                                if rank == 10 or rank == 9:
                                    breakpool += 5
                                elif rank == 8 or rank == 7:
                                    breakpool += 4
                                elif rank == 6 or rank == 5:
                                    breakpool += 3
                                elif rank == 4 or rank == 3:
                                    breakpool += 2
                                elif rank == 2:
                                    breakpool += 1
                                elif rank == 1:
                                    pass
                            else:
                                self.caller.msg("You have to provide a reason to use this command.")
                                return
                            successes = 0
                            if breakpool > 0:
                                breakcount = 0
                                while breakcount < breakpool:
                                    breakdie = random.randint(1,10)
                                    if breakdie >= 8:
                                        successes += 1
                                        if breakdie == 10:
                                            breakcount -= 1
                                        breakcount += 1
                            elif breakpool <= 0:
                                alldice = False
                                while alldice == False:
                                    breakdie = random.randint(1,10)
                                    if breakdie == 10:
                                        successes += 1
                                    elif breakdie == 1 and successes == 0:
                                        alldice = True
                                        dramafail = True
                                    else:
                                        alldice = True
                            if 5 > successes > 0:
                                self.caller.db.currentbreak = "Success," + reason
                                self.caller.msg("Breaking point passed, dot of humanity retained. Please use +break/bestial, +break/wanton, or +break/competitive to choose a condition.")
                                self.caller.AddBeat("Breaking Point",rhs)
                                notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+lhs+" and got a success.")
                                return
                            elif successes >= 5:
                                self.caller.msg("Breaking point passed with an exceptional success. Dot of humanity retained, and Inspired condition added for relating to humanity.")
                                self.caller.db.beats.AddBeat("Breaking Point",reason)
                                self.caller.AddBeat("Breaking Point",rhs)
                                self.caller.db.breaklog.append("Exceptional success. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+lhs+" and got an exceptional success.")
                                self.caller.Inflict("Inspired (Humanity)")
                                return
                            elif successes == 0:
                                self.caller.msg("Breaking point failed. Please use +break/bestial, +break/wanton, or +break/competitive to choose a condition.")
                                self.caller.db.currentbreak = "Failure," + reason
                                notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+lhs+" and got a failure.")
                                return
                            elif successes == 0 and dramafail:
                                self.caller.msg("Breaking point failed dramatically. Jaded condition added, dot of humanity lost, and beat added.")
                                self.caller.db.beats.AddBeat("Breaking Point"," "+reason)
                                self.caller.db.breaklog.append("Dramatic failure, jaded condition added. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                self.caller.Inflict("Jaded")
                                notices.msg(self.caller.name + " just rolled a breaking point for "+ rhs + " width a modifier of "+lhs+" and got a dramatic failure.")
                                return
                        else:
                            self.caller.msg("You need to provide both a reason and a level of breaking point in addition to the modifiers.")
                    else:
                        self.caller.msg("You still need to accept a condition from your previous breaking point!")
                        return
                elif template == "Werewolf":
                    try:
                        breakpool = attributes['Resolve'] + attributes['Composure'] + int(lhs)
                        reason = rhs.split("/")[0]
                        side = rhs.split("/")[1]
                        if "Spiritual" in self.caller.db.touchstones.keys() and side.lower() == "spirit":
                            breakpool += 2
                            breakpool -= (sanity - 5)
                        elif "Physical" in self.caller.db.touchstones.keys() and side.lower() == "flesh":
                            breakpool += 2
                            breakpool += (sanity - 5)
                        breakcounter = 0
                        success = 0
                        while breakcounter < breakpool:
                            breakdie = random.randint(1,10)
                            if breakdie >= 8:
                                success += 1
                                if breakdie == 10:
                                    breakcounter -= 1
                            breakcounter += 1
                        if success > 0:
                            self.caller.msg("Breaking point succeeded, no change to harmony occurred.")
                            self.caller.AddBeat("Breaking Point",rhs)
                            notices.msg(self.caller.name + " just rolled a breaking point for " + reason + " towards " +side.lower() + " and succeeded.")
                            self.caller.db.breaklog.append("Success. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                            return
                        else:
                            if side == "spirit":
                                self.caller.msg("Breaking point towards spirit failed, dot of harmony lost.")
                                notices.msg(self.caller.name + " just rolled a breaking point for " + reason + " towards spirit and failed.")
                                self.caller.db.beats.AddBeat("Breaking Point",rhs)
                                self.caller.db.breaklog.append("Failure towards spirit. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                sanity -= 1
                                return
                            if side == "flesh":
                                self.caller.msg("Breaking point towards flesh failed, dot of harmony gained.")
                                self.caller.db.beats.AddBeat("Breaking Point",rhs)
                                notices.msg(self.caller.name + " just rolled a breaking point for " + reason + " towards flesh and failed.")
                                self.caller.db.breaklog.append("Failure towards flesh. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                                sanity += 1
                                return
                    except ValueError:
                        self.caller.msg("That's not a valid modifier to use!")
                        return
                elif template == "Changeling":
                    if self.caller.db.currentbreak != "":
                        self.caller.msg("You still have to pick a beneficial condition from your last breaking point's exceptional success!")
                        return
                    breakpool = attributes['Wits'] + attributes['Composure']
                    if len(self.caller.db.touchstones) == 0:
                        breakpool -= 2
                    try:
                        breakpool += int(lhs)
                    except ValueError:
                        self.caller.msg("That's not a valid modifier to use!")
                        return
                    breakcounter = 0
                    success = 0
                    dramafail = False
                    if breakpool > 0:
                        while breakcounter < breakpool:
                            breakdie = random.randint(1,10)
                            if breakdie >= 8:
                                success += 1
                                if breakdie == 10:
                                    breakcounter -= 1
                            breakcounter += 1
                    else:
                        alldice = False
                        while not alldice:
                            breakdie = random.randint(1,10)
                            if breakdie == 10:
                                success += 1
                            elif breakdie == 1 and success == 0:
                                alldice = True
                                dramafail = True
                            else:
                                alldice = True
                    if 5 > success > 0:
                        self.caller.msg("Success, dot of clarity retained and acuity condition added.")
                        notices.msg(self.caller.name + " just rolled a breaking point for " + rhs + " with a dice modifier of " + lhs + " and got a success.")
                        self.caller.db.breaklog.append("Success. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.db.beats.AddBeat("Breaking Point",rhs)
                        self.caller.Inflict('Acuity')
                        return
                    elif success >= 5:
                        self.caller.msg("Exceptional success, dot of clarity retained and acuity condition added. Please use +break/steadfast or +break/inspired to choose a beneficial condition.")
                        notices.msg(self.caller.name + " just rolled a breaking point for " + rhs + " with a dice modifier of " + lhs + " and got an exceptional success.")
                        self.caller.Inflict('Acuity')
                        self.caller.AddBeat("Breaking Point",rhs)
                        self.caller.db.currentbreak = "Exceptional Success," + rhs
                        return
                    elif success == 0 and not dramafail:
                        self.caller.msg("Failure, dot of clarity removed and delusional condition added in non-persistent form.")
                        self.caller.db.beats.AddBeat("Breaking Point",rhs)
                        notices.msg(self.caller.name + " just rolled a breaking point for " + rhs + " with a dice modifier of " + lhs + " and got a failure.")
                        self.caller.Inflict('Delusional')
                        sanity -= 1
                        return
                    elif success == 0 and dramafail:
                        self.caller.msg("Dramatic Failure, dot of clarity removed and delusional condition added in persistent form.")
                        self.caller.db.beats.AddBeat("Breaking Point",rhs)
                        notices.msg(self.caller.name + " just rolled a breaking point for " + rhs + " with a dice modifier of " + lhs + " and got a dramatic failure.")
                        self.caller.Inflict('Delusional',True)
                        sanity -= 1
                elif template == "Demon":
                    dicepool = attributes['Wits'] + attributes['Manipulation']
                    if sanity > 7:
                        dicepool += 2
                    elif sanity > 5:
                        dicepool += 1
                    elif sanity > 3:
                        pass
                    elif sanity > 1:
                        dicepool -= 1
                    elif sanity == 1:
                        dicepool -= 2
                    counter = 0
                    if dicepool > 0:
                        while counter < dicepool:
                            die = random.randint(1,10)
                            if die >= 8:
                                success += 1
                                if die == 10:
                                    counter -= 1
                            counter += 1
                    else:
                        alldice = False
                        while not alldice:
                            die = random.randint(1,10)
                            if die == 10:
                                success += 1
                            if die == 1 and success == 0:
                                alldice = True
                                dramafail = True
                            else:
                                alldice = True
                    if 5 > success > 0:
                        self.caller.msg("Success, dot of cover retained. Please use +break/guilty, +break/shaken, +break/spooked, or +break/glitch to add one of the three conditions, or roll for a permanent glitch.")
                        notices.msg(self.caller.name + " just rolled a cover compromise for " + rhs + " with a dice modifier of " + lhs + " and got a success.")
                        self.caller.AddBeat("Breaking Point",rhs)
                        self.caller.db.currentbreak = "Success," + rhs
                        return
                    elif success >= 5:
                        self.caller.msg("Exceptional Success, beat added and point of temporary willpower restored.")
                        notices.msg(self.caller.name + " just rolled a cover compromise for " + rhs + " with a dice modifier of " + lhs + " and got a success.")
                        self.caller.AddBeat("Breaking Point",rhs)
                        self.caller.PoolGain('Willpower',1)
                        self.caller.AddBeat("Breaking Point",rhs)
                        return
                    elif success == 0 and not dramafail:
                        self.caller.msg("Failure, dot of cover lost. Please use +break/flagged, +break/surveilled, +break/hunted, or +break/glitch to add one of the three conditions, or roll for a permanent glitch.")
                        notices.msg(self.caller.name + " just rolled a cover compromise for " + rhs + " with a dice modifier of " + lhs + " and got a failure.")
                        self.caller.db.currentbreak = "Failure," + rhs
                        self.caller.AddBeat("Breaking Point",rhs)
                        return
                    elif success == 0 and dramafail:
                        self.caller.msg("Dramatic Failure, dot of cover lost. Please use +break/blown, +break/betrayed, +break/hunted, or +break/glitch to add one of the three conditions, or make TWO permanent glitch rolls.")
                        notices.msg(self.caller.name + " just rolled a cover compromise for " + rhs + " with a dice modifier of " + lhs + " and got a failure.")
                        self.caller.db.currentbreak = "Dramatic Failure," + rhs
                        self.caller.AddBeat("Breaking Point",rhs)
                        self.caller.AddBeat("Breaking Point",rhs)
                        return
            else:
                self.caller.msg("You need to give a reason to use this command.")
        elif switches[0].lower() == "rampant":
            if template == "Mage":
                if self.caller.db.currentbreak != "":
                    if "Failure" in self.caller.db.currentbreak:
                        if 'Dramatic' in self.caller.db.currentbreak:
                            self.caller.Inflict('Rampant',True)
                        else:
                            self.caller.Inflict('Rampant')
                        self.caller.msg("Breaking point resolved, dot of wisdom removed and rampant condition added.")
                        self.caller.db.currentbreak = ""
                        sanity -= 1
                        return
                else:
                    self.caller.msg("You have no breaking points to resolve at the moment.")
                    return
            else:
                self.caller.msg("Only mages may take rampant as a condition from a breaking point.")
                return
        elif switches[0].lower() == "megalomaniacal":
            if template == "Mage":
                if self.caller.db.currentbreak != "":
                    if "Failure" in self.caller.db.currentbreak:
                        if "Dramatic" in self.caller.db.currentbreal:
                            self.caller.Inflict('Megalomaniacal',True)
                        else:
                            self.caller.Inflict('Megalomaniacal')
                        self.caller.msg("Breaking point resolved, dot of wisdom removed and megalomaniacal condition added.")
                        self.caller.db.currentbreak = ""
                        sanity -= 1
                        return
        elif switches[0].lower() == "steadfast":
            if template == "Changeling":
                if "Exceptional Success" in self.caller.db.currentbreak:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Steadfast condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.db.breaklog.append("Exceptional success, steadfast condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    self.caller.Inflict('Steadfast')
                    return
                else:
                    self.caller.msg("You have no breaking point to resolve!")
                    return
            else:
                self.caller.msg("You can't choose steadfast when resolving a breaking point!")
                return
        elif switches[0].lower() == "surveilled":
            if template == "Demon":
                if "Failure" == self.caller.db.currentbreak.split(",")[0]:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Surveilled condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.Inflict('Surveilled')
                    sanity -= 1
                    self.caller.db.breaklog.append("Failure, surveilled condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    return
                else:
                    self.caller.msg("That isn't an appropriate condition to choose for your last compromise!")
                    return
            else:
                self.caller.msg("You can't choose this condition when resolving a breaking point.")
                return
        elif switches[0].lower() == "flagged":
            if template == "Demon":
                if "Failure" == self.caller.db.currentbreak.split(",")[0]:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Flagged condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.Inflict('Flagged')
                    sanity -= 1
                    self.caller.db.breaklog.append("Failure, flagged condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    return
                else:
                    self.caller.msg("That isn't an appropriate condition to choose for your last compromise!")
                    return
            else:
                self.caller.msg("You can't choose this condition when resolving a breaking point.")
        elif switches[0].lower() == "hunted":
            if template == "Demon":
                if "Failure" in self.caller.db.currentbreak:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Hunted condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.Inflict('Hunted')
                    sanity -= 1
                    if "Dramatic Failure" in self.caller.db.currentbreak:
                        self.caller.db.breaklog.append("Dramatic Failure, hunted condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    else:
                        self.caller.db.breaklog.append("Failure, hunted condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    return
                else:
                    self.caller.msg("That isn't an appropriate condition to choose for your last compromise!")
                    return
            else:
                self.caller.msg("You can't choose this condition when resolving a breaking point.")
        elif switches[0].lower() == "blown":
            if template == "Demon":
                if "Dramatic Failure" in self.caller.db.currentbreak:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Blown condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.Inflict('Blown')
                    sanity -= 1
                    self.caller.db.breaklog.append("Dramatic Failure, blown condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    return
                else:
                    self.caller.msg("That isn't an appropriate condition to choose for your last compromise!")
                    return
            else:
                self.caller.msg("You can't choose this condition when resolving a breaking point.")
        elif switches[0].lower() == "betrayed":
            if template == "Demon":
                if "Dramatic Failure" in self.caller.db.currentbreak:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Betrayed condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.Inflict('Betrayed')
                    sanity -= 1
                    self.caller.db.breaklog.append("Dramatic Failure, betrayed condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    return
                else:
                    self.caller.msg("That isn't an appropriate condition to choose for your last compromise!")
                    return
            else:
                self.caller.msg("You can't choose this condition when resolving a breaking point.")
        elif switches[0].lower() == "inspired":
            if template == "Changeling":
                if "Exceptional Success" in self.caller.db.currentbreak:
                    reason = self.caller.db.currentbreak.split(",")[1]
                    self.caller.msg("Inspired condition chosen.")
                    self.caller.db.currentbreak = ""
                    self.caller.db.breaklog.append("Exceptional success, inspired condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                    self.caller.Inflict('Inspired')
                    return
                else:
                    self.caller.msg("You have no breaking point to resolve!")
                    return
            else:
                self.caller.msg("You can't choose inspired when resolving a breaking point!")
                return
        elif switches[0].lower() == "guilty":
            if self.caller.db.sanityname == "Integrity" or self.caller.db.santiyname == "Cover":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Guilty")
                        self.caller.db.breaklog.append("Success, guilty condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y") )
                        self.caller.msg("Guilty condition chosen.")
                        self.caller.db.currentbreak = ""
                        return
                    elif "Failure" == self.caller.db.currentbreak.split(",")[0] and self.caller.db.sanityname == "Integrity":
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Guilty")
                        self.caller.db.breaklog.append("Failure, guilty condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y") )
                        self.caller.msg("Guilty condition chosen and dot of integrity removed.")
                        self.caller.db.currentbreak = ""
                        sanity -= 1
                        return
                    else:
                        self.caller.msg("That isn't an appropriate condition to choose for your last breaking point.")
                        return
                else:
                    self.caller.msg("You have no breaking point to choose a condition for.")
                    return
            else:
                self.caller.msg("You can't select the, 'Guilty' condition in response to your template's breaking points.")
                return
        elif switches[0].lower() == "shaken":
            if self.caller.db.sanityname == "Integrity" or self.caller.db.sanityname == "Cover":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Shaken")
                        self.caller.db.breaklog.append("Success, shaken condition chosen. Reason: "+reason +" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Shaken condition chosen.")
                        self.caller.db.currentbreak = ""
                        return
                    elif "Failure" == self.caller.db.currentbreak.split(",")[0] and self.caller.db.sanityname == "Integrity":
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Shaken")
                        self.caller.db.breaklog.append("Failure, shaken condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Shaken condition chosen and dot of integrity removed.")
                        sanity -= 1
                        self.caller.db.currentbreak = ""
                        return
                    else:
                        self.caller.msg("That isn't an appropriate condition to choose for your last breaking point.")
                        return
                else:
                    self.caller.msg("You have no breaking point to select a condition for.")
                    return
            else:
                self.caller.msg("You can't select, the, 'Shaken' condition in response to your template's breaking points.")
                return
        elif switches[0].lower() == "spooked":
            if self.caller.db.sanityname == "Integrity" or self.caller.db.sanityname == "Cover":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Spooked")
                        self.caller.db.breaklog.append("Success, spooked condition chosen. Reason: "+reason +" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Spooked condition chosen.")
                        self.caller.db.currentbreak = ""
                        return
                    elif "Failure" == self.caller.db.currentbreak.split(",")[0] and self.caller.db.sanityname == "Integrity":
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Spooked")
                        self.caller.db.breaklog.append("Failure, spooked condition chosen. Reason: "+reason+" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Spooked condition chosen and dot of integrity removed.")
                        self.caller.db.currentbreak = ""
                        sanity -= 1
                        return
                    else:
                        self.caller.msg("That isn't an appropriate condition for your last breaking point.")
                        return
                else:
                    self.caller.msg("You have no breaking point to select a condition for.")
                    return
        elif switches[0].lower() == "madness":
            if self.caller.db.sanityname == "Integrity":
                if self.caller.db.currentbreak != "":
                    if "Dramatic Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Madness")
                        self.caller.db.breaklog.append("Dramatic Failure, madness condition chosen. Reason: "+reason +" Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Madness condition chosen and dot of integrity removed.")
                        sanity -= 1
                        self.caller.db.currentbreak = ""
                        return
                    else:
                        self.caller.msg("Madness isn't an appropriate condition for your last breaking point's result.")
                        return
                else:
                    self.caller.msg("You have no breaking point to resolve.")
                    return
            else:
                self.caller.msg("Your template cannot choose the madness condition in response to breaking points.")
                return
        elif switches[0].lower() == "fugue":
            if self.caller.db.sanityname == "Integrity":
                if self.caller.db.currentbreak != "":
                    if "Dramatic Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Fugue")
                        self.caller.db.breaklog.append("Dramatic Failure, fugue condition chosen. Reason: "+reason+ " Date: " +time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Fugue condition chosen and dot of integrity removed.")
                        sanity -= 1
                        self.caller.db.currentbreak = ""
                        return
                    else:
                        self.caller.msg("Fugue isn't an appropriate condition for your last breaking point's result.")
                        return
                else:
                    self.caller.msg("Fugue isn't a condition your template can acquire from a breaking point.")
                    return
            else:
                self.caller.msg("You have no breaking point to resolve.")
                return
        elif switches[0].lower() == "broken":
            if self.caller.db.sanityname == "Integrity":
                if self.caller.db.currentbreak != "":
                    if "Dramatic Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Broken")
                        self.caller.db.breaklog.append("Dramatic Failure, broken condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        sanity -= 1
                        self.caller.msg("Broken condition chosen and dot of integrity removed.")
                        self.caller.db.currentbreak = ""
                        return
                    else:
                        self.caller.msg("Broken isn't an appropriate condition for your last breaking point's result.")
                        return
                else:
                    self.caller.msg("You have no breaking point to resolve.")
                    return
            else:
                self.caller.msg("Broken isn't a condition your template can take in reaction to a breaking point.")
                return
        elif switches[0].lower() == "bestial":
            if self.caller.db.template == "Vampire":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Bestial")
                        self.caller.db.breaklog.append("Success, bestial condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Bestial condition chosen.")
                        return
                    elif "Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Bestial")
                        self.caller.db.breaklog.append("Failure, bestial condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Bestial condition chosen and dot of humanity removed.")
                        sanity -= 1
                        return
                else:
                    self.caller.msg("You have no breaking point to resolve!")
                    return
            else:
                self.caller.msg("Your template can't select the bestial condition as a breaking point result.")
                return
        elif switches[0].lower() == "competitive":
            if self.caller.db.template == "Vampire":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Competitive")
                        self.caller.db.breaklog.append("Success, competitive condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Competitive condition chosen.")
                        return
                    elif "Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Competitive")
                        self.caller.db.breaklog.append("Failure, competitive condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        sanity -= 1
                        self.caller.msg("Competitive condition chosen and dot of humanity removed.")
                        return
                else:
                    self.caller.msg("You have no breaking point to resolve!")
                    return
            else:
                self.caller.msg("Your template can't select the competitive condition as a breaking point result.")
                return
        elif switches[0].lower() == "wanton":
            if self.caller.db.template == "Vampire":
                if self.caller.db.currentbreak != "":
                    if "Success" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Wanton")
                        self.caller.db.breaklog.append("Success, wanton condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Wanton condition chosen.")
                        return
                    elif "Failure" in self.caller.db.currentbreak:
                        reason = self.caller.db.currentbreak.split(",")[1]
                        self.caller.Inflict("Wanton")
                        self.caller.db.breaklog.append("Failure, wanton condition chosen. Reason: "+reason + " Date: "+time.strftime("%d")+" "+time.strftime("%m")+ " " + time.strftime("%Y"))
                        self.caller.msg("Wanton condition chosen and dot of humanity removed.")
                        sanity -= 1
                        return
                else:
                    self.caller.msg("You have no breaking point to resolve!")
                    return
            else:
                self.caller.msg("Your template can't select the wanton condition as a breaking point result.")
                return
class ChargenHelp(Command):
    key = "+cghelp"
    lock = "cmd:all()"
    def parse (self):
        self.args = self.args.strip()
    def func(self):
        try:
            if self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0] >= 156:
                screenwidth = self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0]
            else:
                screenwidth = 156
        except IndexError:
            screenwidth = 156
        args = self.args
        if not args:
            helplist = os.listdir('./helpfiles/chargen')
            stringout = "/" + "-" * (screenwidth/2 - len('Chargen')/2) + "Chargen" + "-" * (screenwidth/2 - len('Chargen')/2 + 1) + "\\\n"
class MUSHHelp(Command):
    #Ye olde help system. Actually, this stuff is stored in text files so it's not actually so old as one might expect. Still functions similarly though.
    key = "+help"
    lock = "cmd:all()"
    helptitle = ""
    def parse(self):
        self.args = self.args.strip()
        #Pretty simple parser. Removes whitespace.
    def func(self):
        psyvamp = False
        atariya = False
        dreamer = False
        infected = False
        lostboy = False
        plain = False
        try:
            if self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0] >= 156:
                screenwidth = self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0]
            else:
                screenwidth = 156
        except IndexError:
            screenwidth = 156
        cellwidth = ((screenwidth/2) - 2)/3
        for item in self.caller.db.meritlist:
            if item[0].lower() == "psychic vampirism":
                psyvamp = True
            elif item[0].lower() == "damn lucky":
                atariya = True
            elif item[0].lower() == "subliminal conditioning":
                dreamer = True
            elif item[0].lower() == "carrier":
                infected = True
            elif item[0].lower() == "the protocol":
                lostboy = True
            elif item[0].lower() == "plain reader":
                plain = True
        outputstring = ""
        args = self.args.lstrip()
        helptitle = self.helptitle
        dir_list = []
        currentdir = "./helpfiles/"
        commandstring = ""
        if args == "":
        #If there are no arguments, set the 'helptitle' or file being looked for in string form, to main. This is the main menu of the help system.
            helptitle = "main"
        else:
        #If there are arguments, we look to see if there are backslashes in it. The double-backslash thing is because the backslash is the escape character
        #so it has to be escaped to register as an actual backslash.
            if "/" in args:
                for slash in args:
                #Obviously at this point, we know there's at least one backslash. So we look for each and every one in there.
                    if slash == "/":
                        slashindex = args.index("/")
                        #A bit of implicit stuff taking place here. If there's more than one backslash in the list, then obviously it's deeper in. More on that later.
                        #For now however, this makes sure we only get the file name rather than any folders by selecting the final backslash present in the string.
                helptitle = args[slashindex+1:len(args)]
                #Sets the actual file name rather than any of the folders by selecting everything after the final backslash.
                currentdir = "./helpfiles/"+ args[0:slashindex] + "/"
                #Sets the current directory by selecting everything before the final backslash, backslash included.
            elif "\\" in args:
                for slash in args:
                #Obviously at this point, we know there's at least one backslash. So we look for each and every one in there.
                    if slash == "\\":
                        slashindex = args.index("\\")
                        #A bit of implicit stuff taking place here. If there's more than one backslash in the list, then obviously it's deeper in. More on that later.
                        #For now however, this makes sure we only get the file name rather than any folders by selecting the final backslash present in the string.
                helptitle = args[slashindex+1:len(args)]
                #Sets the actual file name rather than any of the folders by selecting everything after the final backslash.
                currentdir = "./helpfiles/"+ args[0:slashindex] + "/"
                #Sets the current directory by selecting everything before the final backslash, backslash included.
            else:
                helptitle = args
                #If there are no backslashes in the argument though, it just grabs the argument as the title.
        filefound = False
        for filesearch in os.listdir(currentdir):
            if filesearch.replace(".txt","").lower() == helptitle.lower():
                helptitle = filesearch.replace('.txt','')
                filefound = True
        if not filefound:
            outputstring = "Please select a valid helpfile, or use '+help' by itself to see the main index."
            return
            #Simple error message, not MUCH to see here.
        if (len(helptitle) % 2) != 0:
        #Checks to see if the helptitle string's length is an odd number. Going to need this for the header.
            helptitle_left = (screenwidth - 6)/4 - (len(helptitle)/2)
            helptitle_right = helptitle_left + 1
        else:
        #Given that only two situations may occur here, an else case would mean that this helptitle has an even length.
            helptitle_left = (screenwidth - 4)/4 - (len(helptitle)/2)
            helptitle_right = helptitle_left
        if os.path.isfile(currentdir+str(helptitle)+'.txt'):
        #This makes sure that the file exists at all.
            displaytitle = helptitle.replace("_"," ")
            outputstring += "/" + "-" * helptitle_left + displaytitle + "-"  * helptitle_right + "\\\n"
            #This actually makes the header, placed after it ensures that the file exists so as not to make a header for a nonexistent file.text that have been fitted to the width of 78 (The area inside the text box)
            #from the singular, long string.
            commandfile = open(currentdir+helptitle+".txt",'r')
            commandstring = commandfile.read()
            helpdirs = os.listdir(currentdir)
            #This checks to see if there is anything within the current directory.
            for x in helpdirs:
            #This iterates through the current directory, and sees if those things are directories themselves.
                if os.path.isdir(currentdir+str(x)):
                #If they are in fact directories, it appends them to the dir_list list.
                    dir_list.append(x)
            if commandstring != "":
            #So, this checks to see if commandstring is something other than empty. This would be the case if an associated command file exists.
                commandlist = []
                commandlist.extend(commandstring.splitlines(True))
                for line in commandlist:
                    line = line.replace("\n","^")
                    line = wrap(line,((screenwidth - 4)/2))
                    for section in line:
                        oldsection = section
                        section = section.replace("^","\n")
                        if section.endswith("\n") and (not(section == "\n")):
                            line.insert((line.index(oldsection)+1),"\n")
                            section = section.replace("\n","")
                            outputstring += "||" + section + " " * (((screenwidth - 4)/2)  - len(section)) + "||\n"
                        elif section == "\n":
                            if section != oldsection.replace("^","\n"):
                                outputstring += "||" + " " * (((screenwidth - 4)/2) - len(section)) + "||\n"
                        else:
                            outputstring += "||" + section + " " * (((screenwidth - 4)/2) - len(section)) + "||\n"
            if currentdir == "./helpfiles/":
            #This checks to see if we're in the helpfiles directory. The only things in here are the main helpfile and the subfolders as far as direct contents go.
                if len(dir_list) != 0:
                #This checks to make sure that the directory list actually has stuff in it. Strictly speaking this shouldn't actually be a problem as the game will
                #be launching with helpfiles and help folders, but you never know.
                    for thing in dir_list:
                    #This checks to see what's in the directory list, and iterates through it.
                        if (thing.lower() == "dreamers" and dreamer == True) or (thing.lower() == "admin" and self.caller.IsAdmin()) or (thing.lower() == "lost_boys" and lostboy == True) or (thing.lower() == "infected" and infected == True) or (thing.lower() == "plain" and plain == True) or(thing.lower() == "psychic_vampire" and psyvamp == True) or (thing.lower() == "atariya" and atariya == True) or (self.caller.db.template == thing.title()) or (self.caller.db.powerstat != 0 and thing.title() == "Supernatural") or (thing.title() == "General") or (thing.title() == "Policies"):
                            outputstring += "+--" + thing.title().replace("_"," ") + "-" * (((screenwidth - 2)/2) - len("+--" + thing.title())) + "+\n"
                            #This adds a header for every item in the directory list.
                            if os.path.isdir("./helpfiles/"+thing):
                            #This also checks to see if the folder in question is a valid folder. Yes, it's a bit redundant but redundant safety never hurt anyone.
                                thing_list = os.listdir("./helpfiles/"+thing)
                                #This forms a list of contents within the subdirectory.
                                for string in thing_list:
                                #This checks for command files in the contents of the directory currently referenced by, 'thing'.
                                    if "commands" in string:
                                        thing_list.remove(string)
                                        #This also removes the associated commands files, because they aren't independent helpfiles.
                                while "__init__.py" in thing_list: thing_list.remove("__init__.py")
                                #This bit actually removes the __init__.py files from thing_list, because those aren't helpfiles.
                                cellcalc = 0
                                filecount = 0
                                for filesearch in thing_list:
                                    cellcalc += len(filesearch)
                                    filecount += 1
                                if filecount != 0:
                                    cell_padding = ((screenwidth/2) - 2)/filecount
                                filestring = ""
                                for file2 in thing_list:
                                    if cell_padding >= len(file2):
                                        break
                                    else:
                                        cellwidth = cell_padding
                                olditems = ""
                                #A variable used to store the unlinked versions of the strings. Useful for not having as complex code.
                                for item2 in thing_list:
                                    item2 = re.sub('.txt','',item2)
                                    if thing_list.index((item2 + '.txt')) == 0:
                                        filestring += "|||lc +help " + thing + "/" + item2 + "|lt" + item2.replace("_"," ") + "|le" + " " * (cellwidth - len("| " + item2)) + "  "
                                        olditems += "| " + item2 + " " * (cellwidth - len("| " + item2)) + "  "
                                    elif len(item2) + len(olditems) > ((screenwidth/2) - 2):
                                        filestring = filestring.rstrip()
                                        olditems = olditems.rstrip()
                                        filestring += " " * ((screenwidth/2) - len(olditems)) + "||\n"
                                        olditems = ""
                                        filestring += "|||lc +help " + thing + "/" + item2 + "|lt" + item2.replace("_"," ") + "|le" + " " * (cellwidth - len("| " + item2)) + "  "
                                        olditems += "| " + item2 + " " * (cellwidth - len("| " + item2)) + "  "
                                    else:
                                        filestring += "|lc +help " + thing + "/" + item2 + "|lt" + item2.replace("_"," ") + "|le" + " " * (cellwidth - len(item2)) + "  "
                                        olditems += item2 + " " * (cellwidth - len(item2)) + "  "
                                    if thing_list.index((item2 + '.txt')) == (len(thing_list) - 1):
                                        filestring = filestring.rstrip()
                                        olditems = olditems.rstrip()
                                        filestring += " " * ((screenwidth/2) - len(olditems)) + "||\n"
                                        olditems = ""
                                outputstring += filestring
                                filestring = ""
                                olditems = ""
                                #Filestring is the entire list of helpfiles under a given category.
            outputstring += "\\" + "-" * ((screenwidth - 4)/2) + "/"
            #Finally, the footer.
        self.caller.msg(outputstring)
class BackgroundCommand(default_cmds.MuxCommand):
    """
    Used to add, remove, or view sections of your character's background.
    
    Usage:
        +bg/add <Information> Adds a given section to your background, stored as a number.
        +bg/del <Number> Removes the section with a given number.
        +bg/view <Character>=<Number> Admins only, views the character's background section.
    """
    key = "+bg"
    lock = "cmd:inside(Chargen)"
    help_category = "Chargen"
    def func(self):
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        if switches[0] == 'add':
            self.caller.db.background.append(self.args)
        if switches[0] == 'view':
            if self.caller.IsAdmin():
                try:
                    charsearch = search.objects(lhs)[0]
                    if inherits_from(charsearch,DefaultCharacter):
                        if rhs:
                            try:
                                int(rhs)
                                bgtable = evtable.EvTable('Background Section '+rhs)
                                bgtable.add_row(charsearch.db.background[int(rhs)])
                                self.caller.msg(str(bgtable))
                            except ValueError:
                                self.caller.msg("A background section must be a number.")
                            return
                    else:
                        self.caller.msg("That's not a character")
                        return
                except IndexError:
                    self.caller.msg("Invalid character.")
                    return
            else:
                try:
                    bgtable = evtable.EvTable('Background Section '+self.args)
                    bgtable.add_row(self.caller.db.background(int(self.args)))
                    self.caller.msg(str(bgtable))
                except ValueError:
                    self.caller.msg("That's not a background section.")
                    return
        if switches[0] == "del":
            if self.caller.IsAdmin() and rhs:
                try:
                    charsearch = search.objects(lhs)[0]
                    if inherits_from(charsearch,DefaultCharacter):
                        try:
                            charsearch.db.background.remove(int(rhs))
                            self.caller.msg(rhs + " removed from the background of " + charsearch.name)
                            return
                        except ValueError:
                            self.caller.msg("That's not a valid section to remove.")
                            return
                except IndexError:
                    self.caller.msg("That isn't a valid character.")
                    return
            else:
                try:
                    charsearch.db.background.remove(int(rhs))
                    self.caller.msg(rhs +" removed from your background.")
                    return
                except ValueError:
                    self.caller.msg('Invalid section to remove.')
                    return
class NoteCommand(default_cmds.MuxCommand):
    """
    Used to set notes about your character, regarding retainers, further elaboration on touchstones, and many more things still.
    
    +note <Name> Shows a note with a given name, if you have it. Without a name, shows any notes you have.
    +note/add <Name>=<Info> Adds a note storing the given info under the given name.
    +note/del <Name> Removes a given note from your list of notes.
    +note/show <Character>=<Note> Shows a given note to a character in the same room.
    """
    key = "+note"
    lock = "cmd:all()"
    help_category="Gameplay"
    def func(self):
        switches = self.switches
        args = self.args
        lhs = self.lhs
        rhs = self.rhs
        if not switches and args:
            if rhs and self.caller.IsAdmin():
                try:
                    charsearch = search.objects(lhs)[0]
                    if inherits_from(charsearch,DefaultCharacter):
                        notetable = evtable.EvTable(header_line_char="-",border='table')
                        for note in charsearch.db.notes.keys():
                            if note.lower() == lhs.lower():
                                notetable.add_header(note)
                                notetable.add_row(charsearch.db.notes[note])
                        self.caller.msg(str(notetable))
                except IndexError:
                    self.caller.msg("Invalid character.")
                    return
        elif not switches and not args:
            if len(self.caller.db.notes.keys()) > 0:
                notetable = evtable.EvTable('Your Notes',header_line_char='-',border='table')
                for note in self.caller.db.notes.keys():
                    notetable.add_row(charsearch.db.notes[note])
                self.caller.msg(str(notetable))
            else:
                self.caller.msg("You don't have any notes to view!")
                return
        elif switches and args:
            if switches[0] == "add":
                self.caller.db.notes[lhs] = rhs
                self.caller.msg("Note titled " + lhs + " set to " + rhs)
                return
            elif switches[0] == "del":
                self.caller.db.notes.remove(lhs)
                self.caller.msg(lhs + " removed from your notes.")
                return
            elif switches[0] == "show":
                for note in self.caller.db.notes.keys():
                    if note.lower() == rhs.lower():
                        notetable = evtable.EvTable(note,header_line_char='-',border='table')
                        notetable.width = 39
                        break
                if notetable:
                    try:
                        charsearch = search.objects(lhs)[0]
                        charsearch.msg(str(notetable))
                    except IndexError:
                        self.caller.msg("Invalid character to show the note.")
                        return
class TouchstoneCommand(default_cmds.MuxCommand):
    """
    Defines your starting touchstone or touchstones for your supernatural character.
    
    Usage:
        +touchstone <Name> Sets your initial touchstone to the name given.
        +touchstone/<Spirit or Phys> <Name> Sets your spirit or physical touchstone to a given
        name.
        +touchstone/del <Name> Deletes a given touchstone.
        +touchstone/show <Character>=<Touchstone> Proves that you have a given touchstone.
    """
    key = "+touchstone"
    lock = "cmd:inside(Chargen)"
    help_category="Gameplay"
    def func(self):
        template = self.caller.db.template
        lhs = self.lhs
        rhs = self.rhs
        switches = self.switches
        args = self.args
        if not args and not switches:
            if template == "Changeling" or template == "Vampire" or template == "Werewolf":
                touchtable = evtable.EvTable('Touchstones',header_line_char="-",border='table')
                if len(self.caller.db.touchstones.keys()) > 0:
                    for stone in self.caller.db.touchstones.keys():
                        touchtable.add_row(stone)
                    touchtable.width=39
                    self.caller.msg(str(touchtable))
                    return
                else:
                    self.caller.msg("You don't have any touchstones!")
                    return
            else:
                self.caller.msg("Your template doesn't have touchstones!")
        if template == "Changeling" and not switches:
            self.caller.db.touchstones['Changeling'] = args
            self.caller.msg('Changeling touchstone set to ' + args)
        elif template == "Vampire" and not switches:
            self.caller.db.touchstones[lhs] = rhs
            self.caller.msg("Touchstone named " + lhs + " set to " + rhs)
        elif template == "Werewolf" and not switches:
            if lhs.lower() == "phys":
                self.caller.db.touchstones['Physical'] = rhs
                self.caller.msg('Physical touchstoned set to ' + rhs)
            elif lhs.lower() == 'spirit':
                self.caller.db.touchstones['Spiritual'] = rhs
                self.caller.msg('Spiritual touchstone set to ' + rhs)
        elif switches:
            if switches[0] == "del":
                if template == "Vampire" or template == "Werewolf":
                    for key in self.caller.db.touchstones.keys():
                        if key.lower() == "spiritual" and self.args.lower() == "spiritual":
                            del self.caller.db.touchstones[key]
                            self.caller.msg("Spiritual touchstone deleted.")
                            return
                        elif key.lower() == "physical" and self.args.lower() == "physical":
                            del self.caller.db.touchstones[key]
                            self.caller.msg("Physical touchstone deleted.")
                            return
                        elif key.lower() == self.args.lower():
                            del self.caller.db.touchstones[key]
                            self.caller.msg("Touchstone named " + key + " deleted.")
                            return
                elif template == "Changeling":
                    del self.caller.db.touchstones['Changeling']
                    self.caller.msg('Touchstone deleted.')
                    return
                else:
                    self.caller.msg("Your template doesn't have touchstones.")
                    return
            elif switches[0] == "show":
                for key in self.caller.db.touchstones.keys():
                    if key.lower() == lhs.lower():
                        try:
                            searchchar = search.objects(rhs)[0]
                            touchtable = evtable.EvTable(key,header_line_char='-',borders='table')
                            touchtable.width = 39
                            searchchar.msg(self.caller.name + " shows their touchstone to you. Name: " + key + "\n" + str(touchtable))
                            self.caller.msg("You show " + searchchar.name + " your touchstone.")
                            return
                        except IndexError:
                            self.caller.msg("That's not a valid character to show your touchstone to!")
                            return
                        
                
class ApproveChar(Command):
    """
    As one might infer, this command is used to approve and unapprove characters.
    Technically the same bit of code, but nevertheless is used like so.
    
    Syntax:
    +approve <Character> Approve a character, allowing them to spend resources, accrue beats, and go on-grid.
    +unapprove <Character> Unapprove a character, preventing them from going on-grid, spending resources,
    or accruing beats.
    
    Please note that both versions of this command will teleport the targeted character to the OOC nexus.
    This is so that newly approved characters can be kept out of chargen, and that newly unapproved characters
    may be removed from the grid.
    """
    key = "+approve"
    aliases = '+unapprove'
    lock = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        self.args = self.args.lstrip()
        genroom = search.objects('Chargen')[0]
        nexusroom = search.objects('OOC Nexus')[0]
        try:
            appchar = search.objects(self.args)[0]
            
            if appchar.db.approved == False and self.cmdstring == "+approve":
                appchar.db.approved = True
                appchar.db.next_lethal = datetime.datetime.now() + datetime.timedelta(days=2)
                appchar.db.next_agg = datetime.datetime.now() + datetime.timedelta(weeks=1)
                if appchar.has_player:
                    appchar.msg("You have been |050approved|n by " + self.caller.name)
                if appchar.db.template == 'Werewolf':
                    appchar.db.next_lethal = datetime.datetime.now() + datetime.timedelta(days=1)
                    appchar.db.next_agg = datetime.datetime.now() + datetime.timedelta(days=3, hours=12)
                elif appchar.db.template == 'Mortal':
                    for merit in appchar.db.meritlist:
                        if merit[0] == "Biokinesis":
                            appchar.db.next_lethal = datetime.datetime.now() + datetime.timedelta(days=1)
                            appchar.db.next_agg = datetime.datetime.now() + datetime.timedelta(days=3, hours=12)
                elif appchar.db.template == 'Beast':
                    appchar.db.next_sate = datetime.datetime.now() + datetime.timedelta(weeks=1)
                if appchar.location == genroom:
                    appchar.location = nexusroom
                appchar.msg(nexusroom.return_appearance(appchar))
                return
            elif appchar.db.approved == True and self.cmdstring == "+approve":
                self.caller.msg("That character is already approved!")
                return
            elif appchar.db.approved == True and self.cmdstring == "+unapprove":
                appchar.db.approved = False
                if appchar.location == genroom:
                    appchar.location = nexusroom
                if appchar.has_player:
                    appchar.msg("You have been |500unapproved|n by " + self.caller.name)
                    appchar.msg(nexusroom.return_appearance(appchar))
                return
            elif appchar.db.approved == False and self.cmdstring == "+unapprove":
                self.caller.msg("That character is not approved.")
                return
        except IndexError:
            self.caller.msg("Invalid character to approve or unapprove.")
            return
class ICCommand(Command):
    """
    Teleports you to the location you left when using +ooc without a message attached.
    """
    key = "+ic"
    lock = "cmd:attr(approved,True)"
    help_category="OOC"
    def func(self):
        if self.caller.db.oldloc == "":
            self.caller.msg("You've never been IC, so you can't return there.")
            return
        else:
            self.caller.location = self.caller.db.oldloc
            self.caller.msg(self.caller.location.return_appearance(self.caller))
class OOCCommand(default_cmds.MuxCommand):
    """
    Teleports you to the OOC nexus when used alone, when used with text following
    the command it lets you speak on an out of character basis while in-character.
    
    Usage:
        +ooc [<Message>]
    """
    key = "+ooc"
    lock = "cmd:attr(approved,True)"
    help_category="OOC"
    def func(self):
        if self.args == "":
            self.caller.db.oldloc = self.caller.location
            self.caller.location = search.objects("OOC Nexus")[0]
            self.caller.msg(self.caller.location.return_appearance(self.caller))
            return
        else:
            self.args = self.args.lstrip()
            self.caller.location.msg_contents("|244<OOC>|n " + self.caller.name + " says, \""+self.args+"\"")
class Shift(default_cmds.MuxCommand):
#A multi-descer and multi-statter all in one. Used by characters that can assume more than one form easily.
    """
    A command used to shift between the multiple forms werewolves have. Any description set on yourself in a given form
    will be saved for the next time you shift to that form, and likewise shifting to hishu form will revert you to your
    human description.
    
    Syntatx:
    
    +shift <Hishu/Dalu/Gauru/Urshu/Urhan>
    """
    key = "+shift"
    lock = "cmd:attr(template,'Werewolf')"
    dalustats = ["Strength,+1","Stamina,+1","Manipulation,-1","Size,+1"]
    gaurustats = ["Strength,+3","Dexterity,+1","Stamina,+2","Size,+2"]
    urshulstats = ["Strength,+2","Dexterity,+2","Stamina,+2","Size,+1","Speed,+3","Manipulation,-1"]
    urhanstats = ["Dexterity,+2","Stamina,+1","Manipulation,-1","Size,-1","Speed,+3"]
    help_category="Gameplay"
    def func(self):
        caller = self.caller
        template = caller.db.template.db.template
        if template.name == "Werewolf":
            if self.args.lower() == "hishu":
                if template.currentform == "Hishu":
                    self.caller.msg("You are already in your human form!")
                else:
                    self.StoreOld(template.currentform)
                    caller.db.desc = template.humandesc
                    if template.currentform == "Dalu":
                        template.attributes['Strength'] -= 1
                        template.attributes['Stamina'] -= 1
                        template.attributes['Manipulation'] += 1
                        template.size -= 1
                    elif template.currentform == "Gauru":
                        template.attributes['Strength'] -= 3
                        template.attributes['Dexterity'] -= 1
                        template.attributes['Stamina'] -= 2
                        template.attributes['Manipulation'] += 1
                        template.size -= 2
                    elif template.currentform == "Urshul":
                        template.attributes['Strength'] -= 2
                        template.attributes['Dexterity'] -= 2
                        template.attributes['Stamina'] -= 2
                        template.attributes['Manipulation'] += 1
                        template.size -= 1
                        template.speed_bonus -= 3
                    elif template.currentform == "Urhan":
                        template.attributes['Dexterity'] -= 2
                        template.attributes['Stamina'] -= 1
                        template.attributes['Manipulation'] += 1
                        template.size += 1
                        template.speed_bonus -= 3
                    template.currentform = "Hishu"
                    for character in caller.location.contents:
                        if character.player:
                            character.msg(caller.name + " shifts into "+caller.pronoun+" human form!")
            elif self.args.lower() == "dalu":
                if template.currentform == "Dalu":
                    self.caller.msg("You are already in dalu form!")
                else:
                    self.StoreOld(template.currentform)
                    caller.db.desc = template.daludesc
                    if template.currentform == "Hishu":
                        template.attributes['Strength'] += 1
                        template.attributes['Stamina'] += 1
                        template.attributes['Manipulation'] -= 1
                        template.size += 1
                    elif template.currentform == "Gauru":
                        template.attributes['Strength'] -= 2
                        template.attributes['Dexterity'] -= 1
                        template.attributes['Stamina'] -= 1
                        template.size -= 2
                    elif template.currentform == "Urshul":
                        template.attributes['Strength'] -= 1
                        template.attributes['Dexterity'] -= 1
                        template.attributes['Stamina'] -= 1
                        template.speed_bonus -= 3
                    elif template.currentform == "Urhan":
                        template.attributes['Strength'] += 1
                        template.attributes['Dexterity'] -= 1
                        template.size += 2
                        template.speed_bonus -= 3
                    template.currentform = "Dalu"
                    for character in caller.location.contents:
                        if character.player:
                            character.msg(caller.name + " shifts into dalu form!")
            elif self.args.lower() == "gauru":
                if template.currentform == "Gauru":
                    self.caller.msg("You are already in gauru form!")
                else:
                    self.StoreOld(template.currentform)
                    caller.db.desc = template.gaurudesc
                    if template.currentform == "Hishu":
                        template.attributes['Strength'] += 3
                        template.attributes['Dexterity'] += 1
                        template.attributes['Stamina'] += 2
                        template.size += 2
                    elif template.currentform == "Dalu":
                        template.attributes['Strength'] += 2
                        template.attributes['Dexterity'] += 1
                        template.attributes['Stamina'] += 1
                        template.attributes['Manipulation'] += 1
                        template.size += 1
                    elif template.currentform == "Urshul":
                        template.attributes['Strength'] += 1
                        template.attributes['Dexterity'] -= 1
                        template.attributes['Manipulation'] += 1
                        template.size += 1
                        template.speed_bonus -= 3
                    elif template.currentform == "Urhan":
                        template.attributes['Strength'] -= 3
                        template.attributes['Dexterity'] += 1
                        template.attributes['Stamina'] -= 1
                        template.attributes['Manipulation'] -= 1
                        template.speed_bonus -= 3
                    template.currentform = "Gauru"
                    for character in caller.location.contents:
                        if character.player:
                            character.msg(caller.name + " shifts into gauru form!")
            elif self.args.lower() == "urshul":
                if template.currentform == "Urshul":
                    self.caller.msg("You are already in urshul form!")
                else:
                    if template.currentform == "Hishu":
                        template.attributes['Strength'] += 2
                        template.attributes['Dexterity'] += 2
                        template.attributes['Stamina'] += 2
                        template.attributes['Manipulation'] -= 1
                        template.size += 1
                        template.speed_bonus -= 3
                    elif template.currentform == "Dalu":
                        template.attributes['Strength'] += 1
                        template.attriubtes[4] += 2
                        template.attributes['Stamina'] += 1
                        template.speed_bonus += 3
                    elif template.currentform == "Gauru":
                        template.attributes['Strength'] -= 1
                        template.attributes['Dexterity'] += 1
                        template.attributes['Manipulation'] -= 1
                        template.speed_bonus += 3
                        template.size -= 1
                    elif template.currentform == "Urhan":
                        template.attributes['Strength'] += 2
                        template.attributes['Stamina'] += 1
                        template.size += 2
                    self.StoreOld(template.currentform)
                    caller.db.desc = template.urshuldesc
                    template.currentform = "Urshul"
                    for character in caller.location.contents:
                        if character.player:
                            character.msg(caller.name + " shifts into urshul form!")
            elif self.args.lower() == "urhan":
                if template.currentform == "urhan":
                    self.caller.msg("You are already in your wolf form!")
                else:
                    self.StoreOld(template.currentform)
                    if template.currentform == "Hishu":
                        template.attributes['Dexterity'] += 2
                        template.attributes['Stamina'] += 1
                        template.attributes['Manipulation'] -= 1
                        template.size -= 1
                        template.speed_bonus += 3
                    elif template.currentform == "Dalu":
                        template.attributes['Strength'] -= 1
                        template.attributes['Dexterity'] += 2
                        template.size -= 2
                        template.speed_bonus += 3
                    elif template.currentform == "Gauru":
                        template.attributes['Strength'] -= 3
                        template.attributes['Dexterity'] += 1
                        template.attributes['Stamina'] -= 1
                        template.attributes['Manipulation'] -= 1
                        template.size -= 3
                        template.speed_bonus += 3
                    elif template.currentform == "Urshul":
                        template.attributes['Strength'] -= 2
                        template.attributes['Stamina'] -= 1
                        template.size -= 2
                    caller.db.desc = template.urhandesc
                    self.currentform = "Urhan"
                    for character in caller.location.contents:
                        if character.player:
                            character.msg(caller.name + " shifts into "+caller.pronoun+" wolf form!")
            template.Update()
    def StoreOld(self, oldform):
        caller = self.caller
        template = caller.db.template.db.template
        if oldform == "Hishu":
            template.humandesc = caller.db.desc
        elif oldform == "Dalu":
            template.daludesc = caller.db.desc
        elif oldform == "Gauru":
            template.daludesc = caller.db.desc
        elif oldform == "Urshul":
            template.urshuldesc = caller.db.desc
        elif oldform == "Urhan":
            template.urhandesc = caller.db.desc
class SetPosition(default_cmds.MuxCommand):
    """
    Used to set your position, describing what exactly you do as a staffer.
    """
    key = "+position"
    lock = "cmd:pperm(Wizards)"
    help_category = "Admin"
    def func(self):
        self.caller.player.db.position = self.args
        self.caller.msg("Staff position set to " + self.args)
        return
class Sheet(default_cmds.MuxCommand):
    """
    Used to view your statistics. Only administrators may view sheets others than their own.
    """
    key="+sheet"
    lock="cmd:all()"
    def func(self):
        arglist = self.arglist
        if(arglist):
        #Checks to see if you're trying to view someone else's sheet, by way of passing an argument.
            if self.caller.locks.check_lockstring(self.caller, "cmd:perm(Wizards)"):
            #Checks to see if you're a wizard or higher. Unlike on some other games, immortals outrank wizards rather than the other way around. There is no equivalent to a MUSH's
            #royalty rank.
                self.Sheet_Display(search.objects(arglist[0])[0])
                #Calls a sheet display method on the first item in the search for the first argument you pass.
            else:
                self.Sheet_Display(self.caller)
                #But if you're not a wizard, it just displays your own sheet.
        else:
            self.Sheet_Display(self.caller)
            #Also displays a sheet if no argument is passed.
    def Sheet_Display(self, target):
        color = "444"
        if target.db.template == "Vampire" or target.db.template == "Ghoul":
            color = "300"
        elif target.db.template == "Werewolf" or target.db.template == "Wolfblood":
            color = "320"
        elif target.db.template == "Mage" or target.db.template == "Proximus":
            color = "235"
        elif target.db.template == "Changeling" or target.db.template == "Fae-Touched":
            color = "030"
        elif target.db.template == "Demon" or target.db.template == "Stigmatic":
            color = "223"
        elif target.db.template == "Mummy":
            color = "330"
        elif target.db.template == "Promethean":
            color = "313"
        elif target.db.template == "Hunter":
            color = "121"
        elif target.db.template == "Beast":
            color = "212"
        mortalplus = ["Ghoul","Wolfblood","Proximus","Fae-Touched","Hunter"]
        supernatural = ["Vampire","Werewolf","Mage","Changeling","Beast","Demon","Mummy","Promethean"]
        outputstring = ""
        profiletable = evtable.EvTable('Profile',border='table',header_line_char='-')
        profiletable.width = 78
        
        dob = datetime.date(1900, target.db.dob_month,1).strftime("%b") + " " + str(target.db.dob_day) + " " + str(target.db.dob_year)
        profilerow1 = ["Full Name: "+str(target.db.icname),"Template: "+target.db.template,"Concept: "+str(target.db.concept)]
        profilerow2 = ["Date of Birth: "+dob, target.db.demeanorname+": "+target.db.demeanor,target.db.naturename+": "+target.db.nature]
        profiletable.add_row(*profilerow1)
        profiletable.add_row(*profilerow2)
        profilerow3 = []
        profilerow4 = []
        if target.db.template in mortalplus:
            if target.db.template == "Proximus" or target.db.template == "Fae-Touched" or target.db.template == "Hunter":
                profilerow3.append(target.db.xsplatname+": "+target.db.xsplat)
                if target.db.template == "Fae-Touched" or target.db.template == "Proximus" or target.db.template == "Ghoul":
                    profilerow3.append(target.db.ysplatname+": "+target.db.ysplat)
        elif target.db.template in supernatural:
            profilerow3.append(target.db.xsplatname+": "+target.db.xsplat)
            profilerow3.append(target.db.ysplatname+": "+target.db.ysplat)
            if target.db.template != "Beast" and target.db.template != "Demon":
                profilerow3.append(target.db.zsplatname+": "+target.db.zsplat)
                if target.db.template == "Changeling":
                    profilerow4.append("Kith: "+target.db.kith)
        profiletable.add_row(*profilerow3)
        if len(profilerow4) != 0:
            profiletable.add_row(*profilerow4)
        profiletable.reformat(corner_top_left_char="/",corner_top_right_char="\\")
        outputstring += str(profiletable).replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n").replace("/","|" + color + "/|n").replace("\\","|" + color + "\\|n")
        attribtable = evtable.EvTable('Attributes',border='table',header_line_char='-')
        attribrow = []
        for x in range(1,4):
            attribrow.append(self.attribparse(x, target))
        for y in attribrow:
            attribtable.add_row(*y)
        attribtable.width=78
        outputstring += "\n" + str(attribtable)[79:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        skillrow = []
        for y in range(1,9):
            skillrow.append(self.skillparse(y, target))
        skilltable = evtable.EvTable('Skills',border='table',header_line_char='-')
        for z in skillrow:
            skilltable.add_row(*z)
        skilltable.width = 78
        outputstring += str(skilltable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        speclist = []
        if target.db.specialties:
            spectable = evtable.EvTable('Specialties',border='table',header_line_char='-')
            spectable.width=78
            for spec in target.db.specialties.keys():
                speclist.append(spec +" ("+target.db.specialties[spec]+")")
                if (target.db.specialties.keys().index(spec) + 1) % 3 == 0 or spec == target.db.specialties.keys()[len(target.db.specialties.keys) - 1]:
                    spectable.add_row(*speclist)
                    speclist = []
            outputstring += str(spectable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        merittable = evtable.EvTable('Merits',border='table',header_line_char='-')
        merittable.width = 78
        if target.db.meritlist != []:
            for meritcheck in target.db.meritlist:
                if meritcheck[0] == "None":
                    continue
                try:
                    merittable.add_row(meritcheck[0]+" ("+meritcheck[2]+")"+": "+meritcheck[1])
                except IndexError:
                    merittable.add_row(meritcheck[0]+": "+meritcheck[1])
            if len(target.db.meritlist) > 0:
                outputstring += str(merittable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        powerlist = []
        powertable = evtable.EvTable(target.db.powername,border='table',header_line_char='-')
        powertable.width=78
        if target.db.template != "Mortal":
            if len(target.db.powers) != 0:
                for power in target.db.powers.keys():
                    if self.IsInt(target.db.powers[power]):
                        if int(target.db.powers[power]) == 0:
                            powerlist.append(power)
                        else:
                            powerlist.append(power+": "+target.db.powers[power])
                    else:
                        powerlist.append(power+": "+target.db.powers[power])
                    if power == target.db.powers.keys()[len(target.db.powers.keys()) - 1] or (target.db.powers.keys().index(power) + 1) % 3 == 0:
                        powertable.add_row(*powerlist)
                        powerlist = []
        if len(target.db.powers.keys()) != 0 and target.db.template != "Mortal":
            outputstring += str(powertable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        techlist = []
        techtable = evtable.EvTable(target.db.techname,border='table',header_line_char='-')
        techtable.width=78
        if target.db.techname != "":
            if len(target.db.techniquelist) != 0:
                for tech in target.db.techniquelist:
                    if not "," in tech:
                        techlist.append(tech)
                    else:
                        techlist.append(tech.split(",")[0] + ": " + tech.split(",")[1])
                    if tech == target.db.techniquelist[len(target.db.techniquelist) - 1] or (target.db.techniquelist.index(tech) + 1) % 3 == 0:
                        techtable.add_row(*techlist)
                        techlist = []
        if len(target.db.techniquelist) != 0:
            outputstring += str(techtable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        miscstats = target.db.miscstats
        misclist = []
        misctable = evtable.EvTable(target.db.miscname,border='table',header_line_char='-')
        misctable.width=78
        if len(miscstats) > 0:
            for misc in miscstats:
                if misc.split(",")[1] == "0":
                    misclist.append(misc.split(",")[0])
                else:
                    misclist.append(misc)
                if misc == miscstats[len(miscstats) - 1] or (miscstats.index(misc) + 1) % 3 == 0:
                    misctable.add_row(*misclist)
                    misclist= []
        if len(miscstats) != 0:
            outputstring += str(misctable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        condblock = []
        condtable = evtable.EvTable('Conditions',border='table',header_line_char='-')
        tilttable = evtable.EvTable('Tilts',border='table',header_line_char='-')
        tilttable.width=78
        condtable.width=78
        if len(target.db.conditions) > 0 or len(target.db.tilts) > 0:
            for cond in target.db.conditions:
                condblock.append(cond)
                if cond == target.db.conditions[len(target.db.conditions) - 1] or (target.db.conditions.index(cond) + 1) % 3 == 0:
                    condtable.add_row(*condblock)
                    condblock = []
            for tilt in self.caller.db.tilts:
                condblock.append(tilt + " (Tilt)")
                if cond == target.db.tilts[len(target.db.tilts) - 1] or (target.db.conditions.index(tilt) + 1) % 3 == 0:
                    tilttable.add_row(*condblock)
                    condblock = []
            if len(target.db.conditions) > 0 and len(target.db.tilts) > 0:
                outputstring += str(condtable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n") + "\n" + str(tilttable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
            elif len(target.db.conditions) > 0:
                outputstring += str(condtable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
            elif len(target.db.tilts) > 0:
                outputstring += str(tilttable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        powerstring = ""
        poolstring = ""
        notdreamer = True
        notpsyvamp = True
        willstring = ""
        vitals1 = []
        vitals2 = []
        vitals3 = []
        vitals4 = []
        vitaltable = evtable.EvTable('Vitals',border='table',header_line_char='-')
        poollist = []
        if target.db.template in supernatural:
            powerstring = target.db.powerstatname + ": " + str(target.db.powerstat)
            poolkeys = target.db.pools.keys()
            if target.db.template != "Mummy" and target.db.template != "Beast":
                poolstring = target.db.pools.keys()[0] + ": " + str(target.db.pools[target.db.pools.keys()[0]].split(",")[0]) + "/" + str(target.db.pools[target.db.pools.keys()[0]].split(",")[1])
                willstring = target.db.pools.keys()[1] + ": " + target.db.pools[target.db.pools.keys()[1]].split(",")[0] + "/" + target.db.pools[target.db.pools.keys()[1]].split(",")[1]
            elif target.db.template == "Mummy":
                poolkeys.sort()
                poollist.append(poolkeys[0] + ": " + str(target.db.pools[poolkeys[0]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[0]].split(",")[1]) )
                poollist.append(poolkeys[1] + ": " + str(target.db.pools[poolkeys[1]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[1]].split(",")[1]))
                poollist.append(poolkeys[2] + ": " + str(target.db.pools[poolkeys[2]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[2]].split(",")[1]))
                poollist.append(poolkeys[3] + ": " + str(target.db.pools[poolkeys[3]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[3]].split(",")[1]))
                poollist.append(poolkeys[4] + ": " + str(target.db.pools[poolkeys[4]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[4]].split(",")[1]))
                willstring = poolkeys[5] + ": " + target.db.pools[poolkeys[5]].split(",")[0] + "/" + target.db.pools[poolkeys[5]].split(",")[1]
            elif target.db.template == "Beast":
                willstring = poolkeys[0] + ": " + target.db.pools[poolkeys[0]].split(",")[0] + "/" + target.db.pools[poolkeys[0]].split(",")[1]
        else:
            poolkeys = target.db.pools.keys()
            if len(target.db.meritlist) > 0:
                for merits in target.db.meritlist:
                    if merits[0] == "Psychic Vampirism":
                        notpsyvamp = False
                    if merits[0] == "Subliminal Conditioning":
                        notdreamer = False
                if notpsyvamp and notdreamer:
                    if target.db.template == "Ghoul" or target.db.template == "Fae-Touched" or target.db.template == "Proximus":
                        poolstring = poolkeys[1] + "," + str(target.db.pools[poolkeys[1]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[1]].split(",")[1])
                    willstring = target.db.pools.keys()[0] + ": " + target.db.pools[target.db.pools.keys()[0]].split(",")[0] + "/" + target.db.pools[target.db.pools.keys()[0]].split(",")[1]
                else:
                    poolstring = poolkeys[1] + "," + str(target.db.pools[poolkeys[1]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[1]].split(",")[1])
                    willstring = target.db.pools.keys()[0] + ": " + target.db.pools[target.db.pools.keys()[0]].split(",")[0] + "/" + target.db.pools[target.db.pools.keys()[0]].split(",")[1]
            else:
                if target.db.template == "Ghoul" or target.db.template == "Fae-Touched" or target.db.template == "Proximus":
                    poolstring = poolkeys[1] + ": " + str(target.db.pools[poolkeys[1]]).split(",")[0] + "/" + str(target.db.pools[poolkeys[1]].split(",")[1])
                willstring = target.db.pools.keys()[0] + ": " + target.db.pools[target.db.pools.keys()[0]].split(",")[0] + "/" + target.db.pools[target.db.pools.keys()[0]].split(",")[1]
        vitals1.extend(["Initiative: "+str(target.db.initiative),"Speed: "+str(target.db.speed),"Defense: "+str(target.db.defense)])
        vitaltable.add_row(*vitals1)
        vitals2.append("Size: "+str(target.db.size))
        vitals2.append(willstring)
        if target.db.template in supernatural or notdreamer == False or notpsyvamp == False or target.db.template == "Ghoul" or target.db.template == "Fae-Touched" or target.db.template == "Proximus":
            if target.db.template in supernatural:
                vitals2.append(powerstring)
                vitaltable.add_row(*vitals2)
            if target.db.template != "Mummy":
                vitals3.append(poolstring)
                vitals3.append(target.db.sanityname + ": " + str(target.db.sanity))
                vitaltable.add_row(*vitals3)
            else:
                vitals3.extend(poollist[0:2])
                vitals4.extend(poollist[3:4])
                vitaltable.add_row(*vitals3)
                vitals4.append(target.db.sanityname + ": " + str(target.db.sanity))
                vitaltable.add_row(*vitals4)
        else:
            vitals2.append(target.db.sanityname + ": " + str(target.db.sanity))
            vitaltable.add_row(*vitals2)
        healthstring = ""
        for x in target.db.health_track:
            if int(x) == 0:
                healthstring += "[_]"
            elif int(x) == 1:
                healthstring += "[/]"
            elif int(x) == 2:
                healthstring += "[X]"
            elif int(x) == 3:
                healthstring += "[*]"
        vitaltable.width=78
        outputstring += str(vitaltable)[78:len(str(vitaltable)) - 78].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        healthrow = evtable.EvTable('Health: '+healthstring,border='cols',header=False)
        healthrow.width=78
        outputstring += str(healthrow).replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n")
        soctable = evtable.EvTable(border='table',header=False,width=78)
        soctable.add_row('Experience: ' + str(target.db.beats/5) +", and " + str(target.db.beats%5) + " beats","Visibility: " + str(target.db.visibility),'Weekly Downtime: ' + str(target.db.downtime) + "/25")
        soctable.reformat(corner_bottom_left_char="\\",corner_bottom_right_char="/")
        outputstring += str(soctable)[78:].replace("|","|" + color + "|||n").replace("-","|"+color+"-|n").replace("+","|"+color+"+|n").replace("\\","|" + color + "\\|n").replace("-|n/","|" + color + "-/|n")
        self.caller.msg(outputstring)
    def VarExists(self, var):
        try:
            var
            return True
        except NameError:
            return False
    def IsInt(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    def skillparse(self, row, target):
        skill_1 = (row - 1)
        mentskills = target.db.mentskills
        mentkeys = mentskills.keys()
        physskills = target.db.physskills
        physkeys = physskills.keys()
        socskills = target.db.socskills
        sockeys = socskills.keys()
        stringlist = []
        score1 = ""
        score2 = ""
        score3 = ""
        if mentskills[mentkeys[skill_1]] > 0:
            score1 = mentskills[mentkeys[skill_1]]
        stringlist.append(mentkeys[skill_1] +": "+str(score1))
        if physskills[physkeys[skill_1]] > 0:
            score2 = physskills[physkeys[skill_1]]
        stringlist.append(physkeys[skill_1] +": "+str(score2))
        if socskills[sockeys[skill_1]] > 0:
            score3 = socskills[sockeys[skill_1]]
        stringlist.append(sockeys[skill_1]+": "+str(score3))
        return stringlist
    def attribparse(self, row2, target):
        attrib1 = (row2 - 1)
        attrib2 = (row2 + 2)
        attrib3 = (row2 + 5)
        attributes = target.db.attributes
        attribkeys = attributes.keys()
        attribbase = target.db.attribbase
        attribfinal = []
        attribscore1 = str(attributes[attribkeys[attrib1]])
        if attributes[attribkeys[attrib1]] != attribbase[attribkeys[attrib1]]:
            attribscore1 += " (" + str(attribbase[attribkeys[attrib1]]) + ")"
        attribfinal.append(attribkeys[attrib1]+": "+attribscore1)
        attribscore2 = str(attributes[attribkeys[attrib2]])
        if attributes[attribkeys[attrib2]] != attribbase[attribkeys[attrib2]]:
            attribscore2 += " (" + str(attribbase[attribkeys[attrib2]]) + ")"
        attribfinal.append(attribkeys[attrib2]+": "+attribscore2)
        attribscore3 = str(attributes[attribkeys[attrib3]])
        if attributes[attribkeys[attrib3]] != attribbase[attribkeys[attrib3]]:
            attribscore3 += " (" + str(attribbase[attribkeys[attrib3]]) + ")"
        attribfinal.append(attribkeys[attrib3]+": "+attribscore3)
        return attribfinal
class FingerCommand(Command):
    key = "+finger"
    locks = "cmd:all()"
    def parse(self):
        self.args = self.args.lstrip()
    def func(self):
        pass
class TimeDesc(default_cmds.MuxCommand):
    """
    Used to set descriptions for particular times of day on the room you're currently in.
    Morning is considered 6 AM to 12 PM, Afternoon 12 PM to 6 PM, Evening 6 PM to 12 AM, and night 12 AM to 6 AM.
    
    Syntax:
    +tdesc/<morning/afternoon/evening/night> <Description>
    """
    key = "+tdesc"
    locks = "cmd:perm(Builders)"
    help_category="Admin"
    def func(self):
        switches = self.switches
        args = self.args
        if switches and args:
            if switches[0] == 'morning':
                self.caller.location.db.morningdesc = self.args
                self.caller.msg('Morning description set to: |/|/' + self.args)
            elif switches[0] == 'afternoon':
                self.caller.location.db.afternoondesc = self.args
                self.caller.msg('Afternoon description set to |/|/' + self.args)
            elif switches[0] == 'evening':
                self.caller.location.db.eveningdesc = self.args
                self.caller.msg('Evening description set to |/|/' + self.args)
            elif switches[0] == 'night':
                self.caller.location.db.nightdesc = self.args
                self.caller.msg('Night description set to |/|/' + self.args)
            else:
                self.caller.msg('Invalid switch.')
                return
        elif not switches:
            self.caller.msg("You have to include a switch to set a given timeframe's description.")
        elif not args:
            self.caller.msg('You need to include a description to set.')
class ShowStaff(Command):
    """
    Lists staff members. Staff are community leaders who help keep the game running.
    """
    key = "+staff"
    def func(self):
        adminlist = []
        poslist = []
        timelist = []
        charlist = DefaultCharacter.objects.filter_family()
        for char in charlist:
            if char.IsPlayerAdmin() and not char.player.db.dark:
                adminlist.append(char.player.name)
                poslist.append(char.player.db.position)
                if not char.has_player:
                    timelist.append(utils.time_format(time.time() - char.player.sessions.get()[0].cmd_last_visible,1))
                else:
                    timelist.append('Currently Connected')
        stafftable = evtable.EvTable("Staff Name","Position","Online",table=[adminlist,poslist,timelist],width=78)
        self.caller.msg(str(stafftable))
class Hide(Command):
    """
    This command toggles hiding on and off. Hidden staff members do not show up on room appearances, nor do they
    leave messages when moving from place to place.
    """
    key = "+hide"
    lock = "cmd:pperm(Wizards)"
    help_category = "Admin"
    def func(self):
        if not self.caller.player.db.dark:
            self.caller.player.db.dark = True
            self.caller.msg("You are now hidden.")
            return
        if self.caller.player.db.dark == True:
            self.caller.player.db.dark = False
            self.caller.msg("You are now unhidden.")
            return
        if self.caller.player.db.dark == False:
            self.caller.player.db.dark = True
            self.caller.msg("You are now hidden.")
            return 
class TOS(Command):
    """
    Used to agree to the game's terms of service when first logging on to the game.
    """
    key = "+tos"
    lock = "cmd:attr(tos_agreed,False)"
    help_category="OOC"
    def func(self):
        tos1_string = ("First, and perhaps foremost. You the player, the person sitting in front of the computer, must be at least eighteen years of age to be able to play here."
                        " We do not make a point of showing explicit material but simply due to the nature of Chronicles of Darkness' setting, it can and will happen. By using "
                        "the next command, you signify on a legal basis that you are in fact at least eighteen years of age. |/ |/Input: VERIFIEDGEEZER")
        self.tos2_string = ("Secondly. You must hereby promise not to attempt to subvert, disrupt, hack, or otherwise harm the operation of this server's software. Modification is to only"
                       " be performed with the express consent of headstaff, as a member of staff. Duplication and redistribution is allowed. By entering the next command, you"
                       " agree to not attack the server in any form.|/|/Input: PEACETREATY")
        self.tos3_string = ("Finally, you must give your word to not harass, abuse, or otherwise treat with malice staff or your fellow players. This game can only succeed through"
                       "cooperation. If you wish to resolve matters with another player one on one you may, but must be willing to provide a log of the discussion as recorded during the discussion should the"
                       " situation escalate. Staff is not here to jump on your honest mistakes, nor are we here to play favorites. But if you do in fact try to abuse staff's"
                       " good will, you will be treated as any other breaker of our rules. As an addendum though not a formal rule, we will note that conflict of characters should"
                       " stay between characters, and conflict of players between players in a civil manner. Player characters conflicting is not forbidden, malicious exchanges"
                       " are. To agree to the rule against abuse, please enter the following command.|/|/Input: COMMUNITY")
        if self.caller.db.tos_stage == 0:
            get_input(self.caller,tos1_string,self.stage1)
        if self.caller.db.tos_stage == 1:
            get_input(self.caller,self.tos2_string,self.stage2)
        if self.caller.db.tos_stage == 2:
            get_input(self.caller, self.tos3_string,self.stage3)
    def stage1(self, caller, prompt, callback):
        if callback == "VERIFIEDGEEZER":
            caller.msg("Understood. Please use +tos again to proceed to the next step.")
            caller.db.tos_stage = 1
        else:
            caller.msg("If you meant to confirm, please use +tos again and input, 'VERIFIEDGEEZER' in all caps without apostraphes. Otherwise, we hope you can find a better MU* to play on.")
    def stage2(self, caller, prompt, callback):
        if callback == "PEACETREATY":
            caller.msg("Thank you for agreeing not to harm the server. Use +tos once more to proceed to the final step.")
            caller.db.tos_stage = 2
        else:
            caller.msg("If you meant to confirm, please use +tos again and input, 'PEACETREATY' in all caps without apostraphes during the second step. If you did not, we do not condone malicious abuse "
                       "of others' software.")
    def stage3(self, caller, prompt, callback):
        if callback == "COMMUNITY":
            caller.msg("Thank you. Cooperation is an extremely important virtue in community-oriented games.")
            caller.db.tos_agreed = True
        else:
            caller.msg("If you feel the spirit of our restrictions is too great, we apologize. Our intent is not to deter, but to aid cooperation. If you did not mean to disagree,"
                       " please try using +tos again and input, 'COMMUNITY' in all caps without apostraphes next time.")
        
class OpenAll(Command):
    """
    Used to open every sphere and mortal+ merit set coded into the game.
    """
    key = "+openall"
    lock = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        settings.VAMP_STATUS = "Open"
        settings.WOLF_STATUS = "Open"
        settings.MAGE_STATUS = "Open"
        settings.LING_STATUS = "Open"
        settings.HUNTER_STATUS = "Open"
        settings.BEAST_STATUS = "Open"
        settings.PROMETHEAN_STATUS = "Open"
        settings.DEMON_STATUS = "Open"
        settings.MUMMY_STATUS = "Open"
        settings.PSYVAMP_STATUS = "Open"
        settings.ATARIYA_STATUS = "Open"
        settings.DREAMER_STATUS = "Open"
        settings.INFECTED_STATUS = "Open"
        settings.PLAIN_STATUS = "Open"
        settings.LOSTBOYS_STATUS = "Open"
        self.caller.msg("Open Sesame! All spheres are now open. Please note, this may include spheres that are not currently mechanically appropriate for play.")
class OpenSphere(Command):
    """
    Used to open a given sphere to applications, if it was previously restricted or closed.
    
    Usage:
        +opensphere <Sphere>
    """
    key = "+opensphere"
    lock = "cmd:pperm(Wizards)"
    help_category="Admin"
    def parse(self):
        self.args = self.args.strip()
    def func(self):
        if self.args.lower() == "vampire":
            if settings.VAMP_STATUS.lower() != "open":
                self.caller.msg("Vampire sphere opened!")
                settings.VAMP_STATUS = "Open"
                return
            else:
                self.caller.msg("Vampire sphere is already open to applications.")
                return
        if self.args.lower() == "werewolf":
            if settings.WOLF_STATUS.lower() != "open":
                settings.WOLF_STATUS = "Open"
                self.caller.msg("Werewolf sphere opened!")
                return
            else:
                self.caller.msg("Werewolf sphere is already open to applications.")
                return
        if self.args.lower() == "mage":
            if settings.MAGE_STATUS.lower() != "open":
                self.caller.msg("Mage sphere opened!")
                settings.MAGE_STATUS = "Open"
                return
            else:
                self.caller.msg("Mage sphere is already open to applications.")
                return
        if self.args.lower() == "changeling":
            if settings.LING_STATUS.lower() != "open":
                settings.LING_STATUS = "Open"
                self.caller.msg("Changeling sphere opened!")
                return
            else:
                self.caller.msg("Changeling sphere is already open to applications.")
                return
        if "hunter" in self.args.lower():
            if not "/" in self.args:
                if settings.HUNTER_STATUS.lower() != "open":
                    settings.HUNTER_sTATUS = "Open"
                    self.caller.msg("Hunter sphere opened!")
                    return
                else:
                    self.caller.msg("Hunter sphere is already open to applications.")
                    return
            else:
                huntsearch = search.scripts('HunterStats')[0]
                for comp in huntsearch.db.compacts:
                    if comp.lower() == self.args.lower() and comp in huntsearch.db.appfactions:
                        self.caller.msg("That compact is already open for player use.")
                        return
                    elif comp.lower() == self.args.lower():
                        huntsearch.db.appfactions.append(comp)
                        self.caller.msg("The compact, \"" + comp + " has been opened for player use.")
                        return
                for cons in huntsearch.db.conspiracies:
                    if cons.lower() == self.args.lower() and cons in huntsearch.db.appfactions:
                        self.caller.msg("That conspiracy is already open for player use.")
                        return
                    elif cons.lower() == self.args.lower():
                        huntsearch.db.appfactions.append(cons)
                        self.caller.msg("The conspiracy, \"" + cons + " has been opened for player use.")
                        return
                self.caller.msg("Invalid compact or conspiracy to open for play.")
                return
        if self.args.lower() == "beast":
            if settings.BEAST_STATUS.lower() != "open":
                settings.BEAST_STATUS = "Open"
                self.caller.msg("Beast sphere opened!")
                return
            else:
                self.caller.msg("Beast sphere is already open to applications.")
                return
        if self.args.lower() == "promethean":
            if settings.PROMETHEAN_STATUS.lower() != "open":
                settings.PROMETHEAN_STATUS = "Open"
                self.caller.msg("Promethean sphere opened!")
                return
            else:
                self.caller.msg("Promethean spehre is already open to applications.")
                return
        if self.args.lower() == 'atariya':
            if settings.ATARIYA_STATUS.lower() != 'open':
                settings.ATARIYA_STATUS = 'Open'
                self.caller.msg('Atariya merits opened for use.')
                return
            else:
                self.caller.msg('Atariya merits are already open for use.')
                return
        if self.args.lower() == 'dreamer' or self.args.lower() == 'dreamers':
            if settings.DREAMER_STATUS != 'Open':
                settings.DREAMER_STATUS = 'Open'
                self.caller.msg('Dreamer merits opened for use.')
                return
            else:
                self.caller.msg('Dreamer merits are already open for use.')
                return
        if self.args.lower() == 'infected':
            if settings.INFECTED_STATUS != 'Open':
                settings.INFECTED_STATUS = 'Open'
                self.caller.msg('Infected merits opened for use.')
                return
            else:
                self.caller.msg('Infected merits are already open for use.')
        if 'lostboy' in self.args.lower():
            if settings.LOSTBOYS_STATUS != 'Open':
                settings.LOSTBOYS_STATUS = 'Open'
                self.caller.msg('Lost boys merits opened for use.')
                return
            else:
                self.caller.msg('Lost boys merits are already open for use.')
                return
        if 'psychic vampire' in self.args.lower():
            if settings.PSYVAMP_STATUS != "Open":
                settings.PSYVAMP_STATUS = "Open"
                self.caller.msg("Psychic vampire merits opened for use.")
                return
            else:
                self.caller.msg("Psychic vampire merits are already open for use.")
                return
        if 'plain' in self.args.lower():
            if settings.PLAIN_STATUS != 'Open':
                settings.PLAIN_STATUS = 'Open'
                self.caller.msg("The Plain merits opened for use.")
                return
            else:
                self.caller.msg("The merits of The Plain are already open for use.")
                return
        else:
            self.caller.msg("Invalid sphere to open.")
class CloseSphere(Command):
    """
    Used to close a given sphere to new applications. When closed, the +Template command will cease to function for all
    but administrators when making a character. The allowance of administrators to make characters in closed spheres
    is so that NPC characters may be made, not for special treatment.
    
    Syntax:
        +closesphere <Sphere>
    """
    key = "+closesphere"
    lock = "cmd:pperm(Wizards)"
    help_category = "Admin"
    def parse(self):
        self.args = self.args.strip()
    def func(self):
        if self.args.lower() == "vampire":
            if settings.VAMP_STATUS.lower() != "closed":
                settings.VAMP_STATUS = "Closed"
                self.caller.msg("Vampire sphere closed.")
                return
            else:
                self.caller.msg("Vampire sphere is already closed to applications.")
                return
        if self.args.lower() == "werewolf":
            if settings.WOLF_STATUS.lower() != "closed":
                settings.WOLF_STATUS = "Closed"
                self.caller.msg("Werewolf sphere closed.")
                return
            else:
                self.caller.msg("Werewolf sphere already closed to applications.")
                return
        if self.args.lower() == "mage":
            if settings.MAGE_STATUS.lower() != "closed":
                settings.MAGE_STATUS = "Closed"
                self.caller.msg("Mage sphere closed.")
                return
            else:
                self.caller.msg("Mage sphere is already closed to applications.")
                return
        if self.args.lower() == "changeling":
            if settings.LING_STATUS.lower() != "closed":
                settings.LING_STATUS = "Closed"
                self.caller.msg("Changeling sphere closed.")
                return
            else:
                self.caller.msg("Changeling sphere is already closed to applications.")
                return
        if "hunter" in self.args.lower():
            if not "/" in self.args:
                if settings.HUNTER_STATUS.lower() != "closed":
                    settings.HUNTER_STATUS = "Closed"
                    self.caller.msg("Hunter sphere closed.")
                    return
                else:
                    self.caller.msg("Hunter sphere is already closed to applications.")
                    return
            else:
                huntsearch = search.scripts('HunterStats')[0]
                for comp in huntsearch.db.compacts:
                    if comp.lower() == self.args.lower() and comp in huntsearch.db.appfactions:
                        huntsearch.db.appfactions.remove(comp)
                        self.caller.msg("The compact, \"" + comp + " has been closed from player use.")
                        return
                    elif comp.lower() == self.args.lower():
                        self.caller.msg("That compact is not open for player use, no need to close it.")
                        return
                for cons in huntsearch.db.conspiracies:
                    if cons.lower() == self.args.lower() and cons in huntsearch.db.appfactions:
                        huntsearch.db.appfactions.remove(cons)
                        self.caller.msg("The conspiracy, \"" + cons + " has been close from player use.")
                        return
                    elif cons.lower() == self.args.lower():
                        self.caller.msg("That conspiracy is not open for player use, no need to close it.")
                        return
                self.caller.msg("Invalid compact or conspiracy to open for play.")
                return
        if self.args.lower() == "beast":
            if settings.BEAST_STATUS.lower() != "closed":
                settings.BEAST_STATUS = "Closed"
                self.caller.msg("Beast sphere closed")
                return
            else:
                self.caller.msg("Beast sphere is already closed to applications.")
                return
        if self.args.lower() == "promethean":
            if settings.PROMETHEAN_STATUS.lower() != "closed":
                settings.PROMETHEAN_STATUS = "Closed"
                self.caller.msg("Promethean sphere closed.")
                return
            else:
                self.caller.msg("Promethean sphere is already closed to applications.")
                return
        if self.args.lower() == 'atariya':
            if settings.ATARIYA_STATUS.lower() != 'closed':
                settings.ATARIYA_STATUS = 'Closed'
                self.caller.msg('Atariya merits closed.')
                return
            else:
                self.caller.msg('Atariya merits are already closed from being taken.')
                return
        if 'dreamer' in self.args.lower():
            if settings.DREAMER_STATUS != 'Closed':
                settings.DREAMER_STATUS = 'Closed'
                self.caller.msg('Dreamer merits closed.')
                return
            else:
                self.caller.msg('Dreamer merits are already closed from being taken.')
                return
        if self.args.lower() == 'infected':
            if settings.INFECTED_STATUS != 'Closed':
                settings.INFECTED_sTATUS = 'Closed'
                self.caller.msg('Infected merits closed.')
                return
            else:
                self.caller.msg('Infected merits are already closed from being taken.')
                return
        if 'lostboy' in self.args.lower():
            if settings.LOSTBOYS_STATUS != 'Closed':
                settings.LOSTBOYS_STATUS = 'Closed'
                self.caller.msg('Lost boys merits closed.')
                return
            else:
                self.caller.msg('Lost boys merits are already closed from being taken.')
                return
        if 'psychic vampire' in self.args.lower():
            if settings.PSYVAMP_STATUS != 'Closed':
                settings.PSYVAMP_STATUS = 'Closed'
                self.caller.msg('Psychic Vampire merits closed.')
                return
            else:
                self.caller.msg('Psychic Vampire merits are already closed from being taken.')
                return
        self.caller.msg('Invalid sphere to close.')
        return
            
class SphereStatus(Command):
    """
    Shows the status of individual templates. 'Open' means that characters may be applied for
    as normal and only subject to the regular house rules on the website. 'Closed' means that
    no more characters of that type may be applied for. Finally, 'Restricted' means that there
    are special limitations on the sphere at the moment that must be addressed in the character
    creation process individually.
    """
    key = "+spheres"
    lock = "cmd:all()"
    help_category="OOC"
    def func(self):
        statuses = []
        if settings.VAMP_STATUS == "Closed":
            statuses.append("Vampire: |400Closed|n")
        elif settings.VAMP_STATUS == "Open":
            statuses.append("Vampire: |040Open|n")
        elif settings.VAMP_STATUS == "Restricted":
            statuses.append("Vampire: |440Restricted|n")
        else:
            statuses.append("Vampire: |440???|n")
        if settings.WOLF_STATUS == "Closed":
            statuses.append("Werewolf: |400Closed|n")
        elif settings.WOLF_STATUS == "Open":
            statuses.append("Werewolf: |040Open|n")
        elif settings.WOLF_STATUS == "Restricted":
            statuses.append("Werewolf: |440Restricted|n")
        else:
            statuses.append("Werewolf: |440???|n")
        if settings.MAGE_STATUS == "Closed":
            statuses.append('Mage: |400Closed|n')
        elif settings.MAGE_STATUS == "Open":
            statuses.append('Mage: |040Open|n')
        elif settings.MAGE_STATUS == "Restricted":
            statuses.append('Mage: |440Restricted|n')
        else:
            statuses.append('Mage: |440???|n')
        if settings.LING_STATUS == "Closed":
            statuses.append('Changeling: |400Closed|n')
        elif settings.LING_STATUS == "Open":
            statuses.append('Changeling: |040Open|n')
        elif settings.LING_STATUS == "Restricted":
            statuses.append('Changeling: |440Restricted|n')
        else:
            statuses.append('Changeling: |440???|n')
        if settings.BEAST_STATUS == "Closed":
            statuses.append('Beast: |400Closed|n')
        elif settings.BEAST_STATUS == "Open":
            statuses.append('Beast: |040Open|n')
        elif settings.BEAST_STATUS == "Restricted":
            statuses.append('Beast: |440Restricted|n')
        else:
            statuses.append('Beast: |440???|n')
        if settings.HUNTER_STATUS == 'Open':
            statuses.append('Hunter: |040Open|n')
        elif settings.HUNTER_STATUS == 'Closed':
            statuses.append('Hunter: |400Closed|n')
        elif settings.HUNTER_STATUS == 'Restricted':
            statuses.append('Hunter: |440Restricted|n')
        else:
            statuses.append('Hunter: |440???|n')
        if settings.PROMETHEAN_STATUS == 'Open':
            statuses.append('Promethean: |040Open|n')
        elif settings.PROMETHEAN_STATUS == 'Closed':
            statuses.append('Promethean: |400Closed|n')
        elif settings.PROMETHEAN_STATUS == 'Restricted':
            statuses.append('Promethean: |440Restricted|n')
        else:
            statuses.append('Promethean: |440???|n')
        if settings.MUMMY_STATUS == 'Open':
            statuses.append('Mummy: |040Open|n')
        elif settings.MUMMY_STATUS == 'Closed':
            statuses.append('Mummy: |400Closed|n')
        elif settings.MUMMY_STATUS == 'Restricted':
            statuses.append('Mummy: |440Restricted|n')
        else:
            statuses.append('Mummy: |440???|n')
        if settings.DEMON_STATUS == 'Closed':
            statuses.append('Demon: |400Closed|n')
        elif settings.DEMON_STATUS == 'Open':
            statuses.append('Demon: |040Open|n')
        elif settings.DEMON_STATUS == 'Restricted':
            statuses.append('Demon: |440Restricted|n')
        else:
            statuses.append('Demon: |440???|n')
        if settings.ATARIYA_STATUS == 'Open':
            statuses.append('Atariya: |040Open|n')
        elif settings.ATARIYA_STATUS == 'Closed':
            statuses.append('Atariya: |400Closed|n')
        elif settings.ATARIYA_STATUS == 'Restricted':
            statuses.append('Atariya: |440Restricted|n')
        else:
            statuses.append('Atariya: |440???|n')
        if settings.DREAMER_STATUS == 'Open':
            statuses.append('Dreamers: |040Open|n')
        elif settings.DREAMER_STATUS == 'Closed':
            statuses.append('Dreamers: |400Closed|n')
        elif settings.DREAMER_STATUS == 'Restricted':
            statuses.append('Dreamers: |440Restricted|n')
        else:
            statuses.append('Dreamers: |440???|n')
        if settings.INFECTED_STATUS == 'Open':
            statuses.append('Infected: |040Open|n')
        elif settings.INFECTED_STATUS == 'Closed':
            statuses.append('Infected: |400Closed|n')
        elif settings.INFECTED_STATUS == 'Restricted':
            statuses.append('Infected: |440Restricted|n')
        else:
            statuses.append('Infected: |440???|n')
        if settings.LOSTBOYS_STATUS == 'Open':
            statuses.append('Lost Boys: |040Open|n')
        elif settings.LOSTBOYS_STATUS == 'Closed':
            statuses.append('Lost Boys: |400Closed|n')
        elif settings.LOSTBOYS_STATUS == 'Restricted':
            statuses.append('Lost Boys: |440Restricted|n')
        else:
            statuses.append('Lost Boys: |440???|n')
        if settings.PLAIN_STATUS == 'Open':
            statuses.append('The Plain: |040Open|n')
        elif settings.PLAIN_STATUS == 'Closed':
            statuses.append('The Plain: |400Closed|n')
        elif settings.PLAIN_STATUS == 'Restricted':
            statuses.append('The Plain: |440Restricted|n')
        else:
            statuses.append('The Plain: |440???|n')
        if settings.PSYVAMP_STATUS == 'Open':
            statuses.append('PsyVampires: |040Open|n')
        elif settings.PSYVAMP_STATUS == 'Closed':
            statuses.append('PsyVampires: |400Closed|n')
        elif settings.PSYVAMP_STATUS == 'Restricted':
            statuses.append('PsyVampires: |440Restricted|n')
        else:
            statuses.append('PsyVampires: |440???|n')
        SphereBox = StatBlock('Sphere Statuses',False,statuses)
        self.caller.msg(SphereBox.Show() + SphereBox.Footer())
class RestrictSphere(Command):
    key = "+restrict"
    lock = "cmd:pperm(Wizards)"
    def func(self):
        if self.args.lower() == "vampire":
            if settings.VAMP_STATUS == "Restricted":
                self.caller.msg("Vampire sphere is already restricted. No need to change it.")
                return
            else:
                settings.VAMP_STATUS = "Restricted"
                self.caller.msg("Vampire sphere has been set to restricted status.")
                return
class CloseAll(Command):
    """
    Closes all the spheres on the game, save for mortals and psychic merits.
    """
    key = "+closeall"
    lock = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        settings.VAMP_STATUS = "Closed"
        settings.WOLF_STATUS = "Closed"
        settings.MAGE_STATUS = "Closed"
        settings.LING_STATUS = "Closed"
        settings.HUNTER_STATUS = "Closed"
        settings.BEAST_STATUS = "Closed"
        settings.PROMETHEAN_STATUS = "Closed"
        settings.MUMMY_STATUS = "Closed"
        settings.DEMON_STATUS = "Closed"
        settings.PSYVAMP_STATUS = "Closed"
        settings.ATARIYA_STATUS = "Closed"
        settings.DREAMER_STATUS = "Closed"
        settings.INFECTED_STATUS = "Closed"
        settings.PLAIN_STATUS = "Closed"
        settings.LOSTBOYS_STATUS = "Closed"
        self.caller.msg("All spheres closed, only basic mortals and psychics are allowed now.")
        try:
            spherechan = search.channels('Spheres')[0]
            spherechan.msg('All spheres set to |400Closed|n.')
        except IndexError:
            spherechan = create_channel('Spheres',desc='A channel to announce opening, closing, and restricting of spheres.')
            spherechan.msg('All spheres set to |400Closed|n')
            
class Panic(Command):
    """
    This command is something of a joke, but can be useful if the Hunter and Beast spheres
    both are judged too problematic to be kept open at once. That said, this command closes
    both the Hunter and Beast spheres as Hunter can be used as a justification by unscrupulous
    players to PK indiscriminately, and Beast can be used as justification by similarly-minded
    individuals to simply be a jerk across the board.
    """
    key = "+panic"
    lock = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        if settings.BEAST_STATUS != "Closed":
            settings.BEAST_STATUS = "Closed"
        if settings.HUNTER_STATUS != "Closed":
            settings.HUNTER_STATUS = "Closed"
        self.caller.msg("|500BWOOP! BWOOP! BWOOP!|n Panic button engaged, problematic spheres closing!")
        try:
            spherechan = search.channels('Spheres')[0]
            spherechan.msg('Beast sphere |400Closed|n.')
            spherechan.msg('Hunter sphere |400Closed|n.')
        except IndexError:
            spherechan = create_channel('Spheres',desc='A channel to announce opening, closing, and restricting of spheres.')
            spherechan.msg('Beast sphere |400Closed|n.')
            spherechan.msg('Hunter sphere |400Closed|n.')
class Prove(default_cmds.MuxCommand):
    """
    Like on many other games, this command may be used to show that you incontravertibly have
    a given stat at a given level. This can be useful if you need to, as the command name implies,
    prove something.
    
    Syntax:
    
    +prove/effective <Stat> Used to prove effective levels of a stat, such as strength over your natural
    limit granted to you by vigor.
    +prove <Stat> Prove an actual, baseline statistic rather than an effective level.
    """
    key = "+prove"
    lock = "cmd:all()"
    help_category="OOC"
    def func(self):
        provestring = ""
        arglist = self.arglist
        rhs = self.rhs
        switches = self.switches
        vowels = ['a','e','i','o','u']
        if len(arglist) == 0:
            self.caller.msg("You need to enter a stat to prove!")
            return
        if switches == "effective":
            for attribute in self.caller.db.attrstats:
                if attribute.name.lower() == arglist[0].lower():
                    if rhs != "":
                        try:
                            if int(rhs) >= 1:
                                if attribute.effective_score >= int(rhs):
                                    provestring = "PROVE: "+str(self.caller) + " has an effective " + attribute.name.lower() + " of at least " + rhs
                                else:
                                    provestring = "PROVE: "+str(self.caller) + " does not have an effective " + attribute.name.lower() +" of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                            else:
                                self.caller.msg("You can't prove a negative or nonexsitent stat!")
                                return
                        except TypeError:
                            self.caller.msg("Invalid value to prove!")
                            return
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has an effective " + attribute.name + " of " + str(attribute.effective_score)
                        self.caller.location.msg_contents(provestring)
                        return
                if provestring == "":
                    self.caller.msg("Only attributes have effective values!")
                    return
            for character in self.caller.location:
                if character.player:
                    character.msg(provestring)
        if len(switches) == 0:
            for attribute in self.caller.db.attrstats.keys():
                if attribute.lower() == arglist[0].lower():
                    if attribute[0] in vowels:
                        conjunction = "an"
                    else:
                        conjunction = "a"
                    if rhs:
                        try:
                            if int(rhs) >= 1:
                                if attribute.score >= int(rhs):
                                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + attribute + " of at least " + rhs
                                    self.caller.location.msg_contents(provestring)
                                    return
                            else:
                                self.caller.msg("You can't prove a negative value, or a value of zero!")
                                return
                        except ValueError:
                            self.caller.msg("Invalid value to prove.")
                            return
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + attribute + " of " + str(self.caller.db.attrstats[attribute])
                        self.caller.location.msg_contents(provestring)
                        return
            for physskill in self.caller.db.physskills.keys():
                if physskill.lower() == arglist[0].lower():
                    if physskill[0].lower() in vowels:
                        conjunction = "an"
                    else:
                        conjunction = "a"
                    if rhs:
                        try:
                            if int(rhs) >= 1:
                                if self.caller.db.physskills[physskill] >= int(rhs):
                                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + physskill + " of at least " + rhs
                                    self.caller.location.msg_contents(provestring)
                                    return
                            else:
                                self.caller.msg("You can't prove a negative or nonexistent stat!")
                                return
                        except ValueError:
                            self.caller.msg("Invalid value to prove!")
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + physskill + " of " + str(self.caller.db.physskills[physskill])
                        self.caller.location.msg_contents(provestring)
                        return
            for mentskill in self.caller.db.mentskills.keys():
                if mentskill.lower() == arglist[0].lower():
                    if mentskill[0].lower() in vowels:
                        conjunction = "an"
                    else:
                        conjunction = "a"
                    if rhs:
                        try:
                            if int(rhs) >= 1:
                                if self.caller.db.mentskills[mentskill] >= int(rhs):
                                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + mentskill + " of at least " + rhs
                                    self.caller.location.msg_contents(provestring)
                                    return
                            else:
                                self.caller.msg("You can't prove a negative or nonexistent stat!")
                                return
                        except ValueError:
                            self.caller.msg("Invalid value to prove!")
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + mentskill + " of " + str(self.caller.db.mentskills[mentskill])
                        self.caller.location.msg_contents(provestring)
                        return
            for socskill in self.caller.db.socskills.keys():
                if socskill.lower() == self.lhs.lower():
                    if socskill[0].lower() in vowels:
                        conjunction = "an"
                    else:
                        conjunction = "a"
                    if rhs:
                        try:
                            if int(rhs) >= 1:
                                if self.caller.db.socskills[socskill] >= int(rhs):
                                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + socskill + " of at least " + rhs
                                    self.caller.location.msg_contents(provestring)
                                    return
                            else:
                                self.caller.msg("You can't prove a negative or nonexistent stat!")
                                return
                        except ValueError:
                            self.caller.msg("Invalid value to prove!")
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + socskill + " of " + str(self.caller.db.socskills[socskill])
                        self.caller.location.msg_contents(provestring)
                        return
            for merit in self.caller.db.meritlist:
                if merit[0].lower() == arglist[0].lower():
                    if merit[0][0].lower() in vowels:
                        conjunction = "an"
                    else:
                        conjunction = "a"
                    if rhs:
                        try:
                            if int(rhs) >= 1:
                                if int(merit[1]) >= int(rhs):
                                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction +" " + merit[0] +" of at least " + rhs
                                    self.caller.location.msg_contents(provestring)
                                    return
                            else:
                                self.caller.msg("You can't prove a negative or nonexistent stat!")
                                return
                        except ValueError:
                            self.caller.msg("Invalid value to prove!")
                    else:
                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + merit[0] + " of " + merit[1]
                        self.caller.location.msg_contents(provestring)
                        return
            if len(self.caller.db.powers) != 0:
                for power in self.caller.db.powers.keys():
                    if power.lower() == arglist[0].lower():
                        if power[0].lower() in vowels:
                            conjunction = "an"
                        else:
                            conjunction = "a"
                        if rhs:
                            try:
                                if int(rhs) >= 1:
                                    if int(self.caller.db.powers[power]) >= int(rhs):
                                        provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + power + " of at least " + rhs
                                        self.caller.location.msg_contents(provestring)
                                        return
                                else:
                                    self.caller.msg("You can't prove a negative or nonexsitent stat!")
                                    return
                            except ValueError:
                                self.caller.msg("Invalid value to prove!")
                                return
                        else:
                            provestring = "PROVE: " + str(self.caller) + " has " + conjunction + power + " of " + self.caller.db.powers[power]
                            self.caller.location.msg_contents(provestring)
                            return
            if len(self.caller.db.techniquelist) != 0:
                for tech in self.caller.db.techniquelist:
                    if tech.lower() == arglist[0].lower() or tech.lower() == self.args.lower():
                        if tech[0][0].lower() in vowels:
                            conjunction = "an"
                        else:
                            conjunction = "a"
                        provestring = "PROVE: " + str(self.caller) + " has the " + tech[0] + " " + self.caller.db.techname
                        self.caller.location.msg_contents(provestring)
                        return
            if self.lhs.lower() == self.caller.db.sanityname.lower():
                if self.lhs[0].lower() in vowels:
                    conjunction = "an"
                else:
                    conjunction = "a"
                if rhs:
                    try:
                        if int(rhs) >= 1:
                            if self.caller.db.sanity >= int(rhs):
                                provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + self.caller.db.sanityname + " of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                            else:
                                self.caller.msg("You can't prove a negative or nonexistent stat!")
                                return
                    except ValueError:
                        self.caller.msg("Invalid value to prove!")
                        return
                else:
                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " "  + self.caller.db.sanityname  + " of " + str(self.caller.db.sanity)
                    self.caller.location.msg_contents(provestring)
                    return
            if self.lhs.lower() == self.caller.db.powerstatname.lower():
                if self.caller.db.powerstatname[0].lower() in vowels:
                    conjunction = "an"
                else:
                    conjunction = "a"
                if rhs:
                    try:
                        if int(rhs) >= 1:
                            if self.caller.db.powerstat >= int(rhs):
                                provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " " + self.caller.db.powerstatname + " of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                        else:
                            self.caller.msg("You can't prove a negative or nonexistent stat!")
                            return
                    except ValueError:
                        self.caller.msg("Invalid value to prove!")
                        return
                else:
                    provestring = "PROVE: " + str(self.caller) + " has " + conjunction + " "  + self.caller.db.powerstatname  + " of " + str(self.caller.db.powerstat)
                    self.caller.location.msg_contents(provestring)
                    return
            if self.lhs.lower() == "defense":
                if rhs:
                    try:
                        if int(rhs) >= 1:
                            if self.caller.db.defense >= int(rhs):
                                provestring = "PROVE: " + str(self.caller) + " has a defense of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                        else:
                            self.caller.msg("You can't prove a negative or nonexistent stat!")
                            return
                    except ValueError:
                        self.caller.msg("Invalid value to prove!")
                        return
                else:
                    provestring = "PROVE: " + str(self.caller) + " has a defense of " + str(self.caller.db.defense)
                    self.caller.location.msg_contents(provestring)
                    return
            if self.lhs.lower() == "size":
                if rhs:
                    try:
                        if int(rhs) >= 1:
                            if self.caller.db.size >= int(rhs):
                                provestring = "PROVE: " + str(self.caller) + " has a size of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                        else:
                            self.caller.msg("You can't prove a negative or nonexistent stat!")
                            return
                    except ValueError:
                        self.caller.msg("Invalid value to prove!")
                        return
                else:
                    provestring = "PROVE: " + str(self.caller) + " has a size of " + str(self.caller.db.size)
                    self.caller.location.msg_contents(provestring)
                    return
            if self.lhs.lower() == "init" or self.lhs.lower == "initiative":
                if rhs:
                    try:
                        if int(rhs) >= 1:
                            if self.caller.db.initiative >= int(rhs):
                                provestring = "PROVE: " + str(self.caller) + " has an initiative of at least " + rhs
                                self.caller.location.msg_contents(provestring)
                                return
                        else:
                            self.caller.msg("You can't prove a negative or nonexistent stat!")
                            return
                    except ValueError:
                        self.caller.msg("Invalid value to prove!")
                        return
                else:
                    provestring = "PROVE: " + str(self.caller) + " has an initiative of " + str(self.caller.db.initiative)
                    self.caller.location.msg_contents(provestring)
                    return
            if self.lhs[0].lower() in vowels:
                conjunction = "an"
            else:
                conjunction = "a"
            if rhs:
                provestring = "PROVE: " + self.caller.name +" does not have " + conjunction + " " + self.lhs + " of at least" + rhs
            else:
                provestring = "PROVE: " + self.caller.name +" does not have the " + self.lhs + " stat." 
            self.caller.location.msg_contents(provestring)
class SpaceArchMastery(default_cmds.MuxCommand):
    """
    This command is used to teleport to another currently-used character, or bring them to your location.
    
    Syntax:
    +tel <Character name> Used to teleport to that character. Please note, +teleport works as well.
    +pull <Character name> Used to bring another character forcibly to your location. +summon does the same thing.
    """
    key = "+tel"
    aliases = ["+summon","+teleport","+pull"]
    locks = "cmd:perm(Wizards)"
    help_category="Admin"
    def func(self):
        if self.cmdstring == "+summon" or self.cmdstring == "+pull":
            for char in self.arglist:
                try:
                    charsearch = search.objects(char)[0]
                    if charsearch.has_player:
                        self.caller.location.msg(charsearch.name + " is summoned away by " + self.caller.name + "!")
                        charsearch.location = self.caller.location  
                        charsearch.msg(self.caller.location.return_appearance(self.caller))
                        for char in self.caller.location.contents:
                            if char.has_player:
                                char.msg(charsearch.name + " has arrived.")
                except IndexError:
                    continue
        elif self.cmdstring == "+tel" or self.cmdstring == "+teleport":
            self.caller.location.msg(self.caller.name + " teleports away!")
            try:
                charsearch = search.objects(self.arglist[0])[0]
                if charsearch.has_player:
                    self.caller.location = charsearch.location
                    self.caller.msg(self.caller.location.return_appearance(self.caller))
                    for char in self.caller.location.contents:
                            if char.has_player:
                                char.msg(self.caller.name + " has arrived.")
            except IndexError:
                self.caller.msg("No such character!")
                return
class BookRef(default_cmds.MuxCommand):
    """
    This command may be used to look up the vast majority of stats, to find which book they are in.
    If multiple books are given as a result, the merit, power, or what-have-you exists in multiple
    books.
    """
    key = "+bookref"
    lock = "cmd:all()"
    help_category="OOC"
    def func(self):
        switches = self.switches
        args = self.args
        try:
            meritsearch = search.scripts('MeritList')[0]
        except IndexError:
            self.caller.msg("Unable to find the merit index. Please contact staff.")
            return
        try:
            beastsearch = search.scripts('BeastStats')[0]
        except IndexError:
            self.caller.msg("Unable to find beast stat index. Please contact staff.")
            return
        try:
            lingsearch = search.scripts('ChangelingStats')[0]
        except IndexError:
            self.caller.msg("Unable to find changeling stat index. Please contact staff.")
            return
        try:
            demonsearch = search.scripts('DemonStats')[0]
        except IndexError:
            self.caller.msg("Unable to find demon stat index. Please contact staff.")
            return
        try:
            huntsearch = search.scripts('HunterStats')[0]
        except IndexError:
            self.caller.msg("Unable to find hunter stat index. Please contact staff.")
            return
        try:
            mummysearch = search.scripts('MummyStats')[0]
        except IndexError:
            self.caller.msg("Unable to find mummy stat index. Please contact staff.")
            return
        try:
            magesearch = search.scripts('MageStats')[0]
        except IndexError:
            self.caller.msg("Unable to find mage stat index. Please contact staff.")
            return
        try:
            promsearch = search.scripts('PrometheanStats')[0]
        except IndexError:
            self.caller.msg("Unable to find promethean stat index. Please contact staff.")
            return
        try:
            vampsearch = search.scripts('VampireStats')[0]
        except IndexError:
            self.caller.msg("Unable to find vampire stat index. Please contact staff.")
            return
        try:
            wolfsearch = search.scripts('WerewolfStats')[0]
        except IndexError:
            self.caller.msg("Unable to find werewolf stat index. Please contact staff.")
            return
        bookref = []
        booksout = ""
        modpower = demonsearch.db.modifications
        techpower = demonsearch.db.technologies
        proppower = demonsearch.db.propulsion
        procpower = demonsearch.db.processes
        embedpower = demonsearch.db.embeds
        exploitpower = demonsearch.db.exploits
        physmerit = meritsearch.db.physical
        mentmerit = meritsearch.db.mental
        socmerit = meritsearch.db.social
        supermerit = meritsearch.db.supernatural
        fightmerit = meritsearch.db.fighting
        addmerit = meritsearch.db.addons
        luckmerit = meritsearch.db.atariya
        progmerit = meritsearch.db.dreamer
        sickmerit = meritsearch.db.infected
        if not switches and args:
            for phys in physmerit:
                if args.lower() == phys[0].lower():
                    bookref.append(phys[2])
            for ment in mentmerit:
                if args.lower() == ment[0].lower():
                    bookref.append(ment[2])
            for soc in socmerit:
                if args.lower() == soc[0].lower():
                    bookref.append(soc[2])
            for fight in fightmerit:
                if args.lower() == fight[0].lower():
                    bookref.append(fight[2])
            for para in supermerit:
                if args.lower() == para[0].lower():
                    bookref.append(para[2])
            for add in addmerit:
                if args.lower() == add[0].lower():
                    bookref.append(add[2])
            for luck in luckmerit:
                if args.lower() == luck[0].lower():
                    bookref.append(luck[2])
            for prog in progmerit:
                if args.lower() == prog[0].lower():
                    bookref.append(prog[2])
            for sick in sickmerit:
                if args.lower() == sick[0].lower():
                    bookref.append(sick[2])
            for lost in meritsearch.db.lostboy:
                if args.lower() == lost[0].lower():
                    bookref.append(lost[2])
            for peace in meritsearch.db.plain:
                if args.lower() == peace[0].lower():
                    bookref.append(peace[2])
            for psy in meritsearch.db.psyvamp:
                if args.lower() == psy[0].lower():
                    bookref.append(psy[2])
            for add in meritsearch.db.addons:
                if args.lower() == add[0].lower():
                    bookref.append(add[2])
            for vamp in meritsearch.db.vampire:
                if args.lower() == vamp[0].lower():
                    bookref.append(vamp[2])
            for blud in meritsearch.db.ghoul:
                if args.lower() == blud[0].lower():
                    bookref.append(blud[2])
            for were in meritsearch.db.werewolf:
                if args.lower() == were[0].lower():
                    bookref.append(were[2])
            for grr in meritsearch.db.wolfblood:
                if args.lower() == grr[0].lower():
                    bookref.append(grr[2])
            for poof in meritsearch.db.mage:
                if args.lower() == poof[0].lower():
                    bookref.append(poof[2])
            for walk in meritsearch.db.sleepwalker:
                if args.lower() == walk[0].lower():
                    bookref.append(walk[2])
            for ling in meritsearch.db.changeling:
                if args.lower() == ling[0].lower():
                    bookref.append(ling[2])
            for fae in meritsearch.db.faetouched:
                if args.lower() == fae[0].lower():
                    bookref.append(fae[2])
            for rawr in meritsearch.db.beast:
                if args.lower() == rawr[0].lower():
                    bookref.append(rawr[2])
            for fire in meritsearch.db.promethean:
                if args.lower() == fire[0].lower():
                    bookref.append(fire[2])
            for gun in meritsearch.db.hunter:
                if args.lower() == gun[0].lower():
                    bookref.append(gun[2])
            for tut in meritsearch.db.mummy:
                if args.lower() == tut[0].lower():
                    bookref.append(tut[2])
            for hell in meritsearch.db.demon:
                if args.lower() == hell[0].lower():
                    bookref.append(hell[2])
            for claw in beastsearch.db.atavisms:
                if args.lower() == claw[0].lower():
                    bookref.append(claw[2])
            for scare in beastsearch.db.nightmares:
                if args.lower() == scare[0].lower():
                    bookref.append(scare[2])
            for pact in lingsearch.db.contracts:
                if args.lower() == pact[0].lower():
                    bookref.append(pact[3])
            for mod in modpower:
                if args.lower() == mod[0].lower():
                    bookref.append(mod[1])
            for tech in techpower:
                if args.lower() == tech[0].lower():
                    bookref.append(tech[1])
            for prop in proppower:
                if args.lower() == prop[0].lower():
                    bookref.append(prop[1])
            for proc in procpower:
                if args.lower() == proc[0].lower():
                    bookref.append(proc[1])
            for embed in embedpower:
                if args.lower() == embed[0].lower():
                    bookref.append(embed[1])
            for exploit in exploitpower:
                if args.lower() == exploit[0].lower():
                    bookref.append(exploit[1])
            for arm in huntsearch.db.advarmory:
                if args.lower() == arm[0].lower():
                    bookref.append(arm[2])
            for bless in huntsearch.db.benediction:
                if args.lower() == bless[0].lower():
                    bookref.append(bless[1])
            for cast in huntsearch.db.castigation:
                if args.lower() == cast[0].lower():
                    bookref.append(cast[1])
            for chem in huntsearch.db.elixir:
                if args.lower() == chem[0].lower():
                    bookref.append(chem[2])
            for old in huntsearch.db.relic:
                if args.lower() == old[0].lower():
                    bookref.append(old[2])
            for bio in huntsearch.db.thaumatechnology:
                if args.lower() == bio[0].lower():
                    bookref.append(bio[2])
            for tat in huntsearch.db.ink:
                if args.lower() == tat[0].lower():
                    bookref.append(tat[1])
            for aff in mummysearch.db.affinities:
                if args.lower() == aff[0].lower():
                    bookref.append(aff[2])
            for utt in mummysearch.db.utterances:
                if args.lower() == utt[0].lower():
                    bookref.append(utt[3])
            for rote in magesearch.db.rotes:
                if args.lower() == rote[1].lower():
                    bookref.append(rote[4])
            for change in promsearch.db.transmutations:
                if args.lower() == change[0].lower():
                    bookref.append(change[6])
            for disc in vampsearch.db.disciplines:
                if args.lower() == disc[0].lower():
                    bookref.append(disc[2])
            for dev in vampsearch.db.devotions:
                if args.lower() == dev[0].lower():
                    bookref.append(dev[1])
            for theb in vampsearch.db.theban_rituals:
                if args.lower() == theb[0].lower():
                    bookref.append(theb[2])
            for cru in vampsearch.db.cruac_rituals:
                if args.lower() == cru[0].lower():
                    bookref.append(cru[2])
            for sca in vampsearch.db.scales:
                if args.lower() == sca[0].lower():
                    bookref.append(sca[3])
            for gift in wolfsearch.db.gifts:
                if args.lower() == gift[0].lower():
                    bookref.append(gift[1])
            for rite in wolfsearch.db.rites:
                if args.lower() == rite[0].lower():
                    bookref.append(rite[3])
            for tell in wolfsearch.db.tells:
                if args.lower() == tell[0].lower():
                    bookref.append(tell[1])
        for reference in bookref:
            for shorthand in meritsearch.db.bookshort:
                if re.sub('-[0-9]*$','',reference) == shorthand:
                    booksout += meritsearch.db.booklong[meritsearch.db.bookshort.index(shorthand)] + " page " + reference.split("-")[1]
                    if reference != bookref[len(bookref) - 1]:
                        booksout += "\n"
        self.caller.msg(booksout)
class OOCMasq(Command):
    """
    This command is used to opt-in to the OOC masquerade, labeling your character on the website
    as 'Supernatural' or, 'Mortal+' rather than the specific kind of supernatural creature or
    paramortal creature you are.
    """
    key = "+masq"
    lock = "cmd:all()"
    help_category="OOC"
    def func(self):
        try:
            if self.caller.db.masquerade == False:
                self.caller.db.masquerade = True;
                self.caller.msg("OOC Masquerade enabled.")
                return
            else:
                self.caller.db.masquerade = False
                self.caller.msg("OOC Masquerade disabled.")
                return
        except AttributeError:
            self.caller.db.masquerade = True;
            self.caller.msg("OOC Masquerade enabled.")
            return
class Roll(default_cmds.MuxCommand):
    """
    Used to roll a given statistic.
    
    Usage:
        +roll[/<switches>] <Stat A> + [<Stat B>] + [<Further stats or modifiers>]
    Switches:
        8 or 9: Roll with 8-again or 9-again. If multiple are used, the greater will apply.
        X: Roll without 10-again
        Weak: Roll without 10-again, and 1s subtract from successes.
        Rote: All dice that come up failures are rerolled once.
        Advanced: You roll twice and take the better of the two results.
        Private: Roll only to yourself.
        
        Rote and 8-again cannot be used together, only the best of 8-again, 9-again,
        and rote will apply.
    """
    key = "+roll"
    lock="cmd:all()"
    dicepool = 0
    help_category="Gameplay"
    def func(self):
        dicepool = self.dicepool
        user = self.caller
        highmod = 0
        switches = self.switches
        othermods = []
        results = []
        stringout = ""
        arglist = self.arglist
        namestring = ""
        modifier = "Add"
        successes2 = 0
        results2 = []
        resultstring = ""
        for x in switches:
            if x.lower() == "rote":
                highmod = "Rote"
            if x == "8":
                if highmod != "Rote":
                    highmod = "8"
            if x == "9":
                if highmod != "Rote" and highmod != "8":
                    highmod = "9"
            if x.lower() == "weak":
                if len(othermods) > 1:
                    for y in othermods:
                        if y == "x":
                            y = "weak"
                        if y == "weak":
                            break
                        else:
                            break
                    if len(othermods) == 1:
                        if othermods[0] == "x":
                            othermods[0] = "weak"
                        else:
                            othermods.add("weak")
                else:
                    othermods = ["weak"]
            if x.lower() == "x":
                if len(othermods) > 1:
                    for y in othermods:
                        if y == "weak":
                            break
                        if y == "x":
                            break
                        else:
                            othermods.add("x")
                if len(othermods) == 1:
                    if othermods[0] == "x" or othermods[0] == "weak":
                        pass
                    else:
                        othermods.add("x")
                else:
                    othermods = ["x"]
            if x.lower() == "advanced":
                if len(othermods) > 1:
                    for y in othermods:
                        if y == "advanced":
                            pass
                        else:
                            othermods.append("advanced")
                if len(othermods) == 1:
                    if othermods[0] == "advanced":
                        pass
                    else:
                        othermods.append("advanced")
                else:
                    othermods.append("advanced")
            if x.lower() == "willpower" or x.lower() == "wp":
                if len(othermods) > 1:
                    for y in othermods:
                        if y == "willpower":
                            pass
                        else:
                            othermods.append("willpower")
                else:
                    othermods.append("willpower")
        for singlearg in arglist:
            for thing in self.caller.db.attribbase.keys():
                if singlearg.lower() == thing.lower():
                    if modifier == "Subtract":
                        dicepool -= self.caller.db.attributes[thing]
                    elif modifier == "Add":
                        dicepool += self.caller.db.attributes[thing]
                    if namestring == "":
                        namestring = "Roll: " + thing
                    else:
                        namestring += " " + thing
                else:
                    pass
            for skill in self.caller.db.mentskills.keys():
                if singlearg.lower() == skill.lower():
                    if self.caller.db.mentskills[skill] == 0:
                        dicepool -= 3
                        if namestring == "":
                            namestring = "Roll: " + skill + " (Untrained)"
                        else:
                            namestring += " "+skill + " (Untrained)"
                    else:
                        if modifier == "Subtract":
                            dicepool -= self.caller.db.mentskills[skill]
                        if modifier == "Add":
                            dicepool += self.caller.db.mentskills[skill]
                        if namestring == "":
                            namestring = "Roll: " + skill
                        else:
                            namestring += " " + skill
            for skill in self.caller.db.physskills.keys():
                if singlearg.lower() == skill.lower():
                    if self.caller.db.physskills[skill] == 0:
                        dicepool -= 1
                        if namestring == "":
                            namestring = "Roll: " + skill + " (Untrained)"
                        else:
                            namestring += " "+skill + " (Untrained)"
                    else:
                        if modifier == "Subtract":
                            dicepool -= self.caller.db.physskills[skill]
                        if modifier == "Add":
                            dicepool += self.caller.db.physskills[skill]
                        if namestring == "":
                            namestring = "Roll: " + skill
                        else:
                            namestring += " " + skill
            for skill in self.caller.db.socskills.keys():
                if singlearg.lower() == skill.lower():
                    if self.caller.db.socskills[skill] == 0:
                        dicepool -= 1
                        if namestring == "":
                            namestring = "Roll: " + skill + " (Untrained)"
                        else:
                            namestring += " "+skill + " (Untrained)"
                    else:
                        if modifier == "Subtract":
                            dicepool -= self.caller.db.socskills[skill]
                        if modifier == "Add":
                            dicepool += self.caller.db.socskills[skill]
                        if namestring == "":
                            namestring = "Roll: " + skill
                        else:
                            namestring += " " + skill
            for merit in self.caller.db.meritlist:
                if singlearg.lower() == merit[0].lower():
                    if modifier == "Subtract":
                        dicepool -= int(merit[1])
                    if modifier == "Add":
                        dicepool += int(merit[1])
                    if namestring == "":
                        namestring = "Roll: " + merit[0]
                    else:
                        namestring += " " + merit[0]
                elif singlearg.lower() == (merit[0].lower() +" (" +merit[2].lower()+")"):
                    if modifier == "Subtract":
                        dicepool -= int(merit[1])
                    if modifier == "Add":
                        dicepool -= int(merit[1])
                    if namestring == "":
                        namestring = "Roll: " + merit[0] + " ("+merit[2]+")"
                    else:
                        namestring += " " + merit[0] + " ("+merit[2]+")"
            for power in self.caller.db.powers.keys():
                if singlearg.lower() == power.lower():
                    if modifier == "Subtract":
                        dicepool -= int(self.caller.db.powers[power])
                    if modifier == "Add":
                        dicepool += int(self.caller.db.powers[power])
                    if namestring == "":
                        namestring = "Roll: " + power
                    else:
                        namestring += " " + power
            if len(self.caller.db.miscstats) != 0:
                for misc in self.caller.db.miscstats:
                    if "," in misc:
                        if singlearg.lower() == misc.split(",")[0]:
                            if modifier == "Subtract":
                                dicepool -= misc.split(",")[1]
                            if modifier == "Add":
                                dicepool -= misc.split(",")[1]
                            if namestring == "":
                                namestring = "Roll: " + misc.split(",")[0]
                            else:
                                namestring += " " + misc.split(",")[0]
                    else:
                        self.caller.msg(misc + " cannot be rolled.")
            if "+" in singlearg and singlearg != "+":   
                oldpos = arglist.index(singlearg)
                temparg = singlearg.split("+")
                arglist.insert(oldpos+2,temparg[0])
                for adder in temparg:
                    if adder == temparg[0]:
                        continue
                    oldpos += 1
                    arglist.insert(oldpos+1,"+")
                    arglist.insert(oldpos+2,adder)
            if "-" in singlearg and singlearg != "-":   
                oldpos = arglist.index(singlearg)
                temparg = singlearg.split("-")
                arglist.insert(oldpos+2,temparg[0])
                for adder in temparg:
                    if adder == temparg[0]:
                        continue
                    oldpos += 1
                    arglist.insert(oldpos+1,"-")
                    arglist.insert(oldpos+2,adder)
                
            try:
                if modifier == "Add":
                    dicepool += int(singlearg)
                if modifier == "Subtract":
                    dicepool -= int(singlearg)
                if namestring == "":
                    namestring = "Roll: " + str(singlearg)
                else:
                    namestring += " " + str(singlearg)
            except ValueError:
                pass
            if singlearg == "+":
                modifier = "Add"
                if(namestring == ""):
                    pass
                else:
                    namestring += " +"
            if singlearg == "-":
                modifier = "Subtract"
                if namestring == "":
                    pass
                else:
                    namestring += " -"
            for char in singlearg:
                splitpoint = 0
                if char == ".":
                    splitpoint = singlearg.index(char)
                    for skill in self.caller.db.skills.keys():
                        if singlearg[0:splitpoint-1] == skill:
                            for specialty in self.caller.db.specialties.keys():
                                if singlearg[splitpoint:len(singlearg)] == specialty:
                                    dicepool += 1
        if "willpower" in othermods:
            dicepool += 3
            namestring += " 3 (Willpower)"
            self.caller.PoolSpend('Willpower',1)
        counter = 0
        rotecount = 0
        successes = 0
        if dicepool >= 1:
            while counter < dicepool:
                result = random.randint(1,10)
                if result == 10 and any(mod == "weak" for mod in othermods) == False and any(mod2 == "x" for mod2 in othermods) == False:
                    counter -= 1
                if result >= 9 and (highmod == "9" or highmod == "8"):
                    counter -= 1
                if result >= 8 and highmod == "8":
                    counter -= 1
                results.append(result)
                counter += 1
            for num in results:
                if num < 8 and highmod == "Rote":
                    rotecount += 1
                if num >= 8:
                    successes += 1
                if num == 1 and any(mod == "weak" for mod in othermods) == True:
                    if successes >= 1:
                        successes -= 1
            counter = 0
            while counter < rotecount:
                result = random.randint(1,10)
                if result >= 8:
                    successes += 1
                    if result == 10:
                        counter -= 1
                results.append(str(result))
                counter += 1
        else:
            counter = 0
            if dicepool <= 0:
                while counter > -1:
                    result = random.randint(1,10)
                    if result == 10 and any(mod == "weak" for mod in othermods) == False and any(mod2 == "x" for mod2 in othermods) == False:
                        counter += 1
                        successes += 1
                    if result == 1 and successes == 0:
                        successes = -1
                    if result == 1 and any(mod == "weak" for mod in othermods):
                        successes -= 1
                    counter -= 1
                    results.append(result)
        if any(mod3.lower() == "advanced" for mod3 in othermods) == True:
            for die in results:
                result2 = random.randint(1,10)
                if result2 == 10 and any(mod == "weak" for mod in othermods) == False and any(mod2 == "x" for mod2 in othermods) == False:
                    counter -= 1
                if result2 >= 9 and (highmod == "9" or highmod == "8"):
                    counter -= 1
                if result2 >= 8 and highmod == "8":
                    counter -= 1
                results2.append(str(result2))
                counter += 1
            for num in results2:
                if num < 8 and highmod == "Rote":
                    rotecount += 1
                if num >= 8:
                    successes2 += 1
                if num == 1 and any(mod == "weak" for mod in othermods) == True:
                    if successes >= 1:
                        successes2 -= 1
            counter = 0
            while counter < rotecount:
                result2 = random.randint(1,10)
                if result >= 8:
                    successes2 += 1
                    if result == 10:
                        counter -= 1
                results2.append(str(result2))
                counter += 1
        results.sort()
        stringout += "/"
        stringout += "-" * 36
        stringout += "Roll"
        stringout += "-" * 36
        stringout += "\\"
        stringout += "\n| "
        tempstring = ""
        for x in results:
            tempstring += str(x) + " "
        namestring += " With: "
        if highmod != 0 and len(othermods) > 0:
            namestring += str(highmod) + ", "
        if len(othermods) == 0 and highmod == 0:
            namestring += "No Modifiers "
        if highmod != 0 and len(othermods) == 0:
            namestring += str(highmod) + " "
        for modifier in othermods:
            if modifier == "weak" and othermods.index(modifier) == len(othermods) - 1:
                namestring += "Weak "
            if modifier == "weak" and othermods.index(modifier) != len(othermods) - 1:
                namestring += "Weak, "
            if modifier == "x" and othermods.index(modifier) == len(othermods) - 1:
                namestring += "No 10-again "
            if modifier == "x" and othermods.index(modifier) != len(othermods) - 1:
                namestring += "No 10-again, "
            if modifier == "advanced" and othermods.index(modifier) != len(othermods) - 1:
                namestring += "Advanced, "
            if modifier == "advanced" and othermods.index(modifier) == len(othermods) - 1:
                namestring += "Advanced "
        resultstring += "Result: "
        padvar = 75
        if successes2 > successes and any(mod4.lower() == "advanced" for mod4 in othermods) == True:
            finalsuccesses = successes2
        else:
            finalsuccesses = successes
        if finalsuccesses == 0:
            resultstring += "Failure!"
        if finalsuccesses == -1:
            resultstring += "|500Dramatic Failure!|n"
            padvar += 6
        if finalsuccesses == 1:
            resultstring += "1 success"
        if finalsuccesses > 1 and successes < 5:
            resultstring += str(finalsuccesses) + " successes!"
        if finalsuccesses >= 5:
            resultstring += "|050"+str(finalsuccesses) + " successes, for an exceptional success!|n"
            padvar += 6
        stringout += namestring + " " * (75 - len(namestring)) + "|"
        stringout += "\n| "
        stringout += resultstring + " " * (padvar - len(resultstring)) + "|"
        stringout += "\n| "
        stringout += tempstring + " " * (75 - len(tempstring)) + "|"
        
        if any(mod4.lower() == "advanced" for mod4 in othermods) == True:
            stringout += "\n| "
            tempstring2 = ""
            results2.sort()
            for die in results2:
                tempstring2 += str(die) + " "
            stringout += tempstring2 + " " * (75 - len(tempstring2)) + "|"
        stringout += "\n"
        stringout += "\\"
        stringout += "-" * 76
        stringout += "/"
        private = False
        for switch in othermods:
            if switch == "private":
                private = True
        if private == False:
            for x in user.location.contents:
                if x.player:
                    x.msg(stringout)
        else:
            self.caller.msg(stringout)
class ArcanaList(Command):
    """
    Shows a list of all mage arcana.
    """
    key = "+arcanalist"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def func(self):
        if self.caller.db.template != "Mage":
            self.caller.msg("Only mages can view a list of all arcana.")
            return
        for x in self.caller.location.db.arcana.db.arcana:
            self.caller.msg(x)
class SetPower(default_cmds.MuxCommand):
    """
    This command is used to set individual, 'Powers' based on supernatural template.
    This does not cover things like the Hurt Locker merits such as Atariya merits
    or Infected merits, but rather covers things like Gifts, Disciplines, Arcana,
    and so on.
    
    Syntax:
    +setpower <Power>=[<Value>] Set a given power to a given value, if that power can
    have numerical values attached to it.
    +setpower <Power>=0 Remove a given power from your sheet.
    """
    key = "+setpower"
    aliases = ["+setpowers"]
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def func(self):
        caller = self.caller
        template = self.caller.db.template
        powers = self.caller.db.powers
        lhs = self.lhs
        rhs = self.rhs
        args = self.args
        if template == "Vampire" or template == "Ghoul":
            for x in self.caller.location.db.disciplines.db.disciplines:
                if rhs:
                    if int(rhs) > 0:
                        if lhs.lower() == x[0].lower():
                            if self.caller.location.db.disciplines.MeetsPrereqs(self.caller,x[0]):
                                if isinstance(self.caller.location.db.disciplines.MeetsPrereqs(self.caller,x[0]),str):
                                    self.caller.msg(self.caller.location.db.disciplines.MeetsPrereqs(self.caller,x[0]))
                                self.caller.AddPower(x[0],rhs)
                                self.caller.msg(x[0] + " set to "+rhs)
                                return
                            else:
                                self.caller.msg("Prerequisites not met.")
                                return
                    else:
                        if self.lhs.lower() == x[0].lower():
                            self.caller.RemPower(x[0])
                            self.caller.msg(x[0] + " removed.")
            if template == "Vampire":
                if not ("=" in args):
                    if args:
                        for y in self.caller.location.db.disciplines.db.devotions:
                            if args.lower() == y[0].lower():
                                if self.caller.location.db.disciplines.MeetsPrereqs(self.caller,y[0]):
                                    self.caller.AddTech(y[0])
                                    self.caller.msg(y[0] + " added.")
                                    return
                                else:
                                    self.caller.msg("You don't meet the prerequisites for this devotion!")
                                    return
                        for cru in self.caller.location.db.disciplines.db.cruac_rituals:
                            if not "Cruac" in self.caller.db.powers.keys():
                                self.caller.msg("You need the discipline of cruac to purchase cruac rituals.")
                                return
                            if args.lower() == cru[0].lower():
                                for num in range(3,len(cru)):
                                    theme = cru[num].split(",")[0]
                                    req = cru[num].split(",")[1]
                                    if theme in self.caller.db.powers.keys():
                                        if int(self.caller.db.powers[theme]) >= int(req):
                                            pass
                                        else:
                                            self.caller.msg("You don't have the " + theme + " theme high enough to purchase this cruac ritual!")
                                            return
                                    else:
                                        self.caller.msg("You need the " + theme + " theme to purchase this cruac ritual!")
                                        return
                                self.caller.db.miscstats.append(cru[0]+","+cru[1])
                                self.caller.msg(cru[0] + " added.")
                                return
                        for the in self.caller.location.db.disciplines.db.theban_rituals:
                            if not "Theban Sorcery" in self.caller.db.powers.keys():
                                self.caller.msg("You need the discipline of Theban Sorcery to purchase Theban rituals.")
                                return
                            if args.lower() == the[0].lower():
                                for num in range(3,len(the)):
                                    theme = the[num].split(",")[0]
                                    req = the[num].split(",")[1]
                                    if theme in self.caller.db.powers.keys():
                                        if int(self.caller.db.powers[theme]) >= int(req):
                                            pass
                                        else:
                                            self.caller.msg("You don't have the " + theme + " theme high enough to purchase this theban ritual!")
                                            return
                                    else:
                                        self.caller.msg("You need the " + theme + " theme to purchase this theban ritual!")
                                        return
                                self.caller.db.miscstats.append(the[0]+","+the[1])
                                self.caller.msg(the[0] + " added.")
                                return
                        
                else:
                    for y in self.caller.db.techniquelist:
                        if "," in y:
                            if y.split(",")[0].lower() == self.lhs.lower():
                                self.caller.RemoveTech(y)
                                self.caller.msg(y[0] + " removed.")
                                return
                        else:
                            if y.lower() == self.lhs.lower():
                                self.caller.RemoveTech(y)
                                self.caller.msg(y + " removed.")
                                return
                self.caller.msg("Only vampires may purchase devotions and rituals.")
                return
        if template == "Werewolf":
            for x in self.caller.location.db.gifts.db.gifts:
                if self.lhs.lower() == x[0].lower() or self.lhs.lower == "gift of "+x[0].lower():
                    for y in self.caller.db.powers.keys():
                        if self.args.strip().lower() == y.lower():
                            self.caller.msg("You've already unlocked this gift!")
                            return
                        if self.args.strip().lower() in y.lower():
                            self.caller.msg("You've already unlocked this gift!")
                            return
                    self.caller.db.powers[x[0]] = '' 
                    self.caller.msg("Gift of "+x[0]+" unlocked. Please choose one facet corresponding to a dot of renown you have as the gift's starting facet." )
                    return
            for y in self.caller.location.db.gifts.db.gifts:
                for z in y:
                    if self.args.lower() == z.lower() and y.index(z) >= 4:
                        for power in self.caller.db.powers.keys():
                            if z in self.caller.db.powers[power]:
                                self.caller.msg("You already have that facet!")
                            else:
                                renownindex = y.index(z)
                                renownlist = []
                                if "," in self.caller.db.powers[power] or self.caller.db.powers[power] != '':
                                    facetlist = []
                                    if ',' in self.caller.db.powers[power]:
                                        facetlist.extend(self.caller.db.powers[power].split(","))
                                    else:
                                        facetlist.append(self.caller.db.powers[power])
                                    for facet in facetlist:
                                        if facet == y[4]:
                                            renownlist.append("Cunning,"+str(facetlist.index(facet)))
                                        if facet == y[5]:
                                            renownlist.append("Glory,"+str(facetlist.index(facet)))
                                        if facet == y[6]:
                                            renownlist.append("Honor,"+str(facetlist.index(facet)))
                                        if facet == y[7]:
                                            renownlist.append("Purity,"+str(facetlist.index(facet)))
                                        if facet == y[8]:
                                            renownlist.append("Wisdom,"+str(facetlist.index(facet)))
                                    if renownindex == 4:
                                        facetlist.insert(0,z)
                                    if renownindex == 5:
                                        for item in renownlist:
                                            if "Cunning" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Honor" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                            elif "Purity" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                            elif "Wisdom" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                    if renownindex == 6:
                                        for item in renownlist:
                                            if "Cunning" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Glory" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Purity" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                            elif "Wisdom" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                    if renownindex == 7:
                                        for item in renownlist:
                                            if "Cunning" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Glory" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Honor" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Wisdom" in item:
                                                indexin = int(item.split(",")[1])
                                                break
                                    if renownindex == 8:
                                        for item in renownlist:
                                            if "Cunning" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Glory" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Honor" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                            elif "Purity" in item:
                                                indexin = int(item.split(",")[1]) + 1
                                                break
                                    facetlist.insert(indexin, z)
                                    facetlist = ','.join(facetlist)
                                    self.caller.db.powers[power] = facetlist
                                    if y[0] == "Nature's Gift":
                                        self.caller.msg(y[0] + " facet, \""+z+"\" added.")
                                    else:
                                        self.caller.msg("Gift of "+y[0]+" facet, \""+z+"\" added.")
                                else:
                                    self.caller.db.powers[power] = z
                                    if y[0] == "Nature's Gift":
                                        self.caller.msg(y[0] + " facet, \""+z+"\" added.")
                                    else:
                                        self.caller.msg("Gift of " + y[0] + " facet, \""+z+ "\" added.")
        if template == "Wolfblood" or template == "Werewolf":
            if not rhs:
                for z in self.caller.location.db.gifts.db.rites:
                    if z[0].lower() == self.args.lower():
                        if int(z[1]) > 2:
                            self.caller.msg("At character creation, werewolves and wolf-blooded may only start with up to two dots of rites.")
                            return
                        for rite in self.caller.db.techniquelist:
                            if rite[1] == "2":
                                self.caller.msg("At character creation, werewolves and wolf-blooded may only start with up to two dots of rites.")
                                return
                            if rite[1] == "1" and len(self.caller.db.techniquelist) > 1:
                                self.caller.msg("At character creation, werewolves and wolf-blooded may only start with up to two dots of rites.")
                                return
                        if z[2] == "Wolf" and template == "Wolfblood":
                            self.caller.msg("Wolf-blooded may not take wolf rites.")
                            return
                        self.caller.AddTech(z[0],z[1])
                        self.caller.msg("Level " + z[1] + " " + z[2] + " rite,\"" + z[0] + "\" added.")
            for zz in self.caller.db.techniquelist:
                if zz.split(",")[0].lower() == self.args.lower():
                    if rhs == "0":
                        self.caller.db.techniquelist.remove(zz)
                        self.caller.msg(zz.split(",")[0] + " rite removed.")
                        return
            self.caller.msg("Invalid rite, facet, or gift.")
            return
        if template == "Wolfblood":
            tells = self.caller.location.db.gifts.db.tells
            for fur in tells:
                if fur[0].lower() == args.lower():
                    if len(self.caller.db.powers) == 0:
                        self.caller.db.powers[fur[0]] = ''
                        self.caller.msg(fur[0] +" tell added.")
                        return
                    elif len(self.caller.db.powers) == 1:
                        for merit in self.caller.db.meritlist:
                            if merit[0] == "Tell":
                                self.caller.db.powers[fur[0]] = ''
                                self.caller.msg(fur[0] + " tell added.")
                                return
                    elif len(self.caller.db.powers) >= 2:
                        self.caller.msg("You can't have that many tells.")
                        return
            self.caller.msg("Invalid tell.")
            return
        if template == "Mage":
            arcanalist = self.caller.db.powers
            rotes = self.caller.location.db.arcana.db.rotes
            templist = arcanalist
            caller = self.caller
            for x in templist:
                x.lower()
            if capwords(self.lhs) in self.caller.location.db.arcana.db.arcana:
                if 6 > int(self.rhs) > 0:
                    lhs = self.lhs
                    rhs = self.rhs
                    caller.AddPower(lhs, rhs)
                    self.caller.msg(lhs +" arcanum added at " + rhs + " dots.")
                    return
                elif int(self.rhs) == 0:
                    caller.RemovePower(self.lhs)
                    self.caller.msg(lhs + " arcanum removed.")
                    return
            else:
                if self.rhs == "0":
                    for rote in caller.db.techniquelist:
                        if self.lhs in rote.split(",")[0].lower():
                            caller.RemoveTech(self.lhs)
                            self.caller.msg(rote.split(",")[0] + " removed.")
                            return
                for x in rotes:
                    if self.lhs.lower() == x[1].lower():
                        for arcanum in arcanalist:
                            if arcanum[0] == x[0]:
                                if int(arcanum[1]) >= int(x[2]):
                                    if self.rhs.lower() == "animal ken":
                                        self.rhs = "animalken"
                                    if self.rhs.lower() in x[3].lower().split(",") or self.rhs.lower() == "praxis":
                                        if self.rhs == "animalken":
                                            self.rhs = "Animal Ken"
                                        caller.AddTech(x[1],x[0],self.rhs)
                                    else:
                                        self.caller.msg("If you'd like a custom skill attached to this rote, please contact staff.")
                                        return
                                else:
                                    self.caller.msg("You need more dots in the " + x[0].lower() + " arcanum to learn this rote!")
                                    return
                            else:
                                self.caller.msg("You need to have the "+x[0].lower()+" arcanum to learn this rote!")
                                return
                    else:
                        self.caller.msg("Invalid rote.")
                        return
        if template == "Changeling" or template == "Fae-Touched":
            kyubey = self.caller.location.db.contracts.db.contracts
            caller = self.caller
            powers = caller.db.powers
            for power in kyubey:
                if power[0].lower() == self.lhs.lower():
                    for contract in powers.keys():
                        if power[0] == contract:
                            if "," in powers[contract]:
                                elemsplit = powers[contract].split(",")
                                value = elemsplit[len(elemsplit)-1]
                            else:
                                value = powers[contract]
                            try:
                                if int(self.rhs) > int(value):
                                    if "," in power[1]:
                                        if self.rhs in power[1].split(","):
                                            self.caller.msg(power[0] + " upgraded to rank " + self.rhs)
                                            elemsplit[len(elemsplit)-1] = self.rhs
                                            powers[contract] = elemsplit.join(",")
                                            return
                                        else:
                                            self.caller.msg("You can't take " + power[0].lower() +" at that rank!")
                                            return
                                elif int(self.rhs) < int(value) and int(self.rhs) >= 1:
                                    if "," in power[1]:
                                        if self.rhs in power[1].split(","):
                                            self.caller.msg(power[0] + " reduced to rank "+ self.rhs)
                                            elemsplit[len(elemsplit)-1] = self.rhs
                                            powers[contract] = elemsplit.join(",")
                                            return
                                        else:
                                            self.caller.msg("You can't reduce "+ power[0].lower() +" to that rank!")
                                            return
                                else:
                                    self.caller.msg("You already have " + power[0].lower() +" at that rank!")
                                    return
                            except ValueError:
                                if rhs.title() in power[2].split(","):
                                    self.caller.msg(rhs.title() + " tag added to " + power[0])
                                    if value != powers[contract]:
                                        for tag in elemsplit:
                                            if tag > rhs.title():
                                                continue
                                            if elemsplit.index(tag) >= 1:
                                                elemsplit.insert(elemsplit.index(tag) - 1,rhs.title())
                                                powers[contract] = elemsplit.join(",")
                                                return
                                            if elemsplit.index(tag) == 0:
                                                elemsplit.insert(0,rhs.title())
                                                powers[contract] = elemsplit.join(",")
                                        return
                                    else:
                                        powers[contract] = rhs.title() + ","+ powers[contract]
                                        return
                                else:
                                    self.caller.msg("Invalid tag to add.")
                                    return
                                    
                    if "," in power[1]:
                        ranks = power[1].split(",")
                        if self.rhs in ranks:
                            self.caller.msg(power[0] + " added at rank "+self.rhs)
                            powers[power[0]] = self.rhs
                            return
                        else:
                            self.caller.msg("Invalid rank to add!")
                            return
                    else:
                        tags = power[2].split(",")
                        if self.rhs == power[1]:
                            self.caller.msg(power[0] + " added at rank "+power[1])
                            powers[power[0]] = power[1]
                            return
                        else:
                            self.caller.msg("Invalid rank to add!")
                            return
            self.caller.msg("Invalid contract!")
            return
        if template == "Beast":
            rawr = caller.location.db.atavisms.db.atavisms
            #Library of atavisms in the chargen room.
            eek = caller.location.db.atavisms.db.nightmares
            #Library of nightmares in the chargen room.
            for smash in rawr:
            #Iterate through the library of atavisms
                if smash[0].lower() == self.args.lower():
                #If the atavism is found in the library, set the relevant dictionary entry to string zero, as it has no value attached.
                    try:
                        testvar = powers[smash[0]]
                    except KeyError:
                    #Check and see if the key exists. If not, add the power.
                        powers[smash[0]] = "0"
                        self.caller.msg(smash[0] + " added.")
            for zoinks in eek:
            #Iterate through the library of nightmares.
                if zoinks[0] == self.arglist[0]:
                #If the nightmare is found, add it to the caller's database of techniques.
                    caller.AddTech(zoinks[0])
                    self.caller.msg(zoinks[0] + " added.")
        if template == "Hunter":
            advarmory = caller.location.db.endowments.db.advarmory
            benediction = caller.location.db.endowments.db.benediction
            castigation = caller.location.db.endowments.db.castigation
            elixir = caller.location.db.endowments.db.elixir
            relic = caller.location.db.endowments.db.relic
            thaum = caller.location.db.endowments.db.thaumatechnology
            ink = caller.location.db.endowments.db.ink
            for gear in advarmory:
                if lhs.lower() == gear[0].lower():
                    if self.caller.db.xsplat == "Task Force VALKYRIE":
                        if int(rhs) in gear[1]:
                            self.caller.AddPower(gear[0],int(rhs))
                            self.caller.msg(gear[0] + " added at " + rhs + " dots.")
                        else:
                            self.caller.msg("You can't take the " + gear[0] + " endowment at " + rhs + " dots.")
                            return
                    else:
                        self.caller.msg("Only members of Task Force VALKYRIE can take the advanced armory endowments.")
                        return
            for bless in benediction:
                if lhs.lower() == bless[0]:
                    if self.caller.db.xsplat == "Malleus Maleficarum":
                        self.caller.db.powers[bless[0]] = ""
                        self.caller.msg(bless[0] +" added.")
                        return
                    else:
                        self.caller.msg("Only members of the Malleus Maleficarum may purchase benedictions.")
                        return
            for burn in castigation:
                if burn[0].lower() == lhs.lower():
                    if self.caller.db.xsplat == "Lucifuge":
                        self.caller.db.powers[burn[0]] = ""
                        self.caller.msg(burn[0] + " added.")
                        return
                    else:
                        self.caller.msg("Only the Lucifuge may purchase the powers of castigation.")
                        return
            for brew in elixir:
                if brew[0].lower() == lhs.lower():
                    if self.caller.db.xsplat == "Ascending Ones":
                        if rhs in brew[1]:
                            self.caller.AddPower(brew[0],int(rhs))
                            self.caller.msg(brew[0] + " added at " + rhs + " dots.")
                            return
                        else:
                            self.caller.msg("You cannot purchase " + brew[0] + " at " + rhs + " dots.")
                            return
            for tat in ink:
                if tat[0].lower() == lhs.lower():
                    if self.caller.db.xsplat == "Knights of St. Adrian":
                        self.caller.db.powers[tat[0]] = ""
                        self.caller.msg(tat[0] + " added.")
                        return
                    else:
                        self.caller.msg("Only members of the Knights of St. Adrian may purchase angelic tattoos.")
                        return
            for art in relic:
                if art[0].lower() == lhs.lower():
                    if self.caller.db.xsplat == "Aegis Kai Doru":
                        if rhs in art[1]:
                            self.caller.AddPower(art[0],rhs)
                            self.caller.msg(art[0] + " added.")
                            return
                    else:
                        self.caller.msg("Only members of Aegis Kai Doru may purchase relics.")
                        return
            for bio in thaum:
                if bio[0].lower() == lhs.lower():
                    if self.caller.db.xsplat == "Cheiron Group":
                        if rhs in bio[1]:
                            self.caller.AddPower(bio[0],bio[1])
                            self.caller.msg(bio[0] + " added at " + bio[1] + " dots.")
                            return
                        else:
                            self.caller.msg("You can't purchase " + bio[0] + " at " + bio[1] + " dots.")
                            return
                    else:
                        self.caller.msg("Only agents of the Cheiron Group may purchase thaumatechnology enhancements.")
                        return
            self.caller.msg("Invalid endowment.")
            return
        if template == "Mummy":
            affinities = caller.location.db.affinities.db.affinities
            utterances = caller.location.db.affinities.db.utterances
            for aff in affinities:
                if lhs.lower() == aff[0]:
                    if len(aff) == 3 and aff[1] != "None" and aff[1] != "Cult":
                        if self.caller.db.xsplat == aff[1]:
                            self.caller.AddPower(aff[0],aff[1])
                            self.caller.msg("Guild affinity " + aff[0] + " added.")
                            return
                        else:
                            self.caller.msg("You're not in the right guild for this affinity.")
                            return
                    else:
                        if aff[1] == "None":
                            self.caller.AddPower(aff[0],"")
                            self.caller.msg(aff[0] + " added to your affinities.")
                            return
                        if aff[1] == "Cult":
                            for merit in self.caller.db.meritlist:
                                if merit[0] == "Cult" and int(merit[1]) >= 3:
                                    self.caller.AddPower(aff[0],aff[2])
                                    self.caller.msg(aff[0] + " added to your affinities.")
                                    return
                        for pillar in self.caller.db.miscstats:
                            if pillar in aff[1]:
                                if int(pillar.split(",")[1]) >= int(aff[2]):
                                    self.caller.AddPower(aff[0],aff[2])
                                    self.caller.msg(aff[0] + " added to your affinities.")
                                    return
                                else:
                                    self.caller.msg("Your " + pillar.split(",")[0] + " pillar isn't high enough to acquire this affinity.")
                                    return
            for utt in utterances:
                if lhs.lower() == utt[0]:
                    if rhs in utt[2]:
                        if rhs == "1":
                            for pillar in self.caller.db.miscstats:
                                if pillar.split(",")[0] == utt[1].split(",")[0]:
                                    if pillar.split(",")[1] == "1":
                                        for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                        self.caller.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added with a rank of " + rhs)
                                        return
                                    else:
                                        self.caller.msg("You need at least one dot in that pillar to purchase this utterance.")
                                        return
                        
                        elif rhs == "5" and utt[1].split(",")[2] == "Defining":
                            if self.caller.db.xsplat == "Lion-Headed":
                                if self.caller.db.miscstats[0].split(",")[1] == "5":
                                    for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                    self.caller.AddTech(utt[0],rhs)
                                    self.caller.msg(utt[0] + " added at 5 dots.")
                                    return
                                else:
                                    self.caller.msg("Your Ab pillar is not high enough to purchase this tier.")
                                    return
                            elif self.caller.db.xsplat == "Falcon-Headed":
                                if self.caller.db.miscstats[1].split(",")[1] == "5":
                                    for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                    self.caller.AddTech(utt[0],rhs)
                                    self.caller.msg(utt[0] + " added at 5 dots.")
                                    return
                                else:
                                    self.caller.msg("Your Ba pillar is not high enough to purchase this tier.")
                                    return
                            elif self.caller.db.xsplat == "Bull-Headed":
                                if self.caller.db.miscstats[2].split(",")[1] == "5":
                                    for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                    self.caller.AddTech(utt[0],rhs)
                                    self.caller.msg(utt[0] + " added at 5 dots.")
                                    return
                                else:
                                    self.caller.msg("Your Ka pillar is not high enough to purchase this tier.")
                                    return
                            elif self.caller.db.xsplat == "Serpent-Headed":
                                if self.caller.db.miscstats[3].split(",")[1] == "5":
                                    for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                    self.caller.AddTech(utt[0],rhs)
                                    self.caller.msg(utt[0] + " added at 5 dots.")
                                    return
                                else:
                                    self.caller.msg("Your Ren pillar is not high enough to purchase this tier.")
                                    return
                            elif self.caller.db.xsplat == "Jackal-Headed":
                                if self.caller.db.miscstats[4].split(",")[1] == "5":
                                    for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                    self.caller.AddTech(utt[0],rhs)
                                    self.caller.msg(utt[0] + " added at 5 dots.")
                                    return
                                else:
                                    self.caller.msg("Your Sheut pillar is not high enough to purchase this tier.")
                                    return
                        else:
                            for pillar in self.caller.db.miscstats:
                                if pillar.split(",")[0] in utt[1]:
                                    if int(utt[2].split(",")[utt[1].index(pillar.split(",")[0])]) <= int(pillar.split(",")[1]):
                                        for technique in self.caller.db.techniquelist:
                                            if utt[0] in technique:
                                                self.caller.RemoveTech(technique)
                                        self.caller.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at " + rhs + " dots.")
                                        return
                                    else:
                                        self.caller.msg("Your " + pillar.split(",")[0] + " pillar isn't high enough to acquire this tier of utterance.")
                                        return
        if template == "Promethean":
            transmutations = caller.location.db.transmutations.db.transmutations
            refine = caller.db.ysplat
            if "=" in self.args:
                if self.rhs == "0":
                    for mute in self.caller.db.powers.keys():
                        if mute.lower() == self.lhs.lower():
                            del self.caller.db.powers[mute]
                            self.caller.msg(mute + " transmutation removed.")
                            return
                        if self.lhs.lower() == self.caller.db.powers[mute].lower():
                            self.caller.msg(self.caller.db.powers[mute] + " alembic removed.")
                            self.caller.db.powers[mute] = ""
                            return
                    self.caller.msg("Invalid transmutation or alembic to remove.")
                    return
                else:
                    self.caller.msg("Use, '+set <transmutation or alembic>=0' to remove it.")
                    return
            for change in transmutations:
                if change[0].lower() == self.arglist[0].lower():
                    if change[1] == "General" or refine in change[1]:
                        if not change[0] in self.caller.db.powers.keys():
                            self.caller.db.powers[change[0]] = ""
                            self.caller.msg("The " + change[0] + " transmutation has been added to your sheet.")
                            return
                        else:
                            self.caller.msg("You already have that transmutation.")
                            return
                    else:
                        self.caller.msg("You can't start with that transmutation.")
                        return
                for alembic in change:
                    if self.arglist[0].lower() == alembic.lower() or self.args.lower() == alembic.lower():
                        if change.index(alembic) >= 2:
                            if self.caller.db.powers[change[0]] != "":
                                self.caller.msg(self.caller.db.powers[change[0]] + " alembic swapped out for " + alembic)
                            else:
                                self.caller.msg(alembic + " added to your " + change[0] + " transmutation.")
                            self.caller.db.powers[change[0]] = alembic
                            return
            self.caller.msg("Invalid transmutation or alembic.")
            return
        if template == "Demon":
            embeds = caller.location.db.embeds.db.embeds
            exploits = caller.location.db.embeds.db.exploits
            mods = caller.location.db.embeds.db.modifications
            process = caller.location.db.embeds.db.processes
            tech = caller.location.db.embeds.db.technologies
            prop = caller.location.db.embeds.db.propulsion
            technique =  caller.db.techniquelist
            miscstats = caller.db.miscstats
            merits = caller.db.meritlist
            terriblerank = 0
            for merit in merits:
                if merit[0].lower() == "terrible form":
                    terriblerank = int(merit[1])
            for layer in embeds:
                if layer[0].lower() == self.arglist[0].lower():
                    for power in powers.keys():
                        if layer[0].lower() == power:
                            self.caller.msg("You already have this embed!")
                            return
                        else:
                            powers.db.powers[layer[0]] = ""
                            self.caller.msg("Embed, \""+layer[0]+"\" added.")
                            return
            for hole in exploits:
                if hole[0].lower() == self.arglist[0].lower():
                    for techno in technique:
                        if layer[0].lower() == techno:
                            self.caller.msg("You already have this exploit!")
                            return
                        else:
                            caller.AddTech(hole[0])
                            self.caller.msg("Exploit, \""+hole[0]+"\" added.")
                            return
            for edit in mods:
                if edit[0].lower() == self.arglist[0].lower():
                    for miscellany in miscstats:
                        if "," in miscellany:
                            if edit[0].lower() == miscellany.split(",")[0].lower():
                                caller.msg("You already have this modification!")
                                return
                            else:
                                modcount = 0
                                for misc2 in miscstats:
                                    for edit2 in mods:
                                        if misc2.split(",")[0] == edit2[0]:
                                            if terriblerank >= 1:
                                                modcount += 1
                                if modcount > 1:
                                    self.caller.msg("You can't have more than two modifications, bonus from terrible form included.")
                                else:
                                    miscstats.append(edit[0])
                                    caller.msg(edit[0] + " modification added.")
                                    return
                        else:
                            if edit[0].lower() == miscellany.lower():
                                caller.msg("You already have this modification!")
                            else:
                                miscstats.append(edit[0])
                                caller.msg(edit[0] + " modification added.")
                                return
            for thread in process:
                if thread[0].lower() == self.arglist[0].lower():
                    threadcount = 0
                    for miscellany in miscstats:
                        if "," in miscellany:
                            for thread2 in process:
                                if thread2 == miscellany.split(",")[0]:
                                    threadcount += 1
                            if (threadcount > 0 and terriblerank <= 3) or (threadcount > 1 and terriblerank == 4):
                                self.caller.msg("You can't have that many processes!")
                            else:
                                self.caller.msg(thread[0] + " process added.")
                                miscstats.append(thread[0])
                        else:
                            for thread2 in process:
                                if thread2 == miscellany:
                                    threadcount += 1
                                if (threadcount > 0 and terriblerank <= 3) or (threadcount > 1 and terriblerank == 4):
                                    self.caller.msg("You can't have that many processes!")
                                else:
                                    self.caller.msg(thread[0] + " process added.")
                                    miscstats.append(thread[0])
            for gear in tech:
                if gear[0].lower() == self.arglist[0].lower():
                    techcount = 0
                    for miscellany in miscstats:
                        if "," in miscellany:
                            for gear2 in tech:
                                try:
                                    if gear2 == miscellany.split(",")[0]:
                                        techcount += 1
                                except IndexError:
                                    if gear2 == miscellany:
                                        techcount += 1
                            if (techcount > 0 and terriblerank <= 1) or (techcount > 1 and terriblerank >= 2):
                                self.caller.msg("You can't have that many technologies!")
                            else:
                                caller.msg(gear[0] + " technology added.")
                        else:
                            for gear2 in tech:
                                if gear2 == miscellany.split[0]:
                                    techcount += 1
                            if (techcount > 0 and terriblerank <= 1) or (techcount > 1 and terriblerank >= 2):
                                self.caller.msg("You can't have that many technologies!")
                            else:
                                caller.msg(gear[0] + " technology added.")
            for zoom in prop:
                if zoom[0].lower() == self.arglist[0].lower():
                    zoomcount = 0
                    for miscellany in miscstats:
                        if "," in miscellany:
                            for zoom2 in prop:
                                try:
                                    if zoom2 == miscellany.split(",")[0]:
                                        zoomcount += 1
                                except IndexError:
                                    if zoom2 == miscellany:
                                        zoomcount += 1
                            if (zoomcount > 0 and terriblerank <= 2) or (zoomcount > 1 and terriblerank > 2):
                                caller.msg("You can't have that many propulsions!")
                            else:
                                caller.msg(zoom[0] + " propulsion added.")
                        else:
                            for zoom2 in prop:
                                if zoom2 == miscellany.split(",")[0]:
                                    zoomcount += 1
                            if (zoomcount > 0 and terriblerank <= 2) or (zoomcount > 1 and terriblerank > 2):
                                caller.msg("You can't have that many propulsions!")
                            else:
                                caller.msg(zoom[0] + " propulsion added.")
class SubmitApp(Command):
    """
    Submit your application for your character, and automatically create a job associated with it.
    Please note that your deadline is viewable via +myjobs.
    """
    key = '+submit'
    lock = 'cmd:inside(Chargen)'
    help_category="Chargen"
    def func(self):
        
        self.caller.db.submitted = True
        self.caller.msg('You have submitted your application! Please give staff some time to process it.')
        handlervar = search.scripts('JobHandler')
        try:
            handlervar = handlervar[0]
        except IndexError:
            handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
            self.caller.msg("Jobs system initialized.")
        try:
            jobchan = search.channels('Jobs')[0]
        except IndexError:
            jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Immortals);listen:perm(Wizards);send:false()')
        try:
            date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
            deadline = datetime.date.today() + datetime.timedelta(days=int(handlervar.db.deadlines[handlervar.db.buckets['APP'] - 1]))
            deadline = deadline.strftime("%a %b %d")
            commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
            handlervar.db.joblist[handlervar.db.buckets['APP'] - 1].append(['Character Application: ' + self.caller.name,self.caller.id,date,deadline,tuple([self.caller.id,self.caller.name + ' would like to be reviewed, prior to approval for play.',commenttime])])
            jobchan.msg(self.caller.name + " has submitted their application for review!")
        except KeyError:
            handlervar.db.buckets['APP'] = len(handlervar.db.buckets) + 1
            handlervar.db.joblist.append([])
            handlervar.db.deadlines[handlervar.db.buckets['APP']] = 3
            date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
            deadline = datetime.date.today() + datetime.timedelta(days=int(handlervar.db.deadlines[handlervar.db.buckets['APP'] - 1]))
            deadline = deadline.strftime("%a %b %d")
            commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
            handlervar.db.joblist[handlervar.db.buckets['APP'] - 1].append(['Character Application: ' + self.caller.name,self.caller.id,date,deadline,tuple([self.caller.id,self.caller.name + ' would like to be reviewed, prior to approval for play.',commenttime])])
        return
class SetStatus(Command):
    """
    Sets a small blurb for a status message, visible in the, 'Who' listing.
    
    Syntax:
    
    +doing <Status>
    """
    key = "+doing"
    aliases = "@doing"
    lock = "cmd:all()"
    help_category="OOC"
    def parse(self):
        self.args = self.args.lstrip()
    def func(self):
        self.caller.player.db.doing = self.args
        self.caller.msg("Status set.")
class ShortDesc(Command):
    """
    Sets your short description. This is the appearance that people will see following your name in room appearances.
    
    Syntax:
    +shortdesc <Short description>
    """
    key = "+shortdesc"
    lock = "cmd:all()"
    help_category="OOC"
    def parse(self):
        self.args = self.args.lstrip()
    def func(self):
        self.caller.db.shortdesc = self.args
        self.caller.msg("Short description set.")
class SetStat(default_cmds.MuxCommand):
    """
    Sets varying core statistics regarding your character.
    
    Syntax:
    +setstat/powerstat <Number> Increase or decrease your powerstat by that amount using merit dots.
    Use the number 0 to reset your powerstat spends, while using 1 or 2 to raise it. Note, the
    number given is the number of powerstat dots you are purchasing compared to your current amount,
    rather than the number of merit dots you are spending or the total number of powerstat dots you
    are purchasing.
    +setstat/merit <Merit Name>=<Rating> Sets a merit to the given rating. Use a rating of 0 to remove
    the merit entirely.
    +Setstat/attribute <Attribute Name>=<Rating> Simple, sets a given attribute to the rating provided.
    +setstat/skill <Skill Name>=<Rating> Sets a merit to the given rating, use a rating of 0 to remove
    expertise in that skill and set it back to untrained.
    +setstat/specialty <Skill>/<Specialty Name> Set a specialty for a given skill. Use an asterisk or star
    in the command while selecting a specialty as normal to remove said specialty. In example,
    "+setstat/specialty *Science/Chemistry" will remove a chemistry specialty in science.
    +setstat/<Template choice> <Value> Sets one of your template choices, such as clan, order, family, or other
    such things to a given value. So a beast's player might use +setstat/hunger Ravager to indicate their
    character has a hunger for Ruin. This also works for social archetypes such as blood and bone, legend and life,
    mask and dirge, and of course virtue and vice.
    """
    key = "+setstat"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def func(self):
        overlist = []
        template = self.caller.db.template
        switches = self.switches
        arglist = self.arglist
        xsplatlist = ["clan","aupisce","path","seeming","faction","decree","family","incarnation","lineage"]
        ysplatlist = ["hunger","court","agenda","order","guild","refinement","covenant","tribe"]
        zsplatlist = ["entitlement","legacy","role","bloodline","lodge"]
        demeanorlist = ["legend","mask","virtue","elpis","blood"]
        naturelist = ["life","mien","vice","torment","dirge","bone"]
        if switches:
            if switches[0] == "powerstat":
                if template == "Mortal" or template == "Fae-Touched" or template == "Ghoul" or template == "Proximus" or template == "Wolfblood":
                    self.caller.msg("Your current template lacks a powerstat to raise.")
                    return
                if arglist:
                    try:
                        if int(arglist[0]) >= 0 and int(arglist[0]) < 3:
                            merittotal = 0
                            for scoremerit in self.caller.db.meritlist:
                                merittotal += int(scoremerit[1])
                            if merittotal > self.caller.db.meritlimit:
                                self.caller.msg("You have too few merit dots remaining to purchase a dot of powerstat!")
                                return
                            self.caller.db.powerstat = int(arglist[0]) + 1
                            if int(arglist[0]) > 0:
                                self.caller.db.meritlimit = 10 - (int(arglist[0])*5)
                                self.caller.msg(arglist[0] + " dots of "+ self.caller.db.powerstatname + " purchased with merits.")
                                return
                            elif int(arglist[0]) == 0:
                                if self.caller.db.powerstat == 1:
                                    self.caller.msg("You have no powerstat purchase to remove.")
                                    return
                                self.caller.msg("Powerstat purchase removed.")
                                self.caller.db.meritlimit = 10
                                return
                            else:
                                self.caller.msg("Please select whether to purchase one or two dots of powerstat with merit points, or enter 0 to remove any previous purchase.")
                                return
                    except ValueError:
                        self.caller.msg("Please enter either 1 or 2 to purchase powerstat dots.")
                        return
                else:
                    self.caller.msg("Please enter a value, whether 1 or 2, to purchase that many powerstat dots.")
                    return
                              
            if switches[0] == "merit":
                try:
                    int(arglist[0])
                except (ValueError, TypeError) as error:
                    self.caller.msg("Invalid rating, please enter a positive number from one to five.")
                    return
                for x in self.caller.location.db.merits.db.mental:
                    overlist.append(x)
                for x in self.caller.location.db.merits.db.physical:
                    overlist.append(x)
                for x in self.caller.location.db.merits.db.social:
                    overlist.append(x)
                for x in self.caller.location.db.merits.db.fighting:
                    overlist.append(x)
                for x in self.caller.location.db.merits.db.supernatural:
                    overlist.append(x)
                if template == "Mortal":
                    for x in self.caller.location.db.merits.db.atariya:
                        overlist.append(x)
                    for x in self.caller.location.db.merits.db.dreamer:
                        overlist.append(x)
                    for x in self.caller.location.db.merits.db.infected:
                        overlist.append(x)
                    for x in self.caller.location.db.merits.db.plain:
                        overlist.append(x)
                    for x in self.caller.location.db.merits.db.lostboy:
                        overlist.append(x)
                    for x in self.caller.location.db.merits.db.psyvamp:
                        overlist.append(x)
                if template == "Vampire":
                    for x in self.caller.location.db.merits.db.vampire:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Werewolf":
                    for x in self.caller.location.db.merits.db.werewolf:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Mage":
                    for x in self.caller.location.db.merits.db.mage:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Changeling":
                    for x in self.caller.location.db.merits.db.changeling:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Promethean":
                    for x in self.caller.location.db.merits.db.promethean:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Beast":
                    for x in self.caller.location.db.merits.db.beast:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)
                if template == "Hunter":
                    for x in self.caller.location.db.merits.db.hunter:
                        for y in overlist:
                            if x[0] == y[0]:
                                overlist.remove(y)
                        overlist.append(x)  
                for merit in overlist:
                    if merit[0].lower() == self.lhs.lower():
                        self.lhs = merit[0]
                if int(self.rhs) > 0:
                    merittotal = 0
                    if self.caller.location.db.merits.MeetsPrereqs(self.caller,self.lhs,self.rhs):
                        for scoremerit in self.caller.db.meritlist:
                            merittotal += int(scoremerit[1])
                        if merittotal >= self.caller.db.meritlimit:
                            self.caller.msg("You can't take that many merit dots!")
                            return
                        self.caller.AddMerit(self.lhs,self.rhs)
                        self.caller.msg(self.lhs+" merit added at "+str(self.rhs)+" dots.")
                        self.caller.Update()
                    else:
                        self.caller.msg("Invalid merit")
                else:
                    for merit in self.caller.db.meritlist:
                        if self.lhs.lower() == merit[0].lower():
                            self.caller.msg(merit[0]+" removed.")
                            self.caller.RemMerit(merit[0])
                            self.caller.Update()
                            return
                    self.caller.msg("You don't have that merit to remove!")
                    return
            elif switches[0] == "attribute":
                if self.args:
                    for attrib in self.caller.db.attrstats.keys():
                        if self.lhs:
                            if attrib.lower() == self.lhs.lower():
                                if self.rhs:
                                    try:
                                        self.caller.db.attrstats[attrib] = int(self.rhs)
                                        self.caller.db.attribbase[attrib] = int(self.rhs)
                                        self.caller.msg(attrib + " set to "+self.rhs)
                                        self.caller.Update()
                                        return
                                    except ValueError:
                                        self.caller.msg("Invalid value to set for " + attrib)
                                        return
                                else:
                                    self.caller.msg("Please enter a value to set "+ attrib + " to.")
                                    return
                    self.caller.msg("Invalid attribute.")
                    return
                else:
                    self.caller.msg("Please select an attribute to set.")
                    return
            elif switches[0] == "skill":
                if self.args:
                    for skill in self.caller.db.physskills.keys():
                        if self.lhs:
                            if skill.lower() == self.lhs.lower():
                                if self.rhs:
                                    try:
                                        self.caller.db.physskills[skill] = int(self.rhs)
                                        self.caller.msg(skill + " set to "+self.rhs)
                                        self.caller.Update()
                                        return
                                    except ValueError:
                                        self.caller.msg("Invalid value to set for "+ skill)
                                        return
                                else:
                                    self.caller.msg("Please enter a value to set "+ skill + " to.")
                                    return
                    for skill in self.caller.db.mentskills.keys():
                        if self.lhs:
                            if skill.lower() == self.lhs.lower():
                                if self.rhs:
                                    try:
                                        self.caller.db.mentskills[skill] = int(self.rhs)
                                        self.caller.msg(skill + " set to "+self.rhs)
                                        self.caller.Update()
                                        return
                                    except ValueError:
                                        self.caller.msg("Invalid value to set for "+ skill)
                                        return
                                else:
                                    self.caller.msg("Please enter a value to set "+ skill + " to.")
                                    return
                    for skill in self.caller.db.socskills.keys():
                        if self.lhs:
                            if skill.lower() == self.lhs.lower():
                                if self.rhs:
                                    try:
                                        self.caller.db.socskills[skill] = int(self.rhs)
                                        self.caller.msg(skill + " set to "+self.rhs)
                                        self.caller.Update()
                                        return
                                    except ValueError:
                                        self.caller.msg("Invalid value to set for "+ skill)
                                        return
                                else:
                                    self.caller.msg("Please enter a value to set "+ skill + " to.")
                                    return
                    self.caller.msg("Invalid skill.")
                    return
                else:
                    self.caller.msg("Please enter a skill to set.")
            elif switches[0].lower() == 'specialty':
                if "/" in self.args:
                    specskill = self.args.split("/")[0]
                    specname = self.args.split("/")[1]
                else:
                    self.caller.msg('You need to input both a skill and a specialty name.')
                    return
                for phys in self.caller.db.physskill.keys():
                    if phys.lower() == specskill.lower():
                        self.caller.db.specialties[specname] = phys
                        self.caller.msg(phys + ' specialty, "' + specname + '" added.')
                        return
                for ment in self.calller.db.mentskills.keys():
                    if ment.lower() == specskill.lower():
                        self.caller.db.specialties[specname] = ment
                        self.caller.msg(ment + ' specialty, "' + specname + '" added.')
                        return
                for soc in self.caller.db.socskills.keys():
                    if soc.lower() == specskill.lower():
                        self.caller.db.specialties[specname] = soc
                        self.caller.msg(soc + ' specialty, "' + specname + '" added.')
                        return
                if "*" in self.args:
                    for spec in self.caller.db.specialties.keys():
                        if spec == self.args.split[1]:
                            self.caller.db.specialties.remove[spec]
                            self.caller.msg(self.caller.db.specialties[spec] + " Specialty in " + spec + " removed." )
                self.caller.msg('Invalid skill.')
                return
            elif switches[0].lower() in xsplatlist:
                if self.caller.db.template == "Beast" and switches[0].lower() == "family":
                    for family in self.caller.location.db.atavisms.db.families:
                        if self.args.lower() == family.lower():
                            self.caller.db.xplst = family
                            self.caller.msg("Family set to "+family)
                            return
                    self.caller.msg("That's not a valid family for a Beast to select.")
                    return
                elif (self.caller.db.template == "Changeling" or self.caller.db.template == "Fae-Touched") and switches[0].lower() == "seeming":
                    for seeming in self.caller.location.db.contracts.db.seemings:
                        if self.args.lower() == seeming.lower():
                            self.caller.db.xsplat = seeming
                            self.caller.msg("Seeming set to "+seeming)
                            return
                    self.caller.msg("That's not a valid seeming to select.")
                    return
                elif self.caller.db.template == "Demon" and switches[0].lower() == "incarnation":
                    for form in self.caller.location.db.embeds.db.incarnations:
                        if self.args.lower() == form.lower():
                            self.caller.db.xsplat = form
                            self.caller.msg("Incarnation set to "+form)
                            return
                    self.caller.msg("That's not a valid incarnation for a demon to select.")
                    return
                elif self.caller.db.template == "Hunter" and switches[0].lower() == "faction":
                    if not self.caller.IsAdmin():
                        for fac in self.caller.location.db.endowments.db.appfactions:
                            if self.args.lower() == fac.lower():
                                self.caller.db.xsplat = fac
                            if fac in self.caller.location.db.endowments.db.compacts:
                                self.caller.msg("Compact set to "+fac)
                                return
                            elif fac in self.caller.location.db.endowments.db.conspiracies:
                                self.caller.msg("Conspiracy set to "+fac)
                                return
                        self.caller.msg("Either you misspelled the faction, or it is not open for play at this time.")
                        return
                    else:
                        for comp in self.caller.location.db.endowments.db.compacts:
                            if self.args.lower() == comp.lower():
                                self.caller.db.xsplat = comp
                                self.caller.msg("Compact set to " + fac)
                        for cons in self.caller.location.db.endowments.db.conspiracies:
                            if self.args.lower() == cons.lower():
                                self.caller.db.xsplat = cons
                                self.caller.msg("Conspiracy set to " + cons)
                                if cons == "Task Force VALKYRIE":
                                    self.caller.db.powername = "Advanced Armory"
                                elif cons == "Aegis Kai Doru":
                                    self.caller.db.powername = "Relics"
                                elif cons == "Ascending Ones":
                                    self.caller.db.powername = "Elixirs"
                                elif cons == "Cheiron Group":
                                    self.caller.db.powername = "Thaumatechnology"
                                elif cons == "Lucifuge":
                                    self.caller.db.powername = "Castigation"
                                elif cons == "Malleus":
                                    self.caller.db.powername = "Benedictions"
                                elif cons == "Faithful of Shulpae":
                                    self.caller.db.powername = "Dread Powers"
                                elif cons == "Knights of St. Adrian":
                                    self.caller.db.powername = "Ink"
                    if self.caller.db.xsplat.lower() != self.args.lower():
                        self.caller.msg("Invalid faction.")
                        return
                elif (self.caller.db.template == "Mage" or self.caller.db.template == "Proximus") and switches[0].lower() == "path":
                    for path in self.caller.location.db.arcana.db.paths:
                        if path.lower() == self.args.lower():
                            self.caller.db.xsplat = path
                            if self.caller.db.template == "Mage":
                                self.caller.msg("Path set to "+path)
                            else:
                                self.caller.msg("Parent path set to "+path)
                            return
                    self.caller.msg("Invalid path.")
                    return
                elif self.caller.db.template == "Mummy" and switches[0].lower() == "decree":
                    for dec in self.caller.location.db.affinities.db.decrees:
                        if dec.lower() == self.args.lower():
                            self.caller.db.xsplat = dec
                            self.caller.msg("Decree set to " + dec)
                            return
                    self.caller.msg("Invalid decree.")
                elif self.caller.db.template == "Promethean" and switches[0].lower() == "lineage":
                    for lin in self.caller.location.db.transmutations.db.lineages:
                        if lin.lower() == self.args.lower():
                            self.caller.db.xsplat = lin
                            self.caller.msg("Lineage set to " + lin)
                            return
                    self.caller.msg("Invalid lineage.")
                    return
                elif (self.caller.db.template == "Vampire" or self.caller.db.template == "Ghoul") and switches[0].lower() == "clan":
                    for clan in self.caller.db.location.disciplines.db.clans:
                        if clan.lower() == self.args.lower():
                            self.caller.db.xsplat = clan
                            if self.caller.db.template == "Ghoul":
                                self.caller.msg("Regnant's clan set to " + clan)
                            else:
                                self.caller.msg("Clan set to " + clan)
                            return
                    self.caller.msg("Invalid clan.")
                    return
                elif self.caller.db.template == "Werewolf" and switches[0].lower() == "aupsice":
                    for ausp in self.caller.location.db.gifts.db.auspices:
                        if ausp.lower() == self.args.lower():
                            self.caller.db.xsplat = ausp
                            self.caller.msg("Auspice set to " + ausp)
                            return
                    self.caller.msg("Invalid auspice.")
                    return
                else:
                    self.caller.msg("You can't set a trait you don't have.")
                    return
            elif switches[0].lower() in ysplatlist:
                if self.caller.db.template == "Beast" and switches[0].lower() == "hunger":
                    for hung in self.caller.location.db.atavisms.db.hungers:
                        if hung.lower() == self.args.lower():
                            self.caller.db.ysplat = hung
                            self.caller.msg("Hunger set to "+hung)
                            return
                    self.caller.msg("Invalid hunger.")
                    return
                elif (self.caller.db.template == "Changeling" or self.caller.db.template == "Fae-Touched") and switches[0].lower() == "court":
                    if self.args.lower() == "seelie":
                        self.caller.db.ysplat = "Seelie"
                        self.caller.msg("Court set to Seelie.")
                        return
                    elif self.args.lower() == "unseelie":
                        self.caller.db.ysplat = "Unseelie"
                        self.caller.msg("Court set to Unseelie.")
                        return
                elif self.caller.db.template == "Demon" and switches[0].lower() == "agenda":
                    for agen in self.caller.location.db.embeds.db.agendas:
                        if agen.lower() == self.args.lower():
                            self.caller.db.ysplat = agen
                            self.caller.msg("Agenda set to " + agen)
                            return
                    self.caller.msg("Invalid agenda.")
                    return
                elif self.caller.db.template == "Mummy" and switches[0].lower() == "guild":
                    for guild in self.caller.location.db.affinities.db.guilds:
                        if guild.lower() == self.args.lower():
                            self.caller.db.ysplat = guild
                            self.caller.msg("Guild set to " + guild)
                            return
                    self.caller.msg("Invalid guild.")
                elif self.caller.db.template == "Promethean" and switches[0].lower() == "refinement":
                    reflist = self.caller.location.db.transmutations.GetRefinement(self.args.lower())
                    if reflist == False:
                        self.caller.msg("Invalid refinement.")
                        return
                    else:
                        self.caller.msg("Refinement set to "+reflist)
                        self.caller.db.ysplat = reflist
                        return
                elif self.caller.db.template == "Vampire" and switches[0].lower() == "covenant":
                    for cov in self.caller.location.db.disciplines.db.covenants:
                        if cov.lower() == self.args.lower():
                            self.caller.db.ysplat = cov
                            self.caller.msg("Covenant set to " + cov)
                            return
                    self.caller.msg("Invalid covenant.")
                    return
                elif self.caller.db.template == "Werewolf" and switches[0].lower() == "tribe":
                    for tribe in self.caller.location.db.gifts.db.tribes:
                        if tribe.lower() == self.args.lower():
                            self.caller.db.ysplat = tribe
                            self.caller.msg("Tribe set to " + tribe)
                            return
                    self.caller.msg("Invalid tribe.")
                    return
            elif switches[0].lower() in zsplatlist:
                if self.caller.db.template == "Changeling" and switches[0].lower() == "entitlement":
                    for title in self.caller.location.db.contracts.db.entitlements:
                        if title.lower() == self.args.lower():
                            self.caller.db.zsplat = title
                            self.caller.msg("Entitlement set to " + title)
                            return
                    self.caller.msg("Invalid entitlement.")
                    return
                elif self.caller.db.template == "Mage" and switches[0].lower() == "legacy":
                    for leg in self.caller.location.db.arcana.db.legacies:
                        if leg.lower() == self.args.lower():
                            self.caller.db.zsplat = leg
                            self.caller.msg("Legacy set to " + leg)
                            return
                    self.caller.msg("Invalid legacy.")
                    return
                elif self.caller.db.template == "Vampire" and switches[0].lower() == "bloodline":
                    for line in self.caller.location.db.disciplines.db.bloodlines:
                        if line.lower() == self.args.lower():
                            self.caller.db.zsplat = line
                            self.caller.msg("Bloodline set to " + line)
                            return
                    self.caller.msg("Invalid bloodline.")
                    return
                elif self.caller.db.template == "Werewolf" and switches[0].lower() == "lodge":
                    for lodge in self.caller.location.db.gifts.db.lodges:
                        if lodge.lower() == self.args.lower():
                            self.caller.db.zsplat = lodge
                            self.caller.msg("Lodge set to " + lodge)
                            return
                    self.caller.msg("Invalid lodge.")
                    return
                elif switches[0].lower() in demeanorlist:
                    if switches[0].lower() == "legend" and self.caller.db.template == "Beast":
                        for legend in self.caller.location.db.atavisms.db.legends:
                            if legend.lower() == self.args.lower():
                                self.caller.db.demeanor = legend
                                self.caller.msg("Legend set to " + legend)
                                return
                        self.caller.msg("Invalid legend archetype.")
                        return
                    elif self.caller.db.template == "Changeling" and switches[0].lower() == "mask":
                        for masque in self.caller.location.db.contracts.db.archetypes:
                            if masque.lower() == self.args.lower():
                                self.caller.db.demeanor = masque
                                self.caller.msg("Mask set to " + masque)
                                return
                        self.caller.msg("Invalid mask archetype.")
                    elif self.caller.db.template == "Demon" or self.caller.db.template == "Hunter" or self.caller.db.template == "Mage" or self.caller.db.template == "Mummy" or self.caller.db.template == "Mortal" and switches[0].lower() == "virtue":
                        self.caller.db.demeanor = self.args.title()
                        self.caller.msg("Virtue set to " + self.args.title())
                        return
                    elif self.caller.db.template == "Promethean":
                        for elpis in self.caller.location.db.transmutations.db.elpides:
                            if elpis.lower() == self.args.lower():
                                self.caller.db.demeanor = elpis
                                self.caller.msg("Elpis set to " + elpis)
                                return
                        self.caller.msg('Invalid elpis.')
                        return
                    elif self.caller.db.template == "Vampire" and switches[0].lower() == "mask":
                        for mask in self.caller.location.db.disciplines.db.archetypes:
                            if mask.lower() == self.args.lower():
                                self.caller.db.demeanor = mask
                                self.caller.msg("Mask set to " + mask)
                                return
                        self.caller.msg("Invalid mask archetype..")
                        return
                    elif self.caller.db.template == "Werewolf" and switches[0].lower() == "blood":
                        for blood in self.caller.location.db.gifts.db.blood:
                            if blood.lower() == self.args.lower():
                                self.caller.db.demeanor = blood
                                self.caller.msg("Blood set to " + blood)
                                return
                        self.caller.msg("Invalid blood archetype.")
                        return
                elif switches[0].lower() in naturelist:
                    if self.caller.db.template == "Changeling" and switches[0].lower() == "mask":
                        for life in self.caller.location.db.atavisms.db.lives:
                            if life.lower() == self.args.lower():
                                self.caller.db.demeanor = life
                                self.caller.msg("Life set to " + life)
                                return
                        self.caller.msg("Invalid life archetype.")
                        return
                    elif self.caller.db.template == "Demon" or self.caller.db.template == "Hunter" or self.caller.db.template == "Mage" or self.caller.db.template == "Mummy" or self.caller.db.template == "Mortal" and switches[0].lower() == "vice":
                        self.caller.db.nature = self.args.title()
                        self.caller.msg("Vice set to " + self.args.title())
                        return
                    elif self.caller.db.template == "Promethean" and switches[0].lower() == "torment":
                        for torment in self.caller.location.db.transmutations.db.torments:
                            if torment.lower() == self.args.lower():
                                self.caller.msg("Torment set to " + self.args.title())
                                self.caller.db.nature = torment
                                return
                        self.caller.msg('Invalid torment.')
                        return
                    elif self.caller.db.template == "Vampire" and switches[0].lower() == "dirge":
                        for dirge in self.caller.location.db.disciplines.db.archetypes:
                            if dirge.lower() == self.args.lower():
                                self.caller.db.nature = dirge
                                self.caller.msg("Dirge set to " + dirge)
                                return
                        self.caller.msg("Invalid dirge archetype.")
                        return
                    elif self.caller.db.template == "Werewolf" and switches[0].lower() == "bone":
                        for bone in self.caller.location.db.gifts.db.bone:
                            if bone.lower() == self.args.lower():
                                self.caller.db.nature = bone
                                self.caller.msg("Bone set to " + bone)
                                return
                        self.caller.msg("Invalid bone archetype.")
                        return
            else:
                self.caller.msg("Invalid switch.")
                return
class SetTemplate(Command):
    """
    This brings up a template menu for the player to choose from. Additional information is provided
    for novices, and furthermore adds information regarding special policies that may or may not be
    present for the template in-game.
    """
    key = "+template"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def parse(self):
        self.args = self.args.strip()
    def func(self):
        self.admins = ['Builders','Wizards','Immortals','Superuser']
        args = self.args
        if not args:
            templatestring = "/" + "-" * 34 + "Template" + "-" * 34 + "\\\n"
            templatestring += "||"
            templatewrap = wrap(" Please click on a template to view its info if your client supports MXP, or enter the command in parentheses if not.")
            templatestring += templatewrap[0] + " " * (76 - len(templatewrap[0])) + "||\n|| " + templatewrap[1] + " " * (75 - len(templatewrap[1])) + "||"
            templatestring += "\n"
            templatestring += "| |lcvampinfo|ltVampire|le " + "(vampinfo)"+" " * (77 - len("| Vampire (vampinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcwolfinfo|ltWerewolf|le " + "(wolfinfo)" + " " * (77 - len("| Werewolf (wolfinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcmageinfo|ltMage|le " + "(mageinfo)" + " " * (77 - len("| Mage (mageinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcchangelinginfo|ltChangeling|le " + "(changelinginfo)" + " " * (77 - len("| Changeling (changelinginfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lchunterinfo|ltHunter|le (hunterinfo)" + " " * (77 - len("| Hunter (hunterinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcbeastinfo|ltBeast|le (beastinfo)" + " " * (77 - len("| Beast (beastinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcprometheaninfo|ltPromethean|le (prometheaninfo)" + " " * (77 - len("| Promethean (prometheaninfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcmummyinfo|ltMummy|le (mummyinfo)" + " " * (77 - len("| Mummy (mummyinfo)")) + "|"
            templatestring += "\n"
            templatestring += "| |lcdemoninfo|ltDemon|le (demoninfo)" + " " * (77 - len("| Demon (demoninfo)")) + "|"
            templatestring += "\n"
            templatestring += "\\" + 76 * "-" + "/"
            self.caller.msg(templatestring)
        else:
            if args.lower() == "vampire":
                if settings.VAMP_STATUS.lower() == "open" or settings.VAMP_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Vampire"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.powerstat = 1
                    self.caller.db.pools.update({'Vitae':str(self.caller.db.powerlist[self.caller.db.powerstat-1]) +","+ str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.xsplatname = "Clan"
                    self.caller.db.ysplatname = "Covenant"
                    self.caller.db.zsplatname = "Bloodline"
                    self.caller.db.powername = "Disciplines"
                    self.caller.db.techname = "Devotions"
                    self.caller.db.miscname = "Rituals"
                    self.caller.db.demeanorname = "Mask"
                    self.caller.db.demeanor = ""
                    self.caller.db.naturename = "Dirge"
                    self.caller.db.nature = ""
                    self.caller.db.powerstatname = "Blood Potency"
                    self.caller.db.sanity = 7
                    self.caller.db.sanityname = "Humanity"
                    self.caller.db.miscstats = []
                    self.caller.db.meritlist = []
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.beats = 50
                    self.caller.msg("Template set to Vampire.")
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Vampire sphere is not open at this time.")
                    return
            if args.lower() == "ghoul":
                if settings.VAMP_STATUS.lower() == "open" or settings.VAMP_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Ghoul"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.pools.update({'Vitae':str(self.caller.db.attributes['Stamina'])+","+str(self.caller.db.attributes['Stamina'])})
                    self.caller.msg("Template set to ghoul.")
                    self.caller.db.powername = "Disciplines"
                    self.caller.db.powers = {}
                    self.caller.db.miscstats = []
                    self.caller.db.techniquelist = []
                    self.caller.db.techname = ""
                    self.caller.db.miscname =""
                    self.caller.db.xsplatname = ""
                    self.caller.db.ysplatname = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.powerstatname = ""
                    self.caller.db.sanity = 7
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.demeanor = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.db.nature = ""
                    self.caller.db.sanityname = "Integrity"
                    self.caller.db.powerstat = 0
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Vampire sphere is currently closed.")
                    return
            if args.lower() == "werewolf":
                if settings.WOLF_STATUS.lower() == "open" or settings.WOLF_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Werewolf"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.powerstat = 1
                    self.caller.db.pools.update({'Essence':str(7) +","+ str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.xsplatname = "Auspice"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Tribe"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = "Lodge"
                    self.caller.db.zsplat =""
                    self.caller.msg("Template set to Werewolf")
                    self.caller.db.powername = "Gifts"
                    self.caller.db.powers = {}
                    self.caller.db.techname = "Rites"
                    self.caller.db.techniquelist = []
                    self.caller.db.miscname = "Renown"
                    self.caller.db.powerstatname = "Primal Urge"
                    self.caller.db.sanityname = "Harmony"
                    self.caller.db.demeanorname = "Blood"
                    self.caller.db.naturename = "Bone"
                    self.caller.db.demeanor = ""
                    self.caller.db.nature = ""
                    self.caller.db.sanity = 7
                    self.caller.db.miscstats = ["Cunning,0","Glory,0","Honor,0","Purity,0","Wisdom,0"]
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Werewolf sphere is not open at this time.")
                    return
            if args.lower() == "wolfblood":
                if settings.WOLF_STATUS.lower() == "open" or settings.WOLF_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Wolfblood"
                    self.caller.db.powername = "Tells"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.miscstats = []
                    self.caller.db.powers = {}
                    self.caller.db.techniquelist = []
                    self.caller.db.techname = ""
                    self.caller.db.miscname =""
                    self.caller.db.xsplatname = ""
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = ""
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.sanityname = "Integrity"
                    self.caller.db.sanity = 7
                    self.caller.db.powerstat = 0
                    self.caller.db.powerstatname = ""
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.naturename = "Vice"
                    self.caller.db.nature = ""
                    self.caller.db.demeanor = ""
                    self.caller.db.meritlist = []
                    self.caller.msg("Template set to wolfblood")
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Werewolf sphere is not open at this time.")
                    return
            if args.lower() == "mage":
                if settings.MAGE_STATUS.lower() == "open" or settings.MAGE_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Mage"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.powerstat = 1
                    self.caller.db.pools.update({'Mana':str(self.caller.db.powerlist[self.caller.db.powerstat-1]) +","+ str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.xsplatname = "Path"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Order"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = "Legacy"
                    self.caller.db.zsplat = ""
                    self.caller.db.powername = "Arcana"
                    self.caller.db.poweres = {}
                    self.caller.db.techname = "Rotes and Praxes"
                    self.caller.db.techniquelist = []
                    self.caller.db.sanityname = "Wisdom"
                    self.caller.db.powerstatname = "Gnosis"
                    self.caller.db.miscname = ""
                    self.caller.db.miscstats = []
                    self.caller.db.sanity = 7
                    self.caller.db.demanor = ""
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.nature = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.msg("Template set to Mage.")
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Mage sphere is not open at this time.")
                    return
            if args.lower() == "proximus":
                if settings.MAGE_STATUS.lower() == "open" or settings.MAGE_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Proximus"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.pools['Mana'] = "5,5"
                    self.caller.db.xsplatname = "Path"
                    self.caller.db.powername = "Blessings"
                    self.caller.db.ysplatname = "Order"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.sanity = 7
                    self.caller.db.miscname = ""
                    self.caller.db.miscstats = []
                    self.caller.db.techname = ""
                    self.caller.db.techniquelist = []
                    self.caller.db.powerstat = 0
                    self.caller.db.powerstatname = ""
                    self.caller.db.sanityname = "Integrity"
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.nature = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.db.meritlist = []
                    self.caller.msg("Template set to proximus")
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Mage sphere is not open at this time.")
            if args.lower() == "changeling":
                if settings.LING_STATUS.lower() == "open" or settings.LING_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Changeling"
                    self.caller.db.powerstat = 1
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.pools.update({'Glamour':str((self.caller.db.powerlist[self.caller.db.powerstat-1])) + "," + str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.powerstatname = "Wyrd"
                    self.caller.db.xsplatname = "Seeming"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Court"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = "Entitlement"
                    self.caller.db.zsplat = ""
                    self.caller.db.powers = {}
                    self.caller.db.techniquelist = []
                    self.caller.db.techname = ""
                    self.caller.db.powername = "Contracts"
                    self.caller.db.miscname = ""
                    self.caller.db.miscstats = []
                    self.caller.db.sanityname = "Clarity"
                    self.caller.db.sanity = 7
                    self.caller.db.demeanorname = "Mask"
                    self.caller.db.naturename = "Mien"
                    self.caller.db.nature = ""
                    self.caller.db.demeanor = ""
                    self.caller.db.kith = ""
                    self.caller.msg("Template set to Changeling")
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Changeling sphere is not open at this time.")
                    return
            if args.lower() == "fae-touched":
                if settings.LING_STATUS.lower() == "open" or settings.LING_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Fae-Touched"
                    self.caller.db.powerstat = 0
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.pools['Glamour'] = "10,10"
                    self.caller.db.xsplatname = "Seeming"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Court"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.powername = "Contracts"
                    self.caller.db.powers = {}
                    self.caller.db.techname = ""
                    self.caller.db.techniquelist = []
                    self.caller.db.miscstats = []
                    self.caller.db.miscname = ""
                    self.caller.db.powerstatname = ""
                    self.caller.db.sanity = 7
                    self.caller.db.sanityname = "Integrity"
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.nature = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.db.meritlist = []
                    self.caller.msg("Template set to fae-touched.")
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Changeling sphere is not open at this time.")
                    return
            if args.lower() == "hunter":
                if settings.HUNTER_STATUS.lower() == "open" or settings.HUNTER_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Hunter"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.xsplatname = "Faction"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = ""
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.powername = "Endowments"
                    self.caller.db.powers = {}
                    self.caller.db.techname = ""
                    self.caller.db.techniquelist = []
                    self.caller.db.miscname = ""
                    self.caller.db.miscstats = []
                    self.caller.db.sanity = 7
                    self.caller.db.powerstat = 0
                    self.caller.db.powerstatname = ""
                    self.caller.db.sanityname = "Integrity"
                    self.caller.msg("Template set to Hunter")
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.nature = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Hunter is not open at this time.")
                    return
            if args.lower() == "beast":
                if settings.BEAST_STATUS.lower() == "open" or settings.BEAST_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Beast"
                    self.caller.msg("Template set to Beast")
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.xsplatname = "Family"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Hunger"
                    self.caller.db.ysplat = ""
                    self.caller.db.demeanorname = "Legend"
                    self.caller.db.naturename = "Life"
                    self.caller.db.nature = ""
                    self.caller.db.demeanor = ""
                    self.caller.db.zsplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.powername = "Atavisms"
                    self.caller.db.techname = "Nightmares"
                    self.caller.db.powerstatname = "Lair"
                    self.caller.db.powerstat = 1
                    self.caller.db.sanity = 4
                    self.caller.db.sanityname = "Satiety"
                    self.caller.db.miscstats = []
                    self.caller.db.techniquelist = []
                    self.caller.db.powers = {}
                    self.caller.db.miscname = ""
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
            if args.lower() == "promethean":
                if settings.PROMETHEAN_STATUS.lower() == "open" or settings.PROMETHEAN_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Promethean"
                    self.caller.msg("Template set to Promethean")
                    self.caller.db.powerstat = 1
                    self.caller.db.pools = self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.pools.update({'Pyros':str((self.caller.db.powerlist[self.caller.db.powerstat-1])/2) + "," + str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.xsplatname = "Lineage"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Refinement"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = "Role"
                    self.caller.db.zsplat = ""
                    self.caller.db.demeanorname = "Elpis"
                    self.caller.db.demeanor = ""
                    self.caller.db.naturename = "Torment"
                    self.caller.db.nature = ""
                    self.caller.db.powers = {}
                    self.caller.db.powername = "Transmutations"
                    self.caller.db.powerstatname = "Azoth"
                    self.caller.db.sanityname = "Pilgrimage"
                    self.caller.db.sanity = 1
                    self.caller.db.miscname = ""
                    self.caller.db.miscstats = []
                    self.caller.db.techname = ""
                    self.caller.db.techniquelist = []
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("Promethean sphere is not open at this time.")
                    return
            if args.lower() == "mortal":
                self.caller.db.template = "Mortal"
                self.caller.msg("Template set to Mortal")
                self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                self.caller.db.powerstat = 0
                self.caller.db.powerstatname = ""
                self.caller.db.sanity = 7
                self.caller.db.sanityname = "Integrity"
                self.caller.db.demeanorname = "Virtue"
                self.caller.db.nature = ""
                self.caller.db.naturename = "Vice"
                self.caller.db.xsplat = ""
                self.caller.db.xsplatname = ""
                self.caller.db.ysplat = ""
                self.caller.db.ysplatname = ""
                self.caller.db.zsplat = ""
                self.caller.db.zsplatname = ""
                self.caller.db.miscname = ""
                self.caller.db.miscstats = []
                self.caller.db.powers = {}
                self.caller.db.techname = ""
                self.caller.db.techniquelist = ""
                self.caller.db.powername = ""
                self.caller.db.meritlist = []
                self.caller.db.beats = 50
                self.caller.Update()
                return
            if args.lower() == "mummy":
                if settings.MUMMY_STATUS.lower() == "open" or settings.MUMMY_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Mummy"
                    self.caller.msg("Template set to Mummy")
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.miscstats = ["Ab,0","Ba,0","Ka,0","Ren,0","Sheut,0"]
                    self.caller.db.pools.update({"Ab":self.caller.db.miscstats[0].split(",")[1]+","+self.caller.db.miscstats[0].split(",")[1]})
                    self.caller.db.pools.update({"Ba":self.caller.db.miscstats[1].split(",")[1]+","+self.caller.db.miscstats[1].split(",")[1]})
                    self.caller.db.pools.update({"Ka":self.caller.db.miscstats[2].split(",")[1]+","+self.caller.db.miscstats[2].split(",")[1]})
                    self.caller.db.pools.update({"Ren":self.caller.db.miscstats[3].split(",")[1]+","+self.caller.db.miscstats[3].split(",")[1]})
                    self.caller.db.pools.update({"Sheut":self.caller.db.miscstats[4].split(",")[1]+","+self.caller.db.miscstats[4].split(",")[1]})
                    self.caller.db.powerstat = 1
                    self.caller.db.powerstatname = "Sekhem"
                    self.caller.db.powers = {}
                    self.caller.db.powername = "Affinities"
                    self.caller.db.techname = "Utterances"
                    self.caller.db.techniquelist = []
                    self.caller.db.sanity = 3
                    self.caller.db.sanityname = "Memory"
                    self.caller.db.xsplatname = "Decree"
                    self.caller.db.ysplatname = "Guild"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplat =""
                    self.caller.db.zsplatname = "Judge"
                    self.caller.db.zsplat = ""
                    self.caller.db.demeanor = ""
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.nature = ""
                    self.caller.db.miscname = "Pillars"
                    self.caller.db.naturename = "Vice"
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("The mummy sphere is currently closed.")
                    return
            if args.lower() == "demon":
                if settings.DEMON_STATUS.lower() == "open" or settings.DEMON_STATUS.lower() == "restricted" or self.caller.IsAdmin():
                    self.caller.db.template = "Demon"
                    self.caller.db.pools = {'Willpower':str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])+
                                            ","+str(self.caller.db.attributes['Resolve']+self.caller.db.attributes['Composure'])}
                    self.caller.db.powerstat = 1
                    self.caller.db.pools.update({"Aether":str(7) +","+ str(self.caller.db.powerlist[self.caller.db.powerstat-1])})
                    self.caller.db.powerstatname = "Primium"
                    self.caller.db.xsplatname = "Incarnation"
                    self.caller.db.xsplat = ""
                    self.caller.db.ysplatname = "Agenda"
                    self.caller.db.ysplat = ""
                    self.caller.db.zsplatname = ""
                    self.caller.db.demeanorname = "Virtue"
                    self.caller.db.demeanor = ""
                    self.caller.db.naturename = "Vice"
                    self.caller.db.nature = ""
                    self.caller.db.zsplat = ""
                    self.caller.msg("Template set to Demon")
                    self.caller.db.powers = {}
                    self.caller.db.powername = "Embeds"
                    self.caller.db.techniquelist = []
                    self.caller.db.techname = "Exploits"
                    self.caller.db.sanity = 7
                    self.caller.db.sanityname = "Cover"
                    self.caller.db.miscname = "Demonic Form"
                    self.caller.db.miscstats = []
                    self.caller.db.meritlist = []
                    self.caller.db.beats = 50
                    self.caller.Update()
                    return
                else:
                    self.caller.msg("The demon sphere is currently closed.")
                    return
            if not args.lower() == "vampire" or args.lower() == "mortal" or args.lower() == "werewolf" or args.lower() == "mage" or args.lower() == "changeling" or args.lower() == "hunter" or args.lower() == "beast" or args.lower() == "demon" or args.lower() == "mummy":
                self.caller.msg("Please select a valid template, or move on as your current template.")
class VampireInfo(Command):
    key = "vampinfo"
    lock = "cmd:all()"
    infostring = ("Vampires are good of course, for politically-minded players. The vampire venue is currently "+settings.VAMP_STATUS.lower()+". However, our main restrictions on this sphere are "
                "not allowing members of VII, or strix player characters. These entities are too hostile to other players to be allowed for play. Likewise, Jiang Shi are not " 
                "valid, as there is too little known of them and neither historical members of broken covenants or lost clans are available.")
    def func(self):
        stringout = "|300/" + "-" * 34 + "|555Vampire|300" + "-" * 35 + "\\|n"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|300|||n" + x + " "* (76 - len(x))+"|300|||n"
        stringout += "\n"
        stringout += "|300\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class WerewolfInfo(Command):
    key = "wolfinfo"
    lock = "cmd:inside(Chargen)"
    infostring = ("Somewhat contrasting to vampires, werewolves are good for those who wish to have a strong sense of unity. The pack is a werewolf's first and foremost obligation,"
    " and concerns of the tribe often come second. The werewolf sphere is currently "+settings.WOLF_STATUS.lower()+" though regardless certain restrictions exist. The Pure are amongst"
    " the most notable restriction for werewolf players, as while they are useful antagonists the nature of a pure player-character is too potentially destructive versus the"
    " potential gains of having such an individual around.")
    def func(self):
        stringout = "|320/"+ "-" * 34 + "|555Werewolf|320" + "-" * 34 + "\\|n"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|320|||n" + x + " " * (76 - len(x))+"|320|||n"
        stringout += "\n|320\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class MageInfo(Command):
    key = "mageinfo"
    lock = "cmd:all()"
    infostring = ("A middle-ground in dynamics between vampires and werewolves both, mages are able to display political unity and discord depending on a shifting climate of"
                  " relations between the varying orders. The mage sphere is currently " + settings.MAGE_STATUS.lower() + " yet like all other spheres, some restrictions are in place"
                  " regardless of sphere status. Banishers are completely unavailable for play, as their existence is for the most part dedicated to destroying mages and magical"
                  " phenomena. Likewise, the Seers of the Throne are unavailable as an order as their approach to magic is ultimately inimical to the majority of player options."
                  " Further, left-handed legacies are unavailable for play or development, as are liches of any sort. Finally, the transcendentally powerful archmages are only"
                  " available to be joined by the players as a means of retiring a character.")
    def func(self):
        stringout = "|235/" + "-" * 36 + "|555Mage|235" + "-" * 36 + "\\|n"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|235|||n" + x + " " * (76 - len(x)) + "|235|||n"
        stringout += "\n|235\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class ChangelingInfo(Command):
    key = "changelinginfo"
    lock = "cmd:all()"
    infostring = ("Generally, changelings can run the gamut between cooperative and conflicting but tend towards the cooperative side of things. The Gentry that took them are "
                  "creatures of singular arrogance and self-importance after all, and emulating them is a quick way to earn your fellows' enmity. The changeling sphere is"
                  " currently " + settings.LING_STATUS.lower() + " and the restrictions in place on the sphere are as follows. First, no privateer or loyalist changelings will be "
                  "permitted for use as player characters. Charlatan, also known as outcast, Gentry will not be permitted either nor will actual Gentry. Fetches are not an"
                  " available 'Mortal+' character type and Huntsmen are completely out of the question as are Cambions or other oneiroi-related entities. Finally, a character"
                  " must be part of the local freehold to avoid suspicion as tends to run amok towards those who are independent.")
    def func(self):
        stringout = "|030/" + "-" * 33 + "|555Changeling|030" + "-" * 33 + "\\|n"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|030|||n" + x + " " * (76 - len(x))  + "|030|||n"
        stringout += "\n|030\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class HunterInfo(Command):
    key = "hunterinfo"
    lock = "cmd:all()"
    infostring = ("Those dedicated to protecting humanity or else exploiting the supernatural for whatever reason, the hunter sphere is based on exactly that. Conflict with "
                  "supernatural entities and individuals. Currently, the hunter sphere is " +settings.HUNTER_STATUS.lower()+" and some explanations are due as to what exactly is and is "
                  "not allowed. The hunter sphere is not free license to kill whatever supernatural or mortal+ character, or even interfering mortal you please. It is meant to "
                  "focus on actual threats to humanity, and quarries with potentially powerful abilities. Low-humanity elders, the Pure, centimani prometheans and more are all "
                  "valid targets for a hunter. Staff will be watching hunter characters closely, and any reports of abuse of the basic premise of hunter will not be "
                  "tolerated.")
    def func(self):
        stringout = "|121/" + "-" * 35 + "|555Hunter|121" + "-" * 35 + "\\"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|121|||n" + x + " " *(76 - len(x)) + "|121|||n"
        stringout += "\n|121\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class BeastInfo(Command):
    key = "beastinfo"
    lock = "cmd:all()"
    infostring = ("The Begotten, Children, and more sobriquets besides, Beasts are monsters conjured from humanity's darkest nightmares and legends. A human mind paired with "
                  "an insatiable Hunger, some attempt to justify their feeding while others struggle to come to terms with it. The Beast sphere is currently "+settings.BEAST_STATUS.lower()+""
                  " and like some other spheres requires a mature mind to handle. Mature in the sense of honest, trustworthy, and able to work through problems rather than the"
                  " idea of being able to handle vice and violence. Playing a Beast is not license to lash out at all other players. Rather, you are wholly responsible as a "
                  "player for how you choose to have your character handle their Hunger. This sphere is not an excuse to be petty or toxic to the game.")
    def func(self):
        stringout = "|101/" + "-" * 36 + "|555Beast|101"+"-" * 35 + "\\"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|101|||n" + x + " " * (76 - len(x)) + "|101|||n"
        stringout += "\n|101\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class PrometheanInfo(Command):
    key = "prometheaninfo"
    lock = "cmd:all()"
    infostring = ("Attempts at creating or restoring life gone wrong, Prometheans are almost universally reviled by the world around them and spread blight wherever they go. "
                  "theirs is not a happy lot, yet their goal remains almost universally the same: Humanity. The great work of alchemy in creation of the philosopher's stone is "
                  "generally taken by the Created to be a metaphor for self-improvement which they have ultimately embraced. The Promethean sphere is currently "
                  "closed indefinitely, as the extremely story-focused progression of prometheans is not an amount of attention that staff can devote to single characters. Plans "
                  "may be made in the future however, to house-rule their mechanics to a more experience based progression.")
    def func(self):
        stringout = "|313/" + "-" * 33 + "|555Promethean|313" + "-" * 33 + "\\"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|313|||n" + x + " " * (76 - len(x)) + "|313|||n"
        stringout += "\n|313\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class MummyInfo(Command):
    key = "mummyinfo"
    lock = "cmd:all()"
    infostring = ("The Arisen, tasked with defending their Judge's interests in the mortal world. Mummies are rather sparsely distributed on an individual basis, yet their "
                "common cultural roots provide little reason for conflict. They are after all, scions of the great empire of Irem. Why should they squabble as their "
                "lessers do? Mummies are currently closed indefinitely, as some of their powers are unbalanced with regards to a MUSH and their structure is built around "
                "elements such as a fluctuating powerstat and several spendable pools. Hence, they are not truly suited to community and balanced gameplay.")
    def func(self):
        stringout = "|440/" + "-" * 35 +"|555Mummy|440" + "-" * 36 + "\\"
        wrapstring = wrap(self.infostring, 76)
        for x in wrapstring:
            stringout += "\n|440|||n" + x + " " * (76 - len(x)) + "|440|||n"
        stringout += "\n|440\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class DemonInfo(Command):
    key = "demoninfo"
    lock = "cmd:all()"
    infostring = ("Renegade servants of the God-Machine, Demons are those wishing to slip the leash of their enigmatic master once and for all while playing a constant game of "
                  "cat and mouse versus their former comrades. The demon sphere is currently closed indefinitely, due to many of their balancing elements relying on how noticeable "
                  "they are to the god-machine, as well as plot-based progression involving acquiring interlocks and their cipher. As a result, they will require moderate house-ruling"
                  " prior to ever being allowed.")
    def func(self):
        stringout = "|223/" + "-" * 35 + "|555Demon|223" + "-" * 36 + "\\"
        wrapstring = wrap(self.infostring,76)
        for x in wrapstring:
            stringout += "\n|223|||n" + x + " " * (76 - len(x)) + "|223|||n"
        stringout += "\n|223\\" + "-" * 76 + "/|n"
        self.caller.msg(stringout)
class SetConcept(Command):
    """
    Used to set your concept.
    Usage:
        +concept <concept>
    """
    key = "+concept"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def parse(self):
        self.args = self.args.strip()
    def func(self):
        self.caller.db.concept = self.args
        self.caller.msg("Concept set to: "+self.args)
class SetDOB(default_cmds.MuxCommand):
    """
    Used to set your date of birth.
    
    Usage:
        +dob <day> <month> <year>
    """
    key = "+dob"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def func(self):
        self.caller.db.dob_day = int(self.arglist[0])
        self.caller.db.dob_month = int(self.arglist[1])
        self.caller.db.dob_year = int(self.arglist[2])
        self.caller.msg("Date of birth set to: " + date(1900,self.arglist[1],1).strftime("%b") +" "+ str(self.arglist[0]) + " " + str(self.arglist[2]))
class SetDOE(default_cmds.MuxCommand):
    """
    Sets your date of Embrace, pretty simple.
    
    Usage:
        +doe <day> <month> <year>
    """
    key = "+doe"
    lock = "cmd:attr(template,Vampire)"
    help_category="Chargen"
    def func(self):
        if self.caller.location.db.name != "Chargen" or self.caller.db.approved == True:
            self.caller.msg("You can only set your date of Embrace in chargen!")
            return
        self.caller.db.doe_day = int(self.arglist[0])
        self.caller.db.doe_month = int(self.arglist[1])
        self.caller.db.doe_year = int(self.arglist[2])
        self.caller.msg("Date of embrace set to: " + date(1900,self.arglist[1],1).strftime("%b") + " " + str(self.arglist[0]) +" " + str(self.arglist[2]))
class SetFullName(Command):
    """
    Used to set your full name
    Usage:
        +fullname <Full Name>
    """
    key = "+fullname"
    lock = "cmd:inside(Chargen)"
    help_category="Chargen"
    def parse(self):
        self.args = self.args.lstrip()
    def func(self):
        self.caller.db.icname = self.args
        self.caller.msg("Full name set to: "+self.args)
#------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
#------------------------------------------------------------

#from evennia.utils import utils
#class MuxCommand(Command):
#    """
#    This sets up the basis for a MUX command. The idea
#    is that most other Mux-related commands should just
#    inherit from this and don't have to implement much
#    parsing of their own unless they do something particularly
#    advanced.
#
#    Note that the class's __doc__ string (this text) is
#    used by Evennia to create the automatic help entry for
#    the command, so make sure to document consistently here.
#    """
#    def has_perm(self, srcobj):
#        """
#        This is called by the cmdhandler to determine
#        if srcobj is allowed to execute this command.
#        We just show it here for completeness - we
#        are satisfied using the default check in Command.
#        """
#        return super(MuxCommand, self).has_perm(srcobj)
#
#    def at_pre_cmd(self):
#        """
#        This hook is called before self.parse() on all commands
#        """
#        pass
#
#    def at_post_cmd(self):
#        """
#        This hook is called after the command has finished executing
#        (after self.func()).
#        """
#        pass
#
#    def parse(self):
#        """
#        This method is called by the cmdhandler once the command name
#        has been identified. It creates a new set of member variables
#        that can be later accessed from self.func() (see below)
#
#        The following variables are available for our use when entering this
#        method (from the command definition, and assigned on the fly by the
#        cmdhandler):
#           self.key - the name of this command ('look')
#           self.aliases - the aliases of this cmd ('l')
#           self.permissions - permission string for this command
#           self.help_category - overall category of command
#
#           self.caller - the object calling this command
#           self.cmdstring - the actual command name used to call this
#                            (this allows you to know which alias was used,
#                             for example)
#           self.args - the raw input; everything following self.cmdstring.
#           self.cmdset - the cmdset from which this command was picked. Not
#                         often used (useful for commands like 'help' or to
#                         list all available commands etc)
#           self.obj - the object on which this command was defined. It is often
#                         the same as self.caller.
#
#        A MUX command has the following possible syntax:
#
#          name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#        The 'name[ with several words]' part is already dealt with by the
#        cmdhandler at this point, and stored in self.cmdname (we don't use
#        it here). The rest of the command is stored in self.args, which can
#        start with the switch indicator /.
#
#        This parser breaks self.args into its constituents and stores them in the
#        following variables:
#          self.switches = [list of /switches (without the /)]
#          self.raw = This is the raw argument input, including switches
#          self.args = This is re-defined to be everything *except* the switches
#          self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                     no = is found, this is identical to self.args.
#          self.rhs: Everything to the right of = (rhs:'right-hand side').
#                    If no '=' is found, this is None.
#          self.lhslist - [self.lhs split into a list by comma]
#          self.rhslist - [list of self.rhs split into a list by comma]
#          self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#          All args and list members are stripped of excess whitespace around the
#          strings, but case is preserved.
#        """
#        raw = self.args
#        args = raw.strip()
#
#        # split out switches
#        switches = []
#        if args and len(args) > 1 and args[0] == "/":
#            # we have a switch, or a set of switches. These end with a space.
#            switches = args[1:].split(None, 1)
#            if len(switches) > 1:
#                switches, args = switches
#                switches = switches.split('/')
#            else:
#                args = ""
#                switches = switches[0].split('/')
#        arglist = [arg.strip() for arg in args.split()]
#
#        # check for arg1, arg2, ... = argA, argB, ... constructs
#        lhs, rhs = args, None
#        lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#        if args and '=' in args:
#            lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#            lhslist = [arg.strip() for arg in lhs.split(',')]
#            rhslist = [arg.strip() for arg in rhs.split(',')]
#
#        # save to object properties:
#        self.raw = raw
#        self.switches = switches
#        self.args = args.strip()
#        self.arglist = arglist
#        self.lhs = lhs
#        self.lhslist = lhslist
#        self.rhs = rhs
#        self.rhslist = rhslist
#
#        # if the class has the player_caller property set on itself, we make
#        # sure that self.caller is always the player if possible. We also create
#        # a special property "character" for the puppeted object, if any. This
#        # is convenient for commands defined on the Player only.
#        if hasattr(self, "player_caller") and self.player_caller:
#            if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                # caller is an Object/Character
#                self.character = self.caller
#                self.caller = self.caller.player
#            elif utils.inherits_from(self.caller, "evennia.players.players.DefaultPlayer"):
#                # caller was already a Player
#                self.character = self.caller.get_puppet(self.session)
#            else:
#                self.character = None
#
