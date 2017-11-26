'''
Created on Jan 29, 2017

@author: CodeKitty
'''
from evennia import default_cmds
from evennia.utils import search
from string import capwords
import re
class ManageXP(default_cmds.MuxCommand):
    """
    Used to manage experience points. Players can check their own XP, while admins can spend XP for players.
    
    Usage:
        +xp <Character> Used to view a given character's beat log, admin only.
        +xp/spend <Amount>=<Reason> Spend <Amount> whole experiences for the reason given.
        +xp/award <Amount>=<Reason> Similar to the previous, except it adds beats instead of taking away whole experiences.
    """
    key = "+xp"
    locks = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        lhs = self.lhs
        rhs = self.rhs
        switches = self.switches
        if not switches:
            try:
                targetchar = search.objects(lhs)[0]
                beatstring = "Showing beats for: " + targetchar.name + "\n"+ targetchar.ShowBeats()
                self.caller.msg(beatstring)
                return
            except IndexError:
                self.caller.msg("Invalid character, cannot view their XP.")
                return
        if switches[0].lower() == "spend":
            try:
                targetchar = search.objects(lhs)[0]
                if rhs:
                    try:
                        if (targetchar.db.experience)/5 >= int(rhs.split("/")[0]):
                            targetchar.db.experience -= int(rhs.split("/")[0]) * 5
                            self.caller.msg("You have spent " + rhs + " of experience on " + targetchar.name + " for " + rhs.split("/")[1])
                            return
                    except ValueError:
                        self.caller.msg("Invalid experience point value to spend.")
                        return
                    except IndexError:
                        self.caller.msg("You need to enter both an experience point value to spend, and a reason.")
                        return
                else:
                    self.caller.msg("You need to input a value to spend a character's XP!")
                    return
            except IndexError:
                self.caller.msg("Invalid character.")
                return
        elif switches[0].lower() == "award":
            try:
                targetchar = search.objects(lhs)[0]
                if rhs:
                    self.caller.msg("You have added a beat to " + targetchar.name + " for " + rhs)
                    self.caller.AddBeat("Staff Awarded",rhs)
                    return
                else:
                    self.caller.msg("You need to input a reason to award a character  a beat!")
                    return
            except IndexError:
                self.caller.msg("Invalid character.")
                return
        elif switches[0].lower() == "remove":
            try:
                targetchar = search.objects(lhs)[0]
                if rhs:
                    for beat in targetchar.db.beatlog:
                        beatsearch = re.search('for .*$',beat).group(0)
                        if rhs.lower() == beatsearch.lower():
                            self.caller.msg("You have removed a beat from " + targetchar.name + " initially awarded for " + beatsearch.replace("for ",""))
                            targetchar.db.beatlog.remove(beat)
                            return
            except IndexError:
                self.caller.msg("Invalid player to remove a beat from.")
                return         
