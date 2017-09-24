'''
Created on Jan 24, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from evennia.utils import search
from evennia import DefaultCharacter
from evennia import create_script
from evennia.scripts.scripts import DefaultScript
from evennia.utils import inherits_from
class MeetCommand(default_cmds.MuxCommand):
    key = "+meet"
    aliases = "+meetme"
    lock = "cmd:all()"
    def func(self):
        arglist = self.arglist
        switches = self.switches
        if switches:
            if arglist:
                if switches[0] == "join":
                    if self.caller.db.invitation:
                        if self.caller.db.approved:
                            if self.caller.db.invitation.db.name.lower() == self.args.lower():
                                self.caller.location.msg_contents(self.caller.name + " teleports away!")
                                inviter = search.objects(self.caller.db.invitation.db.name)[0]
                                self.caller.location = inviter.location
                                self.caller.msg(self.caller.location.return_appearance(self))
                            else:
                                self.caller.msg("You don't have an invitation to join that person.")
                                return
                        else:
                            self.caller.msg('You have to be approved to use the +meet system.')
                            return
                    else:
                        self.caller.msg("You have no invitations pending.")
                        return
                else:
                    self.caller.msg("Invalid switch.")
                    return
                    
        else:
            if arglist:
                if not self.caller.db.approved:
                    self.caller.msg('You have to be approved to use the +meet system.')
                    return
                for invite in arglist:
                    inviteperson = search.objects(str(invite))[0]
                    if inherits_from(inviteperson,DefaultCharacter):
                        if inviteperson.has_player == True:
                            invitation = "+" + "-" * 27 + "Meet" + "-" * 27 + "+\n"
                            invitation += "||" + self.caller.name +" has requested you meet {o at " + self.caller.location.name
                            invitation += " " * (120 - len(invitation)) + "||\n"
                            invitation += "||To accept this invitation, use:"
                            invitation += " " * (183 - len(invitation)) + "||\n"
                            invitation += "||+meet/join "+ self.caller.name
                            invitation += " " * (246 - len(invitation)) + "||\n"
                            invitation += "||Within the next 10 minutes."
                            invitation += " " * (309 - len(invitation)) + "||\n"
                            invitation += "+" + "-"  * 58 + "+"
                            inviteperson.msg(invitation,from_obj=self.caller)
                            inviteperson.db.invitation = create_script("world.travel.InvitationScript",key="Invitation",persistent=False)
                            inviteperson.db.invitation.db.name = self.caller.name
                        else:
                            self.caller.msg(inviteperson.name + " is not online.")
                            return
                    else:
                        self.caller.msg(inviteperson.name + " doesn't seem to exist.")
                        return
                meetstring = ""
                for people in arglist:
                    if people == arglist[len(arglist) - 1]:
                        meetstring += str(people)
                    else:
                        meetstring += str(people) +", "
                self.caller.msg("You ask to meet with "+ meetstring)
class InvitationScript(DefaultScript):
    start_delay = 60 * 10
    def at_script_creation(self):
        super(InvitationScript, self).at_script_creation()
    def at_start(self):
        self.obj.msg("Your invitation to meet "+self.db.name + " has expired.")
        del self