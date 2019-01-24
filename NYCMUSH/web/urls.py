"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include
# default evennia patterns
from evennia.web.urls import urlpatterns
from web.site.views import mplusrules
from web.site.views import beastpage
from web.site.views import mpluspage
from web.site.views import bookpage
from web.charwiki.views import charlist
from web.charwiki.views import charpage
from web.site.views import magepage
from web.site.views import magerules
from web.site.views import demonpage
from web.site.views import beastcustom
from web.site.views import beastrules
# eventual custom patterns
custom_patterns = [
    url(r'^mplus/rules/$', mplusrules),
    url(r'^beast/$', beastpage),
    url(r'^mplus/$',mpluspage),
    url(r'booklist/$',bookpage),
    url(r'^character/$', charlist),
    url(r'^character/(?P<charname>.+)/$',charpage,name='characterpage'),
    url(r'^mage/$', magepage),
    url(r'^mage/rules/$', magerules),
    url(r'^demon/$',demonpage),
    url(r'^beast/customs/$',beastcustom),
    url(r'^beast/rules/$',beastrules),
    ]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns