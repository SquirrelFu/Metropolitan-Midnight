'''
Created on Jan 23, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from textwrap import wrap
class MultiDescCommand(default_cmds.MuxCommand):
    key = "+desc"
    
    def func(self):
        args = self.args
        arglist = self.arglist
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        try:
            screenwidth = self.caller.player.sessions.get()[0].protocol_flags['SCREENWIDTH'][0]
        except IndexError:
            screenwidth = 78
        displaywidth = screenwidth/4
        padwidth = displaywidth/2
        cellwidth = padwidth/2
        if switches:
            if switches[0] == "set":
                if len(arglist) == 1:
                    for desctitle in self.caller.db.desclist.keys():
                        if desctitle.lower() == arglist[0].lower():
                            self.caller.db.desc = self.caller.db.desclist[desctitle]
                            self.caller.msg("Description set to ,\""+"\"")
                            return
                    self.caller.msg("You don't have that description stored.")
                    return
                else:
                    finaldesc = ""
                    for desctitle in self.caller.db.desclist.keys():
                        for item in arglist:
                            if desctitle.lower() == item.lower():
                                if finaldesc == "":
                                    finaldesc += self.caller.db.desclist[desctitle]
                                else:
                                    finaldesc += " " + self.caller.db.desclist[desctitle]
                self.caller.db.desc = finaldesc
                self.caller.msg("Description set to ,\""+"\"")
                    
            if switches[0] == "add":
                if lhs and rhs:
                    self.caller.db.desclist[lhs] = rhs
                    self.caller.msg("Description stored under the name, "+lhs)
            elif switches[0] == "del":
                try:
                    del self.caller.db.desclist[lhs]
                    self.caller.msg(lhs + " deleted")
                except KeyError:
                    try:
                        del self.caller.db.desclist[lhs.title()]
                        self.caller.msg(lhs.title() + " deleted")
                    except KeyError:
                        self.caller.msg("You don't have that description saved!")
            elif switches[0] == "fae":
                if len(arglist) == 1:
                    for desctitle in self.caller.db.desclist.keys():
                        if desctitle.lower() == arglist[0].lower():
                            self.caller.db.lingdesc = self.caller.db.desclist[desctitle]
                            self.caller.msg("Mask description set to ,\""+"\"")
                            return
                    self.caller.msg("You don't have that description stored.")
                    return
                else:
                    finaldesc = ""
                    for desctitle in self.caller.db.desclist.keys():
                        for item in arglist:
                            if desctitle.lower() == item.lower():
                                if finaldesc == "":
                                    finaldesc += self.caller.db.desclist[desctitle]
                                else:
                                    finaldesc += " " + self.caller.db.desclist[desctitle]
                    self.caller.db.lingdesc = finaldesc
                    self.caller.msg("Mien description set to ,\""+"\"")
                
        else:
            if args:
                for key in self.caller.db.desclist.keys():
                        if key.lower() == args.lower():
                            rightwidth = (padwidth - (len(args)/2))
                            if len(args) % 2 == 1:
                                leftwidth = rightwidth - 2
                            else:
                                leftwidth = rightwidth - 1
                            desckeys = "/" + "-" * leftwidth + key + "-" * rightwidth + "\\\n"
                            wrapdesc = wrap(self.caller.db.desclist[key])
                            for thing in wrapdesc:
                                if thing == wrapdesc[len(wrapdesc) - 1]:
                                    desckeys += "||" + thing + " " * (displaywidth - len("|"+thing) - 1) +"||\n"
                            if self.caller.player.sessions.get()[0].protocol_flags['MXP'] and self.caller.db.template != "Changeling":
                                desckeys += "\\" + "-" * (padwidth - 8) + "|lc+desc/set "+args+"|ltSet Description|le" + "-" * (padwidth - 8) + "/"
                            elif self.caller.player.sessions.get()[0].protocol_flags['MXP'] and self.caller.db.template == "Changeling":
                                desckeys += "\\" + "-" * (cellwidth - 5) + "|lc+desc/set "+args+"|ltSet as Mask|le" + "-" * (cellwidth - 6)
                                desckeys += "-" * (cellwidth - 5) + "|lc+desc/fae " + args + "|ltSet as Mien|le" + "-" *  (cellwidth - 5) + "/"
                            else:
                                desckeys += "\\" + "-" * (displaywidth - 2) + "/"
                            self.caller.msg(desckeys)
            elif len(self.caller.db.desclist.keys()) > 0:
                rightwidth = (padwidth - (len("Descriptions")/2))
                leftwidth = rightwidth - 1
                desckeys = "/" + "-" * leftwidth + "Descriptions" + "-" * rightwidth + "\\\n"
                keycount = 0
                unformatted = ""
                for key in self.caller.db.desclist.keys():
                    if keycount == 0:
                        desckeys += "|||lc +desc " + key + "|lt" +key + "|le" + " " * (cellwidth - len("| " + key))
                        unformatted += "| " + key + " " * (cellwidth - len("| " + key))
                    elif keycount != 3:
                        desckeys += "|lc +desc "+key +"|lt"+key + "|le" +" " * ((cellwidth*(keycount+1)) - len(unformatted))
                        unformatted += key + " " * ((cellwidth*(keycount+1)) - len(unformatted))
                    else:
                        desckeys += key + " " * (displaywidth - len(unformatted) - 5) + "||\n"
                        keycount = 0
                        unformatted += key + " " * (displaywidth - len(unformatted + "|") - 1)
                    keycount += 1
                    if key == self.caller.db.desclist.keys()[len(self.caller.db.desclist.keys()) - 1] and keycount != 0:
                        desckeys += " " * (displaywidth - len(unformatted)) + "||\n"
                desckeys += "\\" + "-" * (displaywidth - 2) +"/"
                self.caller.msg(desckeys)
            else:
                self.caller.msg("You have no descriptions stored.")
                