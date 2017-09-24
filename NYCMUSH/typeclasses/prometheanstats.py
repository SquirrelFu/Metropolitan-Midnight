'''
Created on Jan 16, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class PrometheanStatHandler(DefaultScript):
    def at_script_creation(self):
        self.db.transmutations = []
        self.db.lineages = ["Frankenstein","Galateid","Tammuz","Osirian","Ulgan","Unfleshed","Extempore"]
        self.db.roles = []
        self.db.elpides = ['Courage','Drive','Empathy','Fear','Fury','Inspiration','Joy','Love','Sorrow','Pain']
        self.db.torments = ['Alienated','Awkward','Dejection','Logical','Merciless','Methodical','Obsession','Paranoia','Passion','Naive']
        roles = self.db.roles
        roles.append(tuple(['Aes','Bodyguard','Servant','Seeker']))
        roles.append(tuple(['Argentum','Envoy','Observer','Warden']))
        roles.append(tuple(['Aurum','Follower','Leader','Companion']))
        roles.append(tuple(['Cobalus','Confessor','Deviant','Provacateur']))
        roles.append(tuple(['Cuprum','Hermit','Sage','Watcher']))
        roles.append(tuple(['Ferrum','Exemplar','Martyr','Soldier']))
        roles.append(tuple(['Mercurius','Craftsman','Explorer','Scientist']))
        roles.append(tuple(['Phosphorum','Daredevil','Psychopomp','Whip']))
        roles.append(tuple(['Plumbum','Ascetic','Chronicler','Pilgrim']))
        roles.append(tuple(['Stannum','Outcast','Savage','Vigilante']))
        
        self.db.refinementdict = ["Aes/Bronze","Argentum/Silver","Aurum/Gold","Cobalus/Cobalt","Cuprum/Copper","Ferrum/Iron","Mercurius/Quicksilver","Phosphorum/Phosphorus","Plumbum/Lead","Stannum/Tin"]
        transmutations = self.db.transmutations
        transmutations.append(tuple(["Alchemicus","General","Stone","Aqua Regia","Spagyria","Elixir","PtC-119"]))
        transmutations.append(tuple(["Benefice","Aes","Command","Consortium","Control","Community","PtC-123"]))
        transmutations.append(tuple(["Contamination","Cobalus","Indulgence","Madness","Leverage","Suffering","PtC-125"]))
        transmutations.append(tuple(["Corporeum","Aes/Ferrum","Charites","Zephyrus","Hygeius","Motus","PtC-129"]))
        transmutations.append(tuple(["Deception","Aurum","Anonymity","Deception","Doppelganger","Stalker","PtC-131"]))
        transmutations.append(tuple(["Disquietism","Plumbum/Stannum","Externalize","Internalize","Redirect","Weaponize","PtC-134"]))
        transmutations.append(tuple(["Electrification","Stannum","Machinus","Arc","Oscillitus","Imperatus","PtC-137"]))
        transmutations.append(tuple(["Luciferus","Phosphorum","Solar Flare","Morning Star","Blaze of Glory","Beacon of Helios","PtC-141"]))
        transmutations.append(tuple(["Metamorphosis","Cuprum","Aptare","Bestiae Facies","Tegere","Verto","PtC-144"]))
        transmutations.append(tuple(["Mesmerism","Aurum/Cobalus","Phobos","Eros","Eris","Penthos","PtC-147"]))
        transmutations.append(tuple(["Saturninus","Mercurius","Heed the Call","Plumb the Fathom","Stoke the Furnace","Prime the Vessel","PtC-150"]))
        transmutations.append(tuple(["Sensorium","Argentum/Cuprum","Vitreous Humor","Receptive Humor","Stereo Humor","Somatic Humor","PtC-154"]))
        transmutations.append(tuple(["Spiritus","Argentum","Clades","Clupeum","Veritas","Laruae","PtC-158"]))
        transmutations.append(tuple(["Vitality","Ferrum","Unbowed","Unbroken","Unconquered","Unfettered","PtC-161"]))
        transmutations.append(tuple(["Vulcanus","Mercurius","Cauterio","Ignus Aspiratus","Mutatus Aspiratus","Sanctus Aspiratus","PtC-164"]))
    def Search(self,transmutein):
        transmutations = self.db.transmutations
        for x in transmutations:
            if x == transmutein[0]:
                return transmutations.index(x)
            else:
                return False
    def Affinity(self,query):
        for refinement in self.db.refinementdict:
            if query in refinement:
                break
            else:
                return False
        transmutations = self.db.transmutations
        affinitylist = []
        for x in transmutations:
            if query.lower() in x[1].lower():
                if "/" in x[1]:
                    affinitylist.append(x[1].split("/")[0])
                    affinitylist.append(x[1].split("/")[1])
            return affinitylist
    def Transmutations(self, query):
        transmutelist = []
        for thing in self.db.transmutations:
            if query in thing:
                transmutelist.append(thing.name)
            else:
                return False
        return transmutelist
            
    def GetRefinement(self, query):
        refine = self.db.refinementdict
        for ref in refine:
            if query.lower() in ref.lower():
                return ref.split("/")[0]
        return False