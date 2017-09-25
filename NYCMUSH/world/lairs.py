'''
Created on Sep 24, 2017

@author: CodeKitty
'''

from evennia import DefaultScript
from evennia import DefaultObject

class Lair(DefaultObject):
    def at_object_creation(self,name, desc="A hideout", *members):
        self.db.name = name
        self.db.owners = []
        self.db.merits = []
        self.db.mana = -1
        self.db.essence = -1
        if isinstance(members, list):
            for character in members:
                self.db.owners.append(character)
        if desc != "A hideout":
            self.db.desc = desc
    def Update(self):
        for merit in self.db.merits:
            if merit[0].lower() == "hallow":
                if self.db.mana == -1:
                    self.db.mana = int(merit[1]) * 3
            if merit[0].lower() == "dedicated locus":
                if self.db.essence == -1:
                    self.db.essence = int(merit[1])
    def Refresh(self):
        for merit in self.db.merits:
            if merit[0].lower() == "hallow":
                if self.db.mana < int(merit[1]) * 3:
                    self.db.mana += 3
                    if self.db.mana > int(merit[1]) * 3:
                        self.db.mana = int(merit[1]) * 3
            if merit[0].lower() == "dedicated locus":
                if self.db.essence < int(merit[1]):
                    self.db.essence = int(merit[1])
class LairHandler(DefaultScript):
    name = "Lair Handler"
    persistent = True
    def at_script_creation(self):
        self.db.lairlist = []
        lairlist = self.db.lairlist
        for lair in DefaultObject.objects.filter_family():
            if lair.inherits_from(Lair):
                lairlist.append(lair)