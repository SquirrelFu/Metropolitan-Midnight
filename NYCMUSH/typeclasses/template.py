'''
Created on Jan 10, 2017

@author: CodeKitty
'''
class Attribute(object):
    #The class used for all attributes.
    name = ""
    #Of course, the basic name of the attribute.
    category = ""
    #Category defines the sort of attribute it is. Mental, Physical, or Social.
    type = ""
    #Type defines the kind of attribute involved, technically referred to as a category
    #also but just named this for ease's sake. Power, Finesse, or Resistance.
    score = 1
    #Score is the attribute's true rating.
    effective_score = 1
    #Effective score is a bit different. Some powers add to the effective rating, like a
    #vampire's Vigor adding to effective strength or a werewolf's gift doing the same.
    #This is what is used when dice are rolled, but not when calculating limits.
    linked = 0
    #This variable is initialized to an integer of zero, but is to be used for any
    #power or attribute (In the case of werewolves adding renown) whose rating
    #directly influences the effective score.
    def __init__(self, value):
        self.score = value
        self.effective_score = value
    #The constructor here just sets the effective and true value of the attribute to whatever number is passed in.
    def RaiseEffective(self, value):
        self.effective_score += value
    def LowerEffective(self, value):
        if self.effective_score - value > 0:
            self.effective_score = 0
            return
        else:
            self.effective_score -= value
class Strength(Attribute):
    def __init__(self, value):
        super(Strength, self).__init__(value)
        self.name = "Strength"
        self.category = "Physical"
        self.type = "Power"
class Dexterity(Attribute):
    def __init__(self, value):
        super(Dexterity, self).__init__(value)
        self.name = "Dexterity"
        self.category = "Physical"
        self.type = "Finesse"
class Stamina(Attribute):
    def __init__(self, value):
        super(Stamina, self).__init__(value)
        self.name = "Stamina"
        self.category = "Physical"
        self.type = "Resistance"
class Presence(Attribute):
    def __init__(self, value):
        super(Presence, self).__init__(value)
        self.name = "Presence"
        self.category = "Social"
        self.type = "Power"
class Manipulation(Attribute):
    def __init__(self, value):
        super(Manipulation, self).__init__(value)
        self.name = "Manipulation"
        self.category = "Social"
        self.type = "Finesse"
class Composure(Attribute):
    def __init__(self, value):
        super(Composure, self).__init__(value)
        self.name = "Composure"
        self.category = "Social"
        self.type = "Resistance"
class Intelligence(Attribute):
    def __init__(self,value):
        super(Intelligence, self).__init__(value)
        self.name = "Intelligence"
        self.category = "Mental"
        self.type = "Power"
class Wits(Attribute):
    def __init__(self, value):
        super(Wits, self).__init__(value)
        self.name = "Wits"
        self.category = "Mental"
        self.type = "Finesse"
class Resolve(Attribute):
    def __init__(self, value):
        super(Resolve, self).__init__(value)
        self.name = "Resolve"
        self.category = "Mental"
        self.type = "Resistance"
class Skill(object):
    #This is the parent class for all skills. Unlike attributes, skills don't actually have types. They only have categories.
    category = ""
    name = ""
    score = 0
    specialties = []
    def __init__(self, value):
        self.score = value
class Academics(Skill):
    def __init__(self, value):
        super(Academics, self).__init__(value)
        self.name = "Academics"
        self.category = "Mental"
class Computer(Skill):
    def __init__(self, value):
        super(Computer, self).__init__(value)
        self.name = "Computer"
        self.category = "Mental"
class Crafts(Skill):
    def __init__(self, value):
        super(Crafts, self).__init__(value)
        self.name = "Crafts"
        self.category = "Mental"
class Investigation(Skill):
    def __init__(self, value):
        super(Investigation, self).__init__(value)
        self.name = "Investigation"
        self.category = "Mental"
class Medicine(Skill):
    def __init__(self, value):
        super(Medicine, self).__init__(value)
        self.name = "Medicine"
        self.category = "Mental"
class Occult(Skill):
    def __init__(self, value):
        super(Occult, self).__init__(value)
        self.name = "Occult"
        self.category = "Mental"
class Politics(Skill):
    def __init__(self, value):
        super(Politics, self).__init__(value)
        self.name = "Politics"
        self.category = "Mental"
class Science(Skill):
    def __init__(self, value):
        super(Science, self).__init__(value)
        self.name = "Science"
        self.category = "Mental"
class Athletics(Skill):
    def __init__(self, value):
        super(Athletics, self).__init__(value)
        self.name = "Athletics"
        self.category = "Physical"
class Brawl(Skill):
    def __init__(self, value):
        super(Brawl, self).__init__(value)
        self.name = "Brawl"
        self.category = "Physical"
class Drive(Skill):
    def __init__(self, value):
        super(Drive, self).__init__(value)
        self.name = "Drive"
        self.category = "Physical"
class Firearms(Skill):
    def __init__(self, value):
        super(Firearms, self).__init__(value)
        self.name = "Firearms"
        self.category = "Physical"
class Larceny(Skill):
    def __init__(self, value):
        super(Larceny, self).__init__(value)
        self.name = "Larceny"
        self.category = "Physical"
class Stealth(Skill):
    def __init__(self, value):
        super(Stealth, self).__init__(value)
        self.name = "Stealth"
        self.category = "Physical"
class Survival(Skill):
    def __init__(self, value):
        super(Survival, self).__init__(value)
        self.name = "Survival"
        self.category = "Physical"
class Weaponry(Skill):
    def __init__(self, value):
        super(Weaponry, self).__init__(value)
        self.name = "Weaponry"
        self.category = "Physical"
class Animal_Ken(Skill):
    def __init__(self, value):
        super(Animal_Ken, self).__init__(value)
        self.name = "Animal Ken"
        self.category = "Social"
class Empathy(Skill):
    def __init__(self, value):
        super(Empathy, self).__init__(value)
        self.name = "Empathy"
        self.category = "Social"
class Expression(Skill):
    def __init__(self, value):
        super(Expression, self).__init__(value)
        self.name = "Expression"
        self.category = "Social"
class Intimidation(Skill):
    def __init__(self, value):
        super(Intimidation, self).__init__(value)
        self.name = "Intimidation"
        self.category = "Social"
class Persuasion(Skill):
    def __init__(self, value):
        super(Persuasion, self).__init__(value)
        self.name = "Persuasion"
        self.category = "Social"
class Socialize(Skill):
    def __init__(self, value):
        super(Socialize, self).__init__(value)
        self.name = "Socialize"
        self.category = "Social"
class Streetwise(Skill):
    def __init__(self, value):
        super(Streetwise, self).__init__(value)
        self.name = "Streetwise"
        self.category = "Social"
class Subterfuge(Skill):
    def __init__(self, value):
        super(Subterfuge, self).__init__(value)
        self.name = "Subterfuge"
        self.category = "Social"