'''
Created on Jan 22, 2017

@author: CodeKitty
'''
import typeclasses.rooms
from evennia import default_cmds
from downtime import DownTime
from evennia.utils import search
from evennia import create_script
import random
import time
from evennia.utils import inherits_from
import datetime
from evennia import create_channel
from evennia import DefaultScript

class TerritoryUpdater(DefaultScript):
    def at_script_creation(self):
        self.key = "Territory Updater"
        self.desc = "Updates territory health, as well as generates crisis flags based on health."
class Extract(default_cmds.MuxCommand):
    """
    Used to extract essence from a locus, or mana from a hallow based on which command is used.
    Usage:
        +locus <Amount> Extract <Amount> essence from the locus, as no roll is given in the books.
        +oblate Roll Composure plus Gnosis if applicable,and gain (Successes) mana from a hallow. 
        Takes one hour of downtime and works for proximi and mages only.
        +hallow <Amount> Extract <Amount> mana from a hallow, requires prime 3.
    """
    key = "+locus"
    aliases = ["+oblate","+hallow"]
    help_category = "Gameplay"
    def func(self):
        cmdstring = self.cmdstring
        area = self.caller.location
        arglist = self.arglist
        timeinstance = DownTime()
        if cmdstring == "+locus":
            if len(area.db.features) != 0:
                for feature in area.db.features:
                    if isinstance(feature, typeclasses.rooms.Locus):
                        try:
                            if int(arglist[0]) >= 1:
                                self.caller.PoolGain('Essence',int(arglist[0]))
                                for character in area:
                                    if character.has_account:
                                        character.msg(str(self.caller)+" extracts "+arglist[0]+" essence from the locus.")
                            else:
                                self.caller.msg("Please enter a positive number for extracting essence.")
                                return
                        except ValueError:
                            self.caller.msg("Please enter a valid value for extracting essence.")
                            return
                self.caller.msg("There's no locus here to extract essence from!")
            else:
                self.caller.msg("There's no locus here to extract essence from!")
        elif cmdstring == "+oblate":
            if self.caller.db.template == "Mage" or self.caller.db.template == "Proximus":
                if len(area.db.features) != 0:
                    for feature in area.db.features.keys():
                        if isinstance(area.db.features[feature], typeclasses.rooms.Hallow):
                            feature = area.db.features[feature]
                            if self.caller.db.downtime <= 0:
                                self.caller.msg("You don't have enough downtime to oblate at a hallow!")
                                return
                            dicepool = 0
                            dicecounter = 0
                            if self.caller.db.template == "Mage":
                                dicepool += self.caller.db.powerstat
                            dicepool += self.caller.db.attributes['Composure']
                            successes = 0
                            if feature.mana <= 0:
                                self.caller.msg("There's no mana left in this hallow!")
                                return
                            while dicecounter < dicepool:
                                diceresult = random.randint(1,10)
                                if diceresult >= 8:
                                    successes += 1
                                    if diceresult == 10:
                                        dicecounter -= 1
                                dicecounter += 1
                            if successes > 0:
                                if successes > feature.mana:
                                    drainamount = feature.mana
                                    self.caller.PoolGain('Mana',feature.Drain(drainamount))
                                    self.caller.msg("You manage to get the last "+str(drainamount)+" mana from the hallow.")
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1, self.caller.location, "oblation"))
                                    self.caller.db.downtime -= 1
                                    for character in area:
                                        if character.has_account:
                                            character.msg(str(self.caller)+" extracts "+arglist[0]+" essence from the locus through oblation.")
                                    return
                                else:
                                    self.caller.PoolGain('Mana',successes)
                                    self.caller.msg("Your meditations at the hallow grant you "+str(successes)+" mana.")
                                    feature.Drain(successes)
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1, self.caller.location, "Oblation"))
                                    self.caller.db.downtime -= 1
                                    return
                            else:
                                self.caller.msg("Despite your efforts, you gain no mana.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1, self.caller.location, "Oblation, failure."))
                                self.caller.db.downtime -= 1
                                return
                else:
                    self.caller.msg("There's no hallow here for you to perform oblations!")
            else:
                self.caller.msg("Only mages and proximi may perform oblations to gain mana.")
        elif cmdstring == "+hallow":
            if len(area.db.features) != 0:
                if self.caller.db.template == "Mage":
                    for power in self.caller.db.powers.keys():
                        if power.lower() == "prime":
                            if int(self.caller.db.powers["Prime"]) >= 3:
                                dicepool = 0
                                rote = False
                                for tech in self.caller.db.techniquelist:
                                    if tech[0].lower() == "channel mana":
                                        for skill in self.caller.db.physskills.keys():
                                            if skill.lower() == tech[1].lower() and not rote:
                                                dicepool += self.caller.db.physskills[skill]
                                                rote = True
                                                break
                                        for ment in self.caller.db.mentskills.keys():
                                            if ment.lower() == tech[1].lower() and not rote:
                                                dicepool += self.caller.db.mentskills[ment]
                                                rote = True
                                                break
                                        for soc in self.caller.db.socskills.keys():
                                            if soc.lower() == tech[1].lower() and not rote:
                                                dicepool += self.caller.db.socskills[soc]
                                                rote = True
                                                break
                                dicepool += self.caller.db.powerstat
                                dicepool += int(self.caller.db.powers["Prime"])
                                if len(self.arglist[0]) != 0:
                                    try:
                                        if int(self.arglist[0]) >= 1:
                                            dicepool -= (2 * (int(arglist[0])-1))
                                    except TypeError:
                                        self.caller.msg("Invalid amount to drain from the hallow.")
                                        return
                                dicecounter = 0
                                successes = 0
                                while dicecounter < dicepool:
                                    diceresults = random.randint(1,10)
                                    if diceresults >= 8:
                                        if diceresults == 10:
                                            dicecounter -= 1
                                        successes += 1
                                    dicecounter += 1
                                if successes > 0:
                                    if successes > feature.mana:
                                        drainamount = feature.mana
                                        self.caller.msg("You drain the last "+str(feature.mana)+" mana from the hallow.")
                                        feature.Drain(feature.mana)
                                        self.caller.PoolGain('Mana',drainamount)
                                    self.caller.msg("You drain "+self.arglist[0]+" mana from the hallow.")
                                    self.caller.PoolGain('Mana',self.arglist[0])
                                if successes >= 5:
                                    self.caller.msg("With great expertise, you drain "+self.arglist[0]+" mana from the hallow and receive an extra point for free!")
                                    self.caller.PoolGain('Mana',successes+1)
                                    feature.Drain(successes)
                                else:
                                    self.caller.msg("You fail to drain mana from the hallow.")
                            else:
                                self.caller.msg("You need the prime arcanum at three dots to channel mana without an oblation!")
                        else:
                            self.caller.msg("You need the prime arcanum at three dots to channel mana without an oblation.")
                else:
                    self.caller.msg("Only mages may channel mana directly!")
            else:
                self.caller.msg("There's no hallow here from which to extract mana!")
class Hunt(default_cmds.MuxCommand):
    """
    Used to spend downtime and automatically roll, in order to acquire your template's
    expendable pool.
    
    Usage:
        +feed[/ambush|seduce|animals] [<target>]: For vampires, rolls Strength + Streetwise for Ambush,
        Manipulation + Persuasion for Seduce, Wits + Survival for Animals. Returns (Successes)
        vitae and costs 1 hour of downtime. If a target is given, it will attempt to feed on that
        individual instead. Please note that the other individual must give their consent for you
        to feed on them, OOCly. THis does not represent IC consent, so feeding in combat is still
        possible.
        
        +sate[/family] [<downtime|amount>]=[<reason>]: For Beasts, rolls a baseline of 1 die, with extra downtime providing
        extra dice at a 1:1 ratio. If the /family switch is used, this will instead gain one satiety due to
        another supernatural entity gaining their expendable in your IC presence. Please note that
        using this feature requires that you provide a short, one-sentence reason as otherwise it
        could lead to unlimited satiety.
        
        
    """
    key = "+feed"
    aliases = ["+harvest","+sate","+drain","+reap","+hunt"]
    help_category = "Gameplay"
    def func(self):
        template = self.caller.db.template
        territory = self.caller.location
        cmdstring = self.cmdstring
        switches = self.switches
        args = self.args
        dicesuccess = 0
        timeinstance = DownTime()
        if cmdstring == "+feed":
            if template == "Vampire":
                if self.caller.db.powerstat >= 6 and not args:
                    self.caller.msg("You can't feed on common prey anymore, look to your fellow kindred for sustenance.")
                    return
                if switches[0].lower() == "ambush":
                    dicepool = self.caller.db.attributes['Strength'] + self.caller.db.sockills['Streetwise']
                    dicecount = 0
                    if int(self.caller.db.socskills['Streetwise']) == 0:
                        dicepool -= 1
                    dicesuccess = 0
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                            dicecount -= 1
                        dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You were able to find prey, and gained a total of "+str(dicesuccess) + " vitae from your hunt.")
                            self.caller.PoolGain('Vitae',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush"))
                            self.caller.db.downtime -= 1
                        else:
                            self.caller.msg("You were unable to find prey.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush"))
                            self.caller.db.downtime -= 1
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult != 10 and diceresult != 1:
                                alldice = True
                                self.caller.msg("You were unable to find prey.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush"))
                                self.caller.db.downtime -= 1
                            elif diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1:
                                alldice = True
                                self.caller.msg("Uh-oh. Something terrible happened during your hunt. A job has been sent to staff for a scene about it!")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush, dramatic failure"))
                                handlervar = search.scripts('JobHandler')
                                try:
                                    handlervar = handlervar[0]
                                except IndexError:
                                    handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                    self.caller.msg("Jobs system initialized.")
                                try:
                                    jobchan = search.channels('Jobs')[0]
                                except IndexError:
                                    jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                                return
                                self.caller.db.downtime -= 1
                        if dicesuccess > 0:
                            self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" vitae.")
                            self.caller.PoolGain('Vitae',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush"))
                            self.caller.db.downtime -= 1
                elif switches[0].lower() == "seduce":
                    dicepool = self.caller.db.attributes['Manipulation'] + self.caller.db.socskills['Persuasion']
                    dicecount = 0
                    if int(self.caller.db.socskills['Persuasion']) == 0:
                        dicepool -= 1
                    dicesuccess = 0
                    dicecount = 0
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult != 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You were able to find prey, and gained a total of "+str(dicesuccess) + " vitae from your hunt.")
                            self.caller.PoolGain('Vitae',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via seduction"))
                            self.caller.db.downtime -= 1
                        else:
                            self.caller.msg("You were unable to find prey.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via seduction, failure."))
                            self.caller.db.downtime -= 1
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult != 10 and diceresult != 1:
                                alldice = True
                                self.caller.msg("You were unable to find prey.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via seduction, failure."))
                                self.caller.db.downtime -= 1
                            elif diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1 and dicesuccess == 0:
                                alldice = True
                                self.caller.msg("Uh-oh. Something terrible happened during your hunt. A job has been sent to staff for a scene about it!")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via ambush, dramatic failure"))
                                self.caller.db.downtime -= 1
                                handlervar = search.scripts('JobHandler')
                                try:
                                    handlervar = handlervar[0]
                                except IndexError:
                                    handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                    self.caller.msg("Jobs system initialized.")
                                try:
                                    jobchan = search.channels('Jobs')[0]
                                except IndexError:
                                    jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                                return
                        if dicesuccess > 0:
                            self.caller.PoolGain('Vitae',dicesuccess)
                            self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" vitae.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting via seduction"))
                            self.caller.db.downtime -= 1
                elif switches[0].lower() == "animals":
                    if self.caller.db.powerstat > 2:
                        self.caller.msg("Your blood is much too potent to feed on animals.")
                        return
                    else:
                        dicepool = self.caller.db.attributes['Wits'] + self.caller.db.physskills['Survival']
                        dicecount = 0
                        if int(self.caller.db.physskills['Survival']) == 0:
                            dicepool -= 1
                        dicesuccess = 0
                        dicecount = 0
                        if dicepool > 0:
                            while dicecount < dicepool:
                                diceresult = random.randint(1,10)
                                if diceresult >= 8:
                                    dicesuccess += 1
                                    if diceresult != 10:
                                        dicecount -= 1
                                dicecount += 1
                            if dicesuccess > 0:
                                self.caller.PoolGain('Vitae',dicesuccess)
                                self.caller.msg("You were able to find prey, and gained a total of "+str(dicesuccess) + " vitae from your hunt.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting for animals"))
                                self.caller.db.downtime -= 1
                            else:
                                self.caller.msg("You were unable to find prey.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting for animals, failure."))
                                self.caller.db.downtime -= 1
                        else:
                            alldice = False
                            while alldice == False:
                                diceresult = random.randint(1,10)
                                if diceresult != 10 and diceresult != 1:
                                    alldice = True
                                    self.caller.msg("You were unable to find prey.")
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting for animals, failure."))
                                    self.caller.db.downtime -= 1
                                elif diceresult == 10:
                                    dicesuccess += 1
                                elif diceresult == 1 and dicesuccess == 0:
                                    alldice = True
                                    self.caller.msg("Uh-oh. Something terrible happened during your hunt. A job has been sent to staff for a scene about it!")
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting for animals, dramatic failure."))
                                    self.caller.db.downtime -= 1
                                    handlervar = search.scripts('JobHandler')
                                    try:
                                        handlervar = handlervar[0]
                                    except IndexError:
                                        handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                        self.caller.msg("Jobs system initialized.")
                                    try:
                                        jobchan = search.channels('Jobs')[0]
                                    except IndexError:
                                        jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                    gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                    gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                    commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                    handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                    jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                                    return
                                    
                            if dicesuccess > 0:
                                self.caller.PoolGain('Vitae',dicesuccess)
                                self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" vitae.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," hunting for animals"))
                                self.caller.db.downtime -= 1
        if cmdstring == "+harvest":
            if template == "Changeling":
                if len(switches)[0] == 0:
                    if "glamour" in territory.tags.all():
                        dicepool = self.caller.db.attributes['Composure'] + self.caller.db.socskills['Empathy']
                        dicecount = 0
                        if self.caller.db.skills['Empathy'] == 0:
                            dicepool -= 1
                        if dicepool > 0:
                            while dicecount < dicepool:
                                diceresult = random.randint(1,10)
                                if diceresult >= 8:
                                    dicesuccess += 1
                                    if diceresult == 10:
                                        dicecount -= 1
                                dicecount += 1
                            if dicesuccess > 0:
                                self.caller.msg("The ambient emotion washes over you, restoring "+str(dicesuccess)+" glamour.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting ambient emotion"))
                                self.caller.db.downtime -= 1
                                self.caller.db.harvest_amount += dicesuccess
                            else:
                                self.caller.msg("You fail to draw in the ambient emotion.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting ambient emotion, failure."))
                                self.caller.db.downtime -= 1
                        else:
                            alldice = False
                            while alldice == False:
                                diceresult = random.randint(1,10)
                                if diceresult == 10:
                                    dicesuccess += 1
                                elif diceresult == 1:
                                    alldice = True
                                    self.caller.msg("Uh-oh, it seems your harvesting turned into a reaping! You've lost a dot of clarity and gained all your glamour.")
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," ambient harvesting turned reaping"))
                                    self.caller.db.downtime -= 1
                                    self.caller.PoolGain('Glamour',75)
                                    self.caller.db.sanity -= 1
                                    self.caller.db.harvest_amount += 75
                                else:
                                    alldice = True
                                    self.caller.msg("You seem to struggle greatly with harvesting glamour, and are unable to gain any.")
                                    self.caller.db.downtime -= 1
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting ambient emotion, failure."))
                            if dicesuccess > 0:
                                self.caller.msg("Grasping at the strands of ambient emotion, you just barely manage to harvest "+str(dicesuccess)+" glamour.")
                                self.caller.PoolGain('Glamour',dicesuccess)
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting ambient emotion"))
                                self.caller.db.downtime -= 1
                                self.caller.db.harvest_amount += dicesuccess
                    else:
                        self.caller.msg("This isn't a place you can passively harvest from.")
                elif switches[0] == "fear":
                    dicepool = self.caller.db.attributes['Strength'] + self.caller.db.socskills['Intimidation']
                    dicecount = 0
                    if self.caller.db.skills['Intimidation'] == 0:
                        dicepool -= 1
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult == 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You manage to intimidate someone enough to harvest "+str(dicesuccess)+" glamour.")
                            self.caller.PoolGain('Glamour',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting fear"))
                            self.caller.db.downtime -= 1
                            self.caller.db.harvest_amount += dicesuccess
                        else:
                            self.caller.msg("Despite your efforts, you fail to acquire glamour through fear.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," failed harvesting of fear."))
                            self.caller.db.downtime -= 1
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1:
                                self.caller.msg("Uh-oh, it seems your harvesting turned into a reaping! You've lost a dot of clarity and refilled glamour.")
                                self.caller.PoolGain('Glamour',75)
                                self.caller.db.sanity -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," fear harvest turned reaping"))
                                self.caller.db.downtime -= 1
                            else:
                                self.caller.msg("It seems that you're unable to frighten someone effectively enough, or find anyone at all. No glamour gained.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," failed attempt at harvesting fear."))
                                self.caller.db.downtime -= 1
                        if dicesuccess > 0:
                            self.caller.msg("You just barely manage to frighten someone enough to gain "+str(dicesuccess)+" glamour.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting fear"))
                            self.caller.db.downtime -= 1
                            self.caller.PoolGain('Glamour',dicesuccess)
                elif switches[0] == "lust":
                    dicepool = self.caller.db.attributes['Manipulation'] + self.caller.db.socskills['Persuasion']
                    dicecount = 0
                    if self.caller.db.skills['Persuasion'] == 0:
                        dicepool -= 1
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult == 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You manage to seduce your way into harvesting "+str(dicesuccess) + " glamour")
                            self.caller.PoolGain('Glamour',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting lust"))
                            self.caller.db.downtime -= 1
                        else:
                            self.caller.msg("You fail to inspire lust in those around you, and harvest no glamour.")
                            self.caller.db.downtime -= 1
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting lust, failure."))
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1:
                                alldice = True
                                self.caller.msg("Uh-oh, it seems your harvesting turned into a reaping! You've lost a dot of clarity and gained all your glamour.")
                                self.caller.PoolGain('Glamour',75)
                                self.caller.db.sanity -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting lust turned reaping"))
                                self.caller.db.downtime -= 1
                            else:
                                alldice = True
                                self.caller.msg("You seem to struggle greatly with stoking the flames of passion in others, and gain no glamour.")
                                self.caller.db.downtime -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting lust, failure."))
                        if dicesuccess > 0:
                            self.caller.msg("Awkwardly stumbling through your attempts, you nevertheless manage to appear attractive enough to gain " + str(dicesuccess) + " glamour.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting lust"))
                            self.caller.db.downtime -= 1
                            self.caller.PoolGain('Glamour',dicesuccess)
                elif switches[0] == "confusion":
                    dicepool = self.caller.db.attributes['Wits'] + self.caller.db.socskills['Subterfuge']
                    dicecount = 0
                    if self.caller.db.skills['Subterfuge'] == 0:
                        dicepool -= 1
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult == 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You're able to bewilder enough people or a person strongly enough to gain "+str(dicesuccess) + " glamour.")
                            self.caller.PoolGain('Glamour',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting confusion"))
                            self.caller.db.downtime -= 1
                        else:
                            self.caller.msg("You seem to have a hard time confusing anyone.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting confusion, failure."))
                            self.caller.db.downtime -= 1
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1:
                                alldice = True
                                self.caller.msg("Uh-oh, it seems your harvesting turned into a reaping! You've lost a dot of clarity and gained all your glamour.")
                                self.caller.PoolGain('Glamour',75)
                                self.caller.db.sanity -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting confusion turned reaping."))
                                self.caller.db.downtime -= 1
                            else:
                                alldice = True
                                self.caller.msg("No-one really seems fooled, tricked, or otherwise confused by your actions.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting confusion"))
                            self.caller.db.downtime -= 1
                        if dicesuccess > 0:
                            self.caller.msg("You struggle, but your efforts to incite perplexity generate "+str(dicesuccess)+ " glamour.")
                            self.caller.PoolGain('Glamour',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," harvesting confusion"))
                            self.caller.db.downtime -= 1
            else:
                self.caller.msg("Only changelings may harvest glamour.")
        if cmdstring == "+sate":
            if template == "Beast":
                if switches[0].lower() == "family" and args:
                    self.caller.db.timelog.append(timeinstance.TimeLog(0,territory,"Family dinner due to: " + args))
                    self.caller.db.sanity += 1
                    return
                dicepool = 1
                dicecount = 0
                try:
                    if args:
                        dicepool += int(args)
                except ValueError:
                    self.caller.msg("That's an invalid amount of downtime to add!")
                    return
                while dicecount < dicepool:
                    diceresult = random.randint(1,10)
                    if diceresult >= 8:
                        dicesuccess += 1
                        if diceresult == 10:
                            dicecount -= 1
                    dicecount += 1
                if dicesuccess > 0:
                    if self.caller.db.ysplat == "Tyrant":
                        self.caller.msg("Your display of power earns you "+str(dicesuccess)+" satiety.")
                    elif self.caller.db.ysplat == "Collector":
                        self.caller.msg("You make off with some personally valuable objects earning you "+str(dicesuccess)+" satiety.")
                    elif self.caller.db.ysplat == "Nemesis":
                        self.caller.msg("You're able to punish transgressors enough to earn "+str(dicesuccess)+" satiety.")
                    elif self.caller.db.ysplat == "Predator":
                        self.caller.msg("Your prey provides enough of a challenge to earn you "+str(dicesuccess)+" satiety.")
                    elif self.caller.db.ysplat == "Ravager":
                        self.caller.msg("Your destruction earns you "+str(dicesuccess)+" satiety.")
                    if dicesuccess >= 5:
                        if dicesuccess + self.caller.db.sanity >= 10:
                            self.caller.db.sanity = 9
                        else:
                            self.caller.db.sanity += dicesuccess
                    else:
                        self.caller.db.sanity += dicesuccess
                        if args:
                            self.caller.db.timelog.append(timeinstance.TimeLog(1 + int(args),territory)," sating your horror")
                            self.caller.db.downtime -= 1 + int(args)
                        else:
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," sating your horror"))
                            self.caller.db.downtime -= 1
                        self.caller.UpdateSatiety()
                else:
                    if args:
                        self.caller.db.timelog.append(timeinstance.TimeLog(1 + int(args),territory," sating your horror."))
                        self.caller.db.downtime -= 1 + int(args)
                    else:
                        self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," sating your horror."))
                        self.caller.db.downtime -= 1
                    self.caller.msg("You fail to sate your horror, despite your best efforts.")
                    self.caller.UpdateSatiety()
            else:
                self.caller.msg("Only beasts may attempt to gain satiety.")  
        if cmdstring == "+drain":
            isvamp = False
            for merit in self.caller.db.meritlist:
                if merit[0].lower() == "psychic vampirism":
                    isvamp = True
            if isvamp:
                if switches[0].lower() == "seduce":
                    dicepool = self.caller.db.attributes['Manipulation'] + self.caller.db.socskills['Persuasion']
                    if int(self.caller.db.socskills['Persuasion']) == 0:
                        dicepool -= 1
                    dicesuccess = 0
                    dicecount = 0
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult != 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("You were able to find prey, and gained a total of "+str(dicesuccess) + " ephemera from your hunt.")
                            self.caller.PoolGain('Ephemera',dicesuccess)
                            self.caller.location.db.health -= 1
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via seduction"))
                            self.caller.db.downtime -= 1
                        else:
                            self.caller.msg("You were unable to find prey.")
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via seduction, failure"))
                            self.caller.db.downtime -= 1
                    else:
                        alldice = False
                        while alldice == False:
                            diceresult = random.randint(1,10)
                            if diceresult != 10 and diceresult != 1:
                                alldice = True
                                self.caller.msg("You were unable to find prey.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via seduction"))
                                self.caller.db.downtime -= 1
                            elif diceresult == 10:
                                dicesuccess += 1
                            elif diceresult == 1 and dicesuccess == 0:
                                alldice = True
                                self.caller.msg("You fail to find prey, and an extra complication happened along the way. Job created.")
                                handlervar = search.scripts('JobHandler')
                                try:
                                    handlervar = handlervar[0]
                                except IndexError:
                                    handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                    self.caller.msg("Jobs system initialized.")
                                try:
                                    jobchan = search.channels('Jobs')[0]
                                except IndexError:
                                    jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via seduction, dramatic failure"))
                                self.caller.db.downtime -= 1
                                return
                        if dicesuccess > 0:
                            self.caller.PoolGain('Ephemera',dicesuccess)
                            self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" ephemera.")
                            self.caller.location.db.health -= 1
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via seduction"))
                            self.caller.db.downtime -= 1
                if switches[0].lower() == "ambush":
                        dicepool = self.caller.db.attributes['Strength'] + self.caller.db.skills['Streetwise']
                        dicecount = 0
                        if int(self.caller.db.skills['Stretwise']) == 0:
                            dicepool -= 1
                        dicesuccess = 0
                        if dicepool > 0:
                            while dicecount < dicepool:
                                diceresult = random.randint(1,10)
                                if diceresult >= 8:
                                    dicesuccess += 1
                                dicecount -= 1
                            dicecount += 1
                            if dicesuccess > 0:
                                self.caller.msg("You were able to find prey, and gained a total of "+str(dicesuccess) + " ephemera from your hunt.")
                                self.caller.PoolGain('Ephemera',dicesuccess)
                                self.caller.location.db.health -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via ambush"))
                                self.caller.db.downtime -= 1
                            else:
                                self.caller.msg("You were unable to find prey.")
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via ambush, failure"))
                                self.caller.db.downtime -= 1
                        else:
                            alldice = False
                            while alldice == False:
                                diceresult = random.randint(1,10)
                                if diceresult != 10 and diceresult != 1:
                                    alldice = True
                                    self.caller.msg("You were unable to find prey.")
                                    self.caller.location.db.health -= 1
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via ambush"))
                                    self.caller.db.downtime -= 1
                                elif diceresult == 10:
                                    dicesuccess += 1
                                elif diceresult == 1 and dicesuccess == 0:
                                    alldice = True
                                    self.caller.msg("You gain no ephemera, and an extra complication happened along the way. Job created.")
                                    self.caller.location.db.health -= 1
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via ambush, dramatic failure"))
                                    self.caller.db.downtime -= 1
                                    handlervar = search.scripts('JobHandler')
                                    try:
                                        handlervar = handlervar[0]
                                    except IndexError:
                                        handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                        self.caller.msg("Jobs system initialized.")
                                    try:
                                        jobchan = search.channels('Jobs')[0]
                                    except IndexError:
                                        jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                    gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                    gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                    commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                    handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                    jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                            if dicesuccess > 0:
                                self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" ephemera.")
                                self.caller.PoolGain('Ephemera',dicesuccess)
                                self.caller.location.db.health -= 1
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via ambush"))
                                self.caller.db.downtime -= 1
                if switches[0].lower() == "skim":
                    dicepool = self.caller.db.attributes['Wits'] + self.caller.db.skills['Occult']
                    for merit in self.caller.db.meritlist:
                        if merit[0].lower() == "psychic vampirism":
                            dicepool += int(merit[1])
                        elif merit[0].lower() == "breath stealer":
                            if int(merit[1]) > 2:
                                dicepool += 2
                            else:
                                dicepool += int(merit[1])
                    dicecount = 0
                    if self.caller.db.skills['Occult'].score == 0:
                        dicepool -= 3
                    if dicepool > 0:
                        while dicecount < dicepool:
                            diceresult = random.randint(1,10)
                            if diceresult >= 8:
                                dicesuccess += 1
                                if diceresult == 10:
                                    dicecount -= 1
                            dicecount += 1
                        if dicesuccess > 0:
                            self.caller.msg("Managing brief but meaningful contact with your prey, you gain "+str(dicesuccess)+" ephemera.")
                            self.caller.PoolGain('Ephemera',dicesuccess)
                            self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via skimming"))
                            self.caller.db.downtime -= 1
                        else:
                            while alldice == False:
                                diceresult = random.randint(1,10)
                                if diceresult != 10 and diceresult != 1:
                                    alldice = True
                                    self.caller.msg("You were unable to find prey.")
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via skimming, failure"))
                                    self.caller.db.downtime -= 1
                                elif diceresult == 10:
                                    dicesuccess += 1
                                elif diceresult == 1 and dicesuccess == 0:
                                    alldice = True
                                    self.caller.msg("You fail to gain ephemera, and an extra complication arises. Job created.")
                                    handlervar = search.scripts('JobHandler')
                                    try:
                                        handlervar = handlervar[0]
                                    except IndexError:
                                        handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
                                        self.caller.msg("Jobs system initialized.")
                                    try:
                                        jobchan = search.channels('Jobs')[0]
                                    except IndexError:
                                        jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
                                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                    gen_deadline = datetime.datetime.now() + datetime.timedelta(days=7)
                                    gen_deadline = gen_deadline.time.strftime("%a %b %d")
                                    commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                    handlervar.db.joblist[handlervar.db.buckets['PLOT'] - 1].append(["Dramatic Hunting Failure: " + self.caller.location.name,self.caller.id,date,gen_deadline,tuple([self.caller.id,self.caller.name + " failed dramatically at hunting using the " + switches[0] +" method while in " + self.caller.location + " Please plan accordingly.",commenttime])])
                                    jobchan.msg(self.caller.name + " has dramatically failed in hunting in " + self.caller.location.name + " and as a result, created a job.")
                                    self.caller.location.db.health -= 1
                                    self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via skimming, dramatic failure"))
                                    self.caller.db.downtime -= 1
                                    
                            if dicesuccess > 0:
                                self.caller.msg("Phew, that was hard. Still, you managed to find "+str(dicesuccess)+" ephemera.")
                                self.caller.PoolGain('Ephemera',dicesuccess)
                                self.caller.db.timelog.append(timeinstance.TimeLog(1,territory," draining life-force via skimming"))
                                self.caller.db.downtime -= 1
                                
            else:
                self.caller.msg("Only psychic vampires may attempt to drain someone for ephemera.")
        if cmdstring == "+reap":
            if template == "Changeling":
                if not switches:
                    self.caller.msg("WARNING! Reaping from an area, while it will refill your glamour completely, costs you a dot of clarity. If you're sure you want to do this, use +reap/confirm. Likewise, it also exerts additional pressure on an area.")
                    return
                elif switches[0].lower() == "confirm":
                    self.caller.PoolGain('Glamour',75)
                    self.caller.db.sanity -= 1
                    self.caller.location.db.health -= 1
                    self.caller.msg("Reaping performed, dot of clarity removed.")
                    return
        if cmdstring == "+hunt":
            if template == "Werewolf":
                for rite in self.caller.db.techniquelist:
                    if rite[0] == "Sacred Hunt":
                        if self.args == "1":
                            dicepool = self.caller.attributes['Strength'] + self.caller.db.physskils['Survival']
                            dicepool -= 3
                            dicecount = 0
                            successes = 0
                            while dicecount < 0:
                                huntdie = random.randint(1,10)
                                if huntdie >=  8:
                                    successes += 1
                                    if huntdie == 10:
                                        dicecount -= 1
                                dicecount += 1
                            if 11 > successes > 0:
                                self.caller.msg("Tearing into the spirit, you regain " (successes) + " essence.")
                                self.caller.PoolGain('Essence',successes)
                                self.caller.db.downtime -= 3
                                if self.location.db.health > halfhealth:
                                    self.location.db.health -= 2
                                    return
                                elif self.location.db.health <= halfhealth:
                                    self.location.db.health += 2
                                return
                self.caller.msg("You lack the rite of the sacred hunt.")
                return
            else:
                self.caller.msg("Only werewolves may initiate the sacred hunt.")
                return