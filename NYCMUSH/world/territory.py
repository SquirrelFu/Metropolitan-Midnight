'''
Created on Jan 22, 2017

@author: CodeKitty
'''
import datetime
from evennia import DefaultScript
from evennia import create_channel
from evennia import create_script
from evennia import default_cmds
from evennia.objects.objects import DefaultCharacter
from evennia.utils import inherits_from
from evennia.utils import search
from evennia.utils.evmenu import get_input, EvMenu
import random
import time

from downtime import DownTime
import typeclasses.rooms


class Extract(default_cmds.MuxCommand):
    key = "+feed"
    aliases = ['+hunt','+hallow','+oblate','+drain','+sate','+locus']
    def BloodAccept(self):
        return True
    def BloodRefuse(self):
        return False
    def BloodQuery(self):
        options = {'key': 'Yes',
                   'goto': 'BloodAccept'}
          
    def func(self):
        lhs = self.lhs
        #In the case of vampires both psychic and kindred, the target they're attempting to feed ong.
        rhs = self.rhs
        #In the case of actual, undead vampires the amount of blood or vitae they are attempting to steal.
        command = self.cmdstring
        switches = self.switches
        if command == "+feed":
            if not self.caller.db.template.lower() == 'vampire':
                self.caller.msg("Only vampires can feed from humans!")
                return
            if lhs and rhs:
                try:
                    if int(rhs) > self.caller.db.powerstat:
                        self.caller.msg("You can't drain that much vitae from someone at once!")
                        return
                except TypeError:
                    self.caller.msg("Invalid amount of vitae to drain.")
                    return
                for obj in self.caller.location.contents:
                    if inherits_from(obj, DefaultCharacter):
                        if obj.has_account():
                            obj.msg(self.caller + " is trying to feed on you! Do you accept?")
                            if EvMenu(obj,'evennia.utils.evmenu',startnode='BloodQuery'):
                                self.caller.PoolGain('Vitae',int(rhs))
                                if obj.db.template == 'Vampire':
                                    self.caller.msg('You feed on ' + obj.name + ' draining ' + rhs + ' of their vitae!')
                                    obj.PoolSpend('Vitae',int(rhs))
                                    return
                                else:
                                    self.caller.msg('You drain ' + rhs + ' points worth of blood from ' + obj.name + '!')
                                    obj.Damage(2,int(rhs))
                                    return
                            
            for feature in self.caller.location().db.features:
                if feature.name.lower() == 'prey':
                    break
                self.caller.msg("There's no prey pool here to feed from!")
                return
            if switches[0] == 'ambush':
                dicepool = self.caller.db.attributes['Strength'] + self.caller.db.socskills['Streetwise']
                if self.caller.db.socskills['Streetwise'] == 0:
                    dicepool -= 1
            elif switches[0] == 'seduce':
                dicepool = self.caller.db.attributes['Manipulation'] + self.caller.db.socskills['Persuasion']
                if self.caller.db.socskills['Persuasion'] == 0:
                    dicepool -= 1
            elif switches[0] == 'animal':
                if self.caller.db.powerstat >= 3:
                    self.caller.msg('Your blood is too potent to feed from animals!')
                    return
                else:
                    dicepool = self.caller.db.attributes['Wits'] + self.caller.db.physskills['Survival'] + 1
                    if self.caller.db.physskills['Survival'] == 0:
                        dicepool -= 1
            else:
                self.caller.msg("Invalid feeding method.")
                return
            successes = self.DiceRoll(dicepool)
            if successes == -1:
                self.caller.msg("You've had a dramatic failure feeding, and a job has been created accordingly.")
                self.SubmitJob('Vampire feeding dramatic failure: ' + self.caller.name,self.caller.location,self.caller.id)
            elif successes == 0:
                self.caller.msg("Try as you might, you fail to find prey.")
            else:
                self.caller.msg("You gain " + str(successes) + " vitae from hunting!")
        if command == '+drain':
            for merit in self.caller.db.meritlist:
                if merit[0] == 'Psychic Vampirism':
                    break
                self.caller.msg("You can't drain life force if you're not a psychic vampire!")
                return
            for feature in self.caller.location().db.features:
                if feature.name.lower() == 'prey':
                    break
                self.caller.msg("There's no prey pool to drain from!")
                return
            if switches[0] == 'ambush':
                dicepool = self.caller.db.attributes['Strength'] + self.caller.db.socskills['Streetwise'] - 3
                if self.caller.db.socskills['Streetwise'] == 0:
                    dicepool -= 1
            elif switches[0] == 'seduce':
                dicepool = self.caller.db.attributes['Manipulation'] + self.caller.db.socskills['Persuasion'] - 3
                if self.caller.db.socskills['Persuasion'] == 0:
                    dicepool -= 1
            elif switches[0] == 'skim':
                dicepool = self.caller.db.attributes['Wits'] + self.caller.db.mentskills['Occult'] - 3
                if self.caller.db.mentskills['Occult'] == 0:
                    dicepool -= 3
            for merit in self.caller.db.meritlist:
                if merit[0] == 'Breath Stealer':
                    if int(merit[1]) >= 2:
                        dicepool += 2
                    else:
                        dicepool += 1
                    break
                successes = self.DiceRoll(dicepool)
            if successes == -1:
                self.caller.msg("You've had a dramatic failure whilst draining, and a job has been created accordingly.")
                self.SubmitJob('Psychic Vampire feeding dramatic failure: ' + self.caller.name,self.caller.location,self.caller.id)
            elif successes == 0:
                self.caller.msg("Try as you might, you fail to find prey.")
            else:
                self.caller.msg("You gain " + str(successes) + " ephemera from hunting!")
        if command == '+sate':
            if not self.caller.db.template == 'Beast':
                self.caller.msg('Only beasts can sate their Horrors!')
                return
    def DiceRoll(self, number):
        dicecount = 0
        successes = 0
        if number >= 1:
            while dicecount < number:
                roll = random.randint(1,10)
                if roll >= 8:
                    successes += 1
                    if roll == 10:
                        dicecount -= 1
        else:
            roll = random.randint(1,10)
            if roll == 1:
                return -1
            elif roll == 10:
                return 1
            else:
                return 0
    def SubmitJob(self, name, location, subject):
        handlervar = search.scripts('JobHandler')
        failstring = 'A critical failure has occurred while hunting in ' + location + ' staff is advised to run a scene to play out the consequences.'
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
        gen_deadline = datetime.date.today() + datetime.timedelta(days=7)
        gen_deadline = gen_deadline.strftime("%a %b %d")
        commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
        try:
            handlervar.db.joblist[handlervar.db.buckets['HUNT'] - 1].append([name,subject,date,gen_deadline,tuple([subject,failstring,commenttime])])
            jobchan.msg("A critical failure on hunting has occurred, generating a job named: " + name)
            return
        except KeyError:
            handlervar.db.buckets['HUNT'] = len(handlervar.db.buckets) + 1
            handlervar.db.joblist.append([])
            handlervar.db.deadlines.append(['7'])
            handlervar.db.joblist[handlervar.db.buckets['HUNT'] - 1].append([name,subject,date,gen_deadline,tuple([subject,failstring,commenttime])])
            jobchan.msg("A critical failure on hunting has occurred, generating a job named: " + name)
            return