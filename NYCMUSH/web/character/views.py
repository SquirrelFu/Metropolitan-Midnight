from django.shortcuts import render

# Create your views here.

from django.http import Http404
from django.shortcuts import render
from django.conf import settings

def mplusrules(request):
    return render(request, 'mplusrules/plushrmain.html')
def beastpage(request):
    return render(request, 'beastpage/beastmain.html')
def mpluspage(request):
    return render(request, 'mpluspage/mplusmain.html')
def territorypage(request):
    return render(request, 'territory/territorymain.html')
def bookpage(request):
    return render(request, 'bookpage/bookmain.html')
def magepage(request):
    return render(request, 'magepage/magemain.html')
def magerules(request):
    return render(request, 'magerules/magerules.html')