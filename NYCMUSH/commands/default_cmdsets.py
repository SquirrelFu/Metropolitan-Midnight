"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""
from world.multidesc import MultiDescCommand
from evennia import default_cmds
import command
from evennia import CmdSet
from world.downtime import DownTime
from world.inventory import InventoryCommand
from command import ChargenItems
from world.conditions import TiltCommand
from world.conditions import ConditionCommand
from world.weather import CheckWeather
from world.travel import MeetCommand
from evennia.contrib.gendersub import SetGender
from world.boardsystem import BoardCommand
from evennia.contrib.mail import CmdMail
from world.jobs import JobCommand
from world.jobs import RequestCommand
from world.scenesys import PlayerEmit
from world.handstatting import StatOther, ManageXP
from world.beats import BeatCommand
from world.aspirations import AspireCmd
from command import OOCMasq
from world.territory import Hunt
from world.territory import Extract
from typeclasses.rooms import AddHallow
class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(command.Roll())
        self.add(command.Sheet())
        self.add(command.MUSHHelp())
        self.add(command.SpendPool())
        self.add(command.HealthManage())
        self.add(command.Shift())
        self.add(DownTime())
        self.add(InventoryCommand())
        self.add(TiltCommand())
        self.add(ConditionCommand())
        self.add(MultiDescCommand())
        self.add(command.CensusCommand())
        self.add(command.BreakCommand())
        self.add(CheckWeather())
        self.add(command.ICCommand())
        self.add(command.OOCCommand())
        self.add(MeetCommand())
        self.add(SetGender())
        self.add(BoardCommand())
        self.add(CmdMail())
        self.add(JobCommand())
        self.add(RequestCommand())
        self.add(PlayerEmit())
        self.add(command.BookRef)
        self.add(command.ShowStaff())
        self.add(command.Prove())
        self.add(BeatCommand)
        self.add(command.SphereStatus)
        self.add(command.ShortDesc)
        self.add(command.SetStatus)
        self.add(command.NoteCommand)
        self.add(command.TimeDesc)
        self.add(AspireCmd)
        self.add(OOCMasq)
class LocationCmdSet(CmdSet):
#Used for individual locations. One per building, even if multiple rooms are attached to it.
    def at_cmdset_creation(self):
        super(LocationCmdSet, self).at_cmdset_creation()
class GridCmdSet(CmdSet):
#Used for commands attached to neighborhood rooms. Not specific locations, not overarching boroughs or NYC itself.
    def at_cmdset_creation(self):
        self.add(Hunt)
        self.add(Extract)
        self.add(AddHallow)
        super(GridCmdSet, self).at_cmdset_creation()
class ChargenCmdSet(CmdSet):
    """
    This is the command set for chargen. It's attached to the chargen class of rooms. That's it.
    """
    key = "ChargenCmdSet"
    
    def at_cmdset_creation(self):
        super(ChargenCmdSet, self).at_cmdset_creation()
        self.add(command.PowerList())
        self.add(command.SetTemplate())
        self.add(command.SetConcept())
        self.add(command.SetDOB())
        self.add(command.SetFullName())
        self.add(command.VampireInfo())
        self.add(command.WerewolfInfo())
        self.add(command.MageInfo())
        self.add(command.ChangelingInfo())
        self.add(command.HunterInfo())
        self.add(command.BeastInfo())
        self.add(command.PrometheanInfo())
        self.add(command.MummyInfo())
        self.add(command.DemonInfo())
        self.add(command.SetPower())
        self.add(command.SetStat())
        self.add(ChargenItems())
        self.add(command.TouchstoneCommand)
        self.add(command.SubmitApp())
        self.add(command.ChargenHelp())
        self.duplicates = False
class WelcomeCmdSet(CmdSet):
    key = "WelcomeCmdSet"
    
    def at_cmdset_creation(self):
        super(WelcomeCmdSet, self).at_cmdset_creation()
        self.add(command.TOS())
        self.duplicates = False
class PlayerCmdSet(default_cmds.PlayerCmdSet):
    """
    This is the cmdset available to the Player at all times. It is
    combined with the `CharacterCmdSet` when the Player puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultPlayer"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(PlayerCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
            
class AdminSet(CmdSet):
    key = "AdminSet"
    def at_cmdset_creation(self):
        super(AdminSet, self).at_cmdset_creation()
        self.add(command.Panic())
        self.add(command.CloseAll())
        self.add(command.CloseSphere())
        self.add(command.OpenAll())
        self.add(command.OpenSphere())
        self.add(command.MarkNPC())
        self.add(command.SpaceArchMastery())
        self.add(StatOther())
        self.add(command.Hide())
        self.add(command.SetPosition())
        self.add(ManageXP())
        self.add(command.ApproveChar)
class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
