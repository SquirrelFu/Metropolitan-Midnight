# -*- coding: utf-8 -*-
"""
Connection screen

Texts in this module will be shown to the user at login-time 

Evennia will look at global string variables (variables defined
at the "outermost" scope of this module and use it as the
connection screen  If there are more than one, Evennia will
randomize which one it displays 

The commands available to the user when the connection screen is shown
are defined in commands default_cmdsets UnloggedinCmdSet and the
screen is read and displayed by the unlogged-in "look" command 

"""

from django.conf import settings
from evennia import utils

CONNECTION_SCREEN = \
r"""


   _____          __                               __   __  __                 
  /     \   _____/  ||________  ____ ______   ____ ||  || ||__||/  ||______    ____  
 /  \ /  \_/ __ \   __\_  __ \/  _ \\____ \ /  _ \||  || ||  \   __\__  \  /    \ 
/    Y    \  ___/||  ||  ||  || \(  <_> )  ||_> >  <_> )  ||_||  ||||  ||  / __ \||   ||  \
\____||__  /\___  >__||  ||__||   \____/||   __/ \____/||____/__||||__|| (____  /___||  /
        \/     \/                   ||__||                             \/     \/ 
   _____   __     ___      __        __     __                                 
  /     \ ||__|| __|| _/____ ||__|| ____ ||  ||___/  ||_                               
 /  \ /  \||  ||/ __ ||/    \||  ||/ ___\||  ||  \   __\                              
/    Y    \  / /_/ ||   ||  \  / /_/  >   Y  \  ||                                
\____||__  /__\____ ||___||  /__\___  /||___||  /__||                                
        \/        \/    \/  /_____/      \/                                    


A Chronicles of Darkness game set in New York City 

To create a new account (Not a character, an account) please use, "create <name> <password>" 

To connect to an old account, please use, "connect <name> <password>"

To connect as a guest please use, "connect guest".

"""\