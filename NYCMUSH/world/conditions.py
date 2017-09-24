'''
Created on Jan 22, 2017

@author: CodeKitty
'''
from evennia import default_cmds
from textbox import StatBlock
from evennia import DefaultScript
from evennia.utils import search
from evennia import create_script
class TiltCommand(default_cmds.MuxCommand):
    """
    This command is used to add and remove tilts from the character. Environmental tilts do not automatically affect the room,
    but rather represent that your character is currently affected by that environmental tilt.
    
    Syntax:
    +tilt/all Show all tilts in the game.
    +tilt/env Show all environmental tilts
    +tilt <Tilt Name> Add a tilt to your sheet.
    +tilt/rem [<Tilt name>] With a given name, removes that tilt from your sheet.
    +tilt/clear Removes all your tilts
    +tilt/lair Shows all lair traits Beasts can impose, minor traits listed alphabetically first, then major traits.
    """
    key = "+tilt"
    help_category = "Gameplay"
    aliases = ["+tilts"]
    def func(self):
        tilts = []
        args = self.args
        switches = self.switches
        personal = []
        environ = []
        lair = []
        try:
            condscript = search.scripts('ConditionReference')[0]
        except IndexError:
            condscript = create_script('world.conditions.ConditionHandler',key='ConditionReference',persistent=True)
        for tilt in condscript.db.personaltilt:
            personal.append(tilt)
            tilts.append(tilt)
        for thing in condscript.db.envirotilt:
            environ.append(thing)
            tilts.append(thing)
        for trait in condscript.db.lairtilts:
            lair.append(trait)
            tilts.append(trait)
        lair.sort()
        for trait2 in condscript.db.majortilts:
            lair.append(trait2)
            tilts.append(trait2)
        tilts.sort()
        environ.sort()
        personal.sort()
        if args == "":
            if switches:
                if switches[0] == "all":
                    boxout = StatBlock("Tilts",False,tilts)
                    self.caller.msg(boxout.Show() + boxout.Footer())
                elif switches[0] == "env":
                    boxout = StatBlock("Environmental Tilts",False,environ)
                    self.caller.msg(boxout.Show() + boxout.Footer())
                elif switches[0] == "lair":
                    boxout = StatBlock("Lair Traits",False,lair)
                    self.caller.msg(boxout.Show() + boxout.Footer())
                elif switches[0] == "clear":
                    for character in self.caller.location.contents:
                        self.caller.db.tilts = []
                        if character.has_player and character != self.caller:
                            character.msg(self.caller.name + " just cleared their tilts!")
                        elif character == self.caller:
                            self.caller.msg("You've cleared your tilts!")
            else:
                self.caller.msg("Either enter a tilt to apply to your character, or a switch to view tilt categories.")
        else:
            if switches:
                if switches[0] == "rem":
                    for tilt in self.caller.db.tilts:
                        if tilt.lower() == args.lower():
                            self.caller.db.tilts.remove(tilt)
                            self.caller.msg(tilt + " removed.")
                            return
                        elif args.lower() == "burning" and tilt.lower() == "burning (personal)":
                            self.caller.db.tilts.remove(tilt)
                            self.caller.msg(args.title() +" tilt removed.")
                            return
            for item in personal:
                if args.lower() == item.lower():
                    for tilt in self.caller.db.tilts:
                        if tilt.lower() == args.lower():
                            self.caller.msg("You already have that tilt affecting you!")
                            return
                    self.caller.db.tilts.append(item)
                    self.caller.msg(item +" tilt added.")
                    return
                elif args.lower() == "burning" and item.lower() == "burning (personal)":
                    for tilt in self.caller.db.tilts:
                        if tilt.lower() == "burning (personal)":
                            self.caller.msg("You already have that tilt affecting you!")
                            return
                    self.caller.db.tilts.append(item)
                    self.caller.msg(args.title() +" tilt added.")
                    return
            self.caller.msg("Invalid tilt to add!")
