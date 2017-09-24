'''
Created on Jan 13, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class WerewolfStatHandler(DefaultScript):
    renown_names = []
    renown_ratings = [1,2,3,4,5]
    booklist = ["WtF","TP"]
    booklong = ["Werewolf: The Forsaken Second Edition","The Pack"]
    lodgelist = ['Lodge of Garm','Thousand Steel Teeth','Lodge of the Screaming Moon','Temple of Apollo','Eaters of the Dead']
    auspicelist = ["Rahu","Ithaue","Irraka","Elodoth","Cahalith"]
    blood = ['Alpha','Challenger','Destroyer','Fox','Monster','Soldier']
    bone = ['Community Organizer','Cub','Guru','Hedonist','Lone Wolf','Wallflower']
    tribelist = ["Bone Shadows","Blood Talons","Iron Masters","Hunters in Darkness","Storm Lords","Ghost Wolves"]
    def at_script_creation(self):
        self.db.gifts = []
        self.db.facets = []
        self.db.rites = []
        self.db.tells = []
        self.db.auspices = self.auspicelist
        self.db.tribes = self.tribelist
        self.db.books = self.booklist
        self.db.lodges = self.lodgelist
        self.db.booknames = self.booklong
        self.db.renown_names = []
        self.db.blood = self.blood
        self.db.bone = self.bone
        renown_names = self.db.renown_names
        gifts = self.db.gifts
        rites = self.db.rites
        tells = self.db.tells
        if len(renown_names) == 0:
            renown_names.append("Purity")
            renown_names.append("Honor")
            renown_names.append("Glory")
            renown_names.append("Cunning")
            renown_names.append("Wisdom")
            tempnames = []
            for name in renown_names:
                tempnames.append(name)
            tempnames.sort()
            renown_names = tempnames
        if len(gifts) == 0:
            gifts.append(tuple(["Death","WtF-121","Shadow","Bone Shadows","Cold Embrace","Barghest","Memento Mori","Bone Gnaw","Eyes of the Dead"]))
            gifts.append(tuple(["Dominance","WtF-122","Shadow","Rahu","Primal Allure","Glorious Lunacy","Lay Low the Challenger","Snarl of the Predator","Lead the Lesser Pack"]))
            gifts.append(tuple(["the Elementals","WtF-123","Shadow","Ithaeur,Bone Shadows","Breath of Air","Catastrophe","Flesh of Earth","Tongue of Fire","Heart of Water"]))
            gifts.append(tuple(["Evasion","WtF-123","Shadow","Irraka","Feet of Mist","Fog of War","Deny Everything","Hit and Run","Exit Strategy"]))
            gifts.append(tuple(["Insight","WtF-125","Shadow","Cahalith,Elodoth,Bone Shadows","Prey on Weakness","Read the World's Loom","Echo Dream","Scent the Unnatural","One Step Ahead"]))
            gifts.append(tuple(["Inspiration","WtF-127","Shadow","Cahalith,Blood Talons","Lunatic Inspiration","Fearless Hunter","Pack Triumphs Together","Unity","Still Small Voice"]))
            gifts.append(tuple(["Knowledge","WtF-127","Shadow","Cahalith,Iron Masters","Needle","This Story Is True","Know Thy Prey","Lore of the Land","Sift the Sands"]))
            gifts.append(tuple(["Nature's Gift","WtF-129","Shadow","Hunters in Darkness","Nature's Lure","Black Earth Red Hunger", "Knotted Paths","Pack Kin", "Beast Ride"]))
            gifts.append(tuple(["Rage","WtF-130","Shadow","Blood Talons","Incite Fury","Berserker's Might","Perfected Rage","Slaughterer","Raging Lunacy"]))
            gifts.append(tuple(["Shaping","WtF-131","Shadow","Ithaeur,Iron Masters","Moldywarp","Shield-Breaker","Entropy's Toll","Perfection of Form","Sculpt"]))
            gifts.append(tuple(["Stealth","WtF-131","Shadow","Irraka,Hunters in Darkness","Shadow Pelt","Predator's Shadow","Pack Stalks the Prey","The Hunter Waits","Running Silent"]))
            gifts.append(tuple(["Strength","WtF-132","Shadow","Rahu,Blood Talons","Unchained","Predator's Unmatched Pursuit","Crushing Blow","Primal Strength","Rending Claws"]))
            gifts.append(tuple(["Technology","WtF-133","Shadow","Iron Masters","Garble","Unmake","Command Artifice","Shutdown","Iron Slave"]))
            gifts.append(tuple(["Warding","WtF-134","Shadow","Eldoth,Hunters in Darkness","Make Ward","Ward the Wolf's Den","All Doors Locked","Predator's Claim","Boundary Ward"]))
            gifts.append(tuple(["Weather","WtF-135","Shadow","Storm Lords","Cloak of Mist and Haze","Heavens Unleashed", "Hunt Under Iron Skies","Grasp of Howling Winds","Hunt of Fire and Ice"]))
            gifts.append(tuple(["Change","WtF-136","Wolf","Common","Skin Thief","Gaze of the Moon","Luna's Embrace","The Father's Form","Quicksilver Flesh"]))
            gifts.append(tuple(["Hunting","WtF-137","Wolf","Common","Honed Senses","Cow the Prey","Beast Talker","Tireless Hunter","Impossible Spoor"]))
            gifts.append(tuple(["the Pack","WtF-138","Wolf","Common","Reflected Facets","Down the Prey","Totem's Wrath","Maw of Madness","Pack Awareness"]))
        if len(rites) == 0:
            rites.append(tuple(["Chain Rage","1","Wolf","WtF-139"]))
            rites.append(tuple(["Messenger","1","Wolf","WtF-140"]))
            rites.append(tuple(["Bottle Spirit","2","Wolf","WtF-140"]))
            rites.append(tuple(["Sacred Hunt","2","Wolf","WtF-140"]))
            rites.append(tuple(["Kindle Fury","3","Wolf","WtF-140"]))
            rites.append(tuple(["Shadowbind","3","Wolf","WtF-141"]))
            rites.append(tuple(["Fetish","4","Wolf","WtF-141"]))
            rites.append(tuple(["Twilight Purge","4","Wolf","WtF-141"]))
            rites.append(tuple(["Forge ALliance","5","Wolf","WtF-142"]))
            rites.append(tuple(["Urfarah's Bane","5","Wolf","WtF-142"]))
            rites.append(tuple(["Veil","5","Wolf","WtF-142"]))
            rites.append(tuple(["Banish","1","Pack","WtF-142"]))
            rites.append(tuple(["Harness the Cycle","1","Pack","WtF-143"]))
            rites.append(tuple(["Totemic Empowerment","1","Pack","WtF-143"]))
            rites.append(tuple(["Hunting Ground","2","Pack","WtF-143"]))
            rites.append(tuple(["Moon's Mad Love","2","Pack","WtF-144"]))
            rites.append(tuple(["Wellspring","2","Pack","WtF-144"]))
            rites.append(tuple(["Raiment of the Storm","3","Pack","WtF-145"]))
            rites.append(tuple(["Shadowcall","3","Pack","WtF-145"]))
            rites.append(tuple(["Supplication","3","Pack","WtF-145"]))
            rites.append(tuple(["Hidden Path","4","Pack","WtF-145"]))
            rites.append(tuple(["Expel","4","Pack","WtF-146"]))
            rites.append(tuple(["Great Hunt","5","Pack","WtF-146"]))
        if len(tells) == 0:
            tells.append(tuple(["A Wolf's Meat","WtF-300"]))
            tells.append(tuple(["Anger Issues","WtF-300"]))
            tells.append(tuple(["Bite","WtF-300"]))
            tells.append(tuple(["Bitten","WtF-300"]))
            tells.append(tuple(["Clever Fingers","WtF-301"]))
            tells.append(tuple(["Devil Inside","WtF-301"]))
            tells.append(tuple(["Evil Eye","WtF-301"]))
            tells.append(tuple(["Exciting","WtF-301"]))
            tells.append(tuple(["Familiar","WtF-301"]))
            tells.append(tuple(["Fuck Ugly","WtF-301"]))
            tells.append(tuple(["Horse","WtF-301"]))
            tells.append(tuple(["Hostache","WtF-301"]))
            tells.append(tuple(["Liar's Skin","WtF-302"]))
            tells.append(tuple(["Marker","WtF-302"]))
            tells.append(tuple(["Moon Marked","WtF-302"]))
            tells.append(tuple(["Phantom Pack","WtF-303"]))
            tells.append(tuple(["Piercing Eyes","WtF-303"]))
            tells.append(tuple(["Second Skin","WtF-303"]))
            tells.append(tuple(["Shape-Shifted","WtF-303"]))
            tells.append(tuple(["Shadow Twin","WtF-303"]))
            tells.append(tuple(["Skinner","WtF-303"]))
            tells.append(tuple(["Spirit Double","WtF-303"]))
            tells.append(tuple(["Strong Scent","WtF-303"]))
            tells.append(tuple(["Third Nipple","WtF-303"]))
            tells.append(tuple(["Tongues","WtF-304"]))
            tells.append(tuple(["Waystone","WtF-304"]))
            tells.append(tuple(["Wolf Sign","WtF-304"]))