class StatOther(default_cmds.MuxCommand):
    """
    Pstat, short for player stat, is used to change the statistics of other characters.
    Usage:
        +pstat/template <Character>=<Template> Sets a character's template, but also resets a lot of things about them too.
        +pstat/merit <Character>/<Merit name>=<Rating> Sets a merit of the given name to the given rating.
        +pstat/skill <Character>/<Skill>=<Rating> Sets a skill on a character.
        +pstat/attribute <Character>/<Attribute>=<Rating> Sets an attribute on a character.
        +pstat/xsplat <Character>=<xplsat> Sets Clan, Auspice, Seeming, Path, Family, Incarnation, 
        Compact or Conspiracy, Lineage, or Calling as appropriate to the template in question.
        +pstat/ysplat <Character>=<ysplat> Sets Covenant, Tribe, Court, Order, Hunger, Agenda, Refinement, or Guild as appropriate
        to the template in question.
        +pstat/zsplat <Character>=<zsplat> Sets bloodline, lodge, entitlement, legacy, or role as appropriate to the template
        in question.
        +pstat/demeanor <Character>=<New demeanor> Used to set the virtue, mask, blood, and elpis archetypes due to their similarity
        to the World of Darkness "Demeanor" system.
        +pstat/nature <Character>=<New nature> Used to set the vice, dirge, bone, and torment archetypes due to their similarity
        to the World of Darkness, "Nature" system.
        +pstat/spec <Character>/<Skill>=<Specialty> Used to set a specialty on a character. Like players setting specialty on their
        characters, including an asterisk in the setting code will remove that specialty if it is present.
    """
    key = "+pstat"
    locks = "cmd:pperm(Wizards)"
    help_category="Admin"
    def func(self):
        args = self.args
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        arglist = self.arglist
        try:
            target = search.objects(lhs.split("/")[0])[0]
            lhs = lhs.split("/")[1]
        except IndexError:
            try:
                lhs = search.objects(lhs)[0].name
                target = search.objects(lhs.split("/")[0])[0]
            except IndexError:
                self.caller.msg("That's not a valid character to modify!")
                return
            
        template = target.db.template
        if switches[0].lower() == "demeanor":
            target.db.demeanor = rhs
            self.caller.msg(target.db.demeanorname + " on " + target.name + " set to " + rhs)
            target.msg(self.caller.name + " just set your " + target.db.demeanorname + " to " + rhs )
            return
        if switches[0].lower() == "nature":
            target.db.nature = rhs
            self.caller.msg(target.db.naturename + " on " + target.name + " set to " + rhs)
            if target.has_player:
                target.msg(self.caller.name + " just set your " + target.db.naturename + " to " + rhs )
        if switches[0] == "template":
            templatevar = self.SetTemplate(target,rhs)
            if templatevar == False:
                self.caller.msg("Invalid template to set on " + target.name)
                return
        if switches[0] == "merit":
            if lhs == target.name:
                self.caller.msg("You have to select a merit to add to the character.")
                return
            meritscript = search.scripts('MeritHandler')[0]
            overlist = []
            for x in meritscript.db.mental:
                overlist.append(x)
            for x in meritscript.db.physical:
                overlist.append(x)
            for x in meritscript.db.social:
                overlist.append(x)
            for x in meritscript.db.fighting:
                overlist.append(x)
            for x in meritscript.db.supernatural:
                overlist.append(x)
            if template == "Mortal":
                for x in meritscript.db.atariya:
                    overlist.append(x)
                for x in meritscript.db.dreamer:
                    overlist.append(x)
                for x in meritscript.db.infected:
                    overlist.append(x)
                for x in meritscript.db.plain:
                    overlist.append(x)
                for x in meritscript.db.lostboy:
                    overlist.append(x)
                for x in meritscript.db.psyvamp:
                    overlist.append(x)
            if template == "Vampire":
                for x in meritscript.db.vampire:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Werewolf":
                for x in meritscript.db.werewolf:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Mage":
                for x in meritscript.db.mage:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Changeling":
                for x in meritscript.db.changeling:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Promethean":
                for x in meritscript.db.promethean:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Beast":
                for x in meritscript.db.beast:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Hunter":
                for x in meritscript.db.hunter:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Demon":
                for x in meritscript.db.demon:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Mummy":
                for x in meritscript.db.mummy:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Ghoul":
                for x in meritscript.db.ghoul:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Wolfblood":
                for x in meritscript.db.wolfblood:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Fae-Touched":
                for x in meritscript.db.faetouched:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            if template == "Proximus":
                for x in meritscript.db.sleepwalker:
                    for y in overlist:
                        if x[0] == y[0]:
                            overlist.remove(y)
                    overlist.append(x)
            for merit in overlist:
                    if merit[0].lower() == lhs.lower():
                        lhs = merit[0]
            if int(rhs) > 0:
                merittotal = 0
                if meritscript.MeetsPrereqs(target,lhs,rhs):
                    for scoremerit in target.db.meritlist:
                        merittotal += int(scoremerit[1])
                    if merittotal >= target.db.meritlimit:
                        self.caller.msg("You can't add that many merit dots to "+target.name + "|")
                        return
                    target.AddMerit(lhs,rhs)
                    self.caller.msg(lhs+" merit added to " + target.name + " at "+str(rhs)+" dots.")
                    if target.has_account:
                        target.msg(self.caller.name + " has added the " + lhs + " merit to you at " + str(rhs) + " dots.")
                    target.Update()
                else:
                    self.caller.msg("Invalid merit")
            else:
                for merit in target.db.meritlist:
                    if lhs.lower() == merit[0].lower():
                        self.caller.msg(merit[0]+" removed from " + target.name)
                        target.RemMerit(merit[0])
                        if target.has_account:
                            target.msg(self.caller.name + " has removed the " + lhs + " merit from you.")
                        target.Update()
                        return
                self.caller.msg("You don't have that merit to remove!")
                return
        elif switches[0] == "skill":
            if lhs == target.name:
                self.caller.msg("You have to select a skill to raise, lower, or remove.")
                return
            if args:
                for skill in target.db.physskills.keys():
                    if lhs:
                        if skill.lower() == lhs.lower():
                            if rhs:
                                try:
                                    target.db.physskills[skill] = int(rhs)
                                    self.caller.msg(skill + " set to "+rhs + " on " + target.name)
                                    if target.has_account:
                                        target.msg(self.caller.name + " has set your " + lhs + "skill to " + rhs)
                                    target.Update()
                                    return
                                except ValueError:
                                    self.caller.msg("Invalid value to set for "+ skill)
                                    return
                            else:
                                self.caller.msg("Please enter a value to set "+ skill + " to.")
                                return
                for skill in target.db.mentskills.keys():
                    if lhs:
                        if skill.lower() == lhs.lower():
                            if rhs:
                                try:
                                    target.db.mentskills[skill] = int(self.rhs)
                                    self.caller.msg(skill + " set to "+self.rhs + " on " + target.name)
                                    if target.has_account:
                                        target.msg(self.caller.name + " has set your " + lhs + "skill to " + rhs)
                                    target.Update()
                                    return
                                except ValueError:
                                    self.caller.msg("Invalid value to set for "+ skill)
                                    return
                            else:
                                self.caller.msg("Please enter a value to set "+ skill + " to.")
                                return
                for skill in target.db.socskills.keys():
                    if lhs:
                        if skill.lower() == lhs.lower():
                            if rhs:
                                try:
                                    target.db.socskills[skill] = int(rhs)
                                    self.caller.msg(skill + " set to "+ rhs + " on " + target.name)
                                    if target.has_account:
                                        target.msg(self.caller.name + " has set your " + lhs + "skill to " + rhs)
                                    target.Update()
                                    return
                                except ValueError:
                                    self.caller.msg("Invalid value to set for "+ skill)
                                    return
                            else:
                                self.caller.msg("Please enter a value to set "+ skill + " to.")
                                return
                self.caller.msg("Invalid skill.")
                return
            else:
                self.caller.msg("Please enter a skill to set.")
                return
        elif switches[0] == "attribute":
            if lhs == target.name:
                self.caller.msg("You have to select an attribute to raise, lower, or remove.")
                return
            if args:
                for attrib in target.db.attributes.keys():
                    if lhs:
                        if attrib.lower() == lhs.lower():
                            if self.rhs:
                                try:
                                    target.db.attributes[attrib] = int(rhs)
                                    target.db.attribbase[attrib] = int(rhs)
                                    self.caller.msg(attrib + " set to "+rhs + " on " + target.name)
                                    if target.has_account:
                                        target.msg(self.caller.name + " has set your " + lhs + "attribute to " + rhs)
                                    target.Update()
                                    return
                                except ValueError:
                                    self.caller.msg("Invalid value to set for " + attrib)
                                    return
                            else:
                                self.caller.msg("Please enter a value to set "+ attrib + " to.")
                                return
                self.caller.msg("Invalid attribute.")
                return
            else:
                self.caller.msg("Please select an attribute to set.")
                return
        elif switches[0].lower() == "xsplat":
            discscript = search.scripts('VampireStats')[0]
            beastscript = search.scripts('BeastStats')[0]
            lingscript = search.scripts('ChangelingStats')[0]
            demscript = search.scripts('DemonStats')[0]
            promscript = search.scripts('PrometheanStats')[0]
            huntscript = search.scripts('HunterStats')[0]
            magescript = search.scripts('MageStats')[0]
            mumscript = search.scripts('MummyStats')[0]
            wolfscript = search.scripts('WerewolfStats')[0]
            if template == "Vampire":
                for clan in discscript.db.clans:
                    if clan.lower() == arglist[0].lower():
                        target.db.xsplat = clan
                        self.caller.msg(target.name + " has had their clan set to " + clan)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your clan to " + clan)
                        return
                self.caller.msg("Invalid clan.")
            if template == "Beast":
                for family in beastscript.db.families:
                    if family.lower() == arglist[0].lower():
                        target.db.xsplat = family
                        self.caller.msg(target.name + " has had their family set to "+ family)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your family to " + family)
                self.caller.msg("Invalid family.")
                return
            if template == "Changeling":
                for seem in lingscript.db.seemings:
                    if seem.lower() == arglist[0].lower():
                        target.db.xsplat = seem
                        self.caller.msg(target.name + " has had their seeming set to " + seem)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your seeming to " + seem)
                        return
                self.caller.msg("Invalid seeming.")
                return
            if template == "Demon":
                for form in demscript.db.incarnations:
                    if form.lower() == arglist[0].lower():
                        target.db.xsplat = form
                        self.caller.msg(target.name + " has had their incarnation set to " + form)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your incarnation to " + form)
                        return
                self.caller.msg("Invalid incarnation.")
                return
            if template == "Hunter":
                for com in huntscript.db.compacts:
                    if com.lower() == args.lower():
                        target.db.xsplat = com
                        self.caller.msg(target.name + " has had their faction set to the compact " + com)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your faction to the compact " + com)
                        return
                for cons in huntscript.db.conspiracies:
                    if cons.lower() == args.lower():
                        target.db.xsplat = cons
                        self.caller.msg(target.name + " has had their faction set to the conspiracy " + cons)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your faction to the conspiracy " + cons)
                        return
                self.caller.msg("Invalid compact or conspiracy")
                return
            if template == "Mage":
                for path in magescript.db.paths:
                    if path.lower() == arglist[0].lower():
                        target.db.xsplat = path
                        if target.has_account:
                            target.msg(self.caller.name + " has set your path to " + path)
                        self.caller.msg(target.name + " has had their path set to " + path)
                        return
                self.caller.msg("Invalid path")
            if template == "Mummy":
                for dec in mumscript.db.decrees:
                    if dec.lower() == arglist[0].lower():
                        target.db.xsplat = dec
                        if target.has_account:
                            target.msg(self.caller.name + " has set your decree to " + dec)
                        self.caller.msg(target.name + " has had their decree set to " + dec)
                        return
                self.caller.msg("Invalid decree.")
                return
            if template == "Promethean":
                for lin in promscript.db.lineages:
                    if lin.lower() == arglist[0].lower():
                        target.db.xsplat = lin
                        if target.has_account:
                            target.msg(self.caller.name + " has set your lineage to " + lin)
                        self.caller.msg(target.name + " has had their lineage set to "  + lin)
                        return
                self.caller.msg("Invalid lineage.")
                return
            if template == "Werewolf":
                for aus in wolfscript.db.auspices:
                    if aus.lower() == arglist[0].lower():
                        target.db.xsplat = aus
                        if target.has_account:
                            target.msg(self.caller.name + " has set your auspice to " + aus)
                        self.caller.msg(target.name + " has had their auspice set to " + aus)
                        return
                self.caller.msg("Invalid auspice.")
        elif switches[0].lower() == "ysplat":
            discscript = search.scripts('VampireStats')[0]
            beastscript = search.scripts('BeastStats')[0]
            lingscript = search.scripts('ChangelingStats')[0]
            demscript = search.scripts('DemonStats')[0]
            promscript = search.scripts('PrometheanStats')[0]
            huntscript = search.scripts('HunterStats')[0]
            magescript = search.scripts('MageStats')[0]
            mumscript = search.scripts('MummyStats')[0]
            wolfscript = search.scripts('WerewolfStats')[0]
            if template == "Vampire":
                for cov in discscript.db.covenants:
                    if cov.lower() == args.lower():
                        target.db.ysplat = cov
                        self.caller.msg(target.name + " has had their covenant set to " + cov)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your covenant to " + cov)
                        return
                self.caller.msg("Invalid covenant.")
            if template == "Beast":
                for hun in beastscript.db.hungers:
                    if hun.lower() == arglist[0].lower():
                        target.db.ysplat = hun
                        self.caller.msg(target.name + " has had their hunger set to " + hun)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your hunger to " + hun)
                        return
                self.caller.msg("Invalid hunger.")
                return
            if template == "Changeling":
                if arglist[0].lower() == "seelie" or arglist[0].lower() == "unseelie":
                    target.db.ysplat = arglist[0].title()
                    self.caller.msg(target.name + " has had their court set to " + arglist[0].title())
                    if target.has_account:
                        target.msg(self.caller.name + " has set your court to " + arglist[0].title())
                    return
                self.caller.msg("Invalid court.")
                return
            if template == "Demon":
                for agen in demscript.db.agendas:
                    if agen.lower() == arglist[0].lower():
                        target.db.ysplat = agen
                        self.caller.msg(target.name + " has had their agenda set to " + agen)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your agenda to " + agen)
                        return
                self.caller.msg("Invalid agenda.")
                return
            if template == "Promethean":
                ref = promscript.GetRefinement(arglist[0])
                if ref != False:
                    target.db.ysplat = ref
                    self.caller.msg(target.name + " has had their refinement set to " + ref)
                    if target.has_account:
                        target.msg(self.caller.name + " has set your refinement to " + ref)
                    return
                self.caller.msg("Invalid refinement.")
                return
            if template == "Mage":
                for order in magescript.db.orders:
                    if order.lower() == args.lower():
                        target.db.ysplat = order
                        self.caller.msg(target.name + " has had their order set to " + order)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your order to " + order)
                        return
                self.caller.msg("Invalid order.")
                return
            if template == "Mummy":
                for guild in mumscript.db.guilds:
                    if guild.lower() == arglist[0].lower():
                        target.db.ysplat = guild
                        self.caller.msg(target.name + " has had their guild set to " + guild)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your guild to " + guild)
                        return
                self.caller.msg("Invalid guild.")
                return
            if template == "Werewolf":
                for tribe in wolfscript.db.tribes:
                    if tribe.lower() == args.lower():
                        target.db.ysplat = tribe
                        self.caller.msg(target.name + " has had their tribe set to " + tribe)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your tribe to " + tribe)
                        return
                self.caller.msg("Invalid tribe.")
                return
        elif switches[0].lower() == "zsplat":
            discscript = search.scripts('VampireStats')[0]
            lingscript = search.scripts('ChangelingStats')[0]
            promscript = search.scripts('PrometheanStats')[0]
            magescript = search.scripts('MageStats')[0]
            wolfscript = search.scripts('WerewolfStats')[0]
            if template == "Changeling":
                for title in lingscript.db.entitlements:
                    if title.lower() == args.lower():
                        target.db.zsplat = title
                        self.caller.msg(target.name + " has had their entitlement set to " + title)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your entitlement to " + title)
                        return
                self.caller.msg("Invalid entitlement.")
                return
            if template == "Mage":
                for leg in magescript.db.legacies:
                    if leg.lower() == args.lower():
                        target.db.zsplat = leg
                        self.caller.msg(target.name + " has had their legacy set to " + leg)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your legacy to " + leg)
                        return
                self.caller.msg("Invalid legacy.")
                return
            if template == "Promethean":
                for role in promscript.db.roles:
                    for subrole in role:
                        if subrole == arglist[0].lower():
                            target.db.zsplat = subrole
                            if target.has_account:
                                target.msg(self.caller.name + " has set your role to " + subrole)
                            self.caller.msg(target.name + " has had their role set to " + subrole + " in the " + target.db.ysplat + " refinement.")
                            return
                self.caller.msg("Invalid role.")
                return
            if template == "Vampire":
                for line in discscript.db.bloodlines:
                    if line.lower() == args.lower():
                        target.db.zsplat = line
                        self.caller.msg(target.name + " has had their bloodline set to " + line)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your bloodline to " + line)
                        return
                self.caller.msg("Invalid bloodline")
                return
            if template == "Werewolf":
                for lodge in wolfscript.db.lodges:
                    if lodge.lower() == args.lower():
                        target.db.zsplat = lodge
                        self.caller.msg(target.name + " has had their lodge set to " + lodge)
                        if target.has_account:
                            target.msg(self.caller.name + " has set your lodge to " + lodge)
                        return
                self.caller.msg("Invalid lodge.")
                return
        elif switches[0].lower() == "powers":
            discscript = search.scripts('VampireStats')[0]
            beastscript = search.scripts('BeastStats')[0]
            lingscript = search.scripts('ChangelingStats')[0]
            demscript = search.scripts('DemonStats')[0]
            promscript = search.scripts('PrometheanStats')[0]
            huntscript = search.scripts('HunterStats')[0]
            magescript = search.scripts('MageStats')[0]
            mumscript = search.scripts('MummyStats')[0]
            wolfscript = search.scripts('WerewolfStats')[0]
            powers = target.db.powers
            if template == "Wolfblood":
                tells = wolfscript.db.tells
                for fur in tells:
                    if fur[0].lower() == args.lower():
                        if len(target.db.powers) == 0:
                            target.db.powers[fur[0]] = ''
                            self.caller.msg(fur[0] +" tell added.")
                            return
                        elif len(target.db.powers) == 1:
                            for merit in target.db.meritlist:
                                if merit[0] == "Tell":
                                    target.db.powers[fur[0]] = ''
                                    target.msg(fur[0] + " tell added.")
                                    return
                        elif len(self.caller.db.powers) >= 2:
                            self.caller.msg(target.name + " can't have that many tells.")
                            return
                self.caller.msg("Invalid tell.")
                return
            return
            if template == "Beast":
                rawr = beastscript.db.atavisms
                #Library of atavisms in the chargen room.
                eek = beastscript.db.nightmares
                #Library of nightmares in the chargen room.
                for smash in rawr:
                #Iterate through the library of atavisms
                    if smash[0].lower() == self.args.lower():
                    #If the atavism is found in the library, set the relevant dictionary entry to string zero, as it has no value attached.
                        try:
                            testvar = powers[smash[0]]
                        except KeyError:
                        #Check and see if the key exists. If not, add the power.
                            powers[smash[0]] = "0"
                            self.caller.msg(smash[0] + " added to " + target.name)
                for zoinks in eek:
                #Iterate through the library of nightmares.
                    if zoinks[0] == self.arglist[0]:
                    #If the nightmare is found, add it to the caller's database of techniques.
                        target.AddTech(zoinks[0])
                        self.caller.msg(zoinks[0] + " added to " + target.name)
            if template == "Changeling" or template == "Fae-Touched":
                kyubey = lingscript
                powers = target.db.powers
                for power in kyubey:
                    if power[0].lower() == arglist[0].lower():
                        for contract in powers.keys():
                            if power[0] == contract:
                                if "," in powers[contract]:
                                    elemsplit = powers[contract].split(",")
                                    value = elemsplit[len(elemsplit)-1]
                                else:
                                    value = powers[contract]
                                if int(rhs) > int(value):
                                    if "," in power[1]:
                                        if rhs in power[1].split(","):
                                            self.caller.msg(power[0] + " upgraded to rank " + rhs)
                                            elemsplit[len(elemsplit)-1] = rhs
                                            powers[contract] = elemsplit.join(",")
                                            return
                                        else:
                                            self.caller.msg("You can't add " + power[0].lower() +" at that rank on " + target.name + "!")
                                            return
                                elif int(rhs) < int(value) and int(rhs) >= 1:
                                    if "," in power[1]:
                                        if rhs in power[1].split(","):
                                            self.caller.msg(power[0] + " reduced to rank "+ rhs)
                                            elemsplit[len(elemsplit)-1] = rhs
                                            powers[contract] = elemsplit.join(",")
                                            return
                                        else:
                                            self.caller.msg("You can't reduce "+ power[0].lower() +" to that rank on " + target.name + "!")
                                            return
                                else:
                                    self.caller.msg(target.name + " already has " + power[0].lower() +" at that rank!")
                                    return
                        if "," in power[1]:
                            ranks = power[1].split(",")
                            if rhs in ranks:
                                self.caller.msg(power[0] + " added at rank "+ rhs)
                                powers[power[0]] = rhs
                                return
                            else:
                                self.caller.msg("Invalid rank to add!")
                                return
                        else:
                            if self.rhs == power[1]:
                                self.caller.msg(power[0] + " added at rank "+power[1])
                                powers[power[0]] = power[1]
                                return
                            else:
                                self.caller.msg("Invalid rank to add!")
                                return
                self.caller.msg("Invalid contract!")
                return
            if template == "Demon":
                embeds = demscript.db.embeds
                exploits = demscript.db.exploits
                mods = demscript.db.modifications
                process = demscript.db.processes
                tech = demscript.db.technologies
                prop = demscript.db.propulsion
                technique =  target.db.techniquelist
                miscstats = target.db.miscstats
                merits = target.db.meritlist
                terriblerank = 0
                for merit in merits:
                    if merit[0].lower() == "terrible form":
                        terriblerank = int(merit[1])
                for layer in embeds:
                    if layer[0].lower() == arglist[0].lower():
                        for power in powers.keys():
                            if layer[0].lower() == power:
                                self.caller.msg(target.name + " already has this embed!")
                                return
                            else:
                                powers.db.powers[layer[0]] = ""
                                self.caller.msg("Embed, \""+layer[0]+"\" added.")
                                return
                for hole in exploits:
                    if hole[0].lower() == arglist[0].lower():
                        for techno in technique:
                            if layer[0].lower() == techno:
                                self.caller.msg(target.name + " already has this exploit!")
                                return
                            else:
                                target.AddTech(hole[0])
                                self.caller.msg("Exploit, \""+hole[0]+"\" added.")
                                return
                for edit in mods:
                    if edit[0].lower() == arglist[0].lower():
                        for miscellany in miscstats:
                            if "," in miscellany:
                                if edit[0].lower() == miscellany.split(",")[0].lower():
                                    self.caller.msg(target.name + " already has this modification!")
                                    return
                                else:
                                    modcount = 0
                                    for misc2 in miscstats:
                                        for edit2 in mods:
                                            if misc2.split(",")[0] == edit2[0]:
                                                if terriblerank >= 1:
                                                    modcount += 1
                                    if modcount > 1:
                                        self.caller.msg("A character can't have more than two modifications, bonus from terrible form included.")
                                        return
                                    else:
                                        miscstats.append(edit[0])
                                        self.caller.msg(edit[0] + " modification added.")
                                        return
                            else:
                                if edit[0].lower() == miscellany.lower():
                                    self.caller.msg(target.name + " already has this modification!")
                                    return
                                else:
                                    miscstats.append(edit[0])
                                    self.caller.msg(edit[0] + " modification added.")
                                    return
                for thread in process:
                    if thread[0].lower() == arglist[0].lower():
                        threadcount = 0
                        for miscellany in miscstats:
                            if "," in miscellany:
                                for thread2 in process:
                                    if thread2 == miscellany.split(",")[0]:
                                        threadcount += 1
                                if (threadcount > 0 and terriblerank <= 3) or (threadcount > 1 and terriblerank == 4):
                                    self.caller.msg("You can't have that many processes on " + target.name + "!")
                                    return
                                else:
                                    self.caller.msg(thread[0] + " process added.")
                                    miscstats.append(thread[0])
                                    return
                            else:
                                for thread2 in process:
                                    if thread2 == miscellany:
                                        threadcount += 1
                                    if (threadcount > 0 and terriblerank <= 3) or (threadcount > 1 and terriblerank == 4):
                                        self.caller.msg("You can't have that many processes!")
                                        return
                                    else:
                                        self.caller.msg(thread[0] + " process added.")
                                        miscstats.append(thread[0])
                                        return
                for gear in tech:
                    if gear[0].lower() == arglist[0].lower():
                        techcount = 0
                        for miscellany in miscstats:
                            if "," in miscellany:
                                for gear2 in tech:
                                    try:
                                        if gear2 == miscellany.split(",")[0]:
                                            techcount += 1
                                    except IndexError:
                                        if gear2 == miscellany:
                                            techcount += 1
                                if (techcount > 0 and terriblerank <= 1) or (techcount > 1 and terriblerank >= 2):
                                    self.caller.msg(target.name + " can't have that many technologies!")
                                    return
                                else:
                                    self.caller.msg(gear[0] + " technology added.")
                                    return
                            else:
                                for gear2 in tech:
                                    if gear2 == miscellany.split[0]:
                                        techcount += 1
                                if (techcount > 0 and terriblerank <= 1) or (techcount > 1 and terriblerank >= 2):
                                    self.caller.msg(target.name + " can't have that many technologies!")
                                    return
                                else:
                                    self.caller.msg(gear[0] + " technology added.")
                                    return
                for zoom in prop:
                    if zoom[0].lower() == self.arglist[0].lower():
                        zoomcount = 0
                        for miscellany in miscstats:
                            if "," in miscellany:
                                for zoom2 in prop:
                                    try:
                                        if zoom2 == miscellany.split(",")[0]:
                                            zoomcount += 1
                                    except IndexError:
                                        if zoom2 == miscellany:
                                            zoomcount += 1
                                if (zoomcount > 0 and terriblerank <= 2) or (zoomcount > 1 and terriblerank > 2):
                                    self.caller.msg(target.name + " can't have that many propulsions!")
                                    return
                                else:
                                    self.caller.msg(zoom[0] + " propulsion added.")
                                    return
                            else:
                                for zoom2 in prop:
                                    if zoom2 == miscellany.split(",")[0]:
                                        zoomcount += 1
                                if (zoomcount > 0 and terriblerank <= 2) or (zoomcount > 1 and terriblerank > 2):
                                    self.caller.msg(target.name+ " can't have that many propulsions!")
                                    return
                                else:
                                    self.caller.msg(zoom[0] + " propulsion added.")
                                    return
            if template == "Hunter":
                advarmory = huntscript.db.advarmory
                benediction = huntscript.db.benediction
                castigation = huntscript.db.castigation
                elixir = huntscript.db.elixir
                relic = huntscript.db.relic
                thaum = huntscript.db.thaumatechnology
                ink = huntscript.db.ink
                for gear in advarmory:
                    if lhs.lower() == gear[0].lower():
                        if target.db.xsplat == "Task Force VALKYRIE":
                            if int(rhs) in gear[1]:
                                target.AddPower(gear[0],int(rhs))
                                self.caller.msg(gear[0] + " added at " + rhs + " dots.")
                            else:
                                self.caller.msg(target.db.name + " can't take the " + gear[0] + " endowment at " + rhs + " dots.")
                                return
                        else:
                            self.caller.msg("Only members of Task Force VALKYRIE can have the advanced armory endowments.")
                            return
                for bless in benediction:
                    if lhs.lower() == bless[0]:
                        if target.db.xsplat == "Malleus Maleficarum":
                            target.db.powers[bless[0]] = ""
                            self.caller.msg(bless[0] +" added to "+ target.name)
                            return
                        else:
                            self.caller.msg("Only members of the Malleus Maleficarum may have benedictions.")
                            return
                for burn in castigation:
                    if burn[0].lower() == lhs.lower():
                        if target.db.xsplat == "Lucifuge":
                            target.db.powers[burn[0]] = ""
                            self.caller.msg(burn[0] + " added to " + target.name)
                            return
                        else:
                            self.caller.msg("Only the Lucifuge may wield the powers of castigation.")
                            return
                for brew in elixir:
                    if brew[0].lower() == lhs.lower():
                        if target.db.xsplat == "Ascending Ones":
                            if rhs in brew[1]:
                                target.AddPower(brew[0],int(rhs))
                                self.caller.msg(brew[0] + " added at " + rhs + " dots to "+ target.name)
                                return
                            else:
                                self.caller.msg(target.name + " cannot purchase " + brew[0] + " at " + rhs + " dots.")
                                return
                for tat in ink:
                    if tat[0].lower() == lhs.lower():
                        if target.db.xsplat == "Knights of St. Adrian":
                            target.db.powers[tat[0]] = ""
                            self.caller.msg(tat[0] + " added to " + target.name)
                            return
                        else:
                            self.caller.msg("Only members of the Knights of St. Adrian may purchase angelic tattoos.")
                            return
                for art in relic:
                    if art[0].lower() == lhs.lower():
                        if target.db.xsplat == "Aegis Kai Doru":
                            if rhs in art[1]:
                                target.AddPower(art[0],rhs)
                                self.caller.msg(art[0] + " added to " + target.name)
                                return
                        else:
                            self.caller.msg("Only members of Aegis Kai Doru may purchase relics.")
                            return
                for bio in thaum:
                    if bio[0].lower() == lhs.lower():
                        if target.db.xsplat == "Cheiron Group":
                            if rhs in bio[1]:
                                target.AddPower(bio[0],bio[1])
                                self.caller.msg(bio[0] + " added at " + bio[1] + " dots to " + target.name)
                                return
                            else:
                                self.caller.msg("You can't purchase " + bio[0] + " at " + bio[1] + " dots.")
                                return
                        else:
                            self.caller.msg("Only agents of the Cheiron Group may purchase thaumatechnology enhancements.")
                            return
                self.caller.msg("Invalid endowment.")
                return
            if template == "Mage":
                arcanalist = target.db.powers
                rotes = magescript.db.rotes
                templist = arcanalist
                for x in templist:
                    x.lower()
                if capwords(lhs) in magescript.db.arcana:
                    if 6 > int(rhs) > 0:
                        target.AddPower(lhs, rhs)
                        self.caller.msg(lhs + " arcanum added to " + target.name + " at " + rhs + " dots.")
                        return
                    elif int(rhs) == 0:
                        target.RemovePower(lhs)
                        self.caller.msg(lhs + " arcanum removed from " + target.name)
                        return
                else:
                    if rhs == "0":
                        for rote in target.db.techniquelist:
                            if lhs in rote.split(",")[0].lower():
                                target.RemoveTech(lhs)
                                self.caller.msg(rote.split(",")[0] + " removed from " + target.name)
                                return
                    for x in rotes:
                        if lhs.lower() == x[1].lower():
                            for arcanum in arcanalist:
                                if arcanum[0] == x[0]:
                                    if int(arcanum[1]) >= int(x[2]):
                                        if rhs.lower() == "animal ken":
                                            rhs = "animalken"
                                        if rhs.lower() in x[3].lower().split(",") or rhs.lower() == "praxis":
                                            if rhs == "animalken":
                                                rhs = "Animal Ken"
                                            target.AddTech(x[1],x[0],rhs)
                                        else:
                                            target.AddTech(x[1],x[0],rhs)
                                            self.caller.msg("Rote " + x[1] + " from the " + x[0] + "arcanum added with the custom skill " + rhs)
                                            return
                                    else:
                                        self.caller.msg(target.name +" needs more dots in the " + x[0].lower() + " arcanum to learn this rote!")
                                        return
                                else:
                                    self.caller.msg(target.name + " needs to have the "+x[0].lower()+" arcanum to learn this rote!")
                                    return
                        else:
                            self.caller.msg("Invalid rote.")
                            return
            if template == "Mummy":
                affinities = mumscript.db.affinities
                utterances = mumscript.db.utterances
                for aff in affinities:
                    if lhs.lower() == aff[0]:
                        if len(aff) == 2:
                            if target.db.xsplat == aff[1]:
                                target.AddPower(aff[0],aff[1])
                                self.caller.msg("Guild affinity " + aff[0] + " added to " + target.name)
                                return
                            else:
                                self.caller.msg(target.name + " isn't in the right guild for this affinity.")
                                return
                        else:
                            for pillar in target.db.miscstats:
                                if pillar in aff[1]:
                                    if int(pillar.split(",")[1]) >= int(aff[2]):
                                        target.AddPower(aff[0],aff[1])
                                        self.caller.msg(aff[0] + " added to " + target.name)
                                        return
                                    else:
                                        self.caller.msg("The " + pillar.split(",")[0] + " pillar on " + target.name + " isn't high enough to acquire this affinity.")
                                        return
                for utt in utterances:
                    if lhs.lower() == utt[0]:
                        if rhs in utt[2]:
                            if rhs == "1":
                                for pillar in target.db.miscstats:
                                    if pillar.split(",")[0] == utt[1].split(",")[0]:
                                        if pillar.split(",")[1] == "1":
                                            for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                            target.AddTech(utt[0],rhs)
                                            self.caller.msg(utt[0] + " added with a rank of " + rhs + " to " + target.name)
                                            return
                                        else:
                                            self.caller.msg(target.name + " needs at least one dot in that pillar to purchase this utterance.")
                                            return
                            
                            elif rhs == "5" and utt[1].split(",")[2] == "Defining":
                                if target.db.xsplat == "Lion-Headed":
                                    if target.db.miscstats[0].split(",")[1] == "5":
                                        for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                        target.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at 5 dots " + target.name)
                                        return
                                    else:
                                        self.caller.msg("The Ab pillar on " + target.name + " is not high enough to purchase this tier.")
                                        return
                                elif target.db.xsplat == "Falcon-Headed":
                                    if target.db.miscstats[1].split(",")[1] == "5":
                                        for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                        target.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at 5 dots to " + target.name)
                                        return
                                    else:
                                        self.caller.msg("The Ba pillar on " + target.name + " is not high enough to purchase this tier.")
                                        return
                                elif target.db.xsplat == "Bull-Headed":
                                    if target.db.miscstats[2].split(",")[1] == "5":
                                        for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                        target.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at 5 dots.")
                                        return
                                    else:
                                        self.caller.msg("The Ka pillar on " + target.name + " is not high enough to purchase this tier.")
                                        return
                                elif target.db.xsplat == "Serpent-Headed":
                                    if target.db.miscstats[3].split(",")[1] == "5":
                                        for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                        target.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at 5 dots.")
                                        return
                                    else:
                                        self.caller.msg("Your Ren pillar is not high enough to purchase this tier.")
                                        return
                                elif target.db.xsplat == "Jackal-Headed":
                                    if target.db.miscstats[4].split(",")[1] == "5":
                                        for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                        target.AddTech(utt[0],rhs)
                                        self.caller.msg(utt[0] + " added at 5 dots.")
                                        return
                                    else:
                                        self.caller.msg("Your Sheut pillar is not high enough to purchase this tier.")
                                        return
                            else:
                                for pillar in target.db.miscstats:
                                    if pillar.split(",")[0] in utt[1]:
                                        if int(utt[2].split(",")[utt[1].index(pillar.split(",")[0])]) <= int(pillar.split(",")[1]):
                                            for technique in target.db.techniquelist:
                                                if utt[0] in technique:
                                                    target.RemoveTech(technique)
                                            target.AddTech(utt[0],rhs)
                                            self.caller.msg(utt[0] + " added to " + target.name + " at " + rhs + " dots.")
                                            return
                                        else:
                                            self.caller.msg("The " + pillar.split(",")[0] + " pillar on " + target.name + " isn't high enough to acquire this tier of utterance.")
                                            return
            if template == "Promethean":
                transmutations = promscript.db.transmutations
                refine = target.db.ysplat
                if "=" in self.args:
                    if rhs == "0":
                        for mute in target.db.powers.keys():
                            if mute.lower() == lhs.lower():
                                del target.db.powers[mute]
                                self.caller.msg(mute + " transmutation removed from " + target.name)
                                return
                            if lhs.lower() == target.db.powers[mute].lower():
                                self.caller.msg(target.db.powers[mute] + " alembic removed from " + target.name)
                                target.db.powers[mute] = ""
                                return
                        self.caller.msg("Invalid transmutation or alembic to remove.")
                        return
                    else:
                        self.caller.msg("Use, '+set <transmutation or alembic>=0' to remove it.")
                        return
                for change in transmutations:
                    if change[0].lower() == arglist[0].lower():
                        if change[1] == "General" or refine in change[1]:
                            if not change[0] in target.db.powers.keys():
                                target.db.powers[change[0]] = ""
                                self.caller.msg("The " + change[0] + " transmutation has been added to " + target.name)
                                return
                            else:
                                self.caller.msg(target.name + " already has that transmutation.")
                                return
                        else:
                            if not change[0] in target.db.powers.keys():
                                target.db.powers[change[0]] = ""
                                self.caller.msg("The " + change[0] + " transmutation has been added to " + target.name)
                                return
                            else:
                                self.caller.msg(target.name + " already has that transmutation.")
                                self.caller.msg("You just added a transmutation to a character that didn't mean the prerequisites. Be sure you meant to do this.")
                                return
                    for alembic in change:
                        if arglist[0].lower() == alembic.lower() or args.lower() == alembic.lower():
                            if change.index(alembic) >= 2:
                                if target.db.powers[change[0]] != "":
                                    self.caller.msg(target.db.powers[change[0]] + " alembic swapped out for " + alembic + " on " + target.name)
                                else:
                                    self.caller.msg(alembic + " added to the " + change[0] + " transmutation on " + target.name)
                                target.db.powers[change[0]] = alembic
                                return
                self.caller.msg("Invalid transmutation or alembic.")
                return
            if template == "Vampire" or template == "Ghoul":
                for x in discscript.db.disciplines:
                    if rhs:
                        if int(rhs) > 0:
                            if lhs.lower() == x[0].lower():
                                if discscript.MeetsPrereqs(target,x[0]):
                                    target.AddPower(x[0],rhs)
                                    self.caller.msg(x[0] + " set to " + rhs + " on " + target.name)
                                    return
                                else:
                                    target.AddPower(x[0],rhs)
                                    self.caller.msg(x[0] + " set to " + rhs + " on " + target.name)
                                    self.caller.msg("You just set a discipline on a character that did not meet the prerequisites. Be sure you meant to do this.")
                                    return
                        else:
                            if lhs.lower() == x[0].lower():
                                target.RemPower(x[0])
                                self.caller.msg(x[0] + " removed from " + target.name)
                if template == "Vampire":
                    if not ("=" in self.args):
                        if args:
                            for y in discscript.db.devotions:
                                if args.lower() == y[0].lower():
                                    if discscript.MeetsPrereqs(target,y[0]):
                                        target.AddTech(y[0])
                                        self.caller.msg(y[0] + " added to " + target.name)
                                    else:
                                        self.caller.msg(target.name + " doesn't meet the prerequisites for this devotion!")
                    
                    else:
                        for y in target.db.techniquelist:
                            if "," in y:
                                if y.split(",")[0].lower() == lhs.lower():
                                    target.RemoveTech(y)
                                    self.caller.msg(y[0] + " removed from " + target.name)
                                    return
                            else:
                                if y.lower() == self.lhs.lower():
                                    target.RemoveTech(y)
                                    self.caller.msg(y + " removed from " + target.name)
                                    return
                self.caller.msg("Only vampires may learn devotions!")
                return
            if template == "Werewolf":
                for x in wolfscript.db.gifts:
                    if lhs.lower() == x[0].lower() or lhs.lower == "gift of "+x[0].lower():
                        for y in target.db.powers.keys():
                            if args.strip().lower() == y.lower():
                                self.caller.msg("You've already unlocked this gift!")
                                return
                            if args.strip().lower() in y.lower():
                                self.caller.msg("You've already unlocked this gift!")
                                return
                        target.AddPower(x)
                        self.caller.msg("Gift of "+x+" unlocked. Please choose one facet corresponding to a dot of renown you have as the gift's starting facet." )
                        return
                for y in wolfscript.db.gifts:
                    for z in y:
                        if args.lower() == z.lower() and y.index(z) >= 4:
                            for power in target.db.powers.keys():
                                if z in target.db.powers[power]:
                                    self.caller.msg("You already have that facet!")
                                else:
                                    renownindex = y.index(z)
                                    renownlist = []
                                    if "," in target.db.powers[power]:
                                        facetlist = target.db.powers[power].split(",")
                                        for facet in facetlist:
                                            if facet == y[4]:
                                                renownlist.append("Cunning,"+str(facetlist.index(facet)))
                                            if facet == y[5]:
                                                renownlist.append("Glory,"+str(facetlist.index(facet)))
                                            if facet == y[6]:
                                                renownlist.append("Honor,"+str(facetlist.index(facet)))
                                            if facet == y[7]:
                                                renownlist.append("Purity,"+str(facetlist.index(facet)))
                                            if facet == y[8]:
                                                renownlist.append("Wisdom,"+str(facetlist.index(facet)))
                                        if renownindex == 4:
                                            facetlist.insert(0,z)
                                        if renownindex == 5:
                                            for item in renownlist:
                                                if "Cunning" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Honor" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                                elif "Purity" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                                elif "Wisdom" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                        if renownindex == 6:
                                            for item in renownlist:
                                                if "Cunning" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Glory" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Purity" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                                elif "Wisdom" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                        if renownindex == 7:
                                            for item in renownlist:
                                                if "Cunning" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Glory" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Honor" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Wisdom" in item:
                                                    indexin = int(item.split(",")[1])
                                                    return
                                        if renownindex == 8:
                                            for item in renownlist:
                                                if "Cunning" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Glory" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Honor" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                                elif "Purity" in item:
                                                    indexin = int(item.split(",")[1]) + 1
                                                    return
                                        facetlist.insert(indexin, z)
                                        facetlist = ','.join(facetlist)
                                        target.db.powers[power] = facetlist
                                        if y[0] == "Nature's Gift":
                                            self.caller.msg(y[0] + " facet, \""+z+"\" added to " + target.name)
                                        else:
                                            self.caller.msg("Gift of "+y[0]+" facet, \""+z+"\" added  to " + target.name)
                                    else:
                                        self.caller.db.powers[power] = z
                                        if y[0] == "Nature's Gift":
                                            self.caller.msg(y[0] + " facet, \""+z+"\" added to " + target.name)
                                        else:
                                            self.caller.msg("Gift of " + y[0] + " facet, \""+z+ "\" added to " + target.name)
    def SetTemplate(self, target, newtemplate):
            if newtemplate.lower() == "vampire":
                    target.db.template = "Vampire"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.powerstat = 1
                    target.db.pools.update({'Vitae':str(target.db.powerlist[target.db.powerstat-1]) +","+ str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.xsplatname = "Clan"
                    target.db.ysplatname = "Covenant"
                    target.db.zsplatname = "Bloodline"
                    target.db.powername = "Disciplines"
                    target.db.techname = "Devotions"
                    target.db.miscname = "Rituals"
                    target.db.demeanorname = "Mask"
                    target.db.demeanor = ""
                    target.db.naturename = "Dirge"
                    target.db.nature = ""
                    target.db.powerstatname = "Blood Potency"
                    target.db.sanity = 7
                    target.db.sanityname = "Humanity"
                    target.db.miscstats = []
                    target.db.meritlist = []
                    target.msg("Template set to Vampire.")
                    return
            if newtemplate.lower() == "ghoul":
                    target.db.template = "Ghoul"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.pools.update({'Vitae':str(self.db.attributes['Stamina'])+","+str(self.db.attributes['Stamina'])})
                    self.caller.msg(target.name + " has had their template set to ghoul.")
                    target.db.powername = "Disciplines"
                    target.db.powers = {}
                    target.db.miscstats = []
                    target.db.techniquelist = []
                    target.db.techname = ""
                    target.db.miscname =""
                    target.db.xsplatname = ""
                    target.db.ysplatname = ""
                    target.db.zsplatname = ""
                    target.db.powerstatname = ""
                    target.db.sanity = 7
                    target.db.demeanorname = "Virtue"
                    target.db.demeanor = ""
                    target.db.naturename = "Vice"
                    target.db.nature = ""
                    target.db.sanityname = "Integrity"
                    target.db.powerstat = 0
                    target.db.meritlist = []
            if newtemplate.lower() == "werewolf":
                    target.db.template = "Werewolf"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.powerstat = 1
                    target.db.pools.update({'Essence':str(target.db.powerlist[target.db.powerstat-1]) +","+ str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.xsplatname = "Auspice"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Tribe"
                    target.db.ysplat = ""
                    target.db.zsplatname = "Lodge"
                    target.db.zsplat =""
                    self.caller.msg(target.name + " has had their template set to Werewolf")
                    target.db.powername = "Gifts"
                    target.db.powers = {}
                    target.db.techname = "Rites"
                    target.db.techniquelist = []
                    target.db.miscname = "Renown"
                    target.db.powerstatname = "Primal Urge"
                    target.db.sanityname = "Harmony"
                    target.db.demeanorname = "Blood"
                    target.db.naturename = "Bone"
                    target.db.demeanor = ""
                    target.db.nature = ""
                    target.db.sanity = 7
                    target.db.miscstats = ["Cunning,0","Glory,0","Honor,0","Purity,0","Renown,0"]
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "wolfblood":
                    target.db.template = "Wolfblood"
                    target.db.powername = "Tells"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.miscstats = []
                    target.db.powers = {}
                    target.db.techniquelist = []
                    target.db.techname = ""
                    target.db.miscname =""
                    target.db.xsplatname = ""
                    target.db.xsplat = ""
                    target.db.ysplatname = ""
                    target.db.ysplat = ""
                    target.db.zsplatname = ""
                    target.db.zsplat = ""
                    target.db.sanityname = "Integrity"
                    target.db.sanity = 7
                    target.db.powerstat = 0
                    target.db.powerstatname = ""
                    target.db.demeanorname = "Virtue"
                    target.db.naturename = "Vice"
                    target.db.nature = ""
                    target.db.demeanor = ""
                    target.db.meritlist = []
                    self.caller.msg(target.name + " has had their template set to wolfblood.")
            if newtemplate.lower() == "mage":
                    target.db.template = "Mage"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.powerstat = 1
                    target.db.pools.update({'Mana':str(target.db.powerlist[target.db.powerstat-1]) +","+ str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.xsplatname = "Path"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Order"
                    target.db.ysplat = ""
                    target.db.zsplatname = "Legacy"
                    target.db.zsplat = ""
                    target.db.powername = "Arcana"
                    target.db.poweres = {}
                    target.db.techname = "Rotes and Praxes"
                    target.db.techniquelist = []
                    target.db.sanityname = "Wisdom"
                    target.db.powerstatname = "Gnosis"
                    target.db.miscname = ""
                    target.db.miscstats = []
                    target.db.sanity = 7
                    target.db.demanor = ""
                    target.db.demeanorname = "Virtue"
                    target.db.nature = ""
                    target.db.naturename = "Vice"
                    self.caller.msg(target.name + " has had their template set to Mage.")
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "proximus":
                    target.db.template = "Proximus"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.pools['Mana'] = "5,5"
                    target.db.xsplatname = "Path"
                    target.db.powername = "Blessings"
                    target.db.ysplatname = "Order"
                    target.db.xsplat = ""
                    target.db.ysplat = ""
                    target.db.zsplatname = ""
                    target.db.zsplat = ""
                    target.db.sanity = 7
                    target.db.miscname = ""
                    target.db.miscstats = []
                    target.db.techname = ""
                    target.db.techniquelist = []
                    target.db.powerstat = 0
                    target.db.powerstatname = ""
                    target.db.sanityname = "Integrity"
                    target.db.demeanorname = "Virtue"
                    target.db.nature = ""
                    target.db.naturename = "Vice"
                    target.db.meritlist = []
            if newtemplate.lower() == "changeling":
                    target.db.template = "Changeling"
                    target.db.powerstat = 1
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.pools.update({'Glamour':str((target.db.powerlist[target.db.powerstat-1])) + "," + str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.powerstatname = "Wyrd"
                    target.db.xsplatname = "Seeming"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Court"
                    target.db.ysplat = ""
                    target.db.zsplatname = "Entitlement"
                    target.db.zsplat = ""
                    target.db.powers = {}
                    target.db.techniquelist = []
                    target.db.techname = ""
                    target.db.powername = "Contracts"
                    target.db.miscname = ""
                    target.db.miscstats = []
                    target.db.sanityname = "Clarity"
                    target.db.sanity = 7
                    target.db.demeanorname = "Mask"
                    target.db.naturename = "Mien"
                    target.db.nature = ""
                    target.db.demeanor = ""
                    target.db.kith = ""
                    self.caller.msg(target.name + " has had their template set to Changeling")
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "fae-touched":
                    target.db.template = "Fae-Touched"
                    target.db.powerstat = 0
                    self.caller.msg(target.name + " has had their template set to fae-touched.")
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.pools['Glamour'] = "10,10"
                    target.db.xsplatname = "Seeming"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Court"
                    target.db.ysplat = ""
                    target.db.zsplatname = ""
                    target.db.zsplat = ""
                    target.db.powername = "Contracts"
                    target.db.powers = {}
                    target.db.techname = ""
                    target.db.techniquelist = []
                    target.db.miscstats = []
                    target.db.miscname = ""
                    target.db.powerstatname = ""
                    target.db.sanity = 7
                    target.db.sanityname = "Integrity"
                    target.db.demeanorname = "Virtue"
                    target.db.nature = ""
                    target.db.naturename = "Vice"
                    target.db.meritlist = []
            if newtemplate.lower() == "hunter":
                    target.db.template = "Hunter"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.xsplatname = "Faction"
                    target.db.xsplat = ""
                    target.db.ysplatname = ""
                    target.db.ysplat = ""
                    target.db.zsplatname = ""
                    target.db.zsplat = ""
                    target.db.powername = "Endowments"
                    target.db.powers = {}
                    target.db.techname = ""
                    target.db.techniquelist = []
                    target.db.miscname = ""
                    target.db.miscstats = []
                    target.db.sanity = 7
                    target.db.powerstat = 0
                    target.db.powerstatname = ""
                    target.db.sanityname = "Integrity"
                    self.caller.msg.msg(target.name + " has had their template set to Hunter")
                    target.db.demeanorname = "Virtue"
                    target.db.nature = ""
                    target.db.naturename = "Vice"
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "beast":
                    target.db.template = "Beast"
                    self.caller.msg(target.name + " has had their template set to Beast")
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.xsplatname = "Family"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Hunger"
                    target.db.ysplat = ""
                    target.db.demeanorname = "Legend"
                    target.db.naturename = "Life"
                    target.db.nature = ""
                    target.db.demeanor = ""
                    target.db.zsplat = ""
                    target.db.zsplatname = ""
                    target.db.powername = "Atavisms"
                    target.db.techname = "Nightmares"
                    target.db.powerstatname = "Lair"
                    target.db.powerstat = 1
                    target.db.sanity = 4
                    target.db.sanityname = "Satiety"
                    target.db.miscstats = []
                    target.db.techniquelist = []
                    target.db.powers = {}
                    target.db.miscname = ""
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "promethean":
                    target.db.template = "Promethean"
                    self.caller.msg(target.name + " has had their template set to Promethean")
                    target.db.powerstat = 1
                    target.db.pools = target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.pools.update({'Pyros':str((target.db.powerlist[target.db.powerstat-1])/2) + "," + str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.xsplatname = "Lineage"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Refinement"
                    target.db.ysplat = ""
                    target.db.zsplatname = "Role"
                    target.db.zsplat = ""
                    target.db.demeanorname = "Elpis"
                    target.db.demeanor = ""
                    target.db.naturename = "Torment"
                    target.db.nature = ""
                    target.db.powers = {}
                    target.db.powername = "Transmutations"
                    target.db.powerstatname = "Azoth"
                    target.db.sanityname = "Pilgrimage"
                    target.db.sanity = 1
                    target.db.miscname = ""
                    target.db.miscstats = []
                    target.db.techname = ""
                    target.db.techniquelist = []
                    target.db.meritlist = []
                    return
            if newtemplate.lower() == "mortal":
                target.db.template = "Mortal"
                self.caller.msg(target.name + " has had their template set to Mortal")
                target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                target.db.powerstat = 0
                target.db.powerstatname = ""
                target.db.sanity = 7
                target.db.sanityname = "Integrity"
                target.db.demeanorname = "Virtue"
                target.db.nature = ""
                target.db.naturename = "Vice"
                target.db.xsplat = ""
                target.db.xsplatname = ""
                target.db.ysplat = ""
                target.db.ysplatname = ""
                target.db.zsplat = ""
                target.db.zsplatname = ""
                target.db.miscname = ""
                target.db.miscstats = []
                target.db.powers = {}
                target.db.techname = ""
                target.db.techniquelist = ""
                target.db.powername = ""
                target.db.meritlist = []
                return
            if newtemplate.lower() == "mummy":
                target.db.template = "Mummy"
                self.caller.msg(target.name + " has had their template set to Mummy")
                target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                target.db.miscstats = ["Ab,0","Ba,0","Ka,0","Ren,0","Sheut,0"]
                target.db.pools.update({"Ab":target.db.miscstats[0].split(",")[1]+","+target.db.miscstats[0].split(",")[1]})
                target.db.pools.update({"Ba":target.db.miscstats[1].split(",")[1]+","+target.db.miscstats[1].split(",")[1]})
                target.db.pools.update({"Ka":target.db.miscstats[2].split(",")[1]+","+target.db.miscstats[2].split(",")[1]})
                target.db.pools.update({"Ren":target.db.miscstats[3].split(",")[1]+","+target.db.miscstats[3].split(",")[1]})
                target.db.pools.update({"Sheut":target.db.miscstats[4].split(",")[1]+","+target.db.miscstats[4].split(",")[1]})
                target.db.powerstat = 1
                target.db.powerstatname = "Sekhem"
                target.db.powers = {}
                target.db.powername = "Affinities"
                target.db.techname = "Utterances"
                target.db.techniquelist = []
                target.db.sanity = 3
                target.db.sanityname = "Memory"
                target.db.xsplatname = "Decree"
                target.db.ysplatname = "Guild"
                target.db.xsplat = ""
                target.db.ysplat =""
                target.db.zsplatname = "Judge"
                target.db.zsplat = ""
                target.db.demeanor = ""
                target.db.demeanorname = "Virtue"
                target.db.nature = ""
                target.db.miscname = "Pillars"
                target.db.naturename = "Vice"
                target.db.meritlist = []
                return
            if newtemplate.lower() == "demon":
                    target.db.template = "Demon"
                    target.db.pools = {'Willpower':str(target.db.attributes['Resolve']+target.db.attributes['Composure'])+
                                            ","+str(target.db.attributes['Resolve']+target.db.attributes['Composure'])}
                    target.db.powerstat = 1
                    target.db.pools.update({"Aether":str(7) +","+ str(target.db.powerlist[target.db.powerstat-1])})
                    target.db.powerstatname = "Primium"
                    target.db.xsplatname = "Incarnation"
                    target.db.xsplat = ""
                    target.db.ysplatname = "Agenda"
                    target.db.ysplat = ""
                    target.db.zsplatname = ""
                    target.db.demeanorname = "Virtue"
                    target.db.demeanor = ""
                    target.db.naturename = "Vice"
                    target.db.nature = ""
                    target.db.zsplat = ""
                    self.caller.msg(target.name + " has had their template set to Demon")
                    target.db.powers = {}
                    target.db.powername = "Embeds"
                    target.db.techniquelist = []
                    target.db.techname = "Exploits"
                    target.db.sanity = 7
                    target.db.sanityname = "Cover"
                    target.db.miscname = "Demonic Form"
                    target.db.miscstats = []
                    target.db.meritlist = []
                    return
            return False