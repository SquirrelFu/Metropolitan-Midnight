"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include
# default evennia patterns
from evennia.web.urls import urlpatterns
from web.character.views import mplusrules
from web.character.views import beastpage
from web.character.views import mpluspage
from web.character.views import territorypage
from web.character.views import bookpage
from web.charwiki.views import charlist
from web.charwiki.views import charpage
from web.character.views import magepage
from web.character.views import magerules
from web.character.views import demonpage
from web.character.views import beastcustom
# eventual custom patterns
custom_patterns = [
    url(r'^mplus/rules/$', mplusrules),
    url(r'^beast/$', beastpage),
    url(r'^mplus/$',mpluspage),
    url(r'^territory/$',territorypage),
    url(r'booklist/$',bookpage),
    url(r'^character/$', charlist),
    url(r'^character/(?P<charname>.+)/$',charpage,name='characterpage'),
    url(r'^mage/$', magepage),
    url(r'^mage/rules/$', magerules),
    url(r'^demon/$',demonpage),
    url(r'^beast/customs/$',beastcustom)
    ]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns