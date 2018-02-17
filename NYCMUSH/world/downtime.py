'''
Created on Jan 22, 2017

@author: CodeKitty
'''
from evennia import default_cmds
from textbox import StatBlock
from evennia.utils import search
from evennia import DefaultCharacter
from evennia.utils import evtable
import time
from evennia.utils import inherits_from
class DownTime(default_cmds.MuxCommand):
    """
    This command is used to both view and manage downtime. Downtime represents the amount of free time
    your character has for a given week. 
    
    Usage:
        +dt <Amount>=<Reason> The most basic of ways to spend downtime, spending however much for a given reason.
        +dt/peek <Character> Used by admins to view the downtime log of a certain character.
    """
    key = "+dt"
    aliases = ["+downtime"]
    help_category="Gameplay"
    def func(self):
        arglist = self.arglist
        args = self.args
        rhs = self.rhs
        lhs = self.lhs
        switches = self.switches
        if not args:
            self.caller.msg(evtable.EvTable("Downtime",table=self.caller.db.timelog))
            return
        elif self.IsInt(lhs):
            if rhs != "":
                if int(lhs) <= self.caller.db.downtime:
                    self.caller.db.timelog.append(self.TimeLog(int(lhs),self.caller.location.name,rhs))
                    self.caller.msg("Spending "+lhs+" hours of downtime for "+rhs)
                    self.caller.db.downtime -= int(lhs)
                    return
                else:
                    self.caller.msg("You don't have that much downtime left!")
                    return
            else:
                self.caller.msg("You must provide a reason for your downtime expenditure in order to spend it!")
        elif len(switches) > 0:
            if switches[0].lower() == "peek" and self.caller.IsAdmin():
                timelog = []
                if inherits_from(search.objects(arglist[0])[0],DefaultCharacter):
                    try:
                        for item in search.objects(arglist[0])[0].db.timelog:
                            timelog.append(item)
                        timebox = StatBlock(str(search.objects(arglist[0])[0])+"'s time log",False,timelog)
                        timebox.SetColumns(1)
                        self.caller.msg(timebox.Show()+timebox.Footer())
                    except AttributeError:
                        self.caller.msg("Character not found!")
    def TimeLog(self, amount, where, event):
        self.caller.msg("Timelog pinged")
        return
        return str("On "+ time.strftime("%b") + " "+ time.strftime("%d")+" "+ time.strftime("%Y") +" you spent "+str(amount)+" hours for \""+event+"\" while in "+str(where))
    def IsInt(self,value):
        try:
            int(value)
            return True
        except ValueError:
            return False