# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Stat(models.Model):
    name = models.CharField(max_length=25, db_index=True)
    #The name of the stat itself.
    rating = models.SmallIntegerField(default=1)
    #The rating of the stat in dots.
    def __str__(self):
        return self.name
    def __int__(self):
        return self.rating
class Attribute(Stat):
    type = models.CharField(max_length=10)
    #Power, finesse, resistance.
    category = models.CharField(max_length=8)
    #Physical, mental, social
class Skill(Stat):
    category = models.CharField(max_length=8)
    #Physical, mental, social
class Pool(models.Model):
    name = models.CharField(max_length=25)
    #The name of the expendable pool.
    current = models.SmallIntegerField(default=0)
    #The amount of expendable points in the pool
    capacity = models.SmallIntegerField(default=10)
    #The amount of expendable points that a given pool can hold.
    limit = models.SmallIntegerField(default=1)
    #The number of points per turn a character can spend.
    def __str__(self):
        return self.name
    def __int__(self):
        return self.current
class PowerStat(Stat):
    pool = models.ForeignKey(Pool)
    #The pool associated with the powerstat in question.
class Specialty(models.Model):
    name = models.CharField(max_length=25)
    #The name of the specialty in question.
    skill = models.ForeignKey(Skill)
    #The skill that this specialty is found within.
    def __str_(self):
        return self.name
class Template(models.Model):
    name = models.CharField(max_length=25, db_index=True)
    #The name of the template. Can be a mortal, can be a mage, vampire, anything.
    majorTemplate = models.BooleanField(default=False)
    #Whether or not this template has a powerstat. In official terms a, "Supernatural resistance attribute".
    
    def __str__(self):
        return self.name