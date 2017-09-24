'''
Created on Jan 23, 2017

@author: CodeKitty
'''
from server.conf import settings
RSS_ENABLED = settings.RSS_ENABLED
from commands.command import Command
from datetime import date
from textwrap import wrap
#RETAG = re.compile(r'<[^>]*?>')
import re
import time
if RSS_ENABLED:
    try:
        import feedparser
    except ImportError:
        raise ImportError("RSS requires python-feedparser to be installed. Install or set RSS_ENABLED=False.")


class CheckWeather(Command):
    wintermonths = ['Jan','Feb','Mar']
    springmonths = ['Apr','May','Jun']
    summermonths = ['Jul','Aug','Sep']
    fallmonths = ['Oct','Nov','Dec']
    key = "+weather"
    locks = "cmd:all()"
    def func(self):
        if "hedge" in self.caller.location.tags.all():
            self.caller.msg("The wild hedge is subjected to many weathers, none of them Earth's.")
            return
        elif "underworld" in self.caller.location.tags.all():
            self.caller.msg("Deep within the underworld as you are, you find it difficult to ascertain Earth's weather.")
            return
        elif "outdoors" in self.caller.location.tags.all() or "outside" in self.caller.location.tags.all():
            weatherinfo = settings.WEATHER
        elif "indoors" in self.caller.location.tags.all() or "inside" in self.caller.location.tags.all():
            self.caller.msg("As you're indoors, you find it hard to really evaluate the weather outside.")
            return
        else:
            self.caller.msg("You have to go in character to evaluate the weather.")
            return
        feed = feedparser.parse(weatherinfo)
        moonfeed = feedparser.parse(settings.MOON_PHASE)
        screenwidth = self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0]
        boxwidth = screenwidth/4
        feedout = ""
        season = ""
        wintersolstice = date(int(time.strftime("%Y")),12,21)
        springequinox = date(int(time.strftime("%Y")),3,21)
        summersolstice = date(int(time.strftime("%Y")),6,21)
        autumnequinox = date(int(time.strftime("%Y")),9,21)
        numbertoday = date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))
        moonout = ""
        for item in feed['entries']:
            feedout += item['title']
            feedout += re.sub('<[^<]+?>', '', item['summary'])
        for item in moonfeed['entries']:
            moonout += str(item['title'])
        feedout = str(feedout)
        if time.strftime("%b") in self.wintermonths:
            if time.strftime("%b") == "Mar":
                if int(time.strftime("%d")) >= 21:
                    season = "Spring"
                else:
                    season = "Winter"
            else:
                season = "Winter"
        elif time.strftime("%b") in self.springmonths:
            if time.strftime("%b") == "Jun":
                if int(time.strftime("%d")) >= 21:
                    season = "Summer"
                else:
                    season = "Spring"
            else:
                season = "Spring"
        elif time.strftime("%b") in self.summermonths:
            if time.strftime("%b") == "Sep":
                if int(time.strftime("%d")) >= 21:
                    season = "Autumn"
                else:
                    season = "Summer"
            else:
                season = "Summer"
        elif time.strftime("%b") in self.fallmonths:
            if time.strftime("%b") == "Dec":
                if int(time.strftime("%d")) >= 21:
                    season = "Winter"
                else:
                    season = "Autumn"
            else:
                season = "Autumn"
        if season == "Summer":
            nextwait = autumnequinox - numbertoday
            nextseason = "Autumn"
        elif season == "Autumn":
            nextwait = wintersolstice - numbertoday
            nextseason = "Winter"
        elif season == "Winter":
            nextwait = springequinox - numbertoday
            nextseason = "Spring"
        elif season == "Spring":
            nextwait = summersolstice - numbertoday
            nextseason = "Summer"
        weatherbox = ""
        moonstring = str(moonout).replace("a ","").replace("moon","").replace("quarter","half").title()
        atmosphere = re.search(r'.* and \d+\.?[0-9]? F',feedout).group(0)
        atmosphere = re.sub(r' and \d+\.?[0-9]? F','',atmosphere)
        temperature = re.search(r'\d+\.?[0-9]? F',feedout).group(0)
        windspeed = ""
        minspeed = ""
        maxspeed = ""
        try:
            windspeed = re.search(r'([0-9]+?\.?[0-9]? gusting to )?[0-9]+?\.?[0-9]? MPH',feedout).group(0)
            minspeed = re.search(r'[0-9]+?\.?[0-9]? gusting to ',windspeed).replace(" gusting to ","").group(0) + "-"
            maxspeed = re.search(r'[0-9]+?\.?[0-9]? MPH',windspeed).group(0)
            windchill = re.search('The wind chill is [0-9]+',feedout).group(0).replace("The wind chill is ","")
        except AttributeError:
            minspeed = ""
        weatherbox += "/" + "-" * ((boxwidth)/2 - 3) + "Weather" + "-" * (boxwidth/2 - 4) + "\\\n"
        weatherbox += "|| General Atmosphere: "  + atmosphere + " " * (boxwidth - len("| General Atmosphere: " +atmosphere)) + "||\n"
        weatherbox += "|| Temperature: " + temperature + " " * (boxwidth - len("| Temperature: " + temperature)) + "||\n"
        if windspeed != "":
            weatherbox += "|| Wind Speed: " + minspeed + maxspeed + " " * (boxwidth - len("| Wind Speed: " + minspeed + maxspeed)) + "||\n"
            weatherbox += "|| Wind Chill: " + windchill + " F" + " " * (boxwidth - len("| Wind Chill: " + windchill + " F")) + "||\n"
        weatherbox += "|| Phase of the Moon: " + moonstring + " " * (boxwidth - len("| Phase of the Moon" + moonstring)  - 2) + "||\n"
        weatherbox += "|| Season: " + season + " and " + str(nextwait.days) + " days until " + nextseason
        weatherbox += " " * (boxwidth - len("| Season: " + season + " and " + str(nextwait.days) + " days until " + nextseason)) + "||\n"
        weatherbox += "\\" + "-" * ((boxwidth) - 1) + "/"
        self.caller.msg(weatherbox)