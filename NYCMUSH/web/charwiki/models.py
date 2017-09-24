from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CharPageData(models.Model):
    
    name = models.CharField(max_length=50)
    template = models.CharField(max_length=50)
    def __str__(self):
        return self.name