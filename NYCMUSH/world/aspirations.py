'''
Created on Feb 5, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from textbox import StatBlock
class AspireCmd(default_cmds.MuxCommand):
    """
    This command is used to manage aspirations. +asp by itself shows your aspirations.
    Using +asp/add and +asp/del allows you to add and remove short-term and long-term
    aspirations. Precise syntax is below.
    
    Syntax:
    
    +asp Show aspirations
    +asp/add <Short-term/long-term>=<Aspiration> Add whatever's after the equals sign as a short-term or
    long-term aspiration.
    +asp/del <Short-term/long-term>=<Aspiration> Remove a given aspiration from your list.
    +asp/beat <Number>=<Reason> Adds a beat for making progress on a given aspiration, explaining the
    progress with the reason given.
    """
    key = "+asp"
    lock = "cmd:all()"
    help_category = "Gameplay"
    def func(self):
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        args = self.args
        if switches:
            if switches[0] == 'add':
                if "=" in self.args:
                    if lhs.lower() == 'short-term':
                        if self.caller.db.shortterm:
                            if len(self.caller.db.shortterm) >= 2:
                                self.caller.msg('You can only have up to two short-term aspirations.')
                                return
                            else:
                                self.caller.db.shortterm.append(rhs)
                                self.caller.msg('You have added the short-term aspiration, "' + rhs + '"')
                                return
                        else:
                            self.caller.db.shortterm = [rhs]
                            self.caller.msg('You have added the short-term aspiration, "' + rhs + '"')
                            return
                    elif lhs.lower() == 'long-term':
                        if self.caller.db.longterm:
                            if len(self.caller.db.longterm) > 0:
                                self.caller.msg("You can't have more than one long-term aspiration.")
                                return
                            else:
                                self.caller.db.longterm = [rhs]
                                self.caller.msg('Long-term aspiration set to ' + rhs)
                                return
                        else:
                            self.caller.db.longterm = [rhs]
                            self.caller.msg('Long-term aspiration set to ' + rhs)
                            return
            elif switches[0] == 'del':
                if self.caller.db.longterm:
                    for asp in self.caller.db.longterm:
                        if asp.lower() == args.lower():
                            self.caller.db.longterm.remove(asp)
                            self.caller.msg('Aspiration, "' + asp + '" removed.')
                            return
                if self.caller.db.shortterm:
                    for short in self.caller.db.shortterm:
                        if short.lower() == args.lower():
                            self.caller.db.shortterm.remove(short)
                            self.caller.msg('Aspiration, "' + short + '" removed.')
                            return
                self.caller.msg('Invalid aspiration to delete.')
                return
            elif switches[0] == 'beat':
                if rhs:
                    try:
                        if int(lhs) == 1:
                            self.caller.AddBeat("Aspiration",self.caller.db.shortterm[0] + " " + rhs)
                            self.caller.msg('Beat added for progress on aspiration, "' + self.caller.db.shortterm[0] + '"')
                        elif int(lhs) == 2:
                            self.caller.AddBeat("Aspiration",self.caller.db.shortterm[1] + " " + rhs)
                            self.caller.msg('Beat added for progress on aspiration, "' + self.caller.db.shortterm[1] + '"')
                        elif int(lhs) == 3:
                            self.caller.AddBeat("Aspiration",self.caller.db.longterm[0] +" " + rhs)
                            self.caller.msg('Beat added for progress on aspiration, "' + self.caller.db.longterm[0] + '"')
                    except (TypeError, ValueError) as error:
                        self.caller.msg("Invalid number of aspiration.")
                else:
                    self.caller.msg("You have to provide a reason to earn a beat from an aspiration.")
                    return
            self.caller.msg('Invalid switch.')
            return
        else:
            asplist = []
            if not self.caller.db.shortterm == 0:
                asplist.append("1. None")
                asplist.append("2. None")
            elif len(self.caller.db.shortterm) == 1:
                asplist.append("1. " + self.caller.db.shortterm[0])
                asplist.append("2. None")
            elif len(self.caller.db.shortterm) == 2:
                asplist.append("1. " + self.caller.db.shortterm[0])
                asplist.append( "2. " + self.caller.db.shortterm[1])
            if not self.caller.db.longterm:
                asplist.append("3. None")
            else:
                asplist.append("3. " + self.caller.db.longterm[0])
            aspbox = StatBlock("Aspirations for " + self.caller.name, asplist)
            aspbox.SetColumns(1)
            aspbox.section = False
            self.caller.msg(str(aspbox) + "|n" + aspbox.Footer())