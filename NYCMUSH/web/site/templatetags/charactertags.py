'''
Created on Jan 24, 2017

@author: CodeKitty
'''

from django import template
from evennia import DefaultCharacter
from server.conf import settings
register = template.Library()

@register.simple_tag
def mortaldb():
    objlist = DefaultCharacter.objects.filter_family()
    charlist = []
    for char in objlist:
        if char.db.template == "Mortal" and (not char.db.IsMortalPlus):
            charlist.append(char)
    for thing in charlist:
        if thing.id == 1:
            charlist.remove(thing)
        elif thing.db.admin_main == True:
            charlist.remove(thing)
    return charlist
@register.simple_tag
def beaststatus():
    return str(settings.BEAST_STATUS)
@register.simple_tag
def vampstatus():
    return str(settings.VAMPIRE_STATUS)
@register.simple_tag
def wolfstatus():
    return str(settings.WEREWOLF_STATUS)
@register.simple_tag
def magestatus():
    return str(settings.MAGE_STATUS)
@register.simple_tag
def promstatus():
    return str(settings.PROMETHEAN_STATUS)
@register.simple_tag
def huntstatus():
    return str(settings.HUNTER_STATUS)
@register.simple_tag
def demonstatus():
    return str(settings.DEMON_STATUS)
@register.simple_tag
def atariyastatus():
    return str(settings.ATARIYA_STATUS)
@register.simple_tag
def dreamerstatus():
    return str(settings.DREAMER_STATUS)
@register.simple_tag
def infectedstatus():
    return str(settings.INFECTED_STATUS)
@register.simple_tag
def lostboysstatus():
    return str(settings.LOSTBOYS_STATUS)
@register.simple_tag
def plainstatus():
    return str(settings.PLAIN_STATUS)
@register.simple_tag
def psyvampstatus():
    return str(settings.PSYVAMP_STATUS)