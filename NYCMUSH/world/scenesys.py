'''
Created on Jan 28, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from evennia import DefaultCharacter
from evennia import DefaultScript
from evennia import create_script
class SceneCommand(default_cmds.MuxCommand):
    key = "+scene"
    aliases = ["+log"]
    
    def func(self):
        switches = self.switches
        if switches[0] == "create":
            pass
class SceneLogger(DefaultScript):
    
    def at_script_creation(self):
        self.db.chars = []
        self.db.title = []
        self.db.desc = []
        self.db.body = []
        
class PlayerEmit(default_cmds.MuxCommand):
    key = "+emit"
    def func(self):
        if self.arglist:
            if self.arglist[0] == "PROVE:" or self.arglist[0].lower() == "prove:":
                charlist = DefaultCharacter.objects.filter_family()
                self.caller.msg("Please do not attempt to spoof the proving system.")
                for char in charlist:
                    if char.IsAdmin():
                        char.msg(self.caller.name + " (" + self.caller.account.name + ")" + " has tried to spoof the proving system!")
                        continue
                return
            if "-----roll-----" in self.args or "-----Roll-----" in self.args:
                self.caller.msg("Please do not attempt to spoof dice rolls.") 
                charlist = DefaultCharacter.objects.filter_family()
                for char in charlist:
                    if char.IsAdmin():
                        char.msg(self.caller.name + " (" + self.caller.account.name + ")" + " has tried to spoof a dice roll!")
                        continue
                return
        stuffhere = self.caller.location.contents
        for char in stuffhere:
            if char.has_account:
                char.msg(self.args.replace("%t","     ").replace("%r","\n"))