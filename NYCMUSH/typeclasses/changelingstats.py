'''
Created on Jan 13, 2017

@author: CodeKitty
'''
from evennia import DefaultScript
class ChangelingStatHandler(DefaultScript):
    seemings = ["Beast","Elemental","Fairest","Darkling","Ogre","Wizened"]
    kiths = ["Airtouched","Antiquarian","Artist","Author","Blightbent","Bloodbrute","Brewer","Bright One","Broadback","Brollachan","Chatelaine","Chimera","Chirurgeon","Cleareyes",
             "Coldscale","Corpsegrinder","Coyote","Cyclopean","Dancer","Dearheart","Draconic","Earthbones","Farwalker","Fireheart","Flamesiren","Flowering","Gameplayer","Gargantuan",
             "Gravewright","Gremlin","Grey","Gristlegrinder","Hunterheart","Ifrit","Illes","Jeweleyes","Larcenist","Leechfinger","Levinquick","Lurker","Lurkglider","Maker","Manikin",
             "Metalflesh","Miner","Minstrel","Mirrorskin","Moonborn","Muse","Nightsinger","Nix","Oni","Oracle","Palewraith","Playmate","Polychromatic","Razorhand","Render",
             "Riddleseeker","Roteater","Runnerswift","Sandharrowed","Shadowsoul","Skitterskulk","Skogsra","Slewfoot","Smith","Snowskin","Soldier","Steepscrambler","Swimmerskin",
             "Telluric","Thusser","Troll","Truefriend","Tunnelgrub","Venombite","Weisse Frau","Waterborn","Whisperwisp","Windwing","Witchtooth","Woodblood","Woodwalker"]
    entitlements = ["Tempest Knights","Justicars of Themis","The Principality of the Crooked Tongue"]
    archetypes = ['Actor','Artist','Belle','Child','Guru','Follower','Fool','Idealist','Martyr','Monster','Nomad','Predator','Rebel','Romantic','Survivor']
    def at_script_creation(self):
        self.db.contracts = []
        self.db.seemings = self.seemings
        self.db.kiths = self.kiths
        self.db.entitlements = self.entitlements
        contracts = self.db.contracts
        contracts.append(tuple(["Bite of the Wooden Fang","1","Elemental,Ogre","CtL:PTM-89"]))
        contracts.append(tuple(["Changeling Fate","1,2,3","Ogre,Wizened","CtL:PTM-89"]))
        contracts.append(tuple(["Cloak of the Elements","1,2,3","Elemental,Fairest","CtL:PTM-90"]))
        contracts.append(tuple(["Creeping Dread","1","Darkling,Fairest","CtL:PTM-91"]))
        contracts.append(tuple(["Fang and Talon","1,2,3","Beast","CtL:PTM-91"]))
        contracts.append(tuple(["Inanimate Communion","1,2,3","Darkling,Wizened","CtL:PTM-92"]))
        contracts.append(tuple(["Know the Competition","1","Beast,Darkling","CtL:PTM-93"]))
        contracts.append(tuple(["Mask of Superiority","1,2,3","Fairest,Ogre","CtL:PTM-94"]))
        contracts.append(tuple(["Pathfinder","1","Beast,Elemental","CtL:PTM-94"]))
        contracts.append(tuple(["Read Lucidity","1","Darkling,Fairest","CtL:PTM-95"]))
        contracts.append(tuple(["Reflections of the Past","1,2,3,4,5","Fairest,Wizened","CtL:PTM-96"]))
        contracts.append(tuple(["Trivial Reworking","1","Ogre,Wizened","CtL:PTM-96"]))
        contracts.append(tuple(["Boon of the Scuttling Spider","2","Beast,Darkling","CtL:PTM-97"]))
        contracts.append(tuple(["Changeling Hours","2,3,4","Elemental,Fairest","CtL:PTM-98"]))
        contracts.append(tuple(["Dreamsteps","2","Fairest","CtL:PTM-98"]))
        contracts.append(tuple(["Glimpse of a Distant Mirror","2","Beast,Darkling","CtL:PTM-99"]))
        contracts.append(tuple(["Light-Shy","2","Darkling,Wizened","CtL:PTM-100"]))
        contracts.append(tuple(["Might of the Terrible Brute","2","Beast,Ogre","CtL:PTM-100"]))
        contracts.append(tuple(["Murkblur","2","Fairest,Ogre","CtL-PTM:101"]))
        contracts.append(tuple(["Nevertread","2","Beast,Elemental","CtL-PTM:101"]))
        contracts.append(tuple(["Night's Subtle Distractions","2","Darkling,Elemental","CtL-PTM:102"]))
        contracts.append(tuple(["Thorns and Brambles","2,3,4","Darkling,Ogre","CtL:PTM-104"]))
        contracts.append(tuple(["Touch of the Workman's Wrath","2","Elemental,Wizened","CtL-PTM:102"]))
        contracts.append(tuple(["Vainglory","2,3,4","Darkling,Fairest,Wizened","CtL:PTM-103"]))
        contracts.append(tuple(["Blessing of Perfection","3","Fairest,Wizened","CtL:PTM-105"]))
        contracts.append(tuple(["Control Elements","3","Darkling,Elemental","CtL:PTM-106"]))
        contracts.append(tuple(["Discreet Conjuration","3","Darkling,Wizened","CtL:PTM-107"]))
        contracts.append(tuple(["Flickering Hours","3","Elemental,Fairest","CtL:PTM-107"]))
        contracts.append(tuple(["Mirror Walk","3","Beast,Darkling","CtL:PTM-108"]))
        contracts.append(tuple(["Game Master's Table","3","Fairest","CtL:PTM-109"]))
        contracts.append(tuple(["Pipes of the Beastcaller","3","Beast,Ogre","CtL:PTM-110"]))
        contracts.append(tuple(["Portents and Visions","3","Ogre,Wizened","CtL:PTM-110"]))
        contracts.append(tuple(["Riddle-Kith","3","Elemental,Fairest","CtL:PTM-111"]))
        contracts.append(tuple(["Shared Burden","3","Ogre,Wizened","CtL:PTM-111"]))
        contracts.append(tuple(["Skinmask","3","Beast,Fairest","CtL:PTM-112"]))
        contracts.append(tuple(["Temporary Lucidity","3","Fairest,Ogre","CtL:PTM-113"]))
        contracts.append(tuple(["Terrible Harvest","3","Fairest,Ogre,Darkling","CtL:PT-62"]))
        contracts.append(tuple(["Armored Clarity","4","Ogre,Wizened","CtL:PTM-113"]))
        contracts.append(tuple(["Cheater's Gambit","4","Beast,Fairest","CtL:PTM-114"]))
        contracts.append(tuple(["Cloak of the Bear's Massive Form","4","Beast,Ogre","CtL:PTM-115"]))
        contracts.append(tuple(["Elegant Protection","4","Fairest,Ogre","CtL:PTM-115"]))
        contracts.append(tuple(["Hidden Reality","4","Fairest,Wizened","CtL:PTM-116"]))
        contracts.append(tuple(["Luna's Bedlam","4","Fairest,Ogre","CtL-PTM-117"]))
        contracts.append(tuple(["Stealing the Solid Reflection","4","Elemental,Wizened","CtL:PTM-117"]))
        contracts.append(tuple(["Tatterdemalion's Workshop","4","Ogre,Wizened","CtL:PTM-118"]))
        contracts.append(tuple(["Animate Device","5","Beast,Wizened","CtL:PTM-119"]))
        contracts.append(tuple(["Chrysalis","5","Beast,Wizened","CtL:PTM-120"]))
        contracts.append(tuple(["Hedgewall","5","Elemental","CtL:PTM-120"]))
        contracts.append(tuple(["Leaping Toward Nightfall","5","Wizened","CtL:PTM-121"]))
        contracts.append(tuple(["Paralyzing Shudder","5","Darkling,Ogre","CtL:PTM-122"]))
        contracts.append(tuple(["Phantom Glory","5","Elemental,Fairest","CtL:PTM-122"]))
        contracts.append(tuple(["Red Rage of Terrible Revenge","5","Beast,Ogre","CtL:PTM-123"]))
        contracts.append(tuple(["Thief of Reason","5","Beast,Darkling","CtL:PTM-124"]))
        contracts.append(tuple(["Tying the Knots of Fate","5","Fairest,Ogre","CtL:PTM-124"]))
        contracts.append(tuple(["Vision of Fortune's Favor","5","Wizened","CtL:PTM-125"]))