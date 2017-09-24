from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from evennia.utils import search
from evennia.utils.utils import inherits_from
from web.charwiki.templates.charlist.forms import NameForm
from web.charwiki.models import CharPageData
from typeclasses.characters import Character
# Create your views here.
def charpage(request, charname):
    char = get_object_or_404(Character, db_key=charname)
    return render(request, 'charpage/sheet.html',{'character':char})
def charlist(request):
    return render(request, 'charlist/charlist.html')