class ConditionCommand(default_cmds.MuxCommand):
    """
    This command is used to add and remove conditions from your character, as well as log whether they're resolved or else
    fade normally. Marking a condition as resolved requires a reason, and will add a beat to your log for such a thing.
    
    Syntax:
    +cond/all Show all possible tilts.
    +cond/persist [<Condition>] Without a condition name, show all persistent conditions in the game. 
    With a name, add a given condition as persistent if it can be persistent.
    +cond/temp [<Condition>] Without a condition name, show all non-persistent conditions in the game. 
    With a name, add a given condition as non-persistent if it can be.
    +cond/fade <Condition> Remove a condition from your sheet, does not award a beat.
    +cond/resolve <Condition>=<Reason> Remove a condition from your sheet for meeting the resolution criteria, awards a beat.
    Must provide a reason, a sentence or two at most.
    +cond/beat <Condition>=<Reason> Adds a beat to your beat log for being hindered by a condition in a way as specified by
    the reason given.
    """
    key = "+condition"
    aliases = ["+cond"]
    help_category = "Gameplay"
    def func(self):
        conditions = []
        args = self.args
        try:
            condscript = search.scripts('ConditionReference')[0]
        except IndexError:
            condscript = create_script('world.conditions.ConditionHandler',key='ConditionReference',persistent=True)
        conditions.extend(condscript.db.conditionlist)
        conditions.sort()
        condout = []
        switches = self.switches
        persistlist = []
        templist = []
        template = self.caller.db.template
        rhs = self.rhs
        if template == "Vampire":
            for fang in condscript.db.vamplist:
                condout.append(fang[0])
        for item in conditions:
            condout.append(item[0])
            if item[1] == True:
                persistlist.append(item[0])
            else:
                templist.append(item[0])
        if args == "":
            if len(switches) > 0:
                if switches[0] == "all":
                    boxout = StatBlock("Conditions",False,condout)
                    self.caller.msg(boxout.Show() + boxout.Footer())
                    return
                elif switches[0] == "persist":
                    boxout = StatBlock("Persistent Conditions",False,persistlist)
                    self.caller.msg(boxout.Show() + boxout.Footer())
                    return
                elif switches[0] == "temp":
                    boxout = StatBlock("Non-Persistent Conditions",False,templist)
                    self.caller.msg(boxout.Show()+boxout.Footer())
                    return
                else:
                    self.caller.msg("Invalid switch.")
                    return
        else:
            if len(switches) > 0:
                for cond in condout:
                    if self.arglist[0].lower() == cond.lower():
                        if len(switches) > 0:
                            if switches[0] == "persist":
                                if cond == "Gorged" or cond == "Ravenous" or cond == "Sated" or cond == "Slumbering" or cond == "Starving":
                                    self.caller.msg("You can't add or remove these conditions.")
                                    return
                                inflictvar = self.caller.Inflict(cond, True)
                                try:
                                    int(inflictvar)
                                    self.caller.msg("This condition cannot be added as persistent.")
                                    return
                                except ValueError:
                                    self.caller.msg(cond[0] +" added as a persistent condition.")
                                    return
                            elif switches[0] == "fade":
                                if "(Persistent)" in cond:
                                    self.caller.msg("Persistent conditions don't fade normally.")
                                    return
                                for condcheck in self.caller.db.conditions:
                                    if condcheck.lower() == self.arglist[0].lower():
                                        self.caller.Resolve(condcheck)
                                        self.caller.msg(condcheck + " has faded.")
                                        return
                                    elif self.arglist[0].lower() in condcheck.lower():
                                        self.caller.Resolve(condcheck)
                                        self.caller.msg(condcheck + " has faded.")
                                        return
                            elif switches[0] == "resolve":
                                if rhs != None:
                                    if cond == "Gorged" or cond == "Ravenous" or cond == "Sated" or cond == "Slumbering" or cond == "Starving":
                                        self.caller.msg("You can't add or remove these conditions.")
                                        return
                                    elif self.arglist[0].lower() in condcheck.lower():
                                        self.caller.Resolve(condcheck)
                                        self.caller.AddBeat("Condition","Resolved " + condcheck + ": " + rhs)
                                        self.caller.msg(condcheck + " has been resolved for a beat.")
                                        return
                                else:
                                    self.caller.msg("You need to provide a reason for resolving a condition for a beat.")
                                    return
                            elif switches[0] == "beat":
                                if rhs != None:
                                    self.caller.AddBeat("Condition","Beat from " + cond + ": " + rhs)
                                    self.caller.msg("Beat added for being hindered by " + cond)
                                    return
                                else:
                                    self.caller.msg("You need to explain the way in which the condition hindered your character.")
                                    return
                            else:
                                self.caller.msg("Invalid switch.")
                                return
                        else:
                            inflictvar = self.caller.Inflict(cond)
                            self.caller.msg(cond[0] + "added to your conditions list.")
                            return
                self.caller.msg("Invalid condition.")
                return
            else:
                if "(" in args:
                    for cond in condout:
                        if self.arglist[0].lower() == cond.lower():
                            inflictvar = self.caller.Inflict(self.args.title())
                            if inflictvar == True:
                                self.caller.msg(self.args + " added to your conditions list as a persistent condition.")
                                return
                            elif inflictvar == False:
                                self.caller.msg(self.args + " added to your conditions list.")
                                return
                            else:
                                self.caller.msg("Invalid persistence.")
                                return
                else:
                    for cond in condout:
                        if self.args.lower() == cond.lower():
                            inflictvar = self.caller.Inflict(self.args.title())
                            if inflictvar == True:
                                self.caller.msg(self.args + " added to your conditions list as a persistent condition.")
                                return
                            elif inflictvar == False:
                                self.caller.msg(self.args + " added to your conditions list.")
                                return
                            else:
                                self.caller.msg("Invalid persistence.")
                                return
class ConditionHandler(DefaultScript):
    def at_script_creation(self):
        self.db.conditions = []
        self.db.conditionlist = []
        self.db.dreamlist = []
        self.db.infectedlist = []
        self.db.vamplist = []
        self.db.wolflist = []
        self.db.magelist = []
        self.db.personaltilt = []
        self.db.envirotilt = []
        self.db.changelinglist = []
        self.db.demonlist = []
        self.db.beastlist = []
        self.db.prometheanlist = []
        self.db.lairtilts = []
        self.db.majortilts = []
        condlist = self.db.conditionlist
        dreamlist = self.db.dreamlist
        sicklist = self.db.infectedlist
        vamplist = self.db.vamplist
        wolflist = self.db.wolflist
        magelist = self.db.magelist
        pers = self.db.personaltilt
        enviro = self.db.envirotilt
        changelist = self.db.changelinglist
        demonlist = self.db.demonlist
        beastlist = self.db.beastlist
        promlist = self.db.prometheanlist
        lair = self.db.lairtilts
        major = self.db.majortilts
        pers.append("Arm Wrack")
        pers.append("Beaten Down")
        pers.append("Blinded")
        enviro.append("Blizzard")
        pers.append("Deafened")
        pers.append("Drugged")
        enviro.append("Earthquake")
        enviro.append("Extreme Cold")
        enviro.append("Extreme Heat")
        enviro.append("Flooded")
        enviro.append("Heavy Rain")
        enviro.append("Heavy Winds")
        enviro.append("Ice")
        pers.append("Immobilized")
        pers.append("Insane")
        pers.append("Insensate")
        pers.append("Knocked Down")
        pers.append("Leg Wrack")
        pers.append("Poisoned")
        pers.append("Sick")
        pers.append("Stunned")
        pers.append("Bleeding")
        pers.append("Burning (Personal)")
        pers.append("Pierced Armor")
        pers.append("Pinned")
        enviro.append("Poor Light")
        enviro.append("Avalanche")
        enviro.append("Drowning")
        lair.append("Cramped")
        lair.append("Crosswinds")
        lair.append("Currents")
        lair.append("Downpour")
        lair.append("Echoing")
        lair.append("Fog")
        lair.append("Jagged")
        lair.append("Maze")
        lair.append("Sealed Exits")
        lair.append("Slick")
        lair.append("Steam")
        lair.append("Stench")
        lair.append("Stinging")
        lair.append("Swarms")
        lair.append("Thunderous")
        lair.append("Thin Air")
        lair.append("Undergrowth")
        lair.append("Unstable")
        major.append("Burning (Environmental)")
        major.append("Corrosive")
        major.append("Crushing")
        major.append("Darkness")
        major.append("Decayed")
        major.append("Diseased")
        major.append("Disruption")
        major.append("Earthquake")
        major.append("Engulfing")
        major.append("Electrified")
        major.append("Exposed")
        major.append("Heavy")
        major.append("Hurricane")
        major.append("Mirages")
        major.append("Noxious Gases")
        major.append("Suffocating")
        major.append("Razored")
        major.append("Rotting")
        major.append("Toxic")
        major.append("Viscous")
        condlist.append(tuple(["Amnesia",True]))
        condlist.append(tuple(["Blind",False,True]))
        condlist.append(tuple(["Broken",True]))
        condlist.append(tuple(["Bonded",False]))
        condlist.append(tuple(["Connected",False]))
        condlist.append(tuple(["Crippled",True]))
        condlist.append(tuple(["Deprived",False,True]))
        condlist.append(tuple(["Embarrassing Secret",False]))
        condlist.append(tuple(["Fugue",True]))
        condlist.append(tuple(["Guilty",False]))
        condlist.append(tuple(["Informed",False]))
        condlist.append(tuple(["Inspired",False]))
        condlist.append(tuple(["Leveraged",False]))
        condlist.append(tuple(["Lost",False]))
        condlist.append(tuple(["Madness",True]))
        condlist.append(tuple(["Mute",True]))
        condlist.append(tuple(["Notoriety",False]))
        condlist.append(tuple(["Obsession",False]))
        condlist.append(tuple(["Shaken",False]))
        condlist.append(tuple(["Spooked",False]))
        condlist.append(tuple(["Steadfast",False]))
        condlist.append(tuple(["Swooning",False]))
        condlist.append(tuple(["Fixated",False]))
        condlist.append(tuple(["Hunted",True]))
        condlist.append(tuple(["Lethargic",False]))
        condlist.append(tuple(["Oblivious",False]))
        condlist.append(tuple(["Reluctant Aggressor",False]))
        condlist.append(tuple(["Surveiled",False]))
        dreamlist.append(tuple(["Missing Time",True]))
        dreamlist.append(tuple(["Endgame",True]))
        dreamlist.append(tuple(["Latent Programming",True]))
        sicklist.append(tuple(["Latent Symptoms",False]))
        sicklist.append(tuple(["Acute Symptoms",False]))
        sicklist.append(tuple(["Symptomatic Flareup",False]))
        sicklist.append(tuple(["Progressive Infection",False]))
        condlist.append(tuple(["Addicted",True]))
        condlist.append(tuple(["Bestial",False]))
        condlist.append(tuple(["Charmed",True]))
        condlist.append(tuple(["Competitive",True]))
        condlist.append(tuple(["Confused",False]))
        condlist.append(tuple(["Delusional",False,True]))
        vamplist.append(tuple(["Dependent",True]))
        condlist.append(tuple(["Distracted",False]))
        condlist.append(tuple(["Drained",False]))
        vamplist.append(tuple(["Ecstatic",False]))
        condlist.append(tuple(["Enervated",True]))
        condlist.append(tuple(["Enslaved",True]))
        condlist.append(tuple(["Enthralled",True]))
        condlist.append(tuple(["False Memories",True]))
        condlist.append(tuple(["Frightened",False]))
        vamplist.append(tuple(["Humbled",False]))
        condlist.append(tuple(["Intoxicated",False]))
        vamplist.append(tuple(["Jaded",False]))
        vamplist.append(tuple(["Languid",False]))
        condlist.append(tuple(["Mesmerized",False]))
        condlist.append(tuple(["Obsession",True]))
        vamplist.append(tuple(["Raptured",False]))
        vamplist.append(tuple(["Sated",False]))
        condlist.append(tuple(["Scarred",False]))
        condlist.append(tuple(["Soulless",True]))
        vamplist.append(tuple(["Stumbled",False]))
        condlist.append(tuple(["Subservient",True]))
        vamplist.append(tuple(["Tainted",False]))
        vamplist.append(tuple(["Tempted",False]))
        condlist.append(tuple(["Thrall",True]))
        condlist.append(tuple(["Wanton",False]))
        condlist.append(tuple(["Atavism",False]))
        condlist.append(tuple(["Awestruck",True]))
        wolflist.append(tuple(["Ban",False]))
        condlist.append(tuple(["Berserk",False]))
        condlist.append(tuple(["Cowed",False]))
        wolflist.append(tuple(["Cunning",False]))
        condlist.append(tuple(["Demoralized",False]))
        condlist.append(tuple(["Easy Prey",False]))
        wolflist.append(tuple(["Essence Overload",False]))
        condlist.append(tuple(["Exhausted",False]))
        wolflist.append(tuple(["Glorious",False]))
        wolflist.append(tuple(["Honorable",False]))
        wolflist.append(tuple(["Invisible Predator",False]))
        condlist.append(tuple(["Isolated",False]))
        wolflist.append(tuple(["Lost Tracker",False]))
        condlist.append(tuple(["Lured",True]))
        condlist.append(tuple(["Moon Taint",False]))
        condlist.append(tuple(["Mystified",False]))
        condlist.append(tuple(["Paranoid",False]))
        wolflist.append(tuple(["Pure",False]))
        condlist.append(tuple(["Reception",False]))
        condlist.append(tuple(["Resigned",False]))
        condlist.append(tuple(["Shadow Paranoia",False]))
        wolflist.append(tuple(["Shadowlashed",False]))
        wolflist.append(tuple(["Siskur-Dah",True]))
        wolflist.append(tuple(["Stumbled",False]))
        condlist.append(tuple(["Swaggering",False]))
        wolflist.append(tuple(["Symbolic Focus",False]))
        condlist.append(tuple(["Unaware",False]))
        wolflist.append(tuple(["Untraceable",False]))
        wolflist.append(tuple(["Wise",False]))
        magelist.append(tuple(["Defeated",False]))
        magelist.append(tuple(["Megalomaniacal",False,True]))
        magelist.append(tuple(["Mystery Commands",True]))
        magelist.append(tuple(["Rampant",False,True]))
        condlist.append(tuple(["Strained",False]))
        condlist.append(tuple(["Soul Shocked",False]))
        magelist.append(tuple(["Triumphant",False]))
        condlist.append(tuple(["Reticent",False]))
        changelist.append(tuple(["Acuity",False]))
        changelist.append(tuple(["Warped",False]))
        condlist.append(tuple(["Captivated",False]))
        condlist.append(tuple(["Disoriented",False]))
        demonlist.append(tuple(["Aetheric Bleed",False]))
        demonlist.append(tuple(["Demonic Disconnect",False]))
        demonlist.append(tuple(["Demonic Rage",False]))
        demonlist.append(tuple(["Plugged In",False]))
        demonlist.append(tuple(["Impostor",False]))
        demonlist.append(tuple(["Blown",True]))
        demonlist.append(tuple(["Betrayed",True]))
        demonlist.append(tuple(["Hunted",True]))
        demonlist.append(tuple(["Flagged",False]))
        demonlist.append(tuple(["Blackballed",False]))
        beastlist.append(tuple(["Gorged",True]))
        beastlist.append(tuple(["Ravenous",True]))
        beastlist.append(tuple(["Sated",True]))
        beastlist.append(tuple(["Slumbering",True]))
        beastlist.append(tuple(["Starving",True]))
        condlist.append(tuple(["Abruption",False]))
        condlist.append(tuple(["Agoraphobic",False]))
        condlist.append(tuple(["Cursed",False]))
        condlist.append(tuple(["Family Ties",True]))
        condlist.append(tuple(["Fatigued",False]))
        condlist.append(tuple(["Frightened",False]))
        condlist.append(tuple(["Paranoid",False]))
        promlist.append(tuple(["Alienated",False]))
        promlist.append(tuple(["Branded Throng",False]))
        promlist.append(tuple(["Burnout",False]))
        promlist.append(tuple(["Callous",False]))
        promlist.append(tuple(["Degaussed",False]))
        promlist.append(tuple(["Disconnected",False]))
        condlist.append(tuple(["Disquieted 1",True]))
        condlist.append(tuple(["Disquieted 2",True]))
        condlist.append(tuple(["Disquieted 3",True]))
        condlist.append(tuple(["Disquieted 4",True]))
        promlist.append(tuple(["Ephemeral Anchor",False]))
        promlist.append(tuple(["Flawed Vessel",False]))
        promlist.append(tuple(["Fragile",False]))
        promlist.append(tuple(["Greedy Brand",False]))
        promlist.append(tuple(["Hyperextended",False]))
        promlist.append(tuple(["Irritable",False]))
        promlist.append(tuple(["Kinesthesia",False]))
        promlist.append(tuple(["Murderous",False]))
        promlist.append(tuple(["Reckless",False]))
        promlist.append(tuple(["Regressive",False]))
        condlist.append(tuple(["Stricken",False]))
        promlist.append(tuple(["Synesthesia",False]))
        promlist.append(tuple(["Tormented",False]))
        promlist.append(tuple(["Watched",True]))