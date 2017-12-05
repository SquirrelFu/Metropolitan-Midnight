'''
Created on Jan 18, 2017

@author: CodeKitty
'''

#Used for anything that employs dread powers. Mostly assorted beasties outside of the player characters. Faithful of Shulpae are banned,
#but their powers stolen from other supers are gonna be here anyway for the sake of NPCs.

class DreadHandler(object):
    dreadlist = []
    
    def __init__(self):
        dreadlist = self.dreadlist
        if len(dreadlist) == 0:
            dreadlist.append(tuple('Beastmaster','1','CoD-145'))
            dreadlist.append(tuple('Chameleon Horror','1','CoD-145'))
            dreadlist.append(tuple('Discorporate','1','CoD-145'))
            dreadlist.append(tuple('Eye Spy','1','CoD-145'))
            dreadlist.append(tuple('Fire Elemental','1','CoD-145'))
            dreadlist.append(tuple('Influence','1-5','CoD-145'))
            dreadlist.append(tuple('Gremlin','1','CoD-145'))
            dreadlist.append(tuple('Home Ground','1','CoD-145'))
            dreadlist.append(tuple("Hunter's Senses",'1','CoD-145'))
            dreadlist.append(tuple('Hypnotic Gaze','1','CoD-145'))
            dreadlist.append(tuple('Immortal','1','CoD-145'))
            dreadlist.append(tuple('Jump Scare','1','CoD-146'))
            dreadlist.append(tuple('Prodigious Leap','1','CoD-146'))
            dreadlist.append(tuple('Madness and Terror','1','CoD-146'))
            dreadlist.append(tuple('Miracle','1','CoD-146'))
            dreadlist.append(tuple('Maze','1','CoD-146'))
            dreadlist.append(tuple('Mist Form','1','CoD-147'))
            dreadlist.append(tuple('Natural Weapons','1-3','CoD-147'))
            dreadlist.append(tuple('Numen','1','CoD-147'))
            dreadlist.append(tuple('Know Soul','1','CoD-147'))
            dreadlist.append(tuple('Reality Stutter','1','CoD-147'))
            dreadlist.append(tuple('Regenerate','1-5','CoD-147'))
            dreadlist.append(tuple('Snare','1','CoD-147'))
            dreadlist.append(tuple('Soul Thief','1','CoD-147'))
            dreadlist.append(tuple('Surprise Entrance','1','CoD-148'))
            dreadlist.append(tuple('Toxic','1-2','CoD-148'))
            dreadlist.append(tuple('Unbreakable','1','CoD-148'))
            dreadlist.append(tuple('Wall Climb','1','CoD-148'))
            dreadlist.append(tuple("Agonize","1-5","HtV-276"))
            dreadlist.append(tuple("Balefire","1-5","HtV-277"))
            dreadlist.append(tuple("Confuse","1-5","HtV-277"))
            dreadlist.append(tuple("Crushing Blow","3","HtV-278"))
            dreadlist.append(tuple("Damnation","1-5","HtV-278"))
            dreadlist.append(tuple("Dement","1-5","HtV-278"))
            dreadlist.append(tuple("Drain","1-5","HtV-278"))
            dreadlist.append(tuple("Dread Attack","1-5","HtV-278"))
            dreadlist.append(tuple("Ecstasy","1-5","HtV-279"))
            dreadlist.append(tuple("Fury","1-5","HtV-279"))
            dreadlist.append(tuple("Giant Size","4","HtV-279"))
            dreadlist.append(tuple("Gremlinize","1-5","HtV-279"))
            dreadlist.append(tuple("Hypnotism","1-5","HtV-279"))
            dreadlist.append(tuple("Impress","1-5","HtV-280"))
            dreadlist.append(tuple("Judgment of Guilt","5","HtV-280"))
            dreadlist.append(tuple("Lurker in Darkness","1-5","HtV-280"))
            dreadlist.append(tuple("New Face","1-5","HtV-280"))
            dreadlist.append(tuple("Corpse Ride","2","HtV-280"))
            dreadlist.append(tuple("Sleep","1-5","HtV-281"))
            dreadlist.append(tuple("Shadow Harvest","1","HtV-282"))
            dreadlist.append(tuple("Strange Form","1-5","HtV-282"))
            dreadlist.append(tuple("Tendrils","3","HtV-282"))
            dreadlist.append(tuple("Terrify","1-5","HtV-282"))
            dreadlist.append(tuple("Unholy Attribute","1-5","HtV-283"))