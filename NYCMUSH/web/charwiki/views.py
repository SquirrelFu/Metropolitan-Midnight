from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from evennia import DefaultCharacter
from web.charwiki.templates.charlist.forms import NameForm
from typeclasses.characters import Character
# Create your views here.
def charpage(request, charname):
    charList = DefaultCharacter.objects.filter_family()
    if "_" in charname:
        charname = charname.replace("_"," ")

    for actor in charList:
        if actor.key.lower() == charname.lower():
            char = get_object_or_404(Character, db_key=actor.key)
    try:
        return render(request, 'charpage/sheet.html',{'character':char})
    except UnboundLocalError:
        char = get_object_or_404(Character,db_key=charname)
        return render(request, 'charpage.sheet.html',{'character':char})
def charlist(request):
    return render(request, 'charlist/charlist.html')