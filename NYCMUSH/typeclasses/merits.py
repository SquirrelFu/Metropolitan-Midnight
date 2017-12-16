'''
Created on Jan 14, 2017

@author: CodeKitty
'''

from template import *
from evennia import DefaultScript
class MeritHandler(DefaultScript):
    key = "MeritHandler"
    persistent = True
    bookshort = ["CoD","HL","VtR","SotC","WtF","MtA","CtL:PT","BtP","HtV","MR","MtC","DtD","CtL:PTM","PtC","TP","NH:CH","BS","HD"]
    booklong = ["Chronicles of Darkness core","Hurt Locker","Vampire the Requiem: Second Edition","Secrets of the Covenants","Werewolf the Forsaken: Second Edition",
                "Mage: The Awakening Second Edition","Changeling the Lost Playtest Documents","Beast: The Primordial","Hunter: The Vigil","Mortal Remains","Mummy: The Curse",
                "Demon: The Descent","Chageling the Lost Playtest Documents - Merit and Contract Update","Promethean: The Created Second Edition","The Pack","Night Horrors:Conquering Heroes",
                "Blood Sorcery: Sacraments and Blasphemies","Half-Damned"]
    templatelist = ["Beast","Changeling","Mortal","Mortal+","Mage","Werewolf","Vampire","Mummy","Demon","Promethean"]
    mortalplus = ["Ghoul","Wolfblood","Proximus","Fae-Touched","Hunter"]
    mplusmerits = ["Psychic Vampirism","Damn Lucky","Carrier","The Protocol","Plain Reader","Subliminal Conditioning"]
    vampirex = ["Daeva","Gangrel","Mekhet","Nosferatu","Ventrue"]
    wolfx = ["Cahalith","Irraka","Elodoth","Rahu","Ithaeur"]
    magex = ["Obrimos","Mastigos","Moros","Acanthus","Thrysus"]
    beastx = ["Ugallu","Anakim","Eshmaki","Namtaru","Makara"]
    hunterx = ["Ashwood Abbey","The Long Night","Loyalists of Thule","Network Zero","Null Mysteriis","The Union","Aegis Kai Doru","Ascending Ones","Cheiron Group",
               "The Lucifuge","Malleus Maleficarum","Task Force VALKYRIE","Knights of St. Adrian","Habibiti Ma","Utopia Now"]
    mummyx = ["Lion-Headed","Falcon-Headed","Bull-Headed","Serpent-Headed","Jackal-Headed"]
    prometheanx = ["Frankenstein","Osirian","Galateid","Tammuz","Ulgan","Unfleshed","Extempore"]
    demonx = ["Destroyer","Guardian","Messenger","Psychopomp"]
    changelingx = ["Beast","Darkling","Elemental","Fairest","Ogre","Wizened"]
    wolfy = ["Blood Talons","Bone Shadows","Hunters in Darkness","Iron Masters","Storm Lords","Ghost Wolves"]
    def MeetsPrereqs(self, character, meritname,score):
        physical = self.db.physical
        mental = self.db.mental
        social = self.db.social
        fighting = self.db.fighting
        supernatural = self.db.supernatural
        vampire = self.db.vampire
        ghoul = self.db.ghoul
        werewolf = self.db.werewolf
        wolfblood = self.db.wolfblood
        mage = self.db.mage
        proximus = self.db.sleepwalker
        changeling = self.db.changeling
        faetouched = self.db.faetouched
        beast = self.db.beast
        promethean = self.db.promethean
        hunter = self.db.hunter
        mummy = self.db.mummy
        demon = self.db.demon
        addons = self.db.addons
        atariya = self.db.atariya
        infected = self.db.infected
        dreamer = self.db.dreamer
        lostboy = self.db.lostboy
        plain = self.db.plain
        psyvamp = self.db.psyvamp
        for physquery in physical:
            if physquery[0].lower() == meritname.lower() or ("(" in meritname and physquery[0].lower() in meritname.lower()):
                if not (str(score) in physquery[1].split(",") or (not(",") in physquery and str(score) in physquery[1])):
                    return False
                return self.CheckRequirements(character, physquery, score)
        for mentquery in mental:
            if mentquery[0].lower() == meritname.lower() or ("(" in meritname and mentquery[0].lower() in meritname.lower()):
                if not (str(score) in mentquery[1].split(",") or (not(",") in mentquery and str(score) in mentquery[1])):
                    return False
                return self.CheckRequirements(character, mentquery,score)
        for socquery in social:
            if socquery[0].lower() == meritname.lower() or ("(" in meritname and socquery[0].lower() in meritname.lower()):
                if not (str(score) in socquery[1].split(",") or (not(",") in socquery and str(score) in socquery[1])):
                    return False
                return self.CheckRequirements(character, socquery,score)
        for fightquery in fighting:
            if fightquery[0].lower() == meritname.lower() or ("(" in meritname and fightquery[0].lower() in meritname.lower()):
                if not (str(score) in fightquery[1].split(",") or (not(",") in fightquery and str(score) in fightquery[1])):
                    return False
                return self.CheckRequirements(character, fightquery,score)
        for luckquery in atariya:
            if luckquery[0].lower() == meritname.lower() or ("(" in meritname and luckquery[0].lower() in meritname.lower()):
                if not (str(score) in luckquery[1].split(",") or (not(",") in luckquery and str(score) in luckquery[1])):
                    return False
                return self.CheckRequirements(character, luckquery, score)
        for sickquery in infected:
            if sickquery[0].lower() == meritname.lower() or ("(" in meritname and sickquery[0].lower() in meritname.lower()):
                if not(str(score) in sickquery[1].split(",") or (not(",") in sickquery and str(score) in sickquery[1])):
                    return False
                return self.CheckRequirements(character, sickquery, score)
        for dreamquery in dreamer:
            if dreamquery[0].lower() == meritname.lower() or ("(" in meritname and dreamquery[0].lower() in meritname.lower()):
                if not(str(score) in dreamquery[1].split(",") or (not(",") in dreamquery and str(score) in dreamquery[1])):
                    return False
                return self.CheckRequirements(character, dreamquery, score)
        for peacequery in plain:
            if peacequery[0].lower() == meritname.lower() or ("(" in meritname and peacequery[0].lower() in meritname.lower()):
                if not(str(score) in peacequery[1].split(",") or (not(",") in peacequery and str(score) in peacequery[1])):
                    return False
                return self.CheckRequirements(character, peacequery, score)
        for lostquery in lostboy:
            if lostquery[0].lower() == meritname.lower() or ("(" in meritname and lostquery[0].lower() in meritname.lower()):
                if not(str(score) in lostquery[1].split(",") or (not(",") in lostquery and str(score) in lostquery[1])):
                    return False
                return self.CheckRequirements(character, lostquery, score)
        for psyvampquery in psyvamp:
            if psyvampquery[0].lower() == meritname.lower() or ("(" in meritname and psyvampquery[0].lower() in meritname.lower()):
                if not(str(score) in psyvampquery[1].split(",") or (not(",") in psyvampquery and str(score) in psyvampquery[1])):
                    return False
                return self.CheckRequirements(character, psyvampquery, score)
        for superquery in supernatural:
            if superquery[0].lower() == meritname.lower() or ("(" in meritname and superquery[0].lower() in meritname.lower()):
                if not (str(score) in superquery[1].split(",") or (not("," in superquery)) and str(score) in superquery[1]):
                    return False
                if character.db.template == "Mortal":
                    return self.CheckRequirements(character, superquery, score)
                elif character.db.template == "Vampire":
                    for power in character.db.powers.keys():
                        if power == "Coil of Zirnitra":
                            supercount = 0
                            for searchmerit in character.db.meritlist:
                                for searchpower in supernatural:
                                    if searchmerit[0] == searchpower[0]:
                                        supercount += 1
                            if supercount >= int(character.db.powers[power]) and int(character.db.powers[power]) != 5:
                                return False
                            else:
                                return self.CheckRequirements(character, superquery, score)
                else:
                    return False
        for addquery in addons:
            if addquery[0].lower() == meritname.lower() or ("(" in meritname and addquery[0].lower() in meritname.lower()):
                if not(str(score) in addquery[1].split(",") or (not(",") in addquery and str(score) in addquery[1])):
                    return False
                for merits in character.db.meritlist:
                    fightcount = 0
                    for searchfight in fighting:
                        if merits[0] == searchfight[0]:
                            fightcount += int(searchfight[1])
                    for searchadd in addons:
                        if merits[0] == searchadd[0]:
                            fightcount -= int(searchadd[1])
                if int(score) > fightcount:
                    return False
                else:
                    return self.CheckRequirements(character, addquery, score)
        for vampquery in vampire:
            if vampquery[0].lower() == meritname.lower() or ("(" in meritname and vampquery[0].lower() in meritname.lower()):
                if not (str(score) in vampquery[1].split(",") or (not(",") in vampquery and str(score) in vampquery[1])):
                    return False
                if character.db.template == "Vampire":
                    return self.CheckRequirements(character, vampquery, score)
                else:
                    return False
        for ghoulquery in ghoul:
            if ghoulquery[0].lower() == meritname.lower() or ("(" in meritname and ghoulquery[0].lower() in meritname.lower()):
                if not (str(score) in ghoulquery[1].split(",") or (not(",") in vampquery and str(score) in vampquery[1])):
                    return False
                if character.db.template == "Ghoul":
                    return self.CheckRequirements(character, ghoulquery, score)
                else:
                    return False
        for wolfquery in werewolf:
            if wolfquery[0].lower() == meritname.lower():
                if not (str(score) in wolfquery[1].split(",")  or (not("," in wolfquery))):
                    return False
                if character.db.template == "Werewolf":
                    return self.CheckRequirements(character, wolfquery, score)
                else:
                    return False
        for bloodquery in wolfblood:
            if bloodquery[0].lower() == meritname.lower():
                if not (str(score) in bloodquery[1].split(",") or (not("," in wolfquery))):
                    return False
                if character.db.template == "Wolfblood":
                    return self.CheckRequirements(character, bloodquery, score)
                else:
                    return False
        for magequery in mage:
            if magequery[0].lower() == meritname.lower():
                if not (str(score) in magequery[1].split(",")  or (not("," in magequery))):
                    return False
                if character.db.template == "Mage":
                    return self.CheckRequirements(character, magequery, score)
                else:
                    return False
        for proxquery in proximus:
            if proxquery[0].lower() == meritname.lower():
                if not (str(score) in proxquery[1].split(",") or (not("," in proxquery))):
                    return False
                if character.db.template == "Proximus":
                    return self.CheckRequirements(character, proxquery, score)
                else:
                    return False
        for lingquery in changeling:
            if lingquery[0].lower() == meritname.lower():
                if not (str(score) in lingquery.split(",") or (not("," in lingquery))):
                    return False
                if character.db.template == "Changeling":
                    return self.CheckRequirements(character, lingquery, score)
                else:
                    return False
        for faequery in faetouched:
            if faequery[0].lower() == meritname.lower():
                if not (str(score) in faequery.split(",") or (not("," in faequery))):
                    return False
                if character.db.template == "Fae-Touched":
                    return self.CheckRequirements(character, faequery, score)
        for beastquery in beast:
            if beastquery[0].lower() == meritname.lower():
                if not (str(score) in beastquery.split(",") or (not("," in beastquery))):
                    return False
                if character.db.template == "Beast":
                    return self.CheckRequirements(character, beastquery, score)
                else:
                    return False
        for promquery in promethean:
            if promquery[0].lower() == meritname.lower():
                if not (str(score) in promquery.split(",") or (not("," in promquery))):
                    return False
                if character.db.template == "Promethean":
                    return self.CheckRequirements(character, promquery, score)
                else:
                    return False
        for hunterquery in hunter:
            if hunterquery[0].lower() == meritname.lower():
                if character.db.template == "Hunter":
                    if not (str(score) in hunterquery.split(",") or (not("," in hunterquery))):
                        return False
                    return self.CheckRequirements(character, hunterquery, score)
                else:
                    return False
        for mummyquery in mummy:
            if mummyquery[0].lower() == meritname.lower():
                if not (str(score) in mummyquery.split(",") or (not("," in mummyquery))):
                    return False
                if character.db.template == "Mummy":
                    return self.CheckRequirements(character, mummyquery, score)
                else:
                    return False
        for demonquery in demon:
            if demonquery[0].lower() == meritname.lower():
                if not (str(score) in demonquery.split(",") or (not("," in demonquery))):
                    return False
                if character.db.template == "Demon":
                    return self.CheckRequirements(character, demonquery, score)
                else:
                    return False
    def CheckRequirements(self, character, meritin, meritscore):
        if meritin[0].lower() == "supernatural merit":
            for merit in character.db.meritlist:
                if merit in self.supernatural:
                    return True
        if meritin[0].lower() == "status (lost boys network)":
            for merit in character.db.meritlist:
                if merit[0] == "the protocol":
                    return True
        if meritin[0].lower() == "mystery cult initiation":
            for merit in character.db.meritlist:
                if meritin[0].lower() in merit[0].lower():
                    return True
        if len(meritin) == 3:
            return True
        if len(meritin) == 4:
            if isinstance(meritin[3], bool):
                return True
        requirements = []
        for iterate in range(2,len(meritin)):
            requirements.append(meritin[iterate])
        for require in requirements:
            reqstatlist = []
            notelist = []
            if "/" in require:
                reqstatlist = require.split("/")    
                for thing in reqstatlist:
                    if "(" in thing:
                        notelist.append(thing.split("(")[1])
            if len(reqstatlist) != 0:
                for item in reqstatlist:
                    if self.SearchBasics(item, character) == False:
                        return False
                    else:
                        return True
            if self.SearchBasics(require, character) == False:
                return False
            elif "," in require:
            #Checks to see if the requirement needs a specific rating from the stat.
                reqstat = require.split(",")[0]
                reqscore = require.split(",")[1]
                reqnote = ""
                if "(" in reqstat:
                #Checks to see if the requirement needs a specific note on the stat.
                    reqnote = reqstat.split("(")[1].replace(")","")
                    reqstat = reqstat.split("(")[0]
                if require == character.db.sanityname:
                    if ">" in reqstat:
                        if self.CompareMeritStat(character.db.sanity,">",meritscore):
                            pass
                        else:
                            return False
                    elif "<" in reqstat:
                        if self.CompareMeritStat(character.db.sanity,"<",meritscore):
                            pass
                        else:
                            return False
                    elif "=" in reqstat:
                        if self.CompareMeritStat(character.db.sanity,"=",meritscore):
                            pass
                        else:
                            return False
            if "!" in require:
                negatory = require.replace("!","")
                if character.db.xsplat == negatory:
                    return False
                elif character.db.ysplat == negatory:
                    return False
                elif character.db.template == negatory:
                    return False
                for meritsearch in character.db.meritlist:
                    if meritsearch.name.lower() == negatory.lower():
                        if "," in negatory:
                            if negatory.split(",")[1] <= meritsearch.score:
                                return False
                        else:
                            return False
                for attribsearch in character.db.attributes:
                    if attribsearch.name.lower() == negatory.lower():
                        if "," in negatory:
                            if negatory.spli(",")[1] < attribsearch.score:
                                return False
                        else:
                            return False
                for skillsearch in character.db.skills:
                    if skillsearch.name.lower() == negatory.lower():
                        if "," in negatory:
                            if negatory.split(",")[1] < skillsearch.score:
                                return False
                        else:
                            return False
                for searchmerit in character.db.meritlist:
                    if reqstat.lower() == searchmerit.name.lower():
                    #Checks to see if the merit is held by the character at all.
                        if reqnote != "" and searchmerit.note.lower() != reqnote:
                        #Checks to see if the proper note is there or not.
                            return False
                        else:
                            if int(reqscore) > int(searchmerit.score):
                                return False
                            else:
                                break
                    else:
                        return False
        for item in reqstatlist:
            if item == "Mortal+" and not (character.db.template in self.mortalplus):
                return False
            elif item in self.templatelist:
                if item != character.db.template:
                    return False
        for thing in character.db.meritlist:
            if meritin[0].title() in self.mplusmerits:
                if thing[0].title() in self.mplusmerits:
                    return False
            
        return True
    def SearchBasics(self, require, character):
            if "," in require:
            #Checks to see if the requirement needs a specific rating from the stat.
                reqstat = require.split(",")[0]
                reqscore = require.split(",")[1]
                reqnote = ""
                if "(" in reqstat:
                #Checks to see if the requirement needs a specific note on the stat.
                    reqnote = reqstat.split("(")[1].replace(")","")
                    reqstat = reqstat.split("(")[0]
                for attribute in character.db.attributes.keys():
                    if reqstat.lower() == attribute.lower():
                    #Checks to see if the requited stat is in fact, an attribute.
                        if int(reqscore) > int(character.db.attributes[attribute]):
                        #If the stat is an attribute, check and see if the player has the requisite level of it.
                            return False
                        else:
                            break
                for skill in character.db.mentskills.keys():
                    if reqstat.lower() == skill.lower():
                        if int(reqscore) > int(character.db.mentskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat.lower() == "mental":
                    #Some skill requirements are based in category, not specific skill.
                        if int(reqscore) > int(character.db.mentskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat == "Skill":
                    #Further, some skill requirements are based in having any skill at a particular rating.
                        if int(reqscore) > int(character.db.mentskills[skill]):
                            return False
                        else:
                            break
                for skill in character.db.physskills.keys():
                    if reqstat.lower() == skill.lower():
                        if int(reqscore) > int(character.db.physskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat.lower() == "physical":
                    #Some skill requirements are based in category, not specific skill.
                        if int(reqscore) > int(character.db.physskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat == "Skill":
                    #Further, some skill requirements are based in having any skill at a particular rating.
                        if int(reqscore) > int(character.db.physskills[skill]):
                            return False
                        else:
                            break
                for skill in character.db.socskills.keys():
                    if reqstat.lower() == skill.lower():
                        if int(reqscore) > int(character.db.socskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat.lower() == "mental":
                    #Some skill requirements are based in category, not specific skill.
                        if int(reqscore) > int(character.db.socskills[skill]):
                            return False
                        else:
                            break
                    elif reqstat == "Skill":
                    #Further, some skill requirements are based in having any skill at a particular rating.
                        if int(reqscore) > int(character.db.socskills[skill]):
                            return False
                        else:
                            break
                for searchmerit in character.db.meritlist:
                    if reqstat.lower() == searchmerit.name.lower():
                    #Checks to see if the merit is held by the character at all.
                        if reqnote != "" and searchmerit.note.lower() != reqnote:
                        #Checks to see if the proper note is there or not.
                            return False
                        else:
                            if int(reqscore) > int(searchmerit.score):
                                return False
                            else:
                                break
                    else:
                        return False      
    def CompareMeritStat(self, stat, comparison, base):
            compstat = stat.replace(comparison,"")
            if comparison == "+":
                if stat >= compstat + base:
                    pass
                else:
                    return False
            elif comparison == ">":
                if stat > compstat:
                    pass
                else:
                    return False
            elif comparison == "=":
                if stat >= compstat:
                    pass
                else:
                    return False
            elif comparison == "<":
                if stat < compstat:
                    pass
                else:
                    return False
    def BookCode(self, codein):
        booklong = self.booklong
        bookshort = self.bookshort
        return booklong[bookshort.index(codein)]
    def GetBook(self, merit):
        return self.BookCode(self.reference.split("-")[0])
    def at_script_creation(self):
        self.db.atariya = []
        self.db.dreamer = []
        self.db.infected = []
        self.db.lostboy = []
        self.db.plain = []
        self.db.psyvamp = []
        self.db.addons = []
        self.db.physical = []
        self.db.mental = []
        self.db.social = []
        self.db.fighting = []
        self.db.supernatural = []
        self.db.vampire = []
        self.db.ghoul = []
        self.db.werewolf = []
        self.db.wolfblood = []
        self.db.mage = []
        self.db.sleepwalker = []
        self.db.changeling = []
        self.db.faetouched = []
        self.db.beast = []
        self.db.promethean = []
        self.db.hunter = []
        self.db.mummy = []
        self.db.demon = []
        self.db.bookshort = self.bookshort
        self.db.booklong = self.booklong
        physical = self.db.physical
        mental = self.db.mental
        social = self.db.social
        fighting = self.db.fighting
        supernatural = self.db.supernatural
        vampire = self.db.vampire
        ghoul = self.db.ghoul
        werewolf = self.db.werewolf
        wolfblood = self.db.wolfblood
        mage = self.db.mage
        sleepwalker = self.db.sleepwalker
        changeling = self.db.changeling
        faetouched = self.db.faetouched
        beast = self.db.beast
        promethean = self.db.promethean
        hunter = self.db.hunter
        mummy = self.db.mummy
        demon = self.db.demon
        addons = self.db.addons
        atariya = self.db.atariya
        dreamer = self.db.dreamer
        infected = self.db.infected
        lostboy = self.db.lostboy
        plain = self.db.plain
        psyvamp = self.db.psyvamp
        if len(mental) == 0:
            mental.append(tuple(["Area of Expertise","1","CoD-44","Resolve,2","Specialty"]))
            mental.append(tuple(["Common Sense","3","CoD-44"]))
            mental.append(tuple(["Danger Sense","2","CoD-44"]))
            mental.append(tuple(["Direction Sense","1","CoD-44"]))
            mental.append(tuple(["Diviner","1,2,3,4,5","CtL:PTM-44","Lucid Dreamer"]))
            mental.append(tuple(["Eidetic Memory","2","CoD-44"]))
            mental.append(tuple(["Encyclopedic Knowledge","2","CoD-44"]))
            mental.append(tuple(["Eye for the Strange","2","CoD-44","Resolve,2","Occult,1"]))
            mental.append(tuple(["Fast Reflexes","1,2,3","CoD-44","Wits,3/Dexterity,3"]))
            mental.append(tuple(["Good Time Management","1","CoD-44","Academics,2/Science/2"]))
            mental.append(tuple(["Holistic Awareness","CoD-44","1"]))
            mental.append(tuple(["Indomitable","2","CoD-45","Resolve,3"]))
            mental.append(tuple(["Interdisciplinary Specialty","1","CoD-45","Skill,3","Specialty"]))
            mental.append(tuple(["Investigative Aide","1","CoD-45","Skill,3"]))
            mental.append(tuple(["Investigative Prodigy","1,2,3,4,5","CoD-45","Wits,3","Investigation,3"]))
            mental.append(tuple(["Language","1","CoD-45"]))
            mental.append(tuple(["Library","1,2,3,","CoD-46"]))
            mental.append(tuple(["Library Advanced","1,2,3,4,5","BtP-117","Library,3","Safe Place"]))
            mental.append(tuple(["Lucid Dreamer","2","CtL:PTM-54","Resolve,3","!Changeling"]))
            mental.append(tuple(["Meditative Mind","1,2,4","CoD-46"]))
            mental.append(tuple(["Multilingual","1","CoD-46"]))
            mental.append(tuple(["Patient","1","CoD-46"]))
            mental.append(tuple(["Professional Training","1,2,3,4,5","CoD-46"]))
            mental.append(tuple(["Tolerance for Biology","2","CoD-46"]))
            mental.append(tuple(["Trained Observer","1,3","CoD-46"]))
            mental.append(tuple(["Vice-Ridden","2","CoD-46"]))
            mental.append(tuple(["Virtuous","2","CoD-46"]))
            mental.append(tuple(["Warded Dreams","1,2,3","CtL:PTM-58","Resolve,="]))
            mental.append(tuple(["Coheisve Unit","1,2,3","HL-42","Presence,3"]))
            mental.append(tuple(["Defender","1,2,3","HL-42"]))
            mental.append(tuple(["Object Fetishism","1,2,3,4,5","HL-42"]))
            mental.append(tuple(["Punch Drunk","2","HL-43","Willpower,6"]))
            mental.append(tuple(["Scarred","1","HL-43","sanity,-5","Mortal"]))
        if len(physical) == 0:
            physical.append(tuple(["Ambidextrous","3","CoD-47"]))
            physical.append(tuple(["Automotive Genius","1","CoD-47","Crafts,3","Drive,1","Science,1"]))
            physical.append(tuple(["Crack Driver","2,4","CoD-47","Drive,3"]))
            physical.append(tuple(["Demolisher","1,2,3","CoD-47","Strength,3/Intelligence,3"]))
            physical.append(tuple(["Double-Jointed","2","CoD-47","Dexterity,3"]))
            physical.append(tuple(["Fleet of Foot","CoD-47","1,2,3","Athletics,2"]))
            physical.append(tuple(["Giant","3","CoD-47"]))
            physical.append(tuple(["Hardy","1,2,3","CoD-47","Stamina,3"]))
            physical.append(tuple(["Greyhound","1","CoD-48","Athletics,3","Wits,3","Stamina,3"]))
            physical.append(tuple(["Iron Stamina","1,2,3","CoD-48","Stamina,3/Resolve,3"]))
            physical.append(tuple(["Parkour","1,2,3,4,5","CoD-48","Dexterity,3","Athletics,2"]))
            physical.append(tuple(["Quick Draw","1","CoD-49","Wits,3","Weaponry Specialty/Firearms Specialty"]))
            physical.append(tuple(["Relentless","1","CoD-49","Athletics,2","Stamina,3"]))
            physical.append(tuple(["Seizing the Edge","2","CoD-49","Wits,3","Composure,3"]))
            physical.append(tuple(["Sleight of Hand","2","CoD-49","Larceny,3"]))
            physical.append(tuple(["Small-Framed","2","CoD-49"]))
            physical.append(tuple(["Stunt Driver","1,2,3,4,5","CoD-49","Dexterity,3","Drive,3","Wits,3"]))
            physical.append(tuple(["Body as weapon","2","HL-41","Stamina,3","Brawl,2"]))
            physical.append(tuple(["Survivalist","1","HL-43","Iron Stamina,3","Survival,3"]))
        if len(social) == 0:
            social.append(tuple(["Allies","1,2,3,4,5","CoD-49"]))
            social.append(tuple(["Alternate Identity","CoD-50","1,2,4"]))
            social.append(tuple(["Anonymity","1,2,3,4,5","CoD-50","!Fame"]))
            social.append(tuple(["Barfly","2","CoD-50","Socialize,2"]))
            social.append(tuple(["Closed Book","1,2,3,4,5","CoD-50","Manipulation,3","Resolve,3"]))
            social.append(tuple(["Destiny","1,2,3,4,5","MtA-100"]))
            social.append(tuple(["Etiquette","1,2,3,4,5","VtR-120","Composure,3","Socialize,2"]))
            social.append(tuple(["Fame","1,2,3","CoD-50"]))
            social.append(tuple(["Fast-Talking","1,2,3,4,5","CoD-50","Manipulation,3","Subterfuge,2"]))
            social.append(tuple(["Fixer","2","CoD-51","Contacts,2","Wits,3"]))
            social.append(tuple(["Hobbyist Clique","CoD-51","2","Skill,2"]))
            social.append(tuple(["Inspiring","3","CoD-51","Presence,3"]))
            social.append(tuple(["Iron Will","2","CoD-51","Resolve,4"]))
            social.append(tuple(["Mentor","1,2,3,4,5","CoD-51"]))
            social.append(tuple(["Mystery Cult Initiation","CoD-51","1,2,3,4,5"]))
            social.append(tuple(["Resources","CoD-53","1,2,3,4,5"]))
            social.append(tuple(["Pusher","1","CoD-52","Persuasion,2"]))
            social.append(tuple(["Retainer","1,2,3,4,5","CoD-53"]))
            social.append(tuple(["Safe Place","1,2,3,4,5","CoD-54"]))
            social.append(tuple(["Small Unit Tactics","2","CoD-54","Presence,3"]))
            social.append(tuple(["Spin Doctor","1","CoD-54","Manipulation,3","Subterfuge,2"]))
            social.append(tuple(["Staff","1,2,3,4,5","CoD-54"]))
            social.append(tuple(["Status","1,2,3,4,5","CoD-54"]))
            social.append(tuple(["Striking Looks","1,2","CoD-54"]))
            social.append(tuple(["Sympathetic","2","CoD-55"]))
            social.append(tuple(["Table Turner","1","CoD-55","Composure,3","Manipulation,3","Wits,3"]))
            social.append(tuple(["Takes one to know one","1","CoD-55"]))
            social.append(tuple(["Taste","1","CoD-55","Crafts,2","Specialty"]))
            social.append(tuple(["True Friend","3","CoD-56"]))
            social.append(tuple(["Untouchable","1","CoD-56","Manipulation,3","Subterfuge,2"]))
            social.append(tuple(["Air of Menace","2","HL-41","Intimidation,2"]))
            social.append(tuple(["Empath","2","HL-42","Empathy,2"]))
            social.append(tuple(["Peacemaker","2,3""HL-42","Wits,3","Empathy,3"]))
            social.append(tuple(["Support Network","1,2,3,4,5","HL-43", "Integrity"]))
        if len(supernatural) == 0:
            supernatural.append(tuple(["Aura Reading","3","CoD-56"]))
            supernatural.append(tuple(["Automatic Writing","2","CoD-56"]))
            supernatural.append(tuple(["Biokinesis","1,2,3,4,5","CoD-57"]))
            supernatural.append(tuple(["Clairvoyance","3","CoD-57"]))
            supernatural.append(tuple(["Cursed","2","CoD-57"]))
            supernatural.append(tuple(["Laying on Hands","3","CoD-57"]))
            supernatural.append(tuple(["Medium","3","Empathy,2","CoD-57"]))
            supernatural.append(tuple(["Mind of a Madman","2","CoD-57","Empathy,2"]))
            supernatural.append(tuple(["Omen Sensitivity","3","CoD-58"]))
            supernatural.append(tuple(["Producer","1","VtR-299","Mortal"]))
            supernatural.append(tuple(["Numbing Touch","1,2,3,4,5","CoD-58"]))
            supernatural.append(tuple(["Psychokinesis","3,5","CoD-58"]))
            supernatural.append(tuple(["Psychometry","3","CoD-58"]))
            supernatural.append(tuple(["Telekinesis","1,2,3,4,5","CoD-59"]))
            supernatural.append(tuple(["Telepathy","3,5","CoD-59"]))
            supernatural.append(tuple(["Thief of Fate","3","CoD-60"]))
            supernatural.append(tuple(["Unseen Sense","2","CoD-60"]))
            supernatural.append(tuple(["Sleepwalker","1","MtA-306","Mortal"]))
            supernatural.append(tuple(["Weakened Bond","3","VtR-299","Mortal"]))
            supernatural.append(tuple(["Protected","2","VtR-299","Mortal"]))
            supernatural.append(tuple(["Fitful Slumber","1","MtA-306","Mortal/Hunter/Mortal+"]))
            supernatural.append(tuple(["Animal Possession","2,4","HL-72","Animal Ken,3"]))
            supernatural.append(tuple(["Apportation","3,5","HL-72"]))
            supernatural.append(tuple(["Assertive Implement","1,2,3","HL-72","Manipulation,3","Occult,2","Firearms,2/Weaponry,2"]))
            supernatural.append(tuple(["Biomimicry","1,2,3,4","HL-72","Biokinesis,1"]))
            supernatural.append(tuple(["Bless Amulet","1,2,3","HL-72","Occult,3"]))
            supernatural.append(tuple(["Camera Obscura","3","HL-73","Unseen Sense (Ghosts),2/Unseen Sense (Spirits),2"]))
            supernatural.append(tuple(["Consecrate Weaponry","4","HL-73","Resolve,3","Occult,4"]))
            supernatural.append(tuple(["Curse Effigy","3","HL-73"]))
            supernatural.append(tuple(["Dark Passenger","2","HL-73"]))
            supernatural.append(tuple(["Doppelganger","3","HL-73","Biokinesis,1","Subterfuge,3"]))
            supernatural.append(tuple(["Evil Eye","2","HL-73"]))
            supernatural.append(tuple(["Fated Ferocity","1,2,3,4,5","HL-73","Cursed,2","Resolve,3","Stamina,2"]))
            supernatural.append(tuple(["Hardened Exorcist","1","HL-74"]))
            supernatural.append(tuple(["Hidden Variable","2","HL-74","Unseen Sense (God-Machine),2"]))
            supernatural.append(tuple(["Incite Ecosystem","1,2,3,4,5","HL-74","Animal Ken,3"]))
            supernatural.append(tuple(["Invoke Spirit","2","HL-74","Resolve,3","Medium,3"]))
            supernatural.append(tuple(["Mind Control","3","HL-74"]))
            supernatural.append(tuple(["Phantasmagoria","2","HL-74","Telepathy,5","Expression,2"]))
            supernatural.append(tuple(["Psychic Concealment","3","HL-75","Mind Control,3","Stealth,3"]))
            supernatural.append(tuple(["Psychic Onslaught","1,2,3,4,5","HL-75","Telekinesis,1/Psychokinesis,1"]))
            supernatural.append(tuple(["Psychic Poltergeist","2","HL-75","Telekinesis,1"]))
            supernatural.append(tuple(["Psychokinetic Combat","1,2,3,4,5","HL-76","Psychokinesis,3"]))
            supernatural.append(tuple(["Psychokinetic Resistance","1","HL-76","Psychokinesis,1"]))
            supernatural.append(tuple(["Sacrificial Offering","1,2,3,4,5","HL-76","Occult,3","Mystery Cult Initiation,5"]))
            supernatural.append(tuple(["Sojurner","3","HL-76","Apportation,3"]))
            supernatural.append(tuple(["Tactical Telepathy","1,2,3,4,5","HL-76","Telepathy,5"]))
            supernatural.append(tuple(["Technopathy","2,3","HL-77"]))
            supernatural.append(tuple(["Telekinetic Evasion","3","HL-77","Telekinesis,1"]))
            supernatural.append(tuple(["Vengeful Soul","2","HL-77"]))
            supernatural.append(tuple(["Supernatural Resitance","1,2,3,4,5","HL-78","Supernatural Merit"]))
        if len(atariya) == 0:
            atariya.append(tuple(["Damn Lucky","1,2,3,4","HL-79","Mortal"]))
            atariya.append(tuple(["Mr. Lucky","1","HL-80","Mortal","Damn Lucky"]))
            atariya.append(tuple(["Nine Lives","1,2,3,4,5","HL-80","Mortal","Damn Lucky"]))
            atariya.append(tuple(["See the Flow","1,2,3,4,5","HL-81","Mortal","Damn Lucky"]))
            atariya.append(tuple(["Luck Flows Up","2","HL-81","Mortal","Damn Lucky","!Thief of Fate"]))
            atariya.append(tuple(["Easy come, easy go","1","HL-81","Mortal","Damn Lucky"]))
            atariya.append(tuple(["All In","3","HL-81","Mortal","Damn Lucky","Resolve,3"]))
        if len(dreamer) == 0:
            dreamer.append(tuple(["Subliminal Conditioning","1,2,3,4,5","HL-83","Mortal"]))
            dreamer.append(tuple(["A word from our sponsor","2,3","HL-84","Subliminal Conditioning","Mortal"]))
            dreamer.append(tuple(["Realpolitik","1,2,3","HL-84","Mortal","Subliminal Conditioning"]))
            dreamer.append(tuple(["Memory Palace","1,2,3,4,5","HL-84","Mortal","Subliminal Conditioning"]))
            dreamer.append(tuple(["The Treatment","1,2,3,4,5","HL-84","Mortal","Subliminal Conditioning"]))
            dreamer.append(tuple(["Not a bug, but a feature","2,3","HL-85","Mortal","Subliminal conditioning","The Treatment,1"]))
            dreamer.append(tuple(["Mephistopheles","2","HL-85","Mortal","Subliminal Conditioning"]))
            dreamer.append(tuple(["Deja Vu","1,2,3,","HL-85","Mortal","Subliminal Conditioning"]))
            dreamer.append(tuple(["Field Handler","1,2,3,4,5","HL-85","Subliminal Conditioning","Mortal"]))
        if len(infected) == 0:
            infected.append(tuple(["Carrier","1,2,3,4,5","HL-88","Mortal"]))
            infected.append(tuple(["Bulletman Syndrome","5","HL-88","Mortal","Carrier,5"]))
            infected.append(tuple(["The New Flesh","1,3,5","HL-89","Mortal","Carrier,="]))
            infected.append(tuple(["Patient Zero","2","HL-90","Mortal","Carrier,="]))
            infected.append(tuple(["Pround Parent","1","HL-90","Mortal","Carrier,1"]))
            infected.append(tuple(["Bloodkin","1","HL-90","Mortal","Carrier,1"]))
            infected.append(tuple(["Virulent","2,3,4","HL-90","Mortal","Carrier,="]))
        if len(plain) == 0:
            plain.append(tuple(["Plain Reader","1","HL-92","Mortal"]))
            plain.append(tuple(["You are being recorded","1","HL-93","Mortal","Plain Reader,1"]))
            plain.append(tuple(["I'm bleeding on you","1","HL-93","Mortal","Plain Reader,1"]))
            plain.append(tuple(["Most infected thing I've ever seen","2","HL-94","Mortal","Plain Reader,1"]))
            plain.append(tuple(["Over before it started","1","HL-94","Mortal","Plain reader,1"]))
            plain.append(tuple(["Phantom pain","1","HL-94","Mortal","I'm bleeding on you,1"]))
            plain.append(tuple(["Consequences of violence","1","HL-94","Mortal","Plain reaader,1"]))
            plain.append(tuple(["The Push","1,2,3,4,5","HL-94","Mortal","Plain reader"]))
        if len(lostboy) == 0:
            lostboy.append(tuple(["The Protocol","1,2,3,4,5","HL-96","Mortal"]))
            lostboy.append(tuple(["Protocol Fixer","1,2,3,4,5","HL-97","Mortal","The Protocol,1"]))
            lostboy.append(tuple(["Archangel System","5","HL-97","Mortal","The Protocol,5"]))
            lostboy.append(tuple(["Augmented Resilience","1,2,3","HL-98","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Augmented Speed","1,2,3,4,5","HL-98","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Cloaking Device","3","HL-99","Mortal","The Protocol,3"]))
            lostboy.append(tuple(["Holdout Storage","1,2,3","HL-99","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Implanted Interface","2","HL-99","Mortal","The Protocol,2"]))
            lostboy.append(tuple(["Jumper","1,2,3","HL-99","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Last Chance System","5","HL-99","Mortal","The Protocol,5"]))
            lostboy.append(tuple(["Pulse Generator","1,2,3,4,5","HL-99","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Strength Augmentation","1,2,3","HL-100","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Sub-Dermal Armor","2,4","HL-100","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Uncanny Perception","1,2,3","HL-100","Mortal","The Protocol,="]))
            lostboy.append(tuple(["Voice Box","1","HL-100","Mortal","The Protocol,1"]))
        if len(psyvamp) == 0:
            psyvamp.append(tuple(["Psychic Vampirism","1,2,3,4,5","HL-101","Mortal"]))
            psyvamp.append(tuple(["Breath Stealer","1,2,3","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Burst of Speed","1","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Ephemeral Battery","1,2,3,4,5","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Euphoric Touch","1,2,3","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Nocturnal Supremacy","2,5,9,14","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Psychic Infection","1","HL-103","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Psychic Seduction","1","HL-104","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Psychic Transference","2","HL-104","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Shapechanging","2,3","HL-104","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Soul Eater","2","HL-104","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Unearthly Beauty","1,2","HL-104","Mortal","Psychic Vampirism,1"]))
            psyvamp.append(tuple(["Vampiric Potency","1,2,3,4,5","HL-104","Mortal","Psychic Vampirism,1"]))
        if len(fighting) == 0:
            fighting.append(tuple(["Armed Defense","1,2,3,4,5","CoD-60","Dexterity,3","Weponry,2","Defensive Combat (Weaponry)"]))
            fighting.append(tuple(["Brute Force","1,2,3,4,5","PtC-112","Strength,3","Brawl,2","Size,5"]))
            fighting.append(tuple(["Cheap Shot","2","CoD-61","Street Fighting,3","Subterfuge,2"]))
            fighting.append(tuple(["Choke Hold","2","CoD-61","Brawl,2"]))
            fighting.append(tuple(["Close Quarters Combat","1,2,3,4,5,","CoD-61","Wits,3","Athletics,2","Brawl,3"]))
            fighting.append(tuple(["Defensive Combat","1","CoD-61","Brawl,1/Weaponry,1"]))
            fighting.append(tuple(["Fighting Finesse","2","CoD-61","Dexterity,3","Weaponry Specialty/Brawl Specialty"]))
            fighting.append(tuple(["Firefight","1,2,3","CoD-61","Composure,3","Dexterity,3","Athletics,2","Firearms,2"]))
            fighting.append(tuple(["Grappling","1,2,3,4,5","CoD-62","Stamina,3","Stength,2","Athletics,2","Brawl,2"]))
            fighting.append(tuple(["Heavy Weapons","1,2,3,4,5","CoD-62","Stamina,3","Strength,2","Athletics,2","Weaponry,2"]))
            fighting.append(tuple(["Improvised Weaponry","1,2,3","CoD-62","Wits,3","Weaponry,1"]))
            fighting.append(tuple(["Iron Skin","2,4","CoD-63","Martial Arts,2/Street Fighting,2","Stamina,3"]))
            fighting.append(tuple(["Light Weapons","1,2,3,4,5","CoD-63","Wits,3/Fighting Finesse","Dexterity,3","Athletics,2","Weaponry,2"]))
            fighting.append(tuple(["Marksmanship","1,2,3,4","CoD-63","Composure,3","Resolve,3","Firearms,2"]))
            fighting.append(tuple(["Martial Arts","1,2,3,4,5","CoD-63","Resolve,3","Dexterity,3","Athletics,2","Brawl,2"]))
            fighting.append(tuple(["Police Tactics","1,2,3","CoD-64","Brawl,2","Weaponry,1"]))
            fighting.append(tuple(["Shiv","1,2","CoD-64","Street Fighting,2","Weaponry,1"]))
            fighting.append(tuple(["Street Fighting","1,2,3,4,5","CoD-65","Stamina,3","Composure,3","Brawl,2","Streetwise,2"]))
            fighting.append(tuple(["Unarmed Defense","1,2,3,4,5","CoD-64","Dexterity,3","Brawl,2","Defensive Combat (Brawl)"]))
            fighting.append(tuple(["Avoidance","1,2,3,4,5","HL-46","Manipulation,3","Athletics,2","Stealth,2"]))
            fighting.append(tuple(["Berserker","1,2,3","HL-46","Iron Stamina,3","Strength,3"]))
            fighting.append(tuple(["Bowmanship","1,2,3,4","HL-47","Dexterity,3","Firearms,2","Trained Observer,1"]))
            fighting.append(tuple(["Boxing","1,2,3,4,5","HL-47","Strength,2","Dexterity,2","Stamina,2","Athletics,2","Brawl,2"]))
            fighting.append(tuple(["Chain Weapons","1,2","HL-48","Strength,3","Dexterity,3","Athletics,2","Weaponry,2"]))
            fighting.append(tuple(["Combat Archery","1,2,3,4,5","HL-48","Strength,3","Athletics,2","Quick Draw (Bow),1"]))
            fighting.append(tuple(["Falconry","1,2,3,4","HL-48","Wits,3","Animal Ken,3"]))
            fighting.append(tuple(["K-9","1,2,3,4","HL-49","Wits,3","Animal Ken,3"]))
            fighting.append(tuple(["Kino Mutai","1,2,3,4,5","HL-50"]))
            fighting.append(tuple(["Mounted Combat","1,2,3,4","HL-51","Dexterity,3","Athletics,2","Animal Ken,2"]))
            fighting.append(tuple(["Powered Projectile","1,2,3,4","HL-51","Dexterity,3","Athletics,2","Firearms,2"]))
            fighting.append(tuple(["Spear and Bayonet","1,2,3","HL-51","Strength,3","Dexterity,2","Weaponry,2"]))
            fighting.append(tuple(["Staff Fighting",",1,2,3,4","HL-51","Strength,2","Dexterity,3","Weaponry,2"]))
            fighting.append(tuple(["Strength Performance","1,2,3,4","HL-52","Strength,3","Stamina,2","Athletics,2"]))
            fighting.append(tuple(["Systema","1,2,3","HL-52","Dexterity,3","Athletics,3","Wits,2"]))
            fighting.append(tuple(["Thrown Weapons","1,2","HL-52","Dexterity,3","Athletics,2","Quick Draw,1"]))
            fighting.append(tuple(["Two-Weapon Fighting","1,2,3,4","HL-53","Wits,3","Fighting Finesse,2","Weaponry,3"]))
            fighting.append(tuple(["Weapon and Shiled","1,2,3,4","HL-53","Strength,3","Stamina,3","Weaponry,2"]))
            fighting.append(tuple(["Aggressive Driving","1,2,3,4","HL-55"]))
            fighting.append(tuple(["Drone Control","1,2,3","HL-55","Intelligence,3","Computer,3","Drive,2"]))
            fighting.append(tuple(["Trigger Discipline","1","HL-143","Wits,2","Firearms,2"]))
            fighting.append(tuple(["Loaded for bear","1,2","HL-143","Athletics,1","Survival,1"]))
            fighting.append(tuple(["Killer Instinct","1,2,3","BtP-117","Composure,3","Medicine,1","Wits,3"]))
        if len(addons) == 0:
            addons.append(tuple(["Armed Rerstraint","2","HL-53","Staff Fighting,3"]))
            addons.append(tuple(["Boot Party","2","HL-53","Brawl,2"]))
            addons.append(tuple(["Clinch Strike","1","HL-53","Brawl,2"]))
            addons.append(tuple(["Covert Operative","1","HL-53","Wits,3","Dexterity,3","Stealth,2"]))
            addons.append(tuple(["Ground and Pound","2","HL-54","Brawl,2"]))
            addons.append(tuple(["Ground Fighter","3","HL-54","Wits,3","Dexterity,3","Brawl,2"]))
            addons.append(tuple(["Headbutt","1","HL-54","Brawl,2"]))
            addons.append(tuple(["Iron Chin","2,4","HL-54","Resolve,3","Stamina,3"]))
            addons.append(tuple(["Phalanx Fighter","2","HL-54","Weapon and Shield,2","Spear and Bayonet,1"]))
            addons.append(tuple(["Trunk Squeeze","2","HL-54","Brawl,2"]))
            addons.append(tuple(["Retain Weapon","2","HL-54","Wits,2","Brawl,2"]))
            addons.append(tuple(["Roadkill","3","HL-55","Aggressive Driving,2"]))
        if len(vampire) == 0:
            vampire.append(tuple(["Acute Senses","1","VtR-109"]))
            vampire.append(tuple(["Altar","3","VtR-109","Status (Circle of the Crone),1"]))
            vampire.append(tuple(["Anointed","2","VtR-109","Status (Lancea et Sannctum),1"]))
            vampire.append(tuple(["Atrocious","1","VtR-110","!Cutthroat","!Enticing"]))
            vampire.append(tuple(["Attache","1","VtR-110","Status (Invictus),1"]))
            vampire.append(tuple(["Bloodhound","2","VtR-110","Wits,3"]))
            vampire.append(tuple(["Cacophony Savvy","1,2,3","VtR-110","Status (Praxis),1"]))
            vampire.append(tuple(["Carthian Pull","1","VtR-110","Status (Carthians) 1"]))
            vampire.append(tuple(["Claws of the Unholy","1","VtR-110","Protean,4"]))
            vampire.append(tuple(["Close Family","1","VtR-111"]))
            vampire.append(tuple(["Cutthroat","1","VtR-111","!Atrocious","!Enticing"]))
            vampire.append(tuple(["Distinguished Palate","1","VtR-111"]))
            vampire.append(tuple(["Dream Visions","1","VtR-111","Mekhet"]))
            vampire.append(tuple(["Dynasty Membership","1,2,3","VtR-112","Status (Daeva),1/Status (Gangrel),1/Status (Mekhet),1/Status (Nosferatu),1/Status (Ventrue),1"]))
            vampire.append(tuple(["Enticing","1","VtR-112","!Atrocious","!Cutthroat"]))
            vampire.append(tuple(["Feeding Grounds","1,2,3,4,5","VtR-112"]))
            vampire.append(tuple(["Friends in High Places","1","VtR-112","Status (Invictus)","1"]))
            vampire.append(tuple(["Haven","1,2,3,4,5","VtR-112","Safe Place,1"]))
            vampire.append(tuple(["Herd","1,2,3,4,5","VtR-112"]))
            vampire.append(tuple(["Honey Trap","1","VtR-112"]))
            vampire.append(tuple(["Invested","1","VtR-112","Status (Invictus),1"]))
            vampire.append(tuple(["Kiss of the Succubus","1","VtR-113","Daeva"]))
            vampire.append(tuple(["Lineage","1","VtR-113","Status (Daeva),1/Status (Gangrel),1/Status (Mekhet),1/Status (Nosferatu),1/Status (Ventrue),1"]))
            vampire.append(tuple(["Lorekeeper","1","VtR-113","Status (Lancea et Sanctum),1"]))
            vampire.append(tuple(["The Mother-Daughter Bond","1","VtR-113","Status (Circle of the Crone),1"]))
            vampire.append(tuple(["Night Doctor Surgery","3","VtR-113","Status (Carthians),1"]))
            vampire.append(tuple(["Speaker for the Silent","3","VtR-114","Dynasty Membership,1","Status (Invictus),1"]))
            vampire.append(tuple(["Pack Alpha","1","VtR-114","Gangrel"]))
            vampire.append(tuple(["Unnatural Affinity","1,2,3,4,5","VtR-114"]))
            vampire.append(tuple(["Swarm Form","2","VtR-114","Protean,3"]))
            vampire.append(tuple(["Secret Society Junkie","1","VtR-114","Status (Ordo Dracul),1"]))
            vampire.append(tuple(["Sworn","1","VtR-114","Status (Ordo Dracul),1"]))
            vampire.append(tuple(["I know a guy","1","VtR-115","Status (Carthians),1"]))
            vampire.append(tuple(["Touchstone","1,2,3,4,5","VtR-115"]))
            vampire.append(tuple(["Undead Menses","2","VtR-115"]))
            vampire.append(tuple(["Unsettling Gaze","1","VtR-115","Nosferatu"]))
            vampire.append(tuple(["Where the Bodies are Buried","2","VtR-115","Status (Invictus),2"]))
            vampire.append(tuple(["Lex Terrae","2","VtR-116","Status (Carthians),2","Feeding Ground,1"]))
            vampire.append(tuple(["Mandate From the Masses","5","VtR-116","Status (Carthians),5"]))
            vampire.append(tuple(["Right of Return","2","VtR-116","Status (Carthians),2","Status (Praxis),1"]))
            vampire.append(tuple(["Strength of Resolution","1","VtR-116","Status (Carthians),1"]))
            vampire.append(tuple(["Plausible Deniability","4","VtR-116","Status (Carthians),3"]))
            vampire.append(tuple(["Notary","2","VtR-116","Status (Invictus),1"]))
            vampire.append(tuple(["Oath of Action","VtR-117","4"]))
            vampire.append(tuple(["Oath of Fealty","1","VtR-117","Status (Invictus),1"]))
            vampire.append(tuple(["Oath of Penance","3","VtR-117"]))
            vampire.append(tuple(["Kindred Dueling","1,2,3,4,5","VtR-117","Composure,3","Weaponry,2"]))
            vampire.append(tuple(["Riding the Wave","1,2,3,4,5","VtR-118","Composure,3","Resolve,3"]))
            vampire.append(tuple(["Alley Cat","1,2,3","SotC-177""Athletics,2","Stealth,2","Streetwise,2"]))
            vampire.append(tuple(["Army of One","1,2,3,4,5","SotC-177","Status (Carthians),="]))
            vampire.append(tuple(["Casual User","2","SotC-178","!Carthians"]))
            vampire.append(tuple(["Court Jester","2","SotC-178","Status (Praxis),2","Politics,2"]))
            vampire.append(tuple(["Devotion Experimenter","2","SotC-178","Status (Carthians),2","Science,2"]))
            vampire.append(tuple(["Fucking Thief","1","SotC-178","Subterfuge,3"]))
            vampire.append(tuple(["Jack-Booted Thug","2","SotC-178","Status (Carthians),2","Status (Praxis),1","Intimidation,3"]))
            vampire.append(tuple(["Mobilize Outrage","1,2,3","SotC-178","Brawl,2","Willpower,5"]))
            vampire.append(tuple(["Sell Out","3","SotC-179","Status (Carthians),4","Status (Praxis),4"]))
            vampire.append(tuple(["Smooth Crminal","2","SotC-179","Politics,1","Streetwise,2","Subterfuge,2"]))
            vampire.append(tuple(["Toss that shit right back","1","SotC-179","Athletics,2","Dexterity,3"]))
            vampire.append(tuple(["Breaking the Chains","1","SotC-179","Status (Carthians),1"]))
            vampire.append(tuple(["Cease Fire","1,2,3,4,5","SotC-180","Status (Carthians),5"]))
            vampire.append(tuple(["Coda against Sorcery","1,2,3,4,5","SotC-180","Status (Carthians),1"]))
            vampire.append(tuple(["Empower Judiciary","3","SotC-180","Status (Carthians),3"]))
            vampire.append(tuple(["Establish Precedent","2","SotC-180","Status (Carthians),4"]))
            vampire.append(tuple(["Weaponize Dissent","2","SotC-180","Status (Carthians),2"]))
            vampire.append(tuple(["Chorister","2","SotC-181","!Circle of the Crone"]))
            vampire.append(tuple(["Mandragora Garden","1,2,3,4,5","SotC-181","Safe Place,=","Cruac,1"]))
            vampire.append(tuple(["Temple Guardian","1,2,3","SotC-182","Athletics,2","Brawl,2","Weaponry,2"]))
            vampire.append(tuple(["Viral Mythology","3","SotC-182","Cruac,1","Presence,3","Expression,3"]))
            vampire.append(tuple(["What you've done for her lately","1","SotC-182","Cruac,2"]))
            vampire.append(tuple(["Unbridled Chaos","1,2,3,4,5","SotC-183","Cruac,1"]))
            vampire.append(tuple(["Primal Creation","1,2,3,4,5","SotC-183","Cruac,1"]))
            vampire.append(tuple(["Opening the Void","1,2,3,4,5","SotC-184","Cruac,1"]))
            vampire.append(tuple(["Courtoisie","1,2,3","SotC-187","Composure,3","Socialize,2","Weaponry,2"]))
            vampire.append(tuple(["Crowsourcing","1,2,3","SotC-187","Contacts,1","Resources,3"]))
            vampire.append(tuple(["Information Network","1","SotC-187","Contacts,1","Status (Invictus),2"]))
            vampire.append(tuple(["Moderator","1,2,3,4,5","SotC-187","Computer,3","Contacts (Online),1","Status (Invictus),2"]))
            vampire.append(tuple(["One foot in the door","2","SotC-187","!Invictus"]))
            vampire.append(tuple(["Noblesse Oblige","3","SotC-188","Status (City),3"]))
            vampire.append(tuple(["Prestigious Sire","2","SotC-188","Mentor,4"]))
            vampire.append(tuple(["Social Engineering","4","SotC-188","Investigation,2","Manipulation,3","Subterfuge,2","Wits,3"]))
            vampire.append(tuple(["Tech Savvy","1,2,3","SotC-188","Computer,2","Crafts,2","Science,1","Resources,1"]))
            vampire.append(tuple(["Travel Agent","1,2,3,4,5","SotC-188","Contacts (Inter-City),1","Status (Invictus),2"]))
            vampire.append(tuple(["Oath of Abstinence","5","SotC-189"]))
            vampire.append(tuple(["Oath of the Handshake Deal","1","SotC-189"]))
            vampire.append(tuple(["Oath of the Hard Motherfucker","2","SotC-189","!Status (Invictus)"]))
            vampire.append(tuple(["Oath of Matrimony","5","SotC-190"]))
            vampire.append(tuple(["Oath of the Model Prisoner","3","SotC-190"]))
            vampire.append(tuple(["Oath of Office","3","Status (Praxis),3/Status (Invictus),3"]))
            vampire.append(tuple(["Oath of the Refugee","2","SotC-191"]))
            vampire.append(tuple(["Oath of the Righteous Kill","SotC-191","3","Empathy,3","Status (Invictus),3"]))
            vampire.append(tuple(["Oath of the Safe Word","2","SotC-191"]))
            vampire.append(tuple(["Oath of the True Knight","4","SotC-191","Status (Invictus),2"]))
            vampire.append(tuple(["Crusade","1,2,3","SotC-192","Occult,2","Resolve,3","Weaponry,2","Theban Sorcery,2/Sorcerous Eunuch,1"]))
            vampire.append(tuple(["Flock","1,2,3,4,5","SotC-193","Herd,="]))
            vampire.append(tuple(["Laity","2","SotC-193","!Lancea et Sanctum"]))
            vampire.append(tuple(["Sanctuary","1,2,3,4,5","SotC-193","Status (Praxis),2","Status (Lancea et Sanctum),2","Safe Place,1"]))
            vampire.append(tuple(["Sorcerous Eunuch","1","SotC-193","Resolve,3"]))
            vampire.append(tuple(["Stigmata","1,2,3,4,5","SotC-193","Sanity,+3/Mortal"]))
            vampire.append(tuple(["Temple of Damnation","1,2,3,4,5","Sotc-194","Safe Place,="]))
            vampire.append(tuple(["Independent Study","2","SotC-197","!Ordo Dracul"]))
            vampire.append(tuple(["Nest Guardian","1,2,3,4,5","SotC-197"]))
            vampire.append(tuple(["Rites of the Impaled","1,2,3","SotC-197","Resolve,3","Stamina,3","Weaponry,2","Sworn"]))
            vampire.append(tuple(["Twilight Judge","3","SotC-198","Status (Ordo Dracul),4"]))
            vampire.append(tuple(["Chapterhouse","1,2,3,4,5","SotC-199","Status (Ordo Dracul),3"]))
            vampire.append(tuple(["Crucible","3","SotC-199","Occult,4"]))
            vampire.append(tuple(["Feng Shui","1,2,3,4,5","SotC-199","Academics,2","Occult,3"]))
            vampire.append(tuple(["Perilous Nest","1,2,3,4,5","SotC-199","Occult,3"]))
        if len(ghoul) == 0:
            ghoul.append(tuple(["Kindred Dueling","1,2,3,4,5","Composure,3","Weaponry,2"]))
            ghoul.append(tuple(["Taste of Shadow","2","VtR-298"]))
            ghoul.append(tuple(["Taste of the Serpent","2","VtR-298"]))
            ghoul.append(tuple(["Taste of the Wild","2","VtR-298"]))
            ghoul.append(tuple(["Taste of Gold","2","VtR-299"]))
            ghoul.append(tuple(["Taste of Fear","2","VtR-299"]))
            ghoul.append(tuple(["Producer","1","VtR-299"]))
            ghoul.append(tuple(["Weakened Bond","3","VtR-299"]))
            ghoul.append(tuple(["Clear-Sighted","2","VtR-299","Mortal"]))
            ghoul.append(tuple(["Source Sympathy","1","VtR-299"]))
            ghoul.append(tuple(["Protected","2","VtR-299"]))
            ghoul.append(tuple(["Empowered to Speak","1","VtR-300"]))
            ghoul.append(tuple(["Vitae Hound","1","VtR-300"]))
            ghoul.append(tuple(["Beast Whispers","2","VtR-300"]))
            ghoul.append(tuple(["Beloved","1","VtR-300"]))
            ghoul.append(tuple(["Watch Dog","2","VtR-300"]))
        if len(werewolf) == 0:
            werewolf.append(tuple(["Anchored","1,2","WtF-105"]))
            werewolf.append(tuple(["Blood or Bone Affinity","2,5","WtF-105","Sanity,>3","Sanity,<8"]))
            werewolf.append(tuple(["Code of Honor","2","WtF-105","Sanity,>7"]))
            werewolf.append(tuple(["Controlled Burn","2","WtF-105","Resolve,3","Composure,3"]))
            werewolf.append(tuple(["Creative Tactician","3","WtF-105","Purity,2"]))
            werewolf.append(tuple(["Dedicated Locus","1,2,3,4,5","WtF-106","Safe Place,="]))
            werewolf.append(tuple(["Embodiment of the Firstborn","5","WtF-106","!Ghost Wolves"]))
            werewolf.append(tuple(["Fading","3","WtF-106","Cunning,2"]))
            werewolf.append(tuple(["Favored Form","1,2,3,4,5","WtF-106","Powerstat,+1"]))
            werewolf.append(tuple(["Fortified Form","3,4,5","Stamina,3","Survival",2]))
            werewolf.append(tuple(["Hearing Whispers","2","WtF-106","Bone Shadows"]))
            werewolf.append(tuple(["Impartial Mediator","3","WtF-106","Honor,2"]))
            werewolf.append(tuple(["Living Weapon","3,4,5","WtF-107","Stamina,3","Survival,2"]))
            werewolf.append(tuple(["Locus","1,2,3,4,5","Custom","Safe Place,="]))
            werewolf.append(tuple(["Moon-Kissed","1","WtF-107","Auspice,2"]))
            werewolf.append(tuple(["Nowhere to Run","2","WtF-107","Hunters in Darkness"]))
            werewolf.append(tuple(["Pack Dynamics","3,4,5","WtF-107","Wisdom,2"]))
            werewolf.append(tuple(["Residential Area","1,2,3,4,5","WtF-107"]))
            werewolf.append(tuple(["Resonance Shaper","2","WtF-107"]))
            werewolf.append(tuple(["Self-Control","2","WtF-107","Resolve,4"]))
            werewolf.append(tuple(["Song in your Heart","3","WtF-107","Glory,2"]))
            werewolf.append(tuple(["Sounds of the City","2","WtF-107","Iron Masters"]))
            werewolf.append(tuple(["Strings of the Heart","2","WtF-108","Storm Lords"]))
            werewolf.append(tuple(["Weakest Link","2","WtF-108","Blood Talons"]))
            werewolf.append(tuple(["Call Out","2","WtF-108","Honor,2","Intimidation,2","Composure,3"]))
            werewolf.append(tuple(["Efficient Killer","2","WtF-108","Purity,2","Brawl,3","Medicine,2","Strength,3"]))
            werewolf.append(tuple(["Flanking","2","Cunning,2","WtF-108","Wits,3","Stealth,2","Brawl,3"]))
            werewolf.append(tuple(["Instinctive Defense","2","WtF-109","Powerstat,2"]))
            werewolf.append(tuple(["Relentless Assault","1,2,3,4,5","WtF-109","Strength,3","Stamina,3","Brawl,2"]))
            werewolf.append(tuple(["Spiritual Blockage","2","WtF-109","Wisdom,2","Brawl,1","Occult,3","Wits,3"]))
            werewolf.append(tuple(["Tactical Shifting","1,2,3,4,5","WtF-110","Wits,3","Dexterity,3","Athletics,2"]))
            werewolf.append(tuple(["Warcry","2","WtF-110","Glory,2","Presence,3","Expression,2","Intimidation,2"]))
            werewolf.append(tuple(["Den","1,2,3,4,5","TP-29"]))
            werewolf.append(tuple(["Directed Rage","3,4,5","TP-30"]))
            werewolf.append(tuple(["Magnanimous Totem","2,3,4","TP-30"]))
            werewolf.append(tuple(["Territorial Advantage","1,2,3,4,5","TP-31"]))
        if len(wolfblood) == 0:
            wolfblood.append(tuple(["Fenris-Ur's Blood","2","WtF-304"]))
            wolfblood.append(tuple(["Kamdis-Ur's Blood","2","WtF-304"]))
            wolfblood.append(tuple(["Hikaon-Ur's Blood","2","WtF-304"]))
            wolfblood.append(tuple(["Sagrim-Ur's Blood","2","WtF-304"]))
            wolfblood.append(tuple(["Skolis-Ur's Blood","2","WtF-304"]))
            wolfblood.append(tuple(["Ghost Child","2","WtF-304"]))
            wolfblood.append(tuple(["Crescent Moon's Birth","2","WtF-305"]))
            wolfblood.append(tuple(["Full Moon's Birth","2","WtF-305"]))
            wolfblood.append(tuple(["Gibbous Moon's Birth","2","WtF-305"]))
            wolfblood.append(tuple(["Half Moon's Birth","2","WtF-305"]))
            wolfblood.append(tuple(["No Moon's Birth","2","WtF-305"]))
            wolfblood.append(tuple(["Pack Bond","1,2,3","WtF-305"]))
            wolfblood.append(tuple(["Raised By Wolves","1","WtF-305"]))
            wolfblood.append(tuple(["Tell","3","WtF-305"]))
        if len(mage) == 0:
            mage.append(tuple(["Adamant Hand","2","MtA-99","Status (Adamantine Arrow),1","Athletics,3/Brawl,3/Weaponry,3"]))
            mage.append(tuple(["Artifact","3,4,5","MtA-99"]))
            mage.append(tuple(["Astral Adept","3","MtA-100""Mage/Sleepwalker"]))
            mage.append(tuple(["Between the Ticks","2","MtA-100","Wits,3","Time,1"]))
            mage.append(tuple(["Cabal Theme","1","MtA-100"]))
            mage.append(tuple(["Consilium/Order Status","MtA-100","1,2,3,4,5"]))
            mage.append(tuple(["Dream","1,2,3,4,5","Composure3,","Wits,3"]))
            mage.append(tuple(["Egregore","1,2,3,4,5","MtA-101","Status (Mysterium),1"]))
            mage.append(tuple(["Enhanced Item","1,2,3,4,5","MtA-101"]))
            mage.append(tuple(["Familiar","2,4","MtA-101"]))
            mage.append(tuple(["Fast Spells","2","MtA-101","Firearms,2","Time,1"]))
            mage.append(tuple(["Grimoire","1,2,3,4,5","MtA-101"]))
            mage.append(tuple(["Hallow","1,2,3,4,5","MtA-101"]))
            mage.append(tuple(["Imbued Item","1,2,3,4,5","MtA-102"]))
            mage.append(tuple(["Infamous Mentor","1,2,3,4,5","MtA-102","Mentor,="]))
            mage.append(tuple(["High Speech","1","MtA-102"]))
            mage.append(tuple(["Lex Magica","2","MtA-102","Status (Silver Ladder),1"]))
            mage.append(tuple(["Mana Sensitivity","1","MtA-102","Prime,1","Wits,3"]))
            mage.append(tuple(["Masque","1,2,3,4,5","MtA-102","Status (Guardians of the Veil),1"]))
            mage.append(tuple(["Mystery Cult Influence","3,4,5","MtA-103"]))
            mage.append(tuple(["Occultation","1,2,3","MtA-103"]))
            mage.append(tuple(["Potent Nimbus","1,2","MtA-103"]))
            mage.append(tuple(["Potent Resonance","2","MtA-103","Powerstat,3"]))
            mage.append(tuple(["Prelacy","1,2,3,4","MtA-103","Status (Seers of the Throne),3"]))
            mage.append(tuple(["Sanctum","1,2,3,4,5","MtA-104","Safe Place"]))
            mage.append(tuple(["Techne","2","MtA-104","Status (Free Concil),1"]))
            mage.append(tuple(["Shadow Name","1,2,3","MtA-104"]))
        if len(sleepwalker) == 0:
            sleepwalker.append(tuple(["Banner-bearer","1,2,3","MtA-305"]))
            sleepwalker.append(tuple(["Deadpan","3","MtA-305"]))
            sleepwalker.append(tuple(["Loved","3","MtA-306"]))
            sleepwalker.append(tuple(["Proxy Voice","1,2,3","MtA-306","Mentor,1"]))
            sleepwalker.append(tuple(["Relic Attuned","3","MtA-306"]))
            sleepwalker.append(tuple(["Ritual Martyr","2","MtA-306"]))
            sleepwalker.append(tuple(["Ritual Savvy","2","MtA-306","Occult,2"]))
            sleepwalker.append(tuple(["Slippery","2","MtA-306"]))
        if len(changeling) == 0:
            changeling.append(tuple(["Acute Senses","1","CtL:PTM-41","Wits3/Composure,3","Sanity,>6"]))
            changeling.append(tuple(["Arcadian Body","4","CtL:PTM-41"]))
            changeling.append(tuple(["Arcadian Metabolism","3","CtL:PTM-41"]))
            changeling.append(tuple(["Bedlam Bringer","1,2,3","CtL:PTM-42""Powerstat,>5"]))
            changeling.append(tuple(["Bounty","1,2,3,4,5","CtL:PTM-42"]))
            changeling.append(tuple(["Brownie's Boon","1","CtL:PTM-42"]))
            changeling.append(tuple(["Command Intensity","1","CtL:PTM-42","Powerstat,3"]))
            changeling.append(tuple(["Court Goodwill","1,2,3,4,5","CtL:PTM-43"]))
            changeling.append(tuple(["Defensive Dreamscaping","1","CtL:PTM-44","Powerstat,2","Expression,1"]))
            changeling.append(tuple(["Dual Kith","2","CtL:PTM-45"]))
            changeling.append(tuple(["Dull Beacon","1,2,3,4,5","CtL:PTM-45"]))
            changeling.append(tuple(["Elemental Battle","1,2,3,4,5","CtL:PTM-45","Dexterity,3/Wits,3","Brawl,3/Firearms,3/Weaponry,3","Cloak of the Elements"]))
            changeling.append(tuple(["Enchanting Performance","1,2,3","CtL:PTM-46","Presence,3","Expression,3"]))
            changeling.append(tuple(["Environmental Assault","1","Powerstat,2","CtL:PTM-47"]))
            changeling.append(tuple(["Fae Mount","1,2,3,4,5","CtL:PTM-47"]))
            changeling.append(tuple(["Faerie Favor","2","CtL:PTM-48"]))
            changeling.append(tuple(["Fair Harvest","1,2","CtL:PTM-48"]))
            changeling.append(tuple(["Forever and a Day","1","CtL:PTM-48"]))
            changeling.append(tuple(["Faerie Healing","3","CtL:PTM-49"]))
            changeling.append(tuple(["Gentrified Bearing","2","CtL:PTM-49""Powerstat,2"]))
            changeling.append(tuple(["Glamour Fasting","1","CtL:PTM-49"]))
            changeling.append(tuple(["Harvest","1,2,3,4,5","CtL:PTM-49"]))
            changeling.append(tuple(["Hedge Battler","2","CtL:PTM-50"]))
            changeling.append(tuple(["Hedge Duelist","1,2,3","CtL:PTM-50","Dexterity,2","Presencem2","Brawl,2/Weaponry,2","Social,2"]))
            changeling.append(tuple(["Hedge Sense","1","CtL:PTM-50"]))
            changeling.append(tuple(["Hedgebeast Companion","1,2,3","CtL:PTM-50"]))
            changeling.append(tuple(["Hedgespun","1,2,3,4,5","CtL:PTM-50"]))
            changeling.append(tuple(["Hob Kin","2","CtL:PTM-51"]))
            changeling.append(tuple(["Hollow","1,2,3,4,5","CtL:PTM-51"]))
            changeling.append(tuple(["Legendary Language","1","CtL:PTM-54"]))
            changeling.append(tuple(["Lethal Mien","2","CtL:PTM-54"]))
            changeling.append(tuple(["Long of Days","2","CtL:PTM-54"]))
            changeling.append(tuple(["Mantle","1,2,3,4,5","CtL:PTM-55"]))
            changeling.append(tuple(["Many Mask","3","CtL:PTM-55","Powerstat,2","Manipulation,3"]))
            changeling.append(tuple(["Market Sense","1","CtL:PTM-55"]))
            changeling.append(tuple(["Master Shaper","1,3,5","CtL:PTM-56","Empathy,2","Crafts,2"]))
            changeling.append(tuple(["Oneiromantic Finesse","1","CtL:PTM-56","Powerstat,2","Intelligence,3","Weaponry Specialty/Brawl Specialty"]))
            changeling.append(tuple(["Parallel Lives","3,5","CtL:PTM-56"]))
            changeling.append(tuple(["Potent Kith","1,2,3,4,5","CtL:PTM-57"]))
            changeling.append(tuple(["Prophet","1","CtL:PTM-57"]))
            changeling.append(tuple(["Rigid Mask","2","CtL:PTM-57","Subterfuge,2"]))
            changeling.append(tuple(["Stable Trod","1,2,3,4,5","CtL:PTM-57"]))
        if len(faetouched) == 0:
            faetouched.append(tuple(["Dream Shaper","3","Lucid Dreamer","CtL:PT-249"]))
            faetouched.append(tuple(["Dream Walker","4","Lucid Dreamer","CtL:PT-249"]))
            faetouched.append(tuple(["Extremely Expressive","1","CtL:PT-249"]))
            faetouched.append(tuple(["Fae Mien","2","CtL:PT-250"]))
            faetouched.append(tuple(["Find the Oath Braker","2","Sense Vows","CtL:PT-250"]))
            faetouched.append(tuple(["Hedge Delver","2","Survival,2","CtL:PT-250"]))
            faetouched.append(tuple(["Oath Bound","1","CtL:PT-250"]))
            faetouched.append(tuple(["Oath Keeper","3","CtL:PT-250"]))
            faetouched.append(tuple(["Promise of Debt","2","CtL:PT-251"]))
            faetouched.append(tuple(["Promise of Love","2","CtL:PT-251"]))
            faetouched.append(tuple(["Promise of Loyalty","2","CtL:PT-251"]))
            faetouched.append(tuple(["Promise of Protection","3","CtL:PT-251"]))
            faetouched.append(tuple(["Promised to Provide","2","CtL:PT-251"]))
            faetouched.append(tuple(["Promised to Service","2","CtL:PT-252"]))
            faetouched.append(tuple(["Punish the Oath Breaker","3","CtL:PT-252"]))
            faetouched.append(tuple(["Sense Vows","1","CtL:PT-252"]))
        if len(beast) == 0:
            beast.append(tuple(["Danger Sense Advanced","2","BtP-113","Danger Sense"]))
            beast.append(tuple(["Direction Sense Advanced","2","BtP-114","Direction Sense"]))
            beast.append(tuple(["Direction Sense Epic","2","BtP-114","Direction Sense Advanced"]))
            beast.append(tuple(["Double-Jointed Advanced","1","BtP-114","Double Jointed"]))
            beast.append(tuple(["Eidetic Memory Advanced","1","BtP-114","Eidetic Memory"]))
            beast.append(tuple(["Epic Potential","1","BtP-114"]))
            beast.append(tuple(["Fame Advanced","1,2,3","BtP-115","Fame,="]))
            beast.append(tuple(["Fast Reflexes Advanced","1","BtP-115","Fast Reflexes,3"]))
            beast.append(tuple(["Fist of Nightmares","2","BtP-115","Brawl,2","Occult,2"]))
            beast.append(tuple(["Giant Advanced","2","BtP-116","Giant"]))
            beast.append(tuple(["Guilty Pleasure","1","BtP-116"]))
            beast.append(tuple(["Hunter Management","1,2,3","BtP-116","Resolve,3"]))
            beast.append(tuple(["Iron Skin","1,2","BtP-117","Brawl,2","Stamina,2"]))
            beast.append(tuple(["Iron Skin Advanced","1,2","BtP-117","Stamina,4"]))
            beast.append(tuple(["Iron Skin Epic","2","BtP-117","Stamina,5"]))
            beast.append(tuple(["Killer Instinct Advanced", "1,2,3","BtP-117","Killer Instinct,3"]))
            beast.append(tuple(["Spoor","1,2,3,4,5","BtP-120"]))
            beast.append(tuple(["Striking Looks Advanced", "1,2","BtP-121","Striking Looks,2"]))
        if len(promethean) == 0:
            promethean.append(tuple(["Acid Stomach","1","PtC-111"]))
            promethean.append(tuple(["Azothic Object","1,2,3,4,5","PtC-112"]))
            promethean.append(tuple(["Benign Festering","1,2,3","PtC-112"]))
            promethean.append(tuple(["Companion","1,2,3,4,5","PtC-113"]))
            promethean.append(tuple(["Driven","1,2,3,4,5","PtC-113"]))
            promethean.append(tuple(["Efficient Conductor","1","PtC-113"]))
            promethean.append(tuple(["Famous Face","1,2,3","PtC-114"]))
            promethean.append(tuple(["Good Brain","1,2,3,4,5","PtC-114"]))
            promethean.append(tuple(["Hovel","1,2,3,4,5","PtC-115","Safe Place"]))
            promethean.append(tuple(["Moth to the Flame","1","PtC-115"]))
            promethean.append(tuple(["Repute","1,2,3","PtC-116"]))
            promethean.append(tuple(["Residual Memory","1,2,3,4,5","PtC-116"]))
            promethean.append(tuple(["Sleepless","1","PtC-116"]))
            promethean.append(tuple(["Terrible Disfigurement","1","PtC-117"]))
            promethean.append(tuple(["Vivid Dreams","1,2,3,4,5","PtC-117"]))
            promethean.append(tuple(["Weatherproof","1","PtC-117"]))
        if len(hunter) == 0:
            hunter.append(tuple(["Endowments","1,2,3,4,5","HtV-67"]))
            hunter.append(tuple(["Favored Weapon","2","HtV-67"]))
            hunter.append(tuple(["Kindred Dueling","1,2,3,4,5","VtR-117","Composure,3","Weaponry,2"]))
        if len(mummy) == 0:
            mummy.append(tuple(["Cult","1,2,3,4,5"]))
            mummy.append(tuple(["Enigma","1,2,3,4,5","MtC-79"]))
            mummy.append(tuple(["Relic","1,2,3,4,5","MtC-81"]))
            mummy.append(tuple(["Tomb Geometry","1,2,3,4,5","MtC-81"]))
            mummy.append(tuple(["Tomb Peril","1,2,3,4,5","MtC-82"]))
            mummy.append(tuple(["Tomb Endowments","1,2,3,4,5","MtC-83"]))
            mummy.append(tuple(["Vestige","1,2,3,4,5","MtC-83"]))
            mummy.append(tuple(["Witness Mentor","1,2,3,4,5","MtC-84"]))
            mummy.append(tuple(["Witness Retainer","1,2,3,4,5,6","MtC-84"]))
        if len(demon) == 0:
            demon.append(tuple(["Bolthole","1,2,3,4,5","DtD-121"]))
            demon.append(tuple(["Consummate Professional","2","DtD-121"]))
            demon.append(tuple(["Cultists","2,3,4,5","DtD-121"]))
            demon.append(tuple(["Suborned Infrastructure","1,2,3","DtD-121"]))
            demon.append(tuple(["Terrible Form","1,2,3,4","DtD-122"]))
            demon.append(tuple(["Versatile Transformation","1","DtD-122"]))
    def Reset(self):
        self.at_script_creation()