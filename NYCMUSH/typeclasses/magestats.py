'''
Created on Jan 13, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class MageStatHandler(DefaultScript):
    arcana = ["Fate","Forces","Matter","Prime","Spirit","Death","Life","Mind","Space","Time"]
    pathlist = ["Obrimos","Thrysus","Mastigos","Moros","Acanthus"]
    orderlist = ["Free Council","Mysterium","Adamantine Arrow","Silver Ladder","Guardians of the Veil"]
    arcana.sort()
    arcana_ratings = [1,2,3,4,5]
    def GetSkills(self, rotein):
        rotes = self.db.rotes
        for rote in rotes:
            if rote[1].lower() == rotein.lower():
                return rote[3].spli(",")
            else:
                return False
    def at_script_creation(self):
        self.db.arcana = []
        self.db.rotes = []
        self.db.arcana_ratings = self.arcana_ratings
        self.db.paths = self.pathlist
        self.db.orders = self.orderlist
        arcana = self.db.arcana
        rotes = self.db.rotes
        if len(arcana) == 0:
            arcana.append("Death")
            arcana.append("Fate")
            arcana.append("Forces")
            arcana.append("Life")
            arcana.append("Matter")
            arcana.append("Mind")
            arcana.append("Prime")
            arcana.append("Space")
            arcana.append("Spirit")
            arcana.append("Time")
        if len(rotes) == 0:
            rotes.append(tuple(["Death","Ectoplasmic Shaping","1","Crafts,Occult,Larceny","MtA-128"]))
            rotes.append(tuple(["Death","Deepen Shadows","1","Occult,Intimidation,Expression","MtA-128"]))
            rotes.append(tuple(["Death","Forensic Gaze","1","Medicine,Investigation,Expression","MtA-128"]))
            rotes.append(tuple(["Death","Shadow Sculpting","1","Crafts,Science,Expression","MtA-128"]))
            rotes.append(tuple(["Death","Soul Marks","1","Medicine,Occult,Empathy","MtA-128"]))
            rotes.append(tuple(["Death","Speak With Dead","1","Socialize,Expression,Investigation","MtA-128"]))
            rotes.append(tuple(["Death","Corpse Mask","2","Subterfuge,Crafts,Medicine","MtA-129"]))
            rotes.append(tuple(["Death","Decay","2","Subterfuge,Science,Occult","MtA-129"]))
            rotes.append(tuple(["Death","Ectoplasm","1","Occult,Expression,Academics","MtA-129"]))
            rotes.append(tuple(["Death","Ghost Shield","2","Streetwise,Subterfuge,Survival","MtA-129"]))
            rotes.append(tuple(["Death","Shape Ephemera","2","Crafts,Expression,Science","MtA-129"]))
            rotes.append(tuple(["Death","Soul Armor","2","Academics,Occult,Survival","MtA-129"]))
            rotes.append(tuple(["Death","Soul Jar","2","Crafts,Occult,Persuasion","MtA-129"]))
            rotes.append(tuple(["Death","Suppress Aura","2","Subterfuge,Intimidation,Medicine","MtA-130"]))
            rotes.append(tuple(["Death","Suppress Life","2","Subterfuge,Medicine,Academics","MtA-130"]))
            rotes.append(tuple(["Death","Touch of the Grave","2","Survival,Crafts,Persuasion","MtA-130"]))
            rotes.append(tuple(["Death","Without a Trace","2","Science,Stealth,Subterfuge","MtA-130"]))
            rotes.append(tuple(["Death","Cold Snap","3","Survival,Intimidation,Science","MtA-130"]))
            rotes.append(tuple(["Death","Damage Ghost","3","Occult,Intimidation,Brawl","MtA-130"]))
            rotes.append(tuple(["Death","Devouring the Slain","3","Intimidation,Medicine,Persuasion","MtA-130"]))
            rotes.append(tuple(["Death","Ghost Gate","3","Occult,Academics,Expression","MtA-130"]))
            rotes.append(tuple(["Death","Ghost Summons","3","Persuasion,Socialize,Occult","MtA-131"]))
            rotes.append(tuple(["Death","Quicken Corpse","3","Medicine,Crafts,Persuasion","MtA-131"]))
            rotes.append(tuple(["Death","Quicken Ghost","3","Persuasion,Socialize,Medicine","MtA-131"]))
            rotes.append(tuple(["Death","Rotting Flesh","3","Intimidation,Occult,Empathy","MtA-132"]))
            rotes.append(tuple(["Death","Sever Soul","3","Intimidation,Athletics,Expression","MtA-132"]))
            rotes.append(tuple(["Death","Shadow Crafting","3","Academics,Intimidation,Occult","MtA-132"]))
            rotes.append(tuple(["Death","Enervation","4","Occult,Intimidation,Subterfuge","MtA-132"]))
            rotes.append(tuple(["Death","Exorcism","4","Brawl,Intimidation,Occult","Mta-132"]))
            rotes.append(tuple(["Death","Revenant","4","Crafts,Brawl,Intimidation","MtA-132"]))
            rotes.append(tuple(["Death","Shadow Flesh","4","Occult,Medicine,Subterfuge","MtA-132"]))
            rotes.append(tuple(["Death","Withering","4","Intimidation,Medicine,Science","MtA-133"]))
            rotes.append(tuple(["Death","Create Anchor","5","Crafts,Occult,Persuasion","MtA-133"]))
            rotes.append(tuple(["Death","Create Ghost","5","Occult,Expression,Academics","MtA-133"]))
            rotes.append(tuple(["Death","Deny the Reaper","5","Medicine,Occult,Subterfuge","MtA-133"]))
            rotes.append(tuple(["Death","Empty Presence","5","Subterfuge,Persuasion,Stealth","MtA-133"]))
            rotes.append(tuple(["Death","Open Avernian Gate","5","Occult,Crafts,Persuasion","MtA-133"]))
            rotes.append(tuple(["Death","Sever the Awakened Soul","5","Crafts,Intimidation,Medicine","MtA-133"]))
            #End of death rotes
            rotes.append(tuple(["Fate","Interconnections","1","Empathy,Investigation,Medicine","MtA-134"]))
            rotes.append(tuple(["Fate","Oaths Fulfilled","1","Occult,Politics,Investigation","MtA-135"]))
            rotes.append(tuple(["Fate","Quantum Flux","1","Crafts,Firearms,Occult","MtA-135"]))
            rotes.append(tuple(["Fate","Reading the Outmost Eddies","1","Computer,Persuasion,Subterfuge","MtA-135"]))
            rotes.append(tuple(["Fate","Serendipity","1","Academics,Crafts,Survival","MtA-135"]))
            rotes.append(tuple(["Fate","Exceptional Luck","2","Intimidation,Occult,Socialize","MtA-135"]))
            rotes.append(tuple(["Fate","Fabricate Fortune","2","Larceny,Occult,Subterfuge","MtA-136"]))
            rotes.append(tuple(["Fate","Fools Rush In","2","Athletics,Socialize,Streetwise","MtA-136"]))
            rotes.append(tuple(["Fate","Lucky Number","2","Investigation,Larceny,Science","MtA-136"]))
            rotes.append(tuple(["Fate","Shifting the Odds","2","Investigation,Politics,Subterfuge","MtA-136"]))
            rotes.append(tuple(["Fate","Warding Gesture","2","Brawl,Occult,Subterfuge","MtA-136"]))
            rotes.append(tuple(["Fate","Grave Misfortune","3","Intimidation,Occult,Weaponry","MtA-137"]))
            rotes.append(tuple(["Fate","Monkey's Paw","3","Drive,Crafts,Science","MtA-137"]))
            rotes.append(tuple(["Fate","Shared Fate","3","Medicine,Persuasion,Politics","MtA-137"]))
            rotes.append(tuple(["Fate","Superlative Luck","3","Athletics,Crafts,Occult","MtA-137"]))
            rotes.append(tuple(["Fate","Sworn Oaths","3","Expression,Occult,Politics","MtA-137"]))
            rotes.append(tuple(["Fate","Atonement","4","Academics,Empathy,Survival","MtA-137"]))
            rotes.append(tuple(["Fate","Chaos Mastery","4","Empathy,Occult,Science","MtA-138"]))
            rotes.append(tuple(["Fate","Divine Intervention","4","Intimidation,Occult,Subterfuge","MtA-138"]))
            rotes.append(tuple(["Fate","Strings of Fate","4","Academics,Persuasion,Stealth","MtA-138"]))
            rotes.append(tuple(["Fate","Sever Oaths","4","Occult,Subterfuge,Weaponry","MtA-138"]))
            rotes.append(tuple(["Fate","Forge Destiny","5","Intimidation,Occult,Persuasion","MtA-139"]))
            rotes.append(tuple(["Fate","Pariah","5","Investigation,Medicine,Politics","MtA-139"]))
            rotes.append(tuple(["Fate","Miracle","5","Academics,Persuasion,Subterfuge","MtA-40"]))
            rotes.append(tuple(["Fate","Swarm of Locusts","5","Intimidation,Occult,Science","MtA-140"]))
            #End of fate rotes
            rotes.append(tuple(["Forces","Influence Electricity","1","Computer,Crafts,Science","MtA-140"]))
            rotes.append(tuple(["Forces","Influence Fire","1","Crafts,Science,Survival","MtA-140"]))
            rotes.append(tuple(["Forces","Kinetic Efficiency","1","Athletics,Science,Survival","MtA-141"]))
            rotes.append(tuple(["Forces","Influence Heat","1","Occult,Science,Survival","MtA-141"]))
            rotes.append(tuple(["Forces","Nightvision","1","Investigation,Science,Stealth","MtA-141"]))
            rotes.append(tuple(["Forces","Receiver","1","Empathy,Investigation,Science","MtA-141"]))
            rotes.append(tuple(["Forces","Tune In","1","Empathy,Computer,Science","MtA-141"]))
            rotes.append(tuple(["Forces","Control Electricity","2","Crafts,Computer,Science","MtA-142"]))
            rotes.append(tuple(["Forces","ControL Fire","2","Crafts,Science,Survival","MtA-142"]))
            rotes.append(tuple(["Forces","Control Gravity","2","Athletics,Occult,Science","MtA-142"]))
            rotes.append(tuple(["Forces","Control Heat","2","Athletics,Science,Survival","MtA-142"]))
            rotes.append(tuple(["Forces","Control Light","2","Crafts,Investigation,Science","MtA-142"]))
            rotes.append(tuple(["Forces","Control Sound","2","Expression,Stealth,Science","MtA-142"]))
            rotes.append(tuple(["Forces","Control Weather","2","Academics,Science,Survival","MtA-143"]))
            rotes.append(tuple(["Forces","Environmental Shield","2","Occult,Science,Survival","MtA-143"]))
            rotes.append(tuple(["Forces","Invisibility","2","Larceny,Science,Stealth","MtA-143"]))
            rotes.append(tuple(["Forces","Kinetic Blow","2","Athletics,Brawl,Science","MtA-143"]))
            rotes.append(tuple(["Forces","Transmission","2","Crafts,Expression,Science","MtA-144"]))
            rotes.append(tuple(["Forces","Zoom In","2","Investigation,Science,Survival","MtA-144"]))
            rotes.append(tuple(["Forces","Call Lightning","3","Athletics,Firearms,Science","MtA-144"]))
            rotes.append(tuple(["Forces","Gravitiy Supremacy","3","Athletics,Science,Survival","MtA-144"]))
            rotes.append(tuple(["Forces","Telekinesis","3","Athletics,Brawl,Science","MtA-144"]))
            rotes.append(tuple(["Forces","Telekinetic Strike","3","Athletics,Firearms,Science","MtA-145"]))
            rotes.append(tuple(["Forces","Turn Momentum","3","Athletics,Firearms,Science","MtA-145"]))
            rotes.append(tuple(["Forces","Velocity Control","3","Athletics,Drive,Science","MtA-145"]))
            rotes.append(tuple(["Forces","Electromagnetic Pulse","4","Crafts,Computer,Science","MtA-145"]))
            rotes.append(tuple(["Forces","Levitation","4","Athletics,Science,Survival","MtA-145"]))
            rotes.append(tuple(["Forces","Rend Friction","4","Crafts,Drive,Science","MtA-145"]))
            rotes.append(tuple(["Forces","Thunderbolt","4","Athletics,Firearms,Science","MtA-146"]))
            rotes.append(tuple(["Forces","Transform Energy","4","Crafts,Occult,Science","MtA-146"]))
            rotes.append(tuple(["Forces","Adverse Weather","5","Crafts,Occult,Science","MtA-146"]))
            rotes.append(tuple(["Forces","Create Energy","5","Crafts,Occult,Science","MtA-146"]))
            rotes.append(tuple(["Forces","Eradicate Energy","5","Intimidation,Science,Survival","MtA-146"]))
            rotes.append(tuple(["Forces","Earthquake","5","Crafts,Science,Survival","MtA-147"]))
            #End of forces rotes
            rotes.append(tuple(["Life","Analyze Life","1","AnimalKen,Medicine,Survival","MtA-148"]))
            rotes.append(tuple(["Life","Cleanse the Body","1","Athletics,Medicine,Survival","MtA-148"]))
            rotes.append(tuple(["Life","Speak With Beasts","1","AnimalKen,Empathy,Survival","MtA-148"]))
            rotes.append(tuple(["Life","Web of Life","1","Investigation,Medicine,Survival","MtA-148"]))
            rotes.append(tuple(["Life","Body Control","2","Athletics,Medicine,Survival","MtA-148"]))
            rotes.append(tuple(["Life","Control Instincts","2","AnimalKen,Intimidation,Persuasion","MtA-149"]))
            rotes.append(tuple(["Life","Heightened Senses","2","Empathy,Investigation,Survival","MtA-149"]))
            rotes.append(tuple(["Life","Lure and Repel","2","AnimalKen,Persuasion,Survival","MtA-149"]))
            rotes.append(tuple(["Life","Mutable Mask","2","Medicine,Stealth,Subterfuge","MtA-149"]))
            rotes.append(tuple(["Life","Purge Illness","2","Athletics,Medicine,Survival","MtA-149"]))
            rotes.append(tuple(["Life","Bruise Flesh","3","Brawl,Intimidation,Medicine","MtA-150"]))
            rotes.append(tuple(["Life","Degrading the Form","3","Brawl,Medicine,Survival","MtA-150"]))
            rotes.append(tuple(["Life","Honing the Form","3","Athletics,Medicine,Survival","mtA-150"]))
            rotes.append(tuple(["Life","Knit","3","Empathy,Medicine,Survival","MtA-150"]))
            rotes.append(tuple(["Life","Many Faces","3","Medicine,Stealth,Subterfuge","MtA-150"]))
            rotes.append(tuple(["Life","Transform Life","3","AnimalKen,Science,Survival","MtA-150"]))
            rotes.append(tuple(["Life","Accelerate Growth","4","AnimalKen,Medicine,Science","MtA-151"]))
            rotes.append(tuple(["Life","Animal Minion","4","AnimalKen,Science,Survival","MtA-151"]))
            rotes.append(tuple(["Life","Life-Force Assault","4","Brawl,Intimidation,Medicine","MtA-152"]))
            rotes.append(tuple(["Life","Mend","4","Empathy,Medicine,Survival","MtA-152"]))
            rotes.append(tuple(["Life","Regeneration","4","Athletics,Medicine,Survival","MtA-152"]))
            rotes.append(tuple(["Life","Shapechanging","4","AnimalKen,Athletics,Science","MtA-152"]))
            rotes.append(tuple(["Life","Create Life","5","Medicine,Science,Survival","MtA-153"]))
            rotes.append(tuple(["Life","Contagion","5","Medicine,Occult,Science","MtA-154"]))
            rotes.append(tuple(["Life","Salt the Earth","5","Medicine,Science,Survival","MtA-154"]))
            #end of life rotes
            rotes.append(tuple(["Matter","Craftsman's Eye","1","Crafts,Investigation,Science","MtA-154"]))
            rotes.append(tuple(["Matter","Detect Substance","1","Crafts,Investigation,Science","MtA-154"]))
            rotes.append(tuple(["Matter","Discern Composition","1","Crafts,Investigation,Science","MtA-154"]))
            rotes.append(tuple(["Matter","Lodestone","1","Crafts,Larceny,Science","MtA-154"]))
            rotes.append(tuple(["Matter","Remote Control","1","Crafts,Drive,Intimidate","MtA-155"]))
            rotes.append(tuple(["Matter","Alchemist's Touch","2","Crafts,Survival,Persuasion","MtA-155"]))
            rotes.append(tuple(["Matter","Find the Balance","2","Crafts,Persuasion,Science","MtA-155"]))
            rotes.append(tuple(["Matter","Hidden Hoard","2","Larceny,Occult,Subterfuge","MtA-156"]))
            rotes.append(tuple(["Matter","Machine Invisibility","2","Larceny,Science,Stealth","MtA-156"]))
            rotes.append(tuple(["Matter","Shaping","2","Crafts,Expression,Persuasion","MtA-156"]))
            rotes.append(tuple(["Matter","Aegis","3","Athletics,Crafts,Science","MtA-156"]))
            rotes.append(tuple(["Matter","Alter Conductivity","3","Computer,Science,Subterfuge","MtA-156"]))
            rotes.append(tuple(["Matter","Alter Integrity","3","Crafts,Medicine,Subterfuge","MtA-156"]))
            rotes.append(tuple(["Matter","Crucible","3","Crafts,Occult,Science","MtA-157"]))
            rotes.append(tuple(["Matter","Nigredo and Albedo","3","Crafts,Brawl,Medicine","MtA-157"]))
            rotes.append(tuple(["Matter","Shrink and Grow","3","Crafts,Expression,Science","MtA-157"]))
            rotes.append(tuple(["Matter","State Change","3","Crafts,Persuasion,Science","MtA-157"]))
            rotes.append(tuple(["Matter","Windstrike","3","Athletics,Brawl,Crafts","MtA-157"]))
            rotes.append(tuple(["Matter","Wonderful Machine","3","Crafts,Politics,Science","MtA-157"]))
            rotes.append(tuple(["Matter","Ghostwall","4","Athletics,Occult,Stealth","MtA-158"]))
            rotes.append(tuple(["Matter","Golem","4","Crafts,Expression,Occult","MtA-158"]))
            rotes.append(tuple(["Matter","Piercing Earth","4","Athletics,Brawl,Crafts","MtA-158"]))
            rotes.append(tuple(["Matter","Transubstantiation","4","Crafts,Empathy,Science","MtA-158"]))
            rotes.append(tuple(["Matter","Annihilate Matter","5","Athletics,Intimidation,Science","MtA-158"]))
            rotes.append(tuple(["Matter","Ex Nihilo","5","Crafts,Expression,Science","MtA-158"]))
            rotes.append(tuple(["Matter","Self-Repairing Machine","5","Crafts,Expression,Science","MtA-159"]))
            #End of matter rotes
            rotes.append(tuple(["Mind","Know Nature","1","Empathy,Science,Subterfuge","MtA-159"]))
            rotes.append(tuple(["Mind","Mental Scan","1","Empathy,Investigation,Occult","MtA-159"]))
            rotes.append(tuple(["Mind","One Mind, Two Thoughts","1","Academics,Expression,Science","MtA-159"]))
            rotes.append(tuple(["Mind","Perfect Recall","1","Academics,Expression,Science","MtA-160"]))
            rotes.append(tuple(["Mind","Alter Mental Pattern","2","Science,Stealth,Subterfuge","MtA-160"]))
            rotes.append(tuple(["Mind","Dream Reaching","2","Empathy,Medicine,Persuasion","MtA-160"]))
            rotes.append(tuple(["Mind","Emotional Urging","2","Empathy,Intimidation,Subterfuge","MtA-160"]))
            rotes.append(tuple(["Mind","First Impressions","2","Crafts,Socialize,Subterfuge","MtA-160"]))
            rotes.append(tuple(["Mind","Incognito Presence","2","Empathy,Stealth,Subterfuge","MtA-160"]))
            rotes.append(tuple(["Mind","Memory Hole","2","Academics,Medicine,Subterfuge","MtA-160"]))
            rotes.append(tuple(["Mind","Mental Shield","2","Academics,Intimidation,Survival","MtA-160"]))
            rotes.append(tuple(["Mind","Psychic Domination","2","Expression,Intimidation,Subterfuge","MtA-161"]))
            rotes.append(tuple(["Mind","Telepathy","2","Crafts,Empathy,Socialize","MtA-161"]))
            rotes.append(tuple(["Mind","Augment Mind","3","Academics,Expression,Survival","MtA-161"]))
            rotes.append(tuple(["Mind","Clear Thoughts","3","Empathy,Intimidation,Persuasion","MtA-161"]))
            rotes.append(tuple(["Mind","Enhance Skill","3","Academics,Expression,Survival","MtA-161"]))
            rotes.append(tuple(["Mind","Goetic Summons","3","Persuasion,Socialize,Occult","MtA-162"]))
            rotes.append(tuple(["Mind","Imposter","3","Persuasion,Stealth,Subterfuge","MtA-162"]))
            rotes.append(tuple(["Mind","Psychic Assault","3","Academics,Intimidation,Medicine","MtA-162"]))
            rotes.append(tuple(["Mind","Sleep of the Just","3","Academics,Athletics,Occult","MtA-162"]))
            rotes.append(tuple(["Mind","Read the Depths","3","Empathy,Investigation,Medicine","MtA-162"]))
            rotes.append(tuple(["Mind","Universal Language","3","Academics,Investigation,Persuasion","MtA-162"]))
            rotes.append(tuple(["Mind","Befuddle","4","Intimidation,Persuasion,Science","MtA-163"]))
            rotes.append(tuple(["Mind","Gain Skill","4","Crafts,Expression,Science","MtA-163"]))
            rotes.append(tuple(["Mind","Hallucination","4","Academics,Persuasion,Subterfuge","MtA-163"]))
            rotes.append(tuple(["Mind","Mind Flay","4","Expression,Intimidation,Science","MtA-164"]))
            rotes.append(tuple(["Mind","Psychic Projection","4","Academics,Occult,Socialize","MtA-164"]))
            rotes.append(tuple(["Mind","Psychic Reprogramming","4","Intimidation,Medicine,Persuasion","MtA-164"]))
            rotes.append(tuple(["Mind","Terrorize","4","Expression,Intimidation,Medicine","MtA-164"]))
            rotes.append(tuple(["Mind","Amorality","5","Crafts,Empathy,Expression","MtA-164"]))
            rotes.append(tuple(["Mind","No Exit","5","Expression,Persuasion,Science","MtA-164"]))
            rotes.append(tuple(["Mind","Mind Wipe","5","Academics,Intimidation,Occult","MtA-164"]))
            rotes.append(tuple(["Mind","Possession","5","Medicine,Persuasion,Subterfuge","MtA-165"]))
            rotes.append(tuple(["Mind","Psychic Genesis","5","Academics,Persuasion,Science","MtA-165"]))
            rotes.append(tuple(["Mind","Social Networking","5","Persuasion,Politics,Socialize","MtA-165"]))
            #End of mind rotes
            rotes.append(tuple(["Prime","Dispel Magic","1","Athletics,Intimidation,Occult","MtA-165"]))
            rotes.append(tuple(["Prime","Pierce Deception","1","Investigation,Medicine,Occult","MtA-165"]))
            rotes.append(tuple(["Prime","Supernal Vision","1","Empathy,Occult,Survival","MtA-166"]))
            rotes.append(tuple(["Prime","Sacred Geometry","1","Academics,Occult,Survival","MtA-166"]))
            rotes.append(tuple(["Prime","Scribe Grimoire","1","Crafts,Expression,Occult","MtA-166"]))
            rotes.append(tuple(["Prime","Word of Command","1","Crafts,Occult,Persuasion","MtA-166"]))
            rotes.append(tuple(["Prime","As Above, So Below","2","Academics,Occult,Politics","MtA-166"]))
            rotes.append(tuple(["Prime","Cloak Nimbus","2","Politics,Stealth,Subterfuge","MtA-167"]))
            rotes.append(tuple(["Prime","Invisible Runes","2","Expression,Intimidation,Persuasion","MtA-167"]))
            rotes.append(tuple(["Prime","Supernal Veil","2","Occult,Subterfuge,Survival","MtA-168"]))
            rotes.append(tuple(["Prime","Wards and Signs","2","Intimidation,Occult,Survival","MtA-168"]))
            rotes.append(tuple(["Prime","Words of Truth","2","Expression,Intimidation,Persuasion","MtA-168"]))
            rotes.append(tuple(["Prime","Aetheric Winds","3","Athletics,Expression,Occult","MtA-168"]))
            rotes.append(tuple(["Prime","Channel Mana","3","Occult,Politics,Socialize","MtA-168"]))
            rotes.append(tuple(["Prime","Cleanse Pattern","3","Investigation,Occult,Stealth","MtA-168"]))
            rotes.append(tuple(["Prime","Display of Power","3","Brawl,Occult,Socialize","MtA-168"]))
            rotes.append(tuple(["Prime","Ephemeral Enchantment","3","Crafts,Occult,Weaponry","MtA-169"]))
            rotes.append(tuple(["Prime","Geomancy","3","Academics,Expression,Occult","MtA-169"]))
            rotes.append(tuple(["Prime","Platonic Form","3","Academics,Crafts,Expression","MtA-169"]))
            rotes.append(tuple(["Prime","Stealing Fire","3","Expression,Larceny,Persuasion","MtA-169"]))
            rotes.append(tuple(["Prime","Apocalypse","4","Occult,Persuasion,Socialize","MtA-169"]))
            rotes.append(tuple(["Prime","Celestial Fire","4","Athletics,Expression,Occult","MtA-170"]))
            rotes.append(tuple(["Prime","Destroy Tass","4","Brawl,Intimidation,Occult","MtA-170"]))
            rotes.append(tuple(["Prime","Hallow Dance","4","Expression,Occult,Survival","MtA-170"]))
            rotes.append(tuple(["Prime","Supernal Dispellation","4","Athletics,Intimidation,Occult","MtA-170"]))
            rotes.append(tuple(["Prime","Blasphemy","5","Athletics,Occult,Survival","MtA-170"]))
            rotes.append(tuple(["Prime","Create Truth","5","Expression,Occult,Persuasion","MtA-170"]))
            rotes.append(tuple(["Prime","Eidolon","5","Academics,Crafts,Occult","MtA-171"]))
            rotes.append(tuple(["Prime","Forge Purpose","5","Empathy,Expression,Medicine","MtA-171"]))
            rotes.append(tuple(["Prime","Word of Unmaking","5","Intimidation,Occult,Weaponry","MtA-171"]))
            #End of prime rotes
            rotes.append(tuple(["Space","Correspondence","1","Academics,Empathy,Medicine","MtA-172"]))
            rotes.append(tuple(["Space","Ground-Eater","1","Athletics,Science,Survival","MtA-173"]))
            rotes.append(tuple(["Space","Isolation","1","Academics,Intimidation,Subterfuge","MtA-173"]))
            rotes.append(tuple(["Space","Locate Object","1","Empathy,Occult,Science","MtA-173"]))
            rotes.append(tuple(["Space","The Outward and Inward Eye","1","Firearms,Investigation,Occult","MtA-174"]))
            rotes.append(tuple(["Space","Borrow Threads","2","Larceny,Occult,Subterfuge","MtA-174"]))
            rotes.append(tuple(["Space","Break Boundary","2","Athletics,Larceny,Persuasion","MtA-174"]))
            rotes.append(tuple(["Space","Lying Maps","2","Academics,Politics,Survival","MtA-174"]))
            rotes.append(tuple(["Space","Scrying","2","Computer,Occult,Subterfuge","MtA-174"]))
            rotes.append(tuple(["Space","Secret Door","2","Occult,Stealth,Subterfuge","MtA-175"]))
            rotes.append(tuple(["Space","Veil Sympathy","2","Politics,Subterfuge,Survival","MtA-175"]))
            rotes.append(tuple(["Space","Ward","2","Athletics,Subterfuge,Weaponry","MtA-176"]))
            rotes.append(tuple(["Space","Ban","3","Intimidation,Science,Stealth","MtA-176"]))
            rotes.append(tuple(["Space","Perfect Sympathy","3","Academics,Empathy,Larceny","MtA-176"]))
            rotes.append(tuple(["Space","Warp","3","Athletics,Brawl,Medicine","MtA-177"]))
            rotes.append(tuple(["Space","Web-Weaver","3","Crafts,Empathy,Persuasion","MtA-177"]))
            rotes.append(tuple(["Space","Alter Direction","4","Academics,Firearms,Persuasion","MtA-177"]))
            rotes.append(tuple(["Space","Collapse","4","Academics,Firearms,Intimidation","MtA-177"]))
            rotes.append(tuple(["Space","Cut Threads","4","Persuasion,Politics,Weaponry","MtA-177"]))
            rotes.append(tuple(["Space","Secret Room","4","Expression,Science,Survival","MtA-178"]))
            rotes.append(tuple(["Space","Teleportation","4","Larceny,Persuasion,Science","MtA-178"]))
            rotes.append(tuple(["Space","Create Sympathy","5","Empathy,Persuasion,Politics","MtA-178"]))
            rotes.append(tuple(["Space","Forge No Chains","5","Occult,Subterfuge,Survival","MtA-178"]))
            rotes.append(tuple(["Space","Pocket Dimension","5","Crafts,Expression,Survival","MtA-178"]))
            rotes.append(tuple(["Space","Quarantine","5","Academics,Larceny,Socialize","MtA-179"]))
            #End of space rotes
            rotes.append(tuple(["Spirit","Coaxing the Spirits","1","Politics,Athletics,Expression","MtA-180"]))
            rotes.append(tuple(["Spirit","Exorcist's Eye","1","Occult,Survival,Socialize","MtA-180"]))
            rotes.append(tuple(["Spirit","Gremlins","1","Larceny,Politics,Subterfuge","MtA-180"]))
            rotes.append(tuple(["Spirit","Invoke Bane","1","Brawl,Intimidation,Occult","MtA-180"]))
            rotes.append(tuple(["Spirit","Know Spirit","1","Academics,Brawl,Socialize","MtA-180"]))
            rotes.append(tuple(["Spirit","Cap the Well","2","Politics,Survival,Persuasion","MtA-180"]))
            rotes.append(tuple(["Spirit","Channel Essence","2","Occult,Persuasion,Survival","MtA-180"]))
            rotes.append(tuple(["Spirit","Command Spirit","2","Athletics,Medicine,Persuasion","MtA-181"]))
            rotes.append(tuple(["Spirit","Ephemeral Shield","2","AnimaLKen,Medicine,Stealth","MtA-181"]))
            rotes.append(tuple(["Spirit","Gossamer Touch","2","Brawl,Crafts,Intimidation","MtA-181"]))
            rotes.append(tuple(["Spirit","Opener of the Way","2","Athletics,Computer,Socialize","MtA-181"]))
            rotes.append(tuple(["Spirit","Shadow Walk","2","Occult,Stealth,Streetwise","MtA-181"]))
            rotes.append(tuple(["Spirit","Slumber","2","Expression,Occult,Weaponry","MtA-181"]))
            rotes.append(tuple(["Spirit","Erode Resonance","3","Crafts,Brawl,Intimidation","MtA-181"]))
            rotes.append(tuple(["Spirit","Howl From Beyond","3","Expression,Firearms,Medicine","MtA-182"]))
            rotes.append(tuple(["Spirit","Place of Power","3","Academics,Expression,Survival","MtA-182"]))
            rotes.append(tuple(["Spirit","Reaching","3","Athletics,Medicine,Socialize","MtA-182"]))
            rotes.append(tuple(["Spirit","Rouse Spirit","3","Athletics,Expression,Investigation","MtA-182"]))
            rotes.append(tuple(["Spirit","Spirit Summons","3","Persuasion,Socialize,Occult","MtA-182"]))
            rotes.append(tuple(["Spirit","Banishment","4","Brawl,Expression,Occult","MtA-182"]))
            rotes.append(tuple(["Spirit","Bind Spirit","4","Crafts,Brawl,Intimidation","MtA-183"]))
            rotes.append(tuple(["Spirit","Craft Fetish","4","Crafts,Occult,Persuasion","MtA-183"]))
            rotes.append(tuple(["Spirit","Familiar","4","Athletics,Expression,Intimidate","MtA-183"]))
            rotes.append(tuple(["Spirit","Shadow Scream","4","Expression,Firearms,Medicine","MtA-183"]))
            rotes.append(tuple(["Spirit","Shape Spirit","4","Crafts,Medicine,Persuasion","MtA-184"]))
            rotes.append(tuple(["Spirit","Twilit Body","4","Occult,Subterfuge,Survival","MtA-184"]))
            rotes.append(tuple(["Spirit","World Walker","4","Athletics,Persuasion,Survival","MtA-184"]))
            rotes.append(tuple(["Spirit","Annihilate Spirit","5","Intimidation,Science,Weaponry","MtA-184"]))
            rotes.append(tuple(["Spirit","Birth Spirit","5","Crafts,Medicine,Expression","MtA-184"]))
            rotes.append(tuple(["Spirit","Create Locus","5","Crafts,Empathy,Survival","MtA-184"]))
            rotes.append(tuple(["Spirit","Essence Fountain","5","Empathy,Expression,Occult","MtA-185"]))
            rotes.append(tuple(["Spirit","Spirit Manse","5","Crafts,Expression,Survival","MtA-185"]))
            #End of spirit rotes
            rotes.append(tuple(["Time","Divination","1","Academics,Empathy,Investigation","MtA-186"]))
            rotes.append(tuple(["Time","Green Light/Red Light","1","Computer,Larceny,Subterfuge","MtA-187"]))
            rotes.append(tuple(["Time","Momentary Flux","1","Investigation,Streetwise,Survival","MtA-187"]))
            rotes.append(tuple(["Time","Perfect Timing","1","Empathy,Socialize,Streetwise","MtA-187"]))
            rotes.append(tuple(["Time","Postcognition","1","Academics,Empathy,Investigation","MtA-187"]))
            rotes.append(tuple(["Time","Choose the Thread","2","Occult,Science,Subterfuge","MtA-187"]))
            rotes.append(tuple(["Time","Constant Presence","2","Occult,Persuasion,Survival","MtA-187"]))
            rotes.append(tuple(["Time","Hung Spell","2","Crafts,Occult,Expression","MtA-187"]))
            rotes.append(tuple(["Time","Shield of Chronos","2","Academics,Stealth,Subterfuge","MtA-188"]))
            rotes.append(tuple(["Time","Tipping the Hourglass","2","Athletics,Crafts,Investigation","MtA-188"]))
            rotes.append(tuple(["Time","Veil of Moments","2","Medicine,Investigation,Subterfuge","MtA-188"]))
            rotes.append(tuple(["Time","Acceleration","3","Athletics,Drive,Stealth","MtA-188"]))
            rotes.append(tuple(["Time","Chronos' Curse", "3", "Academics,Occult,Intimidation","MtA-189"]))
            rotes.append(tuple(["Time","Shifting Sands","3","Academics,Occult,Survival","MtA-189"]))
            rotes.append(tuple(["Time","Temporal Summoning","3","Athletics,Investigation,Persuasion","MtA-189"]))
            rotes.append(tuple(["Time","Weight of Years","3","Crafts,Intimidation,Medicine","MtA-190"]))
            rotes.append(tuple(["Time","Present as Past","4","Empathy,Investigation,Streetwise","MtA-190"]))
            rotes.append(tuple(["Time","Prophecy","4","Academics,Expression,Investigation","MtA-190"]))
            rotes.append(tuple(["Time","Rend Lifespan","4","Athletics,Medicine,Intimidation","MtA-190"]))
            rotes.append(tuple(["Time","Rewrite History","4","Expression,Investigation,Persuasion","MtA-190"]))
            rotes.append(tuple(["Time","Temporal Stutter","4","Expression,Intimidation,Survival","MtA-191"]))
            rotes.append(tuple(["Time","Blink of an Eye","5","Academics,Crafts,Occult","MtA-191"]))
            rotes.append(tuple(["Time","Corridors of Time","5","Academics,Investigation,Persuasion","MtA-191"]))
            rotes.append(tuple(["Time","Temporal Pocket","5","Occult,Science,Stealth","MtA-191"]))
            #End of time rotes