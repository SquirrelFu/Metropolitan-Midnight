'''
Created on Jul 22, 2017

@author: CodeKitty
'''
from django import template
from evennia import DefaultCharacter
register = template.Library()
import calendar

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
@register.simple_tag
def mortaldb():
    objlist = DefaultCharacter.objects.filter_family()
    charlist = []
    for char in objlist:
        if char.db.template == "Mortal" and (not char.IsMortalPlus()):
            if char.db.approved:
                charlist.append(char)
    for thing in charlist:
        if thing.id == 1:
            charlist.remove(thing)
        elif thing.db.admin_main == True:
            charlist.remove(thing)
            
    return charlist
@register.filter
def ismortalplus(characterin):
    if characterin.IsMortalPlus():
        return True
    else:
        return False