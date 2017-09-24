'''
Created on Jan 22, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from evennia import DefaultScript

class InventoryCommand(default_cmds.MuxCommand):
    key = "+inv"
    aliases = ["+inventory"]
    def func(self):
        switches = self.switches
        if len(switches) > 0:
            if switches[0].lower() == "equipment":
                outtable = self.caller.ShowEquip()
            elif switches[0].lower() == "armor":
                outtable = self.caller.ShowArmor()
            elif switches[0].lower() == "weapons":
                outtable = self.caller.ShowWeapon()
            elif switches[0].lower() == "vehicles":
                outtable = self.caller.ShowVehicles()
            elif switches[0].lower() == "explosives":
                outtable = self.caller.ShowExplosives()
            if outtable == "":
                self.caller.msg("You don't have any " + switches[0].lower()+" in your inventory!")
            else:
                self.caller.msg(str(outtable))
        else:
            outtable = self.caller.ShowAll()
            if len(self.caller.db.equipinv) == 0:
                self.caller.msg("Your inventory is empty!")
            else:
                self.caller.msg(str(outtable))
class EquipmentList(DefaultScript):
    bookref = ["CoD","HL"]
    booklong = ["Chronicles of Darkness","Hurt Locker"]
    def at_script_creation(self):
        self.db.equipment = []
        self.db.armor = []
        self.db.weapons = []
        self.db.vehicles = []
        self.db.explosives = []
        equip = self.db.equipment
        armor = self.db.armor
        vehicles = self.db.vehicles
        weap = self.db.weapons
        bomb = self.db.explosives
        equip.append(tuple(["Automotive Tools","1","CoD-270"]))
        equip.append(tuple(["Cache","1,2,3","CoD-270"]))
        equip.append(tuple(["Communications Headset","2","CoD-271"]))
        equip.append(tuple(["Crime Scene Kit","CoD-271"]))
        equip.append(tuple(["Code Kit","5","CoD-271"]))
        equip.append(tuple(["Cracking Software","2","CoD-271"]))
        equip.append(tuple(["Digital Recorder","1,2","CoD-271"]))
        equip.append(tuple(["Duct Tape","1","CoD-272"]))
        equip.append(tuple(["First-Aid Kit","0,1","CoD-272"]))
        equip.append(tuple(["Flashlight","1","CoD-272"]))
        equip.append(tuple(["Glowstick","2","CoD-272"]))
        equip.append(tuple(["Keylogging Software","2","CoD-272"]))
        equip.append(tuple(["Luminol","2","CoD-272"]))
        equip.append(tuple(["Multi-Tool","1","CoD-272"]))
        equip.append(tuple(["Personal Computer","1,2,3,4","CoD-273"]))
        equip.append(tuple(["Smartphone","1,2","CoD-273"]))
        equip.append(tuple(["Special Effects","2","CoD-273"]))
        equip.append(tuple(["Surveillance Equipment","2","CoD-273"]))
        equip.append(tuple(["Survival Gear","1,2","CoD-273"]))
        equip.append(tuple(["Talcum Powder","2","CoD-273"]))
        equip.append(tuple(["Ultraviolet Ink","2","CoD-273"]))
        equip.append(tuple(["Battering Ram","4","CoD-274"]))
        equip.append(tuple(["Bear Trap","2","CoD-274"]))
        equip.append(tuple(["Caltrops","2","CoD-274"]))
        equip.append(tuple(["Camouflage Clothing","2","CoD-275"]))
        equip.append(tuple(["Climbing Gear","2","CoD-275"]))
        equip.append(tuple(["Crowbar","2","CoD-275"]))
        equip.append(tuple(["Firearm Suppressor","2","CoD-275"]))
        equip.append(tuple(["Gas Mask","5","CoD-275"]))
        equip.append(tuple(["Handcuffs","2","CoD-275"]))
        equip.append(tuple(["Lockpicking Kit","2","CoD-275"]))
        equip.append(tuple(["Night Vision Goggles","2","CoD-276"]))
        equip.append(tuple(["Pepper Spray","2","CoD-276"]))
        equip.append(tuple(["Rope","1","CoD-276"]))
        equip.append(tuple(["Stun Gun","0","CoD-277"]))
        equip.append(tuple(["Cash","1,2,3,4,5","CoD-277"]))
        equip.append(tuple(["Disguise","1,2,3","CoD-277"]))
        equip.append(tuple(["Fashion","1,2,3,4,5","CoD-277"]))
        equip.append(tuple(["Bipod","0","HL-144"]))
        equip.append(tuple(["Ear Protection","0","HL-144"]))
        equip.append(tuple(["Gunsmithing Kit","2","HL-144"]))
        equip.append(tuple(["Light Mount","1","HL-144"]))
        equip.append(tuple(["Reloading Bench","2","HL-144"]))
        equip.append(tuple(["Sighting Tools","2","HL-145"]))
        weap.append(tuple(["Revolver lt","1","Medium","0","2","1","None","CoD-268"]))
        weap.append(tuple(["Revolver hvy","2","Medium","-2","3","1","None","CoD-268"]))
        weap.append(tuple(["Pistol lt","1","Medium","0","2","1","None","CoD-268"]))
        weap.append(tuple(["Pistol hvy","2","Low","-2","3","1","None","CoD-268"]))
        weap.append(tuple(["SMG small","1","High","-2","2","1","Autofire","CoD-268"]))
        weap.append(tuple(["SMG large","2","High","-3","3","2","Autofire","CoD-268"]))
        weap.append(tuple(["Rifle","4","Low","-5","2","3","None","CoD-268"]))
        weap.append(tuple(["Assault Rifle","3","High","-3","3","3","Autofire","CoD-268"]))
        weap.append(tuple(["Shotgun","3","Low","-4","3","2","9-again","CoD-268"]))
        weap.append(tuple(["Crossbow","2","Low","-5","3","3","None","CoD-268"]))
        weap.append(tuple(["Sap","0","-1","1","1","Stun","CoD-269"]))
        weap.append(tuple(["Baton","1","-1","2","2","Brawl","CoD-269"]))
        weap.append(tuple(["Crowbar","2","-2","2","2","None","CoD-269"]))
        weap.append(tuple(["Tire Iron","1","-3","2","2","Guard, Inaccurate","CoD-269"]))
        weap.append(tuple(["Chain","1","-3","2","2","Grapple, Inaccurate, Reach","CoD-269"]))
        weap.append(tuple(["Shield (Small)","0","2","2","2","Concealed","CoD-269"]))
        weap.append(tuple(["Shield (Large)","2","-4","3","3","Concealed","CoD-269"]))
        weap.append(tuple(["Knife","0","-1","1","1","Thrown(A)","CoD-269"]))
        weap.append(tuple(["Rapier","1","-2","1","2","AP1","CoD-269"]))
        weap.append(tuple(["Machete","2","-2","2","2","None","CoD-269"]))
        weap.append(tuple(["Hatchet","1","-2","1","1","None","CoD-269"]))
        weap.append(tuple(["Fire Axe","3","-4","3","3","9-Again, 2h","CoD-269"]))
        weap.append(tuple(["Chainsaw","5","-6","4","3","9-Again, 2h","CoD-269"]))
        weap.append(tuple(["Stake","0","-4","1","1","None","CoD-269"]))
        weap.append(tuple(["Spear","2","-2","2","4","Reach, 2h","CoD-269"]))
        weap.append(tuple(["Stun Gun","1","-1","1","1","Base, Stun","CoD-269"]))
        armor.append(tuple(["Reinforcd Clothing","1/0","1","0","0","Hide","Torso, Arms, Legs"]))
        armor.append(tuple(["Kevlar Vest","1/3","1","0","0","Hide","Torso"]))
        armor.append(tuple(["Flak Jacket","1/4","1","-1","0","Hide","Torso, Arms"]))
        armor.append(tuple(["Full Riot Gear","3/5","2","-2","-2","Torso, Arms, Legs"]))
        armor.append(tuple(["Leather (Hard)","2/0","2","-1","0","Torso, Arms"]))
        armor.append(tuple(["Chainmail","3/1","3","-2","-2","Torso, Arms"]))
        armor.append(tuple(["Plate","4/2","3","-2","-3","Torso, Arms, Legs"]))
        weap.append(tuple(["Big game rifle","5","Low","-5","3","4","Stun","HL-133"]))
        weap.append(tuple(["Short Bow","2","Low","-3","2","3","None","HL-133"]))
        weap.append(tuple(["Long Bow","3","Low","-4","3","4","None","HL-133"]))
        weap.append(tuple(["Pepper Spray","0","1","1","Slow","HL-133"]))
        bomb.append(tuple(["Frag standard","2","0","10","3","2","1","Knockdown, Stun","HL-135"]))
        bomb.append(tuple(["Frag heavy","3","-1","5","4","2","1","Knockdown, Stun","HL-135"]))
        bomb.append(tuple(["Molotov","1","-2","3","2","2","2","Incendiary","HL-135"]))
        bomb.append(tuple(["Pipe Bomb","1","-1","5","2","1","Inaccurate, Stun","HL-135"]))
        bomb.append(tuple(["Smoke","0","10","-","-","2","Concealment","HL-135"]))
        bomb.append(tuple(["Stun","0","0","5","2","2","Knockdown, Stun","HL-135"]))
        bomb.append(tuple(["Thermite","3","5","4","-","2","1","Incendiary ,AP8","HL-135"]))
        bomb.append(tuple(["White Phospohorous","3","5","4","-","2","1","Incendiary, AP3","HL-135"]))
        weap.append(tuple(["Battle Axe","3","-4","3","3","9-again, 2h","HL-138"]))
        weap.append(tuple(["Greatsword","4","-5","4","3","9-again, 2h","HL-138"]))
        weap.append(tuple(["Hunting Knife","1","-1","1","2","Enhance Crafts, Enhance Survival","HL-138"]))
        weap.append(tuple(["Katana","3","-3","2","3","Durability +1","HL-138"]))
        weap.append(tuple(["Longsword","3","-2","2","3","None","HL-138"]))
        weap.append(tuple(["Brass Knuckles","0","0","1","1","Brawl","HL-138"]))
        weap.append(tuple(["Metal Club","2","-2","2","2","Stun","HL-138"]))
        weap.append(tuple(["Nunchaku","1","1","2","2","Stun","None","HL-138"]))
        weap.append(tuple(["Sledgehammer","3","-4","3","3","Knockdown, Stun","HL-138"]))
        weap.append(tuple(["Catchpole","0","-3","2","2","Grapple, Reach","HL-138"]))
        weap.append(tuple(["Tiger Claws","1","-1","2","2","Brawl","HL-138"]))
        weap.append(tuple(["Whip","0","-2","1","2","Grapple","Stun","HL-138"]))
        weap.append(tuple(["Blowtorch","0","-2","2","2","Special","HL-139"]))
        weap.append(tuple(["Nailboard","1","-3","2","2","Fragile, Stun","HL-139"]))
        weap.append(tuple(["Improvised Shield","0","-4","2","2","Concealed","HL-139"]))
        weap.append(tuple(["Nail Gun","0","-2","2","2","Inaccurate, AP1","HL-139"]))
        weap.append(tuple(["Shovel","1","-3","2","2","Knockdown","HL-139"]))
        weap.append(tuple(["Staff","1","-1","2","4","Knockdown, Reach, 2h","HL-139"]))
        armor.append(tuple(["Sports Gear","2/0","2","-1","-1","Torso, Arms, Legs"]))
        armor.append(tuple(["Bomb Suit","4/6","3","-5","-4","Torso, Arms, Head"]))
        armor.append(tuple(["Lorica Segmentata","2/2","3","-2","-3","Torso"]))
        vehicles.append(tuple(["Motorcycle","-1","7","100","High Acceleration"]))
        vehicles.append(tuple(["Compact Car","-2","8","90","None"]))
        vehicles.append(tuple(["Family Car","-3","12","80","None"]))
        vehicles.append(tuple(["Sports Car","-1","140","High Acceleration"]))
        vehicles.append(tuple(["Limousine","-4","20","60","None"]))
        vehicles.append(tuple(["Van","-3","18","80","Slow Acceleration"]))
        vehicles.append(tuple(["Pickup Truck","-2","15","80","Slow Acceleration"]))
        vehicles.append(tuple(["SUV","-2","15","100","None"]))
        vehicles.append(tuple(["Motorboat","-2","10","60","None"]))
        equip.append(tuple(["Helmet","0","HL-142"]))
        equip.append(tuple(["Fiber Optic Sight","0","HL-145"]))
        equip.append(tuple(["Laser Sight","0","HL-145"]))
        equip.append(tuple(["IR Laser Sight","0","HL-145"]))
        equip.append(tuple(["Telescopic Sight","0","HL-145"]))
        equip.append(tuple(["Night Vision Sight","0","HL-145"]))
        equip.append(tuple(["Thermal Sight","0","HL-145"]))
        equip.append(tuple(["Speedloader","0","HL-145"]))
        equip.append(tuple(["Collapsible Stock","0","HL-145"]))
        equip.append(tuple(["Binoculars","0","HL-146"]))
        equip.append(tuple(["Bugs","0","HL-146"]))
        equip.append(tuple(["Bug Sweepers","2","HL-147"]))
        equip.append(tuple(["Disguised Camera","0","HL-147"]))
        equip.append(tuple(["Tracking Device","2","HL-147"]))
        equip.append(tuple(["Reverse Peephole","0","HL-147"]))
        equip.append(tuple(["Spyware","2","HL-147"]))
        equip.append(tuple(["Wi-Fi Sniffer","0","HL-147"]))
        equip.append(tuple(["Wiretap","0","HL-147"]))
        equip.append(tuple(["NBC Suit","5","HL-148"]))
        equip.append(tuple(["Potassium Iodide","1","HL-148"]))
        equip.append(tuple(["Survival Kit (Basic)","1","HL-148"]))
        equip.append(tuple(["Survival Kit (Advanced)","2","HL-148"]))
        equip.append(tuple(["Survival Kit (Superior)","3","HL-148"]))
        equip.append(tuple(["Survival Kit (Urban)","3","HL-148"]))