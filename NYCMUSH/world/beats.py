'''
Created on Jan 23, 2017

@author: CodeKitty
'''
from evennia import default_cmds
from evennia import DefaultScript
from evennia import DefaultCharacter
import datetime
class BeatCommand(default_cmds.MuxCommand):
    """
    Used to both track and log beats, fifths of experience points.
    
    Usage:
        +beat Without anything after it, this shows your beat log.
        +beat/add <Type>=<Reason> Adds beats from a given situation, for a certain reason. Valid types include
        ST beats for running a plot, plot beats for participating in a plot and damage beats for taking enough
        damage to render your character unconscious. Beats for breaking points and conditions are automatically
        added to your log when you resolve conditions.
    """
    key = "+beat"
    aliases = "+beats"
    lock = "cmd:all()"
    help_category = "Gameplay"
    def func(self):
        lhs = self.lhs
        rhs = self.rhs
        args = self.args
        switches = self.switches
        if args == "":
            self.caller.msg(self.caller.ShowBeats())
        elif len(switches) > 0:
            if switches[0] == "add":
                if lhs.lower() == "damage":
                    if rhs != "":
                        self.caller.AddBeat("Damage",rhs)
                        if self.caller.db.template == "Vampire":
                            self.caller.msg("Beat added for taking lethal damage in your last health box.")
                            return
                        else:
                            self.caller.msg("Beat added for taking damage in your last health box.")
                            return
                    else:
                        self.caller.msg("You need to enter a reason to log a beat.")
                        return
                elif lhs.lower() == "st":
                    if rhs != "":
                        self.caller.AddBeat("ST",rhs)
                        self.caller.msg("Beat added for running a plot.")
                        return
                elif lhs.lower() == "plot":
                    if rhs != "":
                        self.caller.AddBeat("Plot",rhs)
                        self.caller.msg("Beat added for participating in a plot.")
                        return
class DramaFail(default_cmds.MuxCommand):
    key = "+dramafail"
    lock = "cmd:all()"
    def func(self):
        pass
class BeatAwarder(DefaultScript):
    def at_script_creation(self):
        curtime = datetime.datetime.now()
        if curtime.hour == 0:
            charlist = DefaultCharacter.objects.filter_family()
            for char in charlist:
                last_duration = curtime.day - char.db.last_login.day
                if char.db.approved and last_duration <= 7:
                    char.db.experience += 1
                    if char.has_player:
                        char.msg("You've been awarded a beat as your daily alottment.")
        else:
            nexttime = curtime + datetime.timedelta(days=1)
            nexttime.replace(hour=0,second=0,minute=0,microsecond=0)
            self.interval = (nexttime - curtime).total_seconds()