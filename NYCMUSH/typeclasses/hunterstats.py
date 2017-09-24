'''
Created on Jan 16, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class HunterHandler(DefaultScript):
    compacts = ["Ashwood Abbey","The Long Night","The Loyalists of Thule","Network Zero","Null Mysteriis","The Union","Habibiti Ma","Utopia Now"]
    conspiracies = ["Aegis Kai Doru","Ascending Ones","Cheiron Group","The Lucifuge","Malleus Maleficarum","Task Force VALKYRIE","Faithful of Shulpae","Knights of St. Adrian"]
    def at_script_creation(self):
        self.db.advarmory = []
        self.db.benediction = []
        self.db.castigation = []
        self.db.elixir = []
        self.db.relic = []
        self.db.thaumatechnology = []
        self.db.ink = []
        self.db.compacts = self.compacts
        self.db.conspiracies = self.conspiracies
        self.db.appfactions = []
        armory = self.db.advarmory
        benediction = self.db.benediction
        castigation = self.db.castigation
        elixir = self.db.elixir
        ink = self.db.ink
        relic = self.db.relic
        magitech = self.db.thaumatechnology
        if len(armory) == 0:
            armory.append(tuple(["Compound Rounds","1,2,3,4,5","MR-56"]))
            armory.append(tuple(["Etheric Rounds","1,2,3,4,5","HtV-150"]))
            armory.append(tuple(["Witch Buster","1","HtV-151"]))
            armory.append(tuple(["The Bleeder","2","HtV-152"]))
            armory.append(tuple(["Etheric Goggles","2,4","HtV-151"]))
            armory.append(tuple(["Gleipnir Restraints","2","MR-32"]))
            armory.append(tuple(["Equalizer Grenade","3","HtV-153"]))
            armory.append(tuple(["Gungnir System","3,5","HtV-154"]))
            armory.append(tuple(["VDSB","3","HtV-154"]))
            armory.append(tuple(["Etheric Tracker","4","HtV-155"]))
            armory.append(tuple(["Munin Serum","4","HtV-155"]))
            armory.append(tuple(["Mjolnir Cannon","4,5","HtV-156"]))
        if len(benediction) == 0:
            benediction.append(tuple(["The Apostle's Teachings","HtV-157"]))
            benediction.append(tuple(["Armor of St. Martin","HtV-158"]))
            benediction.append(tuple(["Epipodian Safeguard","HtV-159"]))
            benediction.append(tuple(["Blessed Protection of Saint Agrippa","HtV-159"]))
            benediction.append(tuple(["The Boon of Lazarus","HtV-160"]))
            benediction.append(tuple(["Fortitude of St. George","HtV-160"]))
            benediction.append(tuple(["The Hands of St. Luke","HtV-160"]))
            benediction.append(tuple(["Sanctification of the Blessed Virgin","HtV-161"]))
            benediction.append(tuple(["The Shepherd's Blessing","HtV-161"]))
            benediction.append(tuple(["True Sight of St. Abel","HtV-162"]))
            benediction.append(tuple(["Vade Retro Satana","HtV-162"]))
            benediction.append(tuple(["Wrathful Sword of St. Michael the Archangel","HtV-163"]))
            benediction.append(tuple(["Peace of St. Joseph","MR-31"]))
            benediction.append(tuple(["Saint Collen's Clarity","MR-56"]))
            tempbless = list(benediction)
            tempbless.sort()
            self.db.benediction = tempbless
        if len(castigation) == 0:
            castigation.append(tuple(["Calling forth the Pit","HtV-164"]))
            castigation.append(tuple(["Familiar","HtV-165"]))
            castigation.append(tuple(["Gaze of the Pentient","HtV-167"]))
            castigation.append(tuple(["Gulf of Hades","MR-30"]))
            castigation.append(tuple(["Hellfire","HtV-168"]))
            castigation.append(tuple(["Infernal Visions","HtV-168"]))
            castigation.append(tuple(["Mandate of Hell","HtV-169"]))
            castigation.append(tuple(["Rebuke Lies","MR-132"]))
            castigation.append(tuple(["Sense of the Unrighteous","HtV-170"]))
            castigation.append(tuple(["Shackles of Pandemonium","HtV-170"]))
            castigation.append(tuple(["Tongue of Babel","HtV-171"]))
            castigation.append(tuple(["Unholy Aura","MR-55"]))
        if len(elixir) == 0:
            elixir.append(tuple(["Crocodile Tears","1","HtV-172"]))
            elixir.append(tuple(["Eye of Ra","1","HtV-173"]))
            elixir.append(tuple(["Hound Mark","1,3","MR-53"]))
            elixir.append(tuple(["Liar Pills","1","MR-130"]))
            elixir.append(tuple(["Breath of Ma'at","2","HtV-173"]))
            elixir.append(tuple(["Elixir of the Fiery Heart","2","HtV-174"]))
            elixir.append(tuple(["Gentle Mind","2","MR-29"]))
            elixir.append(tuple(["Bennu-Bird Feather","3","HtV-174"]))
            elixir.append(tuple(["A Glimpse of After","3","HtV-174"]))
            elixir.append(tuple(["Mind-Talking Drug","3","HtV-175"]))
            elixir.append(tuple(["Breath of the Dragon","4","HtV-175"]))
            elixir.append(tuple(["Amun's Water","4","HtV-176"]))
            elixir.append(tuple(["Incense of the Next World","4","HtV-176"]))
            elixir.append(tuple(["Blood of the Cobra","5","HtV-177"]))
            elixir.append(tuple(["Mesmeric Vapors","5","HtV-177"]))
        if len(relic) == 0:
            relic.append(tuple(["One-Eyed Kings","1","HtV-178"]))
            relic.append(tuple(["Skeleton Ken","1","HtV-180"]))
            relic.append(tuple(["Blood of Pope Joan","2","HtV-180"]))
            relic.append(tuple(["Eye of Hubris","2","HtV-180"]))
            relic.append(tuple(["Heart of the Succubus","2"]))
            relic.append(tuple(["Orpheus' Eye","2","MR-28"]))
            relic.append(tuple(["The Silver Key","2","MR-52"]))
            relic.append(tuple(["Icarine Servitor","3","HtV-180"]))
            relic.append(tuple(["Ringsel","3","HtV-181"]))
            relic.append(tuple(["Watchful Keris","3","HtV-181"]))
            relic.append(tuple(["Heart of Stone","4","HtV-181"]))
            relic.append(tuple(["Witch-Candle","4","HtV-183"]))
            relic.append(tuple(["Aegis Talisman","5","HtV-183"]))
            relic.append(tuple(["Dead Man's Face","5","HtV-184"]))
            relic.append(tuple(["Doru Talisman","5","HtV-184"]))
        if len(magitech) == 0:
            magitech.append(tuple(["Anger Patch","1","HtV-185"]))
            magitech.append(tuple(["Weapon of Last Resort","1,2","HtV-186"]))
            magitech.append(tuple(["Devil's Eyes","2","HtV-186"]))
            magitech.append(tuple(["Lover's Lips","2","HtV-187"]))
            magitech.append(tuple(["Personal Defense Swarm","3","HtV-187"]))
            magitech.append(tuple(["Quick-Step","3","HtV-188"]))
            magitech.append(tuple(["Cranial Cortex Augmentation","4","MR-54"]))
            magitech.append(tuple(["Twitcher","4","HtV-189"]))
            magitech.append(tuple(["Regenerative Nodule","4","HtV-189"]))
            magitech.append(tuple(["Vitriol Pump","4","MR-29"]))
            magitech.append(tuple(["Banality Worm","5","HtV-189"]))
            magitech.append(tuple(["Hand of Glory","5","HtV-190"]))
        if len(ink) == 0:
            ink.append(tuple(["Bear Mace","MR-139"]))
            ink.append(tuple(["Brother Road","MR-139"]))
            ink.append(tuple(["Fist of Revelation","MR-140"]))
            ink.append(tuple(["King of the Road","MR-140"]))
            ink.append(tuple(["The Lord Provides","MR-140"]))
            ink.append(tuple(["LOVE/HATE","MR-140"]))
            ink.append(tuple(["Pain Magnet","MR-141"]))
            ink.append(tuple(["Tough as the Last Guy","MR-141"]))