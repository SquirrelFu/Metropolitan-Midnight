'''
Created on Jan 16, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class MummyHandler(DefaultScript):
#Used to handle mummy stats on a room, a broader index of sorts.
    decrees = ["Lion-Headed","Falcon-Headed","Bull-Headed","Serpent-Headed","Jackal-Headed"]
    guilds = ["Maa-Kep","Mesen-Nebu","Sesha-Hebsu","Tef-Aabhi"]
    
    def AffinityBingo(self, judgein):
        ab = False
        ba = False
        ka = False
        ren = False
        sheut = False
        for affindex in range(2,6):
            if self.AffinitySearch(judgein[affindex])[1] == "Ab":
                ab = True
            elif self.AffinitySearch(judgein[affindex])[1] == "Ba":
                ba = True
            elif self.AffinitySearch(judgein[affindex])[1] == "Ka":
                ka = True
            elif self.AffinitySearch(judgein[affindex])[1] == "Ren":
                ren = True
            elif self.AffinitySearch(judgein[affindex])[1] == "Sheut":
                sheut = True
        if ab and ba and ka and ren and sheut:
            return True
        else:
            return False 
    def AffinitySearch(self,affin):
        for item in self.affinities:
            if item[0] == affin:
                return item
    def at_script_creation(self):
        self.key = "MummyHandler"
        self.db.affinities = []
        self.db.utterances = []
        self.db.judges = []
        affinities = self.db.affinities
        utterances = self.db.utterances
        judges = self.db.judges
        if len(affinities) == 0:
            affinities.append(tuple(["Affable Aid","Maa-Kep","MtC-34"]))
            affinities.append(tuple(["Divine Flesh","Mesen-Nebu","MtC-39"]))
            affinities.append(tuple(["Eyes of Justice","Sesha-Hebsu","MtC-45"]))
            affinities.append(tuple(["Fated Soul","Su-Menent","MtC-49"]))
            affinities.append(tuple(["Model Lifeweb","Tef-Aabhi","MtC-55"]))
            affinities.append(tuple(["Ancient Horror Unveiling","Sheut","3","MtC-99"]))
            affinities.append(tuple(["Anointed Prowess","Ka","1","MtC-99"]))
            affinities.append(tuple(["Auspicious Mastery","Ba","1","MtC-99"]))
            affinities.append(tuple(["Beast Companion","Ba","1","MtC-100"]))
            affinities.append(tuple(["Beast Soul Fury","Sheut","1","MtC-100"]))
            affinities.append(tuple(["Blessed Panoply","Ren","2","MtC-100"]))
            affinities.append(tuple(["Blessed Soul","Ab","1","MtC-101"]))
            affinities.append(tuple(["By Steps Unseen","Sheut","3","MtC-101"]))
            affinities.append(tuple(["Charmed Lives","Ren","2","MtC-101"]))
            affinities.append(tuple(["Dauntless Explorer","Ka","2","MtC-101"]))
            affinities.append(tuple(["Deathsight","Sheut","1","MtC-102"]))
            affinities.append(tuple(["Divine Countenance","Ab","1","MtC-102"]))
            affinities.append(tuple(["Dominating Might","Ka","3","MtC-102"]))
            affinities.append(tuple(["Enduring Flesh","Ka","1","MtC-102"]))
            affinities.append(tuple(["Enlightened Senses","Ren","2","MtC-102"]))
            affinities.append(tuple(["Entombed Glory","None","MtC-103"]))
            affinities.append(tuple(["Epic Heart","Ab","2","MtC-103"]))
            affinities.append(tuple(["Eternal Legend","Ren","5","MtC-103"]))
            affinities.append(tuple(["Falcon Soul Aloft","Ba","1","MtC-104"]))
            affinities.append(tuple(["Familiar Face","Ren","1","MtC-104"]))
            affinities.append(tuple(["Fearsome Soul","Sheut","3","MtC-104"]))
            affinities.append(tuple(["Gift of Truth","Ren","1","MtC-104"]))
            affinities.append(tuple(["Glorious Mien","Ab","2","MtC-105"]))
            affinities.append(tuple(["God-King's Scepter","Cult","3","MtC-105"]))
            affinities.append(tuple(["Godsight","Ren","3","MtC-105"]))
            affinities.append(tuple(["Grip of Death","Sheut","2","MtC-105"]))
            affinities.append(tuple(["Guardian Wrath","Ka","2","MtC-106"]))
            affinities.append(tuple(["Healing Counsel","Ab","3","MtC-106"]))
            affinities.append(tuple(["Living in Now","Ba","2","MtC-106"]))
            affinities.append(tuple(["Living Monolith","Ka","2","MtC-106"]))
            affinities.append(tuple(["Miraculous Benefactor","Ab","2","MtC-107"]))
            affinities.append(tuple(["Night Creature","Sheut","2","MtC-107"]))
            affinities.append(tuple(["Nihilist Awakening","Ba","3","MtC-107"]))
            affinities.append(tuple(["Paragon Shames the Weak","Ka","3","MtC-107"]))
            affinities.append(tuple(["Pharoah Reigns Anew","Ab","3","MtC-107"]))
            affinities.append(tuple(["Radiant Lifeforce","Ren","1","MtC-108"]))
            affinities.append(tuple(["Retributive Curse","Ka","2","MtC-108"]))
            affinities.append(tuple(["Rouse the Khaibit","Sheut","2","MtC-108"]))
            affinities.append(tuple(["Running like Flight","Ba","2","MtC-108"]))
            affinities.append(tuple(["Shrouding Aura","Ka","3","MtC-109"]))
            affinities.append(tuple(["Sight Beyond Eyes","Ba","3","MtC-109"]))
            affinities.append(tuple(["Soul Infusion","Ba","3","MtC-109"]))
            affinities.append(tuple(["Soulsight","Ab","3","MtC-109"]))
            affinities.append(tuple(["Voice of Conscience","Ab","2","MtC-110"]))
            affinities.append(tuple(["Voice of Temptation","Sheut","2","MtC-111"]))
            affinities.append(tuple(["Wisdom of the Ancients","Ba","1","MtC-111"]))
            affinities.append(tuple(["Words Summoned Forth","Ren","3","MtC-111"]))
        if len(judges) == 0:
            judges.append(tuple(["Akhi","Ab","Voice of Conscience","Beast Companion","Beast Soul Fury","Guardian Wrath","Words Summoned Forth"]))
            judges.append(tuple(["Am-Khaibit","Sheut","Night Creature","Eternal Legend","Glorious Mien","Nihilist Awakening","Shrouding Aura"]))
            judges.append(tuple(["An-Afkh","Ba","Auspicious Mastery","Blessed Panoply","Deathsight","Miraculous Benefactor","Radiant Lifeforce"]))
            judges.append(tuple(["An-Hotep","Ka","Enduring Flesh","Charmed Lives","Healing Counsel","Night Creature","Running Like Flight"]))
            judges.append(tuple(["Arem-Abfu","Random","Ancient Horror Unveiling","Guardian Wrath","Living in Now","Soulsight","Words Summoned Forth"]))
            judges.append(tuple(["Artem-Khet","Sheut","Voice of Temptation","Auspicious Mastery","Blessed Soul","Gift of Truth","Retributive Curse"]))
            judges.append(tuple(["Bastu","Ren","Enlightened Senses","Anointed Prowess","By Steps Unseen","Sight Beyond Eyes","Soulsight"]))
            judges.append(tuple(["Fentu","Ka","Anointed Prowess","Beast Companion","Beast Soul Fury","Enlightened Senses","Epic Heart"]))
            judges.append(tuple(["Hepet-Khet","Ab","Glorious Mien","Dominating Might","Familiar Face","Grip of Death","Running like Flight"]))
            judges.append(tuple(["Her-Uru","Sheut","Fearsome Soul","Auspicious Mastery","Divine Countenance","Familiar Face","Shrouding Aura"]))
            judges.append(tuple(["Heraf-Het","Ba","Nihilist Awakening","Ancient Horror Unveiling","Enduring Flesh","Familiar Face","Voice of Conscience"]))
            judges.append(tuple(["Hetch-Abhu","Ka","Paragon Shames the Weak","Falcon Soul Aloft","Godsight","Pharoah Reigns Anew","Rouse the Khaibit"]))
            judges.append(tuple(["Kenemiti","Ren","Gift of Truth","Retributive Curse","Soul Infusion","Soulsight","Voice of Temptation"]))
            judges.append(tuple(["Khem-Inhu","Ren","Radiant Lifeforce","Auspicious Mastery","Deathsight","Guardian Wrath","Voice of Conscience"]))
            judges.append(tuple(["Maar-Nantuuf","Ka","Living Monolith","Enlightened Senses","Glorious Mien","Sight Beyond Eyes","Voice of Temptation"]))
            judges.append(tuple(["Neb-Abitu","Ba","Sight Beyond Eyes","Night Creature","Shrouding Aura","Voice of Conscience","words Summoned Forth"]))
            judges.append(tuple(["Neb-Heru","Ab","Epic Heart","Charmed Lives","Fearsome Soul","Living Monolith","Wisdom of the Ancients"]))
            judges.append(tuple(["Neb-Imkhu","Ren","Familiar Face","By Steps Unseen","Epic Heart","Living in Now","Shrouding Aura"]))
            judges.append(tuple(["Nebha","Sheut","Rouse the Khaibit","Blessed Soul","Dauntless Explorer","Falcon Soul Aloft","Gift of Truth"]))
            judges.append(tuple(["Nekhenhu","Sheut","Deathsight","Enduring Flesh","Godsight","Healing Counsel","Soul Infusion"]))
            judges.append(tuple(["Qerrti","Ab","Miraclous Benefactor","Anointed Prowess","Radiant Lifeforce","Soul Infusion","Voice of Temptation"]))
            judges.append(tuple(["Ruruti","Ab","Blessed Soul","Beast Fury Soul","Blessed Panoply","Guardian Wrath","Running like Flight"]))
            judges.append(tuple(["Sekhiru","Ren","Blessed Panoply","Living in Now","Night Creature","Retributive Curse","Soulsight"]))
            judges.append(tuple(["Ser-Kheru","Ba","Running like Flight","Charmed Lives","Dauntless Explorer","Grip of Death","Voice of Conscience"]))
            judges.append(tuple(["Ser-Tihu","Ab","Healing Counsel","Radiant Lifeforce","Deathsight","Retributive Curse","Sight Beyond Eyes"]))
            judges.append(tuple(["Set-Quest","Ka","Dominating Might","Charmed Lives","Glorious Mien","Grip of Death","Nihilist Awakening"]))
            judges.append(tuple(["Shet-Kheru","Ba","Wisdom of the Ancients","Godsight","Guardian Wrath","Pharaoh Reigns Anew","Voice of Temptation"]))
            judges.append(tuple(["Ta-Retinhu","Ka","Guardian Wrath","Divine Countenance","Fearsome Soul","Running like Flight","Words Summoned Forth"]))
            judges.append(tuple(["Temp-Sepu","Ren","Charmed Lives","Auspicious Mastery","Dominating Might","Fearsome Soul","Pharaoh Reigns Anew"]))
            judges.append(tuple(["Tenemhu","Sheut","Beast Soul Fury","Enlightened Senses","Running like Flight","Shrouding Aura","Soulsight"]))
            judges.append(tuple(["Tutuutef","Ab","Pharaoh Reigns Anew","Anointed Prowess","Beast Companion","Charmed Lives","Voice of Temptation"]))
            judges.append(tuple(["Uamenti","Ka","Shrouding Aura","Epic Heart","Familiar Face","Grip of Death","Soul Infusion"]))
            judges.append(tuple(["Uatch-Rekhet","Ren","Godsight","Ancient Horror Unveiling","Divine Countenance","Nihilist Awakening","Retributive Curse"]))
            judges.append(tuple(["Unem-Besek","Ren","Eternal Legend","Beast Companion","Beast Soul Fury","Dominating Might","Glorious Mien"]))
            judges.append(tuple(["Unem-Sef","Sheut","Grip of Death","Enduring Flesh","Gift of Truth","Running like Flight","Soulsight"]))
            judges.append(tuple(["Usekh-Nemtet","Any","Dauntless Explorer","Deathsight","Godsight","Sight Beyond Eyes","Soulsight"]))
            judges.append(tuple(["Utu-Nesert","Ba","Falcon Soul Aloft","Blessed Soul","Dauntless Explorer","Radiant Lifeforce","Rouse the Khaibit"]))
        if len(utterances) == 0:
            utterances.append(tuple(["Awaken the Dead","Ba,Sheut,Ren","1,3,5","MtC-113"]))
            utterances.append(tuple(["Blessed is the God-King","Ren,Ab,Defining","1,3,5","MtC-115"]))
            utterances.append(tuple(["Cthonic Dominion","Ba,Sheut,Ren","1,3,5","MtC-116"]))
            utterances.append(tuple(["Command the Beasts","Sheut,Ren,Sheut","1,2,4","MtC-117"]))
            utterances.append(tuple(["Doom Affliction","Ab,Ka,Ba","1,2,4","MtC-118"]))
            utterances.append(tuple(["Dreams of Dead Gods","Ba,Ka,Ab","1,2,4","MtC-118"]))
            utterances.append(tuple(["Dust Beneath Feet","Ba,Ka,Sheut","1,2,4","MtC-120"]))
            utterances.append(tuple(["Gift of the Golden Ank","Ka,Ba,Ab","1,2,4","MtC-121"]))
            utterances.append(tuple(["Kiss of Apep","Ren,Ka,Sheut","1,3,5","MtC-122"]))
            utterances.append(tuple(["Obedient Clay","Ba,Ren,Ab","1,2,4","MtC-123"]))
            utterances.append(tuple(["Palace Knows its Pharaoh","Ba,Ka,Ba","1,3,5","MtC-14"]))
            utterances.append(tuple(["Power of Re","Ab,Sheut,Ab","1,2,4","MtC-125"]))
            utterances.append(tuple(["Rebuke the Vizier","Ka,Ba,Ren","1,3,5","MtC-126"]))
            utterances.append(tuple(["Revelations of Smoke and Flame","Sheut,Ab,Ba","1,3,5","MtC-127"]))
            utterances.append(tuple(["Rite of the Sacred Scarab","Ka,Ren,Ka","1,3,5","MtC-128"]))
            utterances.append(tuple(["Secrets Ripped From Skies","Ba,Sheut,Ren","1,3,5","MtC-130"]))
            utterances.append(tuple(["Seeds of Life","Ka,Ren,Ab","1,2,4","MtC-131"]))
            utterances.append(tuple(["Torn Veil of Forgetting","Sheut,Ab,Ba","1,3,5","MtC-132"]))
            utterances.append(tuple(["Water of Life and Death","Ren,Sheut,Ba","1,2,4","MtC-133"]))
            utterances.append(tuple(["Word of the Amanuensis","Ren,Ab,Ren","1,3,5","MtC-133"]))
            utterances.append(tuple(["Words of Dead Fury","Sheut,Ka,Ba","1,3,5","MtC-134"]))
            utterances.append(tuple(["Words of Dead Glory","Sheut,Ba,Ka","1,2,4","MtC-137"]))
            utterances.append(tuple(["Words of Dead Hunger","Ren,Ba,Sheut","1,2,4","MtC-137"]))
            utterances.append(tuple(["Wrathful Desert Power","Ab,Ba,Ka","1,3,5","MtC-138"]))