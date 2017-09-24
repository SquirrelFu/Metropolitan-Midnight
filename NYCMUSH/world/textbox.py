'''
Created on Jan 22, 2017

@author: CodeKitty
'''
from textwrap import wrap
import re
class TextBox(object):
    def __init__(self, header, text, section=False, color="444", width=80):
        self.header = header
        self.text = text
        self.width = width
        self.section = section
        self.colorcode = color
    def __str__(self):
        return self.Show()
    def SetHeader(self, header):
        self.header = header
    def SetBody(self, body):
        self.text = body
    def SetWidth(self, width):
        self.width = width
    def Show(self):
        text = self.text
        width = self.width
        color = self.colorcode
        outputstring = ""
        textspace = width - 2
        outputstring += self.Header()
        outputstring += "\n"
        wrappedtext = wrap(text,width)
        for text in wrappedtext:
            outputstring += "|" + color + "|||n" + text + " " * textspace + "|" + color + "|||n\n"
        return outputstring
    def Header(self):
        headerwidth = (self.width - len(self.header)) - 2
        color = self.colorcode
        if headerwidth%2 == 1:
            leftmargin = headerwidth/2
            rightmargin = leftmargin + 1
        else:
            leftmargin = headerwidth/2
            rightmargin = leftmargin
        if self.section:
            returnstring = "|" + color + "+"
        else:
            returnstring =  "|"+color+"/"
        returnstring += "-" * leftmargin +"|n"+self.header+"|"+color + "-" * rightmargin
        if self.section:
            returnstring += "+"
        else:
            returnstring += "\\"
        return returnstring
    def Footer(self):
        footerwidth = self.width - 2
        returnfooter = "|" + self.colorcode + "\\" + "-" * footerwidth + "/"
        return returnfooter
class StatBlock(TextBox):
    section = True
    def SetColumns(self, value):
        self.columns = value
    def __init__(self,header,*stats):
        if len(stats) > 0:
            self.fieldcolor = ""
            self.namecolor = ""
            if isinstance(stats[0], bool):
                self.section = stats[0]
                self.stats = stats[1:]
                if isinstance(self.stats[0],list):
                    self.stats = self.stats[0]
            elif isinstance(stats[0], list):
                self.stats = stats[0]
            else:
                self.stats = stats
        else:
            self.stats = stats
        super(StatBlock, self).__init__(header,"",self.section,"444",78)
        self.headerrows = -1
        self.columns = 3
    def FieldColor(self, colorin):
        self.fieldcolor = colorin
    def NameColor(self, colorin):
        self.namecolor = colorin
    def ClearTextColors(self):
        self.fieldcolor = ""
        self.namecolor = ""
    def Show(self):
        columns = self.columns
        stats = self.stats
        width = self.width
        color = self.colorcode
        outputstring = ""
        textspace = int(width)-2
        cellspace = textspace/3
        extraspace = textspace - (cellspace*3)
        outputstring += self.Header()
        outputstring += "\n"
        column = 0
        blockstring = ""
        block_unformatted =""
        headercount = 0
        spacecharacter = " "
        startcharacter = "|" + color + "|||n"
        endcharacter = "|"+color+"|||n\n"
        for x in stats:
            if x == "":
                continue
            if headercount == self.headerrows or (x == stats[0] and self.headerrows != -1):
                spacecharacter = "|"+color+"-" + "|n"
                endcharacter = "|"+color + "+|n\n"
                startcharacter = "|"+color+"+|n"
                headercount = 0
            if x.count(",") == 1:
                if column == 0:
                    block_unformatted += "|" + x.split(",")[0] +": "+ x.split(",")[1]
                    blockstring += startcharacter + x.split(",")[0] + ": " + x.split(",")[1] + spacecharacter * (cellspace - len(block_unformatted))
                    block_unformatted += " " * (cellspace - len(block_unformatted))
                    column += 1
                    if columns == column:
                        block_reserve = ""
                        if len(block_unformatted) > textspace:
                            block_reserve = wrap(blockstring,textspace)
                            blockstring += block_reserve[0]
                        blockstring += spacecharacter * (((width - 2) - len(block_unformatted)+extraspace)) + endcharacter
                        if len(block_unformatted) > textspace:
                            blockstring += block_reserve[1]+" " * (((width - 2) - len(block_unformatted)+extraspace)) + endcharacter
                        outputstring += blockstring
                        block_unformatted = ""
                        blockstring = ""
                        block_reserve = ""
                        column = 0
                        spacecharacter= " "
                        endcharacter = "|" + color + "|||n\n"
                        startcharacter = "|" + color + "|||n"
                        headercount += 1
                elif column == (columns - 1):
                    block_unformatted += x.split(",")[0] + ": "+ x.split(",")[1]
                    blockstring += x.split(",")[0] + ": " + x.split(",")[1]
                    if x != stats[len(stats)-1]:
                        blockstring += " " * (((width - 2) - len(block_unformatted)+extraspace)) + endcharacter
                        column = 0
                        outputstring += blockstring
                        blockstring = ""
                        block_unformatted = ""
                        headercount += 1
                        spacecharacter= " "
                        endcharacter = "|" + color + "|||n\n"
                        startcharacter = "|" + color + "|||n"
                else:
                    block_unformatted += x.split(",")[0] + ": " + x.split(",")[1]
                    blockstring += x.split(",")[0] + ": " + x.split(",")[1] + spacecharacter * ((cellspace*2) - len(block_unformatted))
                    block_unformatted += " " * ((cellspace*2) - len(block_unformatted))
                    column += 1
                if x == stats[len(stats)-1] or len(block_unformatted) > textspace + 1:
                    block_reserve = ""
                    if len(block_unformatted) > textspace + 1:
                        block_reserve = wrap(blockstring,textspace)
                        blockstring = block_reserve[0]
                    blockstring += spacecharacter * (((width - 1) - len(block_unformatted))) + endcharacter
                    if len(block_unformatted) > textspace + 1:
                        blockstring += block_reserve[1]+" " * ((textspace - len(block_unformatted))) + endcharacter
                    outputstring += blockstring
                    block_unformatted = ""
                    blockstring = ""
                    block_reserve = ""
                    column = 0
                    spacecharacter= " "
                    endcharacter = "|" + color + "|||n\n"
                    startcharacter = "|" + color + "|||n"
                    headercount += 1
            elif x.count(",") == 0:
                if column == 0:
                    block_unformatted += "|" + re.sub(r'\|[0-9][0-9][0-9]','',x).replace(r"|n","")
                    blockstring += startcharacter + x + spacecharacter * (cellspace - len(block_unformatted))
                    block_unformatted += " " * (cellspace - len(block_unformatted))
                    column += 1
                    if column == (columns):
                        block_reserve = ""
                        if len(block_unformatted) > textspace:
                            block_reserve = wrap(blockstring,textspace)
                            blockstring = block_reserve[0]
                        blockstring += spacecharacter * (((width - 1) - len(block_unformatted))) + endcharacter
                        if len(block_unformatted) > textspace:
                            blockstring += block_reserve[1]+ spacecharacter * ((textspace - len(block_unformatted))) + endcharacter
                        outputstring += blockstring
                        block_unformatted = ""
                        blockstring = ""
                        block_reserve = ""
                        column = 0
                        spacecharacter= " "
                        endcharacter = "|" + color + "|||n\n"
                        startcharacter = "|" + color + "|||n"
                        headercount += 1
                        if x == stats[len(stats) - 1]:
                            return outputstring
                elif column == (columns - 1) and (not("\n" in blockstring)):
                    if len(x) + len(block_unformatted) > textspace:
                        remainingspace = textspace - len(block_unformatted)
                        wrapitem = wrap(x,remainingspace)
                        blockstring += wrapitem[0] + spacecharacter * (textspace - (len(wrapitem[0]) + len(block_unformatted)) + 1)
                        blockstring += endcharacter
                        block_unformatted += wrapitem[0] + spacecharacter * (textspace - (len(wrapitem[0]) + len(block_unformatted)) + 1)
                        blockstring += startcharacter + spacecharacter * ((cellspace*2) - 1) + wrapitem[1]
                        block_unformatted += startcharacter + spacecharacter * ((cellspace*2) - 1) + wrapitem[1]
                        blockstring += spacecharacter * (cellspace - len(wrapitem[1])+2)
                        blockstring += endcharacter
                        outputstring += blockstring
                        block_unformatted = ""
                        blockstring = ""
                        endcharacter = "|" + color + "|||n\n"
                        startcharacter = "|" + color +"|||n"
                        headercount += 1
                        spacecharacter = " "
                        column = 0
                    elif x != stats[len(stats)-1]:
                        block_unformatted += re.sub(r'\|[0-9][0-9][0-9]','',x).replace(r"|n","")
                        blockstring += x
                        blockstring += spacecharacter * (((width - 1) - len(block_unformatted))) + endcharacter
                        column = 0
                        outputstring += blockstring
                        blockstring = ""
                        block_unformatted = ""
                        spacecharacter= " "
                        endcharacter = "|" + color + "|||n\n"
                        startcharacter = "|" + color + "|||n"
                        headercount += 1
                else:
                    block_unformatted += re.sub(r'\|[0-9][0-9][0-9]','',x).replace(r"|n","")
                    blockstring += x + spacecharacter * ((cellspace*2) - len(block_unformatted))
                    block_unformatted += " " * ((cellspace*2) - len(block_unformatted))
                    column += 1
                if x == stats[len(stats)-1] or len(block_unformatted) > textspace:
                    block_reserve = ""
                    if len(block_unformatted) > textspace + 1:
                        block_reserve = wrap(blockstring,textspace)
                        blockstring = block_reserve[0]
                        blockstring += spacecharacter * (((width - 1) - len(block_unformatted))) + endcharacter
                        blockstring += block_reserve[1]+" " * ((textspace - len(block_unformatted))) + endcharacter
                    elif not x in blockstring:
                        blockstring += x + spacecharacter * (textspace - (len(block_unformatted) + len(re.sub(r'\|[0-9][0-9][0-9]','',x).replace(r"|n","")))+1) + endcharacter
                    else:
                        blockstring += spacecharacter * (textspace - len(block_unformatted) + 1) + endcharacter
                    outputstring += blockstring
                    block_unformatted = ""
                    blockstring = ""
                    block_reserve = ""
                    column = 0
                    spacecharacter= " "
                    endcharacter = "|" + color + "|||n\n"
                    startcharacter = "|" + color + "|||n"
                    headercount += 1
            elif x.count(",") > 1:
                block_unformatted += "|" + x.split(",")[0]
                blockstring += "|" + color + "|||n" + x.split(",")[0] + " ("
                for y in x.split(","):
                    if y != x.split(",")[len(x.split(",")) - 1] and y != x.split(",")[0]:
                        blockstring += y + ", "
                        block_unformatted += y + ", "
                    elif y != x.split(",")[0]:
                        blockstring += y
                        block_unformatted += y
                blockstring += ")"
                block_unformatted += ")"
                if len(block_unformatted) > textspace:
                    block_reserve = wrap(blockstring,textspace)
                    outputstring += block_reserve[0]
                if len(block_unformatted) > textspace:
                    outputstring += block_reserve[1] + " " * (textspace - len(block_reserve[1]))
                else:
                    blockstring += " " * (textspace - len(block_unformatted) - 1) + "|" + color + "|||n\n"
                block_unformatted = ""
                block_reserve = ""
                outputstring += blockstring
                column = 0
        return outputstring
    def SetColor(self, value):
        self.colorcode = value
    def SetWidth(self, value):
        self.width = value
    def SetHeaderInterval(self, value):
        self.headerrows = value
