'''
Created on Jan 14, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class BeastStatHandler(DefaultScript):
    def at_script_creation(self):
        self.db.families = ["Anakim","Makara","Namtaru","Eshmaki","Ugallu"]
        self.db.hungers = ["Tyrant","Collector","Ravager","Nemesis","Predator"]
        self.db.atavisms = []
        self.db.nightmares = []
        self.db.legends = ['Judgmental','Relentless','Unexpected','Seductive','Vicious','Watchful']
        self.db.lives = ['Parental','Shy','Cautious','Loyal','Honest','Selfless']
        atavisms = self.db.atavisms
        nightmares = self.db.nightmares
        if len(atavisms) == 0:
            atavisms.append(tuple(["Alien Allure","Makara","BtP-123"]))
            atavisms.append(tuple(["Basilisk's Touch","Namtaru","BtP-123"]))
            atavisms.append(tuple(["Cyclopean Streanth","Anakim","BtP-124"]))
            atavisms.append(tuple(["Dragonfire","Eshmaki","BtP-124"]))
            atavisms.append(tuple(["Eye of Heaven","Ugallu","Btp-124"]))
            atavisms.append(tuple(["From the Shadows","Eshmaki","BtP-125"]))
            atavisms.append(tuple(["Heart of the Ocean","Makara","BtP-125"]))
            atavisms.append(tuple(["Infestation","Namtaru","BtP-125"]))
            atavisms.append(tuple(["Limb From Limb","Eshaki","BtP-127"]))
            atavisms.append(tuple(["Looming Presence","Anakim","BtP-127"]))
            atavisms.append(tuple(["Mimir's Wisdom","Anakim","BtP-127"]))
            atavisms.append(tuple(["Monster from the Deep","Makara","BtP-128"]))
            atavisms.append(tuple(["Needs Must","Ugallu","BtP-128"]))
            atavisms.append(tuple(["Relentless Hunter","Eshmaki","BtP-129"]))
            atavisms.append(tuple(["Shadowed Soul","Namtaru","BtP-129"]))
            atavisms.append(tuple(["Siren's Treacherous Song","Makara","BtP-130"]))
            atavisms.append(tuple(["Storm-Lashed","Ugallu","BtP-130"]))
            atavisms.append(tuple(["Titanic Blow","Anakim","BtP-131"]))
            atavisms.append(tuple(["Unbreakable","Namtaru","Btp-131"]))
            atavisms.append(tuple(["Wings of The Raptor","Ugallu","BtP-132"]))
        if len(nightmares) == 0:
            nightmares.append(tuple(["All Your Teeth Are Falling Out","Common","BtP-134"]))
            nightmares.append(tuple(["Behold, My True Form!","Common","BtP-134"]))
            nightmares.append(tuple(["Bugs Everywhere!","Common","BtP-134"]))
            nightmares.append(tuple(["Everything You Do Is Worthless","Common","BtP-135"]))
            nightmares.append(tuple(["Fear Is Contagious","Common","BtP-135"]))
            nightmares.append(tuple(["Flying And Falling","Common","BtP-136"]))
            nightmares.append(tuple(["Run Away","Common","BtP-136"]))
            nightmares.append(tuple(["They are all around you","Common","BtP,136"]))
            nightmares.append(tuple(["You are alone","Common","BtP-136"]))
            nightmares.append(tuple(["You are not alone","Common","BtP-137"]))
            nightmares.append(tuple(["You can't wake up","Common","BtP-137"]))
            nightmares.append(tuple(["You cannot run","Common","BtP-137"]))
            nightmares.append(tuple(["You deserve this","Common","BtP-137"]))
            nightmares.append(tuple(["You must obey","Common","BtP-138"]))
            nightmares.append(tuple(["You will never rest","Common","BtP-138"]))
            nightmares.append(tuple(["You are infected","Vampire","BtP-138"]))
            nightmares.append(tuple(["We know all your secrets","Vampire,Mekhet","BtP-138"]))
            nightmares.append(tuple(["Your rage consumes you","Werewolf","BtP-139"]))
            nightmares.append(tuple(["Your tools betray you","Werwewolf,Iron Masters","BtP-139"]))
            nightmares.append(tuple(["You are better than them","Mage","BtP-139"]))
            nightmares.append(tuple(["The void is waiting","Mage","BtP-140"]))
            nightmares.append(tuple(["Everyone hates you","Promethean","BtP-140"]))
            nightmares.append(tuple(["You cannot kill it","Promethean,Tammuz","BtP-140"]))
            nightmares.append(tuple(["You are lost","Changeling","BtP-140"]))
            nightmares.append(tuple(["You are an imposter","Changeling,Manikin","BtP-141"]))
            nightmares.append(tuple(["Death is a prison","Sin-Eater","BtP-141"]))
            nightmares.append(tuple(["You can't take it with you","Sin-Eater,Bonepicker","BtP-142"]))
            nightmares.append(tuple(["Tabula Rasa","Mummy","BtP-142"]))
            nightmares.append(tuple(["Cursed Object","Mummy,Maa-Kep","BtP-142"]))