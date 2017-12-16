'''
Created on Jan 28, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from evennia import DefaultCharacter
from evennia import DefaultScript
from evennia import create_script
from evennia.utils import inherits_from
class SceneCommand(default_cmds.MuxCommand):
    key = "+scene"
    aliases = ["+log"]
    
    def func(self):
        switches = self.switches
        args = self.args
        if switches[0].lower() == "create":
            sceneScript = create_script('SceneLogger')
            sceneScript.AddChar(self.caller)
            sceneScript.db.sceneLocation = self.caller.location
            if args:
                sceneScript.key = args
        elif switches[0].lower() == "join":
            if not args:
                self.caller.msg("You have to add a scene ID to join a scene!")
                return
            scriptList = SceneLogger.objects.all()
            for scene in scriptList:
                try:
                    if int(args) == scene.scene_id:
                        scene.AddChar(self.caller)
                        self.caller.msg("Scene number " + str(scene.scene_id) + " joined")
                        break
                except ValueError:
                    self.caller.msg("Scene IDs are only ever numbers.")
                    return
class SceneLogger(DefaultScript):
    
    def at_script_creation(self):
        sceneList = SceneLogger.objects.filter_family()
        self.db.chars = []
        self.db.title = ""
        self.desc = ""
        self.db.body = []
        sceneCount = 0
        for scene in sceneList:
            sceneCount += 1
        self.db.scene_id = sceneCount
    def AddPose(self, charIn, poseIn):
        self.db.body.append(tuple(charIn,poseIn))
    def AddChar(self, charIn):
        self.db.chars.append(charIn)
    def SetOwner(self, ownerIn):
        self.db.scene_owner = ownerIn
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
                char.msg(self.args.replace("%t","    ").replace("%r","\n"))