'''
Created on Jan 13, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class VampireStatHandler(DefaultScript):
    bookreference = ["VtR","SotC","BS","VtR1",'ATYoN']
    clanlist = ["Daeva","Gangrel","Mekhet","Nosferatu","Ventrue"]
    covenantlist = ["Carthians","Circle of the Crone","Invictus","Lancea et Sanctum","Ordo Dracul"]
    bloodlines = ['Khaibit','Neglatu','Kerberos']
    sorceries = ['Theban Sorcery','Cruac']
    #Shorthand book codes for the books from whence content is drawn. They MUST be in the same order as the booktitles list below.
    booktitles = ["Vampire the Requiem: Second Edition","Secrets of the Covenants","Blood Sorcery: Sacraments and Blasphemies",
                  "Vampire the Requiem: First Edition",'A Thousand Years of Night']
    def MeetsPrereqs(self, character, discipline):
        disciplines = self.db.disciplines
        for indexdiscipline in disciplines:
            if indexdiscipline[0].lower() == discipline.lower():
                disciplinewarning = "As you are not a member of "
                affiliation = []
                if "/" in indexdiscipline[1]:
                    affiliation.append(indexdiscipline[1].split("/")[0])
                    affiliation.append(indexdiscipline[1].split("/")[1])
                    for aff in affiliation:
                        if character.db.xsplat == aff or character.db.ysplat == aff:
                            return True
                else:
                    affiliation = indexdiscipline[1]
                    if character.db.xsplat == affiliation or character.db.ysplat == affiliation:
                        return True
                if affiliation == "All":
                    return True
                if affiliation == "Blood Sorcery":
                    for sorc in self.db.sorceries:
                        for key in character.db.powers.keys():
                            if key == sorc:
                                return True
                    return False
                if len(affiliation) == 2:
                    disciplinewarning += "clans " + affiliation[0] + " or " + affiliation[1] + " you must provide a reason as to how you acquired this discipline in your backstory."
                    return disciplinewarning
                elif affiliation in self.clanlist:
                    disciplinewarning += "clan " + affiliation + " you must provide a reason as to how you acquired this discipline in your backstory."
                    return disciplinewarning
                else:
                    return False
        for indexdevotion in self.db.devotions:
            if indexdevotion[0].lower() == discipline.lower():
                for iterreq in range(2,len(indexdevotion)+1):
                    reqsplit = indexdevotion[iterreq].split(",")
                    try:
                        character.msg(str(character.db.powers[reqsplit[0]])+" "+str(reqsplit[1]))
                        if int(character.db.powers[reqsplit[0]]) >= int(reqsplit[1]):
                            return True
                    except IndexError:
                        return False
        for indexritual in self.db.cruac_rituals:
            if indexritual[0] == discipline.lower():
                try:
                    if int(character.db.powers["Cruac"]) >= int(indexritual[1]):
                        return True
                except IndexError:
                    return False
        for indextheban in self.db.theban_rituals:
            if indextheban[0] == discipline.lower():
                try:
                    if int(character.db.powers["Theban Sorcery"]) >= int(indextheban[1]):
                        return True
                except IndexError:
                    return False
    def BookCode(self, code):
        booktitles = self.booktitles
        bookreference = self.bookreference
        return booktitles[bookreference.index(code)]
    def at_script_creation(self):
        self.db.disciplines = []
        self.db.discipline_ratings = [1,2,3,4,5]
        self.db.cruac_rituals = []
        self.db.theban_rituals = []
        self.db.scales = []
        self.db.clans = self.clanlist
        self.db.covenants = self.covenantlist
        self.db.books = self.bookreference
        self.db.booknames = self.booktitles
        self.db.sorceries = self.sorceries
        self.db.devotions = []
        disciplines = self.db.disciplines
        cruac = self.db.cruac_rituals
        theban = self.db.theban_rituals
        scales = self.db.scales
        devotions = self.db.devotions
        if len(disciplines) == 0:
            disciplines.append(tuple(["Animalism","All","VtR-126"]))
            disciplines.append(tuple(["Auspex","Mekhet","VtR-128"]))
            disciplines.append(tuple(["Celerity","All","VtR-130"]))
            disciplines.append(tuple(["Coil of the Ascendant","Ordo Dracul","VtR-155"]))
            disciplines.append(tuple(["Coil of the Wyrm","Ordo Dracul","VtR-157"]))
            disciplines.append(tuple(["Coil of the Voivode","Ordo Dracul","VtR-158"]))
            disciplines.append(tuple(["Coil of Zirnitra","Ordo Dracul","SotC-200"]))
            disciplines.append(tuple(["Coil of Ziva","Ordo Dracul","SotC-201"]))
            disciplines.append(tuple(["Cruac","Circle of the Crone","VtR-151"]))
            disciplines.append(tuple(['Coil of Quintessence','Ordo Dracul','ATYoN-81']))
            disciplines.append(tuple(["Creation","Blood Sorcery","BS-19"]))
            disciplines.append(tuple(["Destruction","Blood Sorcery","BS-20"]))
            disciplines.append(tuple(["Divination","Blood Sorcery","BS-21"]))
            disciplines.append(tuple(["Dominate","Ventrue","VtR-131"]))
            disciplines.append(tuple(["Majesty","Daeva","VtR-133"]))
            disciplines.append(tuple(["Nightmare","Nosferatu","VtR-135"]))
            disciplines.append(tuple(["Obfuscate","All","VtR-137"]))
            disciplines.append(tuple(["Protean","Gangrel","VtR-139"]))
            disciplines.append(tuple(["Protection","Blood Sorcery","BS-22"]))
            disciplines.append(tuple(["Resilience","All","VtR-141"]))
            disciplines.append(tuple(["Theban Sorcery","Lancea et Sanctum","VtR-151"]))
            disciplines.append(tuple(["Transmutation","Blood Sorcery","BS-22"]))
            disciplines.append(tuple(["Vigor","All","VtR-141"]))
        if len(devotions) == 0:
            devotions.append(tuple(["Body of Will","VtR-142","Resilience,3","Vigor,1"]))
            devotions.append(tuple(["Chain of Command","VtR-142","Dominate,3","Vigor,1"]))
            devotions.append(tuple(["Cloak the Gathering","VtR-143","Obfuscate,5"]))
            devotions.append(tuple(["Conditioning","VtR-143","Dominate,4"]))
            devotions.append(tuple(["Cross-Contamination","VtR-143","Majesty,1","Nightmare,1"]))
            devotions.append(tuple(["Cult of Personality","VtR-143","Majesty,4","Vigor,3"]))
            devotions.append(tuple(["Enchantment","VtR-143","Majesty,4","Obfuscate,2"]))
            devotions.append(tuple(["Enfeebling Aura","VtR-143","Majesty,1","Resilience,1"]))
            devotions.append(tuple(["Foul Grave","VtR-144","Protean,1","Nightmare,1"]))
            devotions.append(tuple(["Force of Nature","VtR-144","Protean,4","Resilience,4","Vigor,2"]))
            devotions.append(tuple(["Gargoyle's Vigilance","VtR-144","Auspex,1","Resilience,2"]))
            devotions.append(tuple(["Hint of Fear","VtR-144","Celerity,2","Nightmare,2"]))
            devotions.append(tuple(["Juggernaut's Gait","VtR-145","Resilience,5","Vigor,3"]))
            devotions.append(tuple(["Quicken Sight","VtR-145","Auspex,1","Celerity,1"]))
            devotions.append(tuple(["Reason's Salon","VtR-146","Animalism,4","Resilience,2"]))
            devotions.append(tuple(["Riot","VtR-146","Animalism,4","Majesty,5"]))
            devotions.append(tuple(["Shared Sight","VtR-146","Auspex,4","Dominate,1"]))
            devotions.append(tuple(["Shatter the Shroud","VtR-146","Auspex,2","Vigor,1"]))
            devotions.append(tuple(["Stalwart Servant","VtR-146","Dominate,3","Resilience,1"]))
            devotions.append(tuple(["Subsume the Lesser Beast","VtR-147","Animalism,4","Dominate,3"]))
            devotions.append(tuple(["Summoning","VtR-147","Dominate/Majesty,4"]))
            devotions.append(tuple(["Sun's Brutal Dreamscape","VtR-148","Nightmare,5","Resilience,2"]))
            devotions.append(tuple(["Touch of Deprivation","VtR-148","Obfuscate,4","Dominate,2"]))
            devotions.append(tuple(["Undying Familiar","VtR-148","Animalism,2","Resilience,2"]))
            devotions.append(tuple(["Wet Dream","VtR-148","Majesty,2","Nightmare,2"]))
            devotions.append(tuple(["The Wish","VtR-148","Celerity,2","Majesty,4","Vigor,2"]))
            devotions.append(tuple(["Vermin Flood","VtR-149","Animalism,3","Vigor,2","Celerity,2"]))
            devotions.append(tuple(["Wraith's Presence","VtR-149","Obfuscate,3","Nightmare,1"]))
            devotions.append(tuple(['Annals of Death','ATYoN-72','Auspex,3']))
            devotions.append(tuple(['Bones of the Mountain','ATYoN-73','Protean,4','Resilence,3','Vigor,3']))
            devotions.append(tuple(['Celebrity','ATYoN-73','Majesty,2']))
            devotions.append(tuple(['Consumption','ATYoN-74','Dominate,5']))
            devotions.append(tuple(['Crush of Years','ATYoN-74','Nightmare,4','Majesty,3']))
            devotions.append(tuple(['Legion','ATYoN-74','Animalism,5','Auspex,3']))
            devotions.append(tuple(['Malignant Smog','ATYoN-75','Protean,5']))
            devotions.append(tuple(['Pass into Yesteryear','ATYoN-76','Obfuscate,3','Nightmare,1']))
            devotions.append(tuple(['Preternatural Instinct','ATYoN-76','Auspex,4','Celerity,1']))
            devotions.append(tuple(['Spontaneous Ignition','ATYoN-76','Celerity,5','Resilience,1']))
            devotions.append(tuple(['Unbridled Force','ATYoN-76','Vigor,5','Dominate,2']))
        if len(cruac) == 0:
            cruac.append(tuple(["Pangs of Prosperina","1","VtR-152","Transmutation,1"]))
            cruac.append(tuple(["Rigor Mortis","1","VtR-152","Transmutation,1"]))
            cruac.append(tuple(["Cheval","2","VtR-152","Divination,2"]))
            cruac.append(tuple(["The Hydra's Vitae","2","VtR-152","Destruction,2"]))
            cruac.append(tuple(["Deflection of Wooden Doom","3","VtR-153","Protection,3"]))
            cruac.append(tuple(["Touch of the Morrigan","3","VtR-153","Destrucion,3"]))
            cruac.append(tuple(["Blood Price","4","VtR-153","Creation,4","Destruction/Transmutation,4"]))
            cruac.append(tuple(["Willful Vitae","4","VtR-153","Protection,4"]))
            cruac.append(tuple(["Blood Blight","4","VtR-153","Destruction,4"]))
            cruac.append(tuple(["Feeding the Crone","4","VtR-153","Transmutation,3","Destruction,4"]))
            cruac.append(tuple(["The Mantle of Amorous Fire","1","SotC-184","Transmutation,1"]))
            cruac.append(tuple(["The Pool of Forbidden Truths","1","SotC-184","Divination,1"]))
            cruac.append(tuple(["Donning the Beast's Flesh","3","SotC-184","Transmutation,3"]))
            cruac.append(tuple(["Mantle of the Beast's Breath","2","SotC-184","Transmutation,2"]))
            cruac.append(tuple(["Shed the Virulent Bowels","2","SotC-185","Destruction,2"]))
            cruac.append(tuple(["Curse of Aphrodite's Favor","3","SotC-185","Transmutation,3"]))
            cruac.append(tuple(["Curse of the Beloved Toy","3","SotC-185","Divination,3"]))
            cruac.append(tuple(["Gorgon's Gaze","4","SotC-185","Transmutation,4"]))
            cruac.append(tuple(["Mantle of the Glorious Dervish","SotC-185","3","Transmutation,3"]))
            cruac.append(tuple(["Bounty of the Storm","4","SotC-185","Divination,4"]))
            cruac.append(tuple(["Denying Hades","5","SotC-186","Transmutation,5"]))
            cruac.append(tuple(["Mantle of the Predator Goddess","4","SotC-186","Transmutation,4"]))
            cruac.append(tuple(["Birthing the God","5","SotC-186","Creation,5"]))
            cruac.append(tuple(["Mantle of the Crone","5","SotC-186","Creation,5"]))
            cruac.append(tuple(["Manananggal's Working",'3','ATYoN-78']))
            cruac.append(tuple(["Gwydion's Curse",'5','ATYoN-78']))
            cruac.append(tuple(['Scapegoat','5','ATYoN-78']))
        if len(theban) == 0:
            theban.append(tuple(["Blood Scourge","1","VtR-153","Transmutation,1","Destruction,1"]))
            theban.append(tuple(["Vitae Reliquary","1","VtR-153","Transmutation,1"]))
            theban.append(tuple(["Blandishment of Sin","1","VtR-153","Destruction,1"]))
            theban.append(tuple(["Curse of Babel","2","VtR-153","Transmutation,2"]))
            theban.append(tuple(["Liar's Plague","2","VtR-153","Creation,2","Divination,2"]))
            theban.append(tuple(["Malediction of Despair","3","VtR-154","Divination,2","Transmutation,3"]))
            theban.append(tuple(["Gift of Lazarus","4","VtR-154","Transmutation,4"]))
            theban.append(tuple(["Stigmata","4","VtR-154","Destruction,4"]))
            theban.append(tuple(["Transubstantiation","5","VtR-154","Transmutation,5"]))
            theban.append(tuple(["Apple of Eden","1","SotC-194","Divination,1"]))
            theban.append(tuple(["Marian Apparition","1","SotC-194","Divination,1"]))
            theban.append(tuple(["Revelatory Shroud","1","SotC-194","Divination,1"]))
            theban.append(tuple(["Apparition of the Host","2","SotC-194","Divination,1"]))
            theban.append(tuple(["Bloody Icon","2","SotC-195","Transmutation,2"]))
            theban.append(tuple(["The Walls of Jericho","2","SotC-195","Destruction,2"]))
            theban.append(tuple(["Aaron's Rod","3","SotC-195","Transmutation,3"]))
            theban.append(tuple(["Blessing the Legion","3","SotC-195","Transmutation,3"]))
            theban.append(tuple(["Miracle of the Dead Sun","3","SotC-196","Protection,3"]))
            theban.append(tuple(["Pledge to the Worthless One","3","SotC-196","Transmutation,3"]))
            theban.append(tuple(["Great Prophecy","4","SotC-196","Divination,4"]))
            theban.append(tuple(["The Guiding Star","3","SotC-196","Protection,3"]))
            theban.append(tuple(["Apocalypse","5","SotC-197","Trnasmutation,5"]))
            theban.append(tuple(["The Judgment Fast","5","SotC-197","Transmutation,5"]))
            theban.append(tuple(['Curse of Isolation','4','ATYoN-79']))
            theban.append(tuple(['Orison of Voices','4','ATYoN-79']))
            theban.append(tuple(['Sins of the Ancestors','4','ATYoN-79']))
        if len(scales) == 0:
            scales.append(tuple(["Day-Wake Conditioning","1","Ascendant","VtR-156"]))
            scales.append(tuple(["Flesh-Graft Treatment","4","Ascendant","VtR-156"]))
            scales.append(tuple(["Epidermal Shielding Bath","5","Ascendant","VtR-156"]))
            scales.append(tuple(["Kindred Sense Endowment","2","Wyrm","VtR-157"]))
            scales.append(tuple(["Augmented Vitae Draught","4","Wyrm","VtR-157"]))
            scales.append(tuple(["Surgical Heart Removal","5","Wyrm","VtR-158"]))
            scales.append(tuple(["Blood-Cleansing Ritual","1","Voivode","VtR-158"]))
            scales.append(tuple(["Sanguinary Invigoration","2","Voivode","VtR-159"]))
            scales.append(tuple(["Fealty's Reward","3","Voivode","VtR-159"]))
            scales.append(tuple(["Mass Embrace","5","Voivode","VtR-159"]))
            scales.append(tuple(["Psychic Lobotomy","1","Zirnitra","SotC-200"]))
            scales.append(tuple(["Grafting Unholy Flesh","4","Zirnitra","SotC-200"]))
            scales.append(tuple(["Bleed the Sin","2","Ziva","SotC-201"]))
            scales.append(tuple(["Siphon the Soul","3","Ziva","SotC-202"]))
            scales.append(tuple(['Codependency','5','Quintessence','ATYoN-82']))
            scales.append(tuple(['Cold of the Grave','3','ATYoN-82']))
    def Reset(self):
        self.at_script_creation()
    def DisciplineList(self):
        return self.db.disciplines
class Devotion(object):
#Used to store devotions on characters.
    def __init__(self, name, *disciplines):
        self.name = name
        self.disciplines = list(disciplines)