'''
Created on Feb 5, 2017

@author: CodeKitty
'''

from django import forms
from web.charwiki.models import CharPageData
class NameForm(forms.ModelForm):
    class Meta:
        model = CharPageData
        fields = ('name','template')