'''
Created on Jan 26, 2017

@author: CodeKitty
'''

from evennia import DefaultScript
from evennia import default_cmds
from evennia import create_script
from evennia.utils import search
import time
from textwrap import wrap
import datetime
from evennia.utils import create
from evennia import DefaultCharacter
import os
from evennia.utils import inherits_from
from evennia import create_channel
class JobHandler(DefaultScript):
    
    def at_script_creation(self):
        self.db.buckets = {}
        self.db.joblist = []
        self.db.deadlines = []
class JobCommand(default_cmds.MuxCommand):
    key = "+job"
    aliases = ["+jobs","+myjobs","+myjob"]
    
    def func(self):
        handlervar = search.scripts('JobHandler')
        args = self.args
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        cmdstring = self.cmdstring
        try:
            handlervar = handlervar[0]
        except IndexError:
            handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
            self.caller.msg("Jobs system initialized.")
        if not args and not switches:
            if self.caller.IsAdmin() and (cmdstring != "+myjobs" and cmdstring != "+myjob"):
                jobbody = ""
                header = "/" + "-" * 36 +"Jobs" + "-" * 36 + "\\\n"
                header += "|| # " + " " * 12 + "Title" + " " * 11 + "  Submitted On   " + "  Submitted By   " + " Due Date  " + "||\n"
                finalbody = ""
                taglist = sorted(list(handlervar.db.buckets.keys()))
                for tag in taglist:
                    if len(handlervar.db.joblist[handlervar.db.buckets[tag.upper()] - 1]) != 0:
                        jobbody += "+---" + tag + "-" * (4 - len(tag))
                        jobbody += "-" * (77 - len(jobbody)) + "+\n"
                        for job in handlervar.db.joblist[handlervar.db.buckets[tag] - 1]:
                            submitter = search.objects("#"+str(job[1]))[0].name
                            jobrow = "||"
                            if (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) < 10:
                                jobrow += " "
                                jobrow +=  str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                                jobrow += " "
                            elif (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) > 9:
                                jobrow += " "
                                jobrow += str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                            elif (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) > 99:
                                jobrow += str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                            titlecrop = job[0][:28]
                            if len(titlecrop) % 2 == 0:
                                jobrow += " " * (14 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                            else:
                                jobrow += " " * (13 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                            if len(job[2]) % 2 == 0:
                                jobrow += " " * (8 - len(job[2])/2) + job[2] + " " * (9 - len(job[2])/2)
                            else:
                                jobrow += " " * (8 - len(job[2])/2) + job[2] + " " * (8 - len(job[2])/2)
                            if len(submitter) % 2 == 0:
                                jobrow += " " * (8 - len(submitter)/2) + submitter + " " * (9 - len(submitter)/2)
                            else:
                                jobrow += " " * (8 - len(submitter)/2) + submitter + " " * (8 - len(submitter)/2)
                            if len(job[3]) % 2 == 0:
                                jobrow += " " * (5 - len(job[3])/2) + job[3] + " " * (6 - len(job[3])/2)
                            else:
                                jobrow += " " * (5 - len(job[3])/2) + job[3] + " " * (5 - len(job[3])/2)
                            jobrow += " " * (78 - len(jobrow)) + "||\n"
                            jobbody += jobrow
                            jobrow = ""
                    finalbody += jobbody
                    jobbody = ""
                footer = "\\" + "-" * 76 + "/"
                self.caller.msg(header + finalbody + footer)
            else:
                headername = self.caller.name
                if len(headername) % 2 == 0:
                    header = "/" + "-" * (33 - len(headername)/2) +"Jobs for " + headername + "-" * (34 - len(headername)/2) + "\\\n"
                    jobbody = ""
                else:
                    header = "/" + "-" * (33 - len(headername)/2) +"Jobs for " + headername + "-" * (33 - len(headername)/2) + "\\\n"
                    jobbody = ""
                header += "|| # " + " " * 12 + "Title" + " " * 11 + "  Submitted On   " + "  Submitted By   " + " Due Date  " + "||\n"
                finalbody = ""
                taglist = sorted(list(handlervar.db.buckets.keys()))
                for tag in taglist:
                    if len(handlervar.db.joblist[handlervar.db.buckets[tag] - 1]) != 0:
                        for job in handlervar.db.joblist[handlervar.db.buckets[tag] - 1]:
                            injob = False
                            if job[1] != self.caller.id:
                                for person in range(4,len(job)):
                                    if job[person] == self.caller.id:
                                        injob = True
                                        break
                            else:
                                injob = True
                                if jobbody == "":
                                    jobbody += "+---" + tag + "-" * (4 - len(tag))
                                    jobbody += "-" * (77 - len(jobbody)) + "+\n"
                            if not injob:
                                continue
                            try:
                                submitter = search.objects("#"+str(job[1]))[0].name
                            except IndexError:
                                submitter = "Unfindable"
                            jobrow = "||"
                            if (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) < 10:
                                jobrow += " "
                                jobrow +=  str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                                jobrow += " "
                            elif (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) > 9:
                                jobrow += " "
                                jobrow += str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                            elif (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) > 99:
                                jobrow += str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                            titlecrop = job[0][:28]
                            if len(titlecrop) % 2 == 0:
                                jobrow += " " * (14 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                            else:
                                jobrow += " " * (13 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                            if len(job[2]) % 2 == 0:
                                jobrow += " " * (8 - len(job[2])/2) + job[2] + " " * (9 - len(job[2])/2)
                            else:
                                jobrow += " " * (8 - len(job[2])/2) + job[2] + " " * (8 - len(job[2])/2)
                            if len(submitter) % 2 == 0:
                                jobrow += " " * (8 - len(submitter)/2) + submitter + " " * (9 - len(submitter)/2)
                            else:
                                jobrow += " " * (8 - len(submitter)/2) + submitter + " " * (8 - len(submitter)/2)
                            if len(job[3]) % 2 == 0:
                                jobrow += " " * (5 - len(job[3])/2) + job[3] + " " * (6 - len(job[3])/2)
                            else:
                                jobrow += " " * (5 - len(job[3])/2) + job[3] + " " * (5 - len(job[3])/2)
                            jobrow += " " * (78 - len(jobrow)) + "||\n"
                            jobbody += jobrow
                            jobrow = ""
                    finalbody += jobbody
                    jobbody = ""
                footer = "\\" + "-" * 76 + "/"
                self.caller.msg(header + finalbody + footer)
        elif switches and args:
            if self.caller.IsAdmin():
                if switches[0] == "newbucket":
                    if 0 < len(lhs) < 6:
                        try:
                            testvar = str(handlervar.db.buckets[args.upper()])
                            self.caller.msg("That bucket already exists.")
                            return
                        except KeyError:
                            if rhs:
                                try:
                                    handlervar.db.buckets[lhs.upper().strip()] = len(handlervar.db.buckets) + 1
                                    handlervar.db.joblist.append([])
                                    handlervar.db.deadlines.append(self.rhs)
                                    self.caller.msg("Bucket created with the tag "+lhs.upper() + " and a deadline of "+rhs + " days per job.")
                                    return
                                except TypeError:
                                    self.caller.msg("You have to add a deadline amount for the bucket to be created!")
                                    return
                            else:
                                self.caller.msg("You have to add a deadline amount for the bucket to be created!")
                                return
                    else:
                        self.caller.msg("Bucket tags must at most, be five characters in length.")
                        return
                elif switches[0] == "deadline":
                    try:
                        handlervar.db.deadlines[handlervar.db.buckets[lhs.upper()]]
                    except KeyError:
                        self.caller.msg("That's not a valid bucket.")
                        return
                    except IndexError:
                        self.caller.msg("Deadline value not initialized.")
                        return
            if switches[0] == "add":
                try:
                    bucketindex = handlervar.db.buckets[lhs.split("/")[0].upper()] - 1
                    examinebucket = handlervar.db.joblist[bucketindex]
                    try:
                        examinejob = examinebucket[int(lhs.split("/")[1]) - 1]
                    except IndexError:
                        self.caller.msg("That's not a valid job.")
                        return
                    injob = False
                    for comment in examinejob:
                        if comment[0] == self.caller.id:
                            injob = True
                    if injob or self.caller.IsAdmin():
                        pass
                    else:
                        self.caller.msg("You can't comment to jobs that you aren't a part of.")
                        return
                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                    commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                    examinejob.append(tuple([self.caller.id,rhs,commenttime]))
                    self.caller.msg("Comment added to "+lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1])
                    mailcomment = "On " + commenttime +" " + self.caller.name + " commented:\n" + rhs
                    mailheader = self.caller.name + " commented on " + lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1]
                    sendlist = []
                    for char in examinejob:
                        if char in sendlist:
                            continue
                        try:
                            if int(char) == self.caller.id:
                                continue
                        except ValueError:
                            continue
                        except TypeError:
                            if int(char[0]) == self.caller.id:
                                continue
                        try:
                            charsearch = search.objects("#" + str(char))[0].name
                            if self.caller.account.search(charsearch) is not None:
                                sendlist.append(self.caller.account.search(charsearch))
                            continue
                        except IndexError:
                            continue
                        except TypeError:
                            charsearch = search.objects("#" + str(char))[0].name
                            if self.caller.account.search(charsearch) is not None:
                                sendlist.append(self.caller.account.search(charsearch))
                            continue
                    for receive in sendlist:
                        receive.msg("You have received a new @mail from the job system.")
                        new_message = create.create_message(self.caller, str(mailcomment), receivers=receive, header=mailheader)
                        new_message.tags.add("U", category="mail")
                        new_message.tags.add("JobHandler",category="script sender")
                    return
                except KeyError:
                    self.caller.msg("That's not a valid bucket to comment in.")
                    return
                except ValueError:
                    self.caller.msg("You need to use a number to comment on a job.")
                    return
                except IndexError:
                    self.caller.msg("That's not a valid job number to comment to.")
                    return
            if switches[0] == "invite":
                if self.caller.IsAdmin():
                    try:
                        bucketindex = handlervar.db.buckets[lhs.split("/")[0].upper()] - 1
                        examinebucket = handlervar.db.joblist[bucketindex]
                        examinejob = examinebucket[int(lhs.split("/")[1]) - 1]
                        try:
                            charsearch = search.objects(rhs)[0]
                            charid = charsearch.id
                            examinejob.append(charid)
                            self.caller.msg(charsearch.name + " added to the job.")
                            return
                        except IndexError:
                            self.caller.msg("That's not a valid player to add to this job.")
                            return
                    except KeyError:
                        self.caller.msg("That's not a valid job to add a player to.")
                    except IndexError:
                        self.caller.msg("That's not a valid job number.")
                        return
                    except ValueError:
                        self.caller.msg("You need to use a number to select a job.")
                        return
                else:
                    self.caller.msg("Only staff can add additional people to a job.")
                    return
            if switches[0] == "uninvite":
                if self.caller.IsAdmin():
                    try:
                        bucketindex = handlervar.db.buckets[lhs.split("/")[0].upper()] - 1
                        examinebucket = handlervar.db.joblist[bucketindex]
                        examinejob = examinebucket[int(lhs.split("/")[1]) - 1]
                        for item in examinejob:
                            try:
                                charsearch = search.objects("#"+str(item))[0]
                                if examinejob.index(item) > 5:
                                    examinejob.remove(item)
                                    self.caller.msg(charsearch.name + " removed from the list.")
                                    return
                                else:
                                    continue
                            except IndexError:
                                continue
                        self.caller.msg("That's not a valid player to remove.")
                        return
                    except KeyError:
                        self.caller.msg("That's not a valid job to remove a player from.")
                    except IndexError:
                        self.caller.msg("That's not a valid job number.")
                        return
                    except ValueError:
                        self.caller.msg("You need to use a number to select a job.")
                        return
                else:
                    self.caller.msg("Only staff can remove someone from a job.")
                    return
            if switches[0] == "approve":
                if self.caller.IsAdmin():
                    if not "/" in args:
                        self.caller.msg("You need to select a bucket and the number of job to approve.")
                        return
                    else:
                        bucketname = args.split("/")[0].upper()
                        if bucketname in handlervar.db.buckets.keys():
                            bucketindex = handlervar.db.buckets[bucketname] - 1
                            try:
                                approvejob = handlervar.db.joblist[bucketindex][int(lhs.split("/")[1]) - 1]
                            except IndexError:
                                self.caller.msg("There aren't that many jobs in that bucket!")
                                return
                            if self.rhs:
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                approvejob.append(tuple([self.caller.id,rhs,commenttime]))
                                self.caller.msg("Comment added to "+lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1])
                                mailcomment = "On " + commenttime +" " + self.caller.name + " approved your job with the comment:\n" + rhs
                                mailheader = self.caller.name + " approved " + lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1]
                                sendlist = []
                                for char in approvejob:
                                    if char in sendlist:
                                        continue
                                    try:
                                        if int(char) == self.caller.id:
                                            continue
                                    except ValueError:
                                        continue
                                    except TypeError:
                                        if int(char[0]) == self.caller.id:
                                            continue
                                    try:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                    except IndexError:
                                        continue
                                    except TypeError:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                for receive in sendlist:
                                    receive.msg("You have received a new @mail from the job system.")
                                    new_message = create.create_message(self.caller, str(mailcomment), receivers=receive, header=mailheader)
                                    new_message.tags.add("U", category="mail")
                                checkfile = str(".\jobdumps\\" + time.strftime("%B") + "_" + time.strftime("%y") + ".txt")
                                if os.path.isdir(".\jobdumps\\"):
                                    dumpfile = open(checkfile,'a+')
                                else:
                                    dumpfile = open(checkfile,'w+')
                                charlist = []
                                for thing in approvejob:
                                    try:
                                        if isinstance(thing, tuple):
                                            if thing != approvejob[len(approvejob) - 1]: 
                                                charsearch = search.objects('#'+str(thing[0]))[0]
                                                if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                    charlist.append(charsearch.name)
                                                    continue
                                            else:
                                                approver = charsearch = search.objects('#'+str(thing[0]))
                                                approver = approver[0].name
                                                break
                                        else:
                                            charsearch = search.objects('#'+str(thing))[0]
                                            if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                charlist.append(charsearch.name)
                                                continue
                                    except IndexError:
                                        continue
                                if dumpfile.read() != '':
                                    dumpfile.seek(1)
                                    dumpfile.write('\n')
                                dumpfile.write('Job Title: ' + approvejob[0] + ", Submitted On: " + approvejob[2] + ", Deadline: " + approvejob[3] + ", Approved By: " + approver + "\n")
                                for comment in range(4,len(approvejob)):
                                    if isinstance(approvejob[comment], tuple):
                                        charsearch = search.objects('#'+str(approvejob[comment][0]))[0]
                                        dumpfile.write('On '+approvejob[comment][2] + ' ' + charsearch.name + ' wrote \n' + approvejob[comment][1] + "\n\n")
                                dumpfile.write('--Job Approved--')
                                self.caller.msg("You have approved job " + str(bucketindex + 1) + " in the  " + bucketname + " bucket.")
                                handlervar.db.joblist[bucketindex].remove(approvejob)
                            else:
                                self.caller.msg("You have to add a comment to approve a job.")
                                return  
                                
                        else:
                            self.caller.msg("Invalid bucket.")
                            return
                else:
                    self.caller.msg("Only staff can approve jobs.")
                    return
            elif switches[0].lower() == "deny":
                if self.caller.IsAdmin():
                    if not "/" in args:
                        self.caller.msg("You need to select a bucket and the number of job to deny.")
                        return
                    else:
                        bucketname = args.split("/")[0].upper()
                        if bucketname in handlervar.db.buckets.keys():
                            bucketindex = handlervar.db.buckets[bucketname] - 1
                            try:
                                denyjob = handlervar.db.joblist[bucketindex][int(lhs.split("/")[1]) - 1]
                            except IndexError:
                                self.caller.msg("There aren't that many jobs in the bucket!")
                                return
                            if self.rhs:
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                denyjob.append(tuple([self.caller.id,rhs,commenttime]))
                                self.caller.msg("Comment added to "+lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1])
                                mailcomment = "On " + commenttime +" " + self.caller.name + " denied your job with the comment:\n" + rhs
                                mailheader = self.caller.name + " denied " + lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1]
                                sendlist = []
                                for char in denyjob:
                                    if char in sendlist:
                                        continue
                                    try:
                                        if int(char) == self.caller.id:
                                            continue
                                    except ValueError:
                                        continue
                                    except TypeError:
                                        if int(char[0]) == self.caller.id:
                                            continue
                                    try:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                    except IndexError:
                                        continue
                                    except TypeError:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                for receive in sendlist:
                                    receive.msg("You have received a new @mail from the job system.")
                                    new_message = create.create_message(self.caller, str(mailcomment), receivers=receive, header=mailheader)
                                    new_message.tags.add("U", category="mail")
                                checkfile = str(".\\jobdumps\\" + time.strftime("%B") + "_" + time.strftime("%y") + ".txt")
                                if os.path.isdir(".\\jobdumps\\"):
                                    dumpfile = open(checkfile,'a+')
                                else:
                                    dumpfile = open(checkfile,'w+')
                                charlist = []
                                for thing in denyjob:
                                    try:
                                        if isinstance(thing, tuple):
                                            if thing != denyjob[len(denyjob) - 1]: 
                                                charsearch = search.objects('#'+str(thing[0]))[0]
                                                if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                    charlist.append(charsearch.name)
                                                    continue
                                            else:
                                                denier = charsearch = search.objects('#'+str(thing[0]))
                                                denier = denier[0].name
                                                break
                                        else:
                                            charsearch = search.objects('#'+str(thing))[0]
                                            if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                charlist.append(charsearch.name)
                                                continue
                                    except IndexError:
                                        continue
                                if dumpfile.read() != '':
                                    dumpfile.seek(1)
                                    dumpfile.write('\n')
                                dumpfile.write('Job Title: ' + denyjob[0] + ", Submitted On: " + denyjob[2] + ", Deadline: " + denyjob[3] + ", Denied By: " + denier + "\n")
                                for comment in range(4,len(denyjob)):
                                    if isinstance(denyjob[comment], tuple):
                                        charsearch = search.objects('#'+str(denyjob[comment][0]))[0]
                                        dumpfile.write('On '+denyjob[comment][2] + ' ' + charsearch.name + ' wrote \n' + denyjob[comment][1] + "\n\n")
                                dumpfile.write('!--Job Denied--!')
                                self.caller.msg("You have denied job " + str(bucketindex + 1) + " in the  " + bucketname + " bucket.")
                                handlervar.db.joblist[bucketindex].remove(denyjob)
                            else:
                                self.caller.msg("You have to add a comment to deny a job.")
                                return   
                                
                        else:
                            self.caller.msg("Invalid bucket.")
                            return
                else:
                    self.caller.msg("Only staff can deny jobs.")
                    return
            elif switches[0].lower() == "cancel":
                if self.caller.IsAdmin():
                    if not "/" in args:
                        self.caller.msg("You need to select a bucket and the number of job to cancel.")
                        return
                    else:
                        bucketname = args.split("/")[0].upper()
                        if bucketname in handlervar.db.buckets.keys():
                            bucketindex = handlervar.db.buckets[bucketname] - 1
                            try:
                                canceljob = handlervar.db.joblist[bucketindex][int(lhs.split("/")[1]) - 1]
                            except IndexError:
                                self.caller.msg("There aren't that many jobs in the bucket!")
                                return
                            if self.rhs:
                                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                                canceljob.append(tuple([self.caller.id,rhs,commenttime]))
                                self.caller.msg("Comment added to "+lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1])
                                mailcomment = "On " + commenttime +" " + self.caller.name + " cancelled your job with the comment:\n" + rhs
                                mailheader = self.caller.name + " cancelled " + lhs.split("/")[0].upper() + " job number " + lhs.split("/")[1]
                                sendlist = []
                                for char in canceljob:
                                    if char in sendlist:
                                        continue
                                    try:
                                        if int(char) == self.caller.id:
                                            continue
                                    except ValueError:
                                        continue
                                    except TypeError:
                                        if int(char[0]) == self.caller.id:
                                            continue
                                    try:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                    except IndexError:
                                        continue
                                    except TypeError:
                                        charsearch = search.objects("#" + str(char))[0].name
                                        if self.caller.account.search(charsearch) is not None:
                                            sendlist.append(self.caller.account.search(charsearch))
                                        continue
                                for receive in sendlist:
                                    receive.msg("You have received a new @mail from the job system.")
                                    new_message = create.create_message(self.caller, str(mailcomment), receivers=receive, header=mailheader)
                                    new_message.tags.add("U", category="mail")
                                checkfile = str(".\\jobdumps\\" + time.strftime("%B") + "_" + time.strftime("%y") + ".txt")
                                if os.path.isdir(".\\jobdumps\\"):
                                    dumpfile = open(checkfile,'a+')
                                else:
                                    dumpfile = open(checkfile,'w+')
                                charlist = []
                                for thing in canceljob:
                                    try:
                                        if isinstance(thing, tuple):
                                            if thing != canceljob[len(canceljob) - 1]: 
                                                charsearch = search.objects('#'+str(thing[0]))[0]
                                                if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                    charlist.append(charsearch.name)
                                                    continue
                                            else:
                                                canceller = charsearch = search.objects('#'+str(thing[0]))
                                                canceller = canceller[0].name
                                                break
                                        else:
                                            charsearch = search.objects('#'+str(thing))[0]
                                            if charsearch is not None and inherits_from(charsearch, DefaultCharacter):
                                                charlist.append(charsearch.name)
                                                continue
                                    except IndexError:
                                        continue
                                if dumpfile.read() != '':
                                    dumpfile.seek(1)
                                    dumpfile.write('\n')
                                dumpfile.write('Job Title: ' + canceljob[0] + ", Submitted On: " + canceljob[2] + ", Deadline: " + canceljob[3] + ", Cancelled By: " + canceller + "\n")
                                for comment in range(4,len(canceljob)):
                                    if isinstance(canceljob[comment], tuple):
                                        charsearch = search.objects('#'+str(canceljob[comment][0]))[0]
                                        dumpfile.write('On '+canceljob[comment][2] + ' ' + charsearch.name + ' wrote \n' + canceljob[comment][1] + "\n\n")
                                dumpfile.write('*--Job Cancelled--*')
                                self.caller.msg("You have cancelled job " + str(bucketindex + 1) + " in the  " + bucketname + " bucket.")
                                handlervar.db.joblist[bucketindex].remove(canceljob)
                                
                            else:
                                self.caller.msg("You have to add a comment to cancel a job.")
                                return
                        else:
                            self.caller.msg("Invalid bucket.")
                            return
                else:
                    self.caller.msg("Only staff can cancel jobs.")
                    return
            elif switches[0].upper() in str(handlervar.db.buckets.keys()):
                #Checks to see if the command is some variant of, "+job/<bucket>"
                bucketkey = switches[0].upper()
                try:
                    jobnumber = int(args)
                except ValueError:
                    self.caller.msg("You have to enter a number to check a job.")
                    return
                checkbucket = handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1]
                if len(bucketkey) % 2 == 0:
                #Checks to see if the bucket's name is of an even length.
                    header = "/" + "-" * (36 - len(bucketkey)/2) + bucketkey.upper() + " Job" + "-" * (36 - len(bucketkey)/2) + "\\\n"
                    header += "|| # " + " " * 12 + "Title" + " " * 11 + "  Submitted On   " + "  Submitted By   " + " Due Date  " + "||\n"
                else:
                    header = "/" + "-" * (35 - len(bucketkey)/2) + bucketkey.upper() + " Job" + "-" * (36 - len(bucketkey)/2) + "\\\n"
                    header += "|| # " + " " * 12 + "Title" + " " * 11 + "  Submitted On   " + "  Submitted By   " + " Due Date  " + "||\n"
                jobbody = ""
                finalbody = ""
                jobrow = ""
                for job in checkbucket:
                # Iterates through the bucket itself.
                    injob = False
                    # Assumes that the individual is not in fact, the job's originator or added to the job.
                    if job[1] != self.caller.id and (not self.caller.IsAdmin()):
                    # Checks to see if the job's creator is the person who's calling the command.
                        for person in range(4, len(job)):
                        # Iterates through the entries after the initial job's data. Items 0-3 are, in order:
                        # the title of the job, the ID of the submitter, the date of the job's submission, the deadline of the job, and then the initial
                        # comment submitted with the job as a tuple. The tuple's items are: The comment's submitter, the comment's body, and the timestamp.
                            if job[person] == self.caller.id:
                            # Checks to see if the item itself is a single item equal to the caller's ID.
                                injob = True
                                # If that is in fact the case, then mark that the character is on the job and stop the iterating loop.
                                break
                    else:
                    # In the event that the character is in fact, the submitter of the job, note that they're on the job.
                        injob = True
                    try:
                        if not injob:
                        # If you're not in the job, the below code block checks to see if it's the last item.
                        # If it is, it sends an error message. If it's not, it 
                            if checkbucket.index(job) == int(jobnumber) - 1:
                                self.caller.msg("This isn't your job.")
                                return
                            else:
                                continue
                        if checkbucket.index(job) < (int(jobnumber) - 1):
                            continue
                    except ValueError:
                        self.caller.msg("That's not a valid job number!")
                        return
                    # The above bit is here on account of the fact that everything below it is for writing the job-specific information. Ergo, if
                    # this isn't the right job then that shouldn't be done and one should move on.
                    try:
                    # Searches for the job's submitter. This try/except block is here to make sure
                    # that the character still exists. If they don't, the error exception sets the
                    # submitter's name to, 'Unfindable'.
                        submitter = search.objects("#" + str(job[1]))[0].name
                    except IndexError:
                        submitter = "Unfindable"
                    jobrow = "||"
                    if (handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1].index(job) + 1) < 10:
                        jobrow += " "
                        jobrow += str(handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1].index(job) + 1)
                        jobrow += " "
                    elif (handlervar.db.joblsit.index(job) + 1) > 9:
                        jobrow += " "
                        jobrow += (handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1].index(job) + 1)
                    elif (handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1].index(job) + 1) > 99:
                        jobrow += str(handlervar.db.joblist[handlervar.db.buckets[bucketkey] - 1].index(job) + 1)
                    # The above if/elif block adds an appropriate amount of spaces around the job number.
                    titlecrop = str(job[0])[:28]
                    # This crops the title of the job for the width of the title space.
                    if len(titlecrop) % 2 == 0:
                        jobrow += " " * (14 - len(titlecrop) / 2) + titlecrop + " " * (14 - len(titlecrop) / 2)
                    else:
                        jobrow += " " * (13 - len(titlecrop) / 2) + titlecrop + " " * (14 - len(titlecrop) / 2)
                    # Checks to see if the title is of even or odd length, spaces accordingly.
                    if len(job[2]) % 2 == 0:
                        jobrow += " " * (8 - len(job[2]) / 2) + job[2] + " " * (9 - len(job[2]) / 2)
                    else:
                        jobrow += " " * (8 - len(job[2]) / 2) + job[2] + " " * (8 - len(job[2]) / 2)
                    # Provides spacing for the submission date.
                    if len(submitter) % 2 == 0:
                        jobrow += " " * (8 - len(submitter) / 2) + submitter + " " * (9 - len(submitter) / 2)
                    else:
                        jobrow += " " * (8 - len(submitter) / 2) + submitter + " " * (8 - len(submitter) / 2)
                    # Provides spacing for the submitter's name.
                    if len(job[3]) % 2 == 0:
                        jobrow += " " * (5 - len(job[3]) / 2) + job[3] + " " * (6 - len(job[3]) / 2)
                    else:
                        jobrow += " " * (5 - len(job[3]) / 2) + job[3] + " " * (5 - len(job[3]) / 2)
                    # Provides spacing for the deadline.
                    jobrow += " " * (78 - len(jobrow)) + "||\n"
                    # Adds the remaining spaces to the job.
                    jobbody += jobrow
                    jobrow = ""
                    if checkbucket.index(job) == int(jobnumber) - 1:
                        break
                    # Checks to see if you've found the job you're looking for.
                    if checkbucket.index(job) > (int(jobnumber) - 1):
                        break
                    # Checks to see if you've gone past the job you're looking for. If so, it stops the loop.
                if int(jobnumber) > len(checkbucket):
                    self.caller.msg("There aren't that many jobs in that bucket!")
                    return
                if not injob:
                    self.caller.msg("This isn't your job.")
                    return
                # Considering that the default state of whether or not the character is on the job is, 'False'
                # the above block will stop the command if the job that it stopped on is past the integer input.
                finalbody += jobbody
                jobbody = ""
                bodylength = len(finalbody)
                for person in range(4, len(job)):
                    try:
                        if len(job[person]) > 1:
                            continue
                    except TypeError:
                        charsearch = search.objects("#" + str(job[person]))[0]
                        if charsearch:
                            pass
                        else:
                            charsearch = "Unfindable"
                        if bodylength == len(finalbody):
                            finalbody += "|| Participants: " + submitter + ", " + charsearch.name
                        else:
                            finalbody += ", " + charsearch.name
                if len(finalbody) != bodylength:
                    finalbody += " " * (78 - (len(finalbody) - bodylength)) + "||\n"
                for comment in range(4, len(job)):
                    try:
                        charsearch = search.objects("#" + str(job[comment][0]))[0]
                        finalbody += "+---" + charsearch.name + "-" * 5 + job[comment][2] + "-" * (77 - len("+---" + charsearch.name + "-----" + job[comment][2])) + "+\n"
                        textwrap = wrap(job[comment][1], 76)
                        for text in textwrap:
                            finalbody += "||" + text + " " * (76 - len(text)) + "||\n"
                    except TypeError:
                        continue
                    except IndexError:
                        continue
                footer = "\\" + "-" * 76 + "/"
                self.caller.msg(header + finalbody + footer)
                return
        elif args:
            if not switches:
                if self.args.upper() in handlervar.db.buckets.keys():
                    for tag in handlervar.db.buckets.keys():
                        if tag == self.args.upper():
                            viewbucket = tag
                            break
                    bucketindex = handlervar.db.buckets[viewbucket] - 1
                    header = "/" + "-" * (35 - len(viewbucket)/2) + viewbucket + " Jobs" + "-" * (36 - len(viewbucket)/2) + "\\\n"
                    header += "|| # " + " " * 12 + "Title" + " " * 11 + "  Submitted On   " + "  Submitted By   " + " Due Date  " + "||\n"
                    row = ""
                    body = ""
                    for job in handlervar.db.joblist[bucketindex]:
                        injob = False
                        if job[1] != self.caller.id and (not(self.caller.IsAdmin())):
                            for person in range(4,len(job)):
                                if job[person] == self.caller.id:
                                    injob = True
                                    break
                        else:
                            injob = True
                        if not injob:
                            continue
                        try:
                            submitter = search.objects("#"+str(job[1]))[0].name
                        except IndexError:
                            submitter = "Unfindable"
                        row += "||"
                        if (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) < 10:
                            row += " " + str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) + " "
                        elif 100 > (handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1) > 9:
                            row += " " + str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                        else:
                            row += str(handlervar.db.joblist[handlervar.db.buckets[tag] - 1].index(job) + 1)
                        titlecrop = job[0][:28]
                        if len(titlecrop) % 2 == 0:
                            row += " " * (14 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                        else:
                            row += " " * (13 - len(titlecrop)/2) + titlecrop + " " * (14 - len(titlecrop)/2)
                        if len(job[2]) % 2 == 0:
                            row += " " * (8 - len(job[2])/2) + job[2] + " " * (9 - len(job[2])/2)
                        else:
                            row += " " * (8 - len(job[2])/2) + job[2] + " " * (8 - len(job[2])/2)
                        if len(submitter) % 2 == 0:
                            row += " " * (8 - len(submitter)/2) + submitter + " " * (9 - len(submitter)/2)
                        else:
                            row += " " * (8 - len(submitter)/2) + submitter + " " * (8 - len(submitter)/2)
                        if len(job[3]) % 2 == 0:
                            row += " " * (5 - len(job[3])/2) + job[3] + " " * (6 - len(job[3])/2)
                        else:
                            row += " " * (5 - len(job[3])/2) + job[3] + " " * (5 - len(job[3])/2)
                        row += " " * (78 - len(row)) + "||\n"
                        body += row
                        row = ""
                    footer = "\\" + "-" * 76 + "/"
                    self.caller.msg(header + body + footer)
                    return
                else:
                    self.caller.msg("You need to select a bucket to view a specific job, or the jobs within a bucket.")
                    return
            
        else:
            self.caller.msg("Please use +help +myjobs to see the commands for using the job system.")
            return
        
class RequestCommand(default_cmds.MuxCommand):
    """
    Used to open a job to ask staff to do something be it spend your XP,
    run a plot, or something else entirely.
    
    Usage:
        +request/<
    """
    key = "+request"
    aliases = "+req"
    def func(self):
        args = self.args
        switches = self.switches
        lhs = self.lhs
        rhs = self.rhs
        handlervar = search.scripts('JobHandler')
        try:
            handlervar = handlervar[0]
        except IndexError:
            handlervar = create_script('world.jobs.JobHandler',key='JobHandler',persistent=True)
            self.caller.msg("Jobs system initialized.")
        try:
            jobchan = search.channels('Jobs')[0]
        except IndexError:
            jobchan = create_channel('Jobs',desc='A channel for announcing incoming jobs to staff.',locks='control:perm(Developer);listen:perm(Admin);send:false()')
        if args:
            if not switches:
                date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                gen_deadline = datetime.date.today() + datetime.timedelta(days=7)
                gen_deadline = gen_deadline.strftime("%a %b %d")
                commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                try:
                    handlervar.db.joblist[handlervar.db.buckets['GEN'] - 1].append([lhs,self.caller.id,date,gen_deadline,tuple([self.caller.id,rhs,commenttime])])
                    self.caller.msg("Request submitted with the title: " + lhs + " to the general jobs category.")
                    jobchan.msg(self.caller.name + " has submitted a request to the GEN bucket with the name: "+lhs)
                    return
                except KeyError:
                    handlervar.db.buckets['GEN'] = len(handlervar.db.buckets) + 1
                    handlervar.db.joblist.append([])
                    handlervar.db.deadlines.append(['7'])
                    handlervar.db.joblist[handlervar.db.buckets['GEN'] - 1].append([lhs,self.caller.id,date,gen_deadline,tuple([self.caller.id,rhs,commenttime])])
                    self.caller.msg("Request submitted with the title: " + lhs + " to the general jobs category.")
                    jobchan.msg(self.caller.name + " has submitted a request to the GEN bucket with the name: "+lhs)
                    return
            else:
                if switches[0].upper() in handlervar.db.buckets.keys():
                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                    deadline = datetime.date.today() + datetime.timedelta(days=int(handlervar.db.deadlines[handlervar.db.buckets[switches[0].upper()] - 1]))
                    deadline = deadline.strftime("%a %b %d")
                    commenttime = date + " at " + time.strftime("%I").strip("0") + ":" + time.strftime("%M") + " " + time.strftime("%p")
                    handlervar.db.joblist[handlervar.db.buckets[switches[0].upper()] - 1].append([lhs,self.caller.id,date,deadline,tuple([self.caller.id,rhs,commenttime])])
                    self.caller.msg("Request submitted with the title " + lhs + " to the " + switches[0].upper() + " category.")
                    jobchan.msg(self.caller.name + " has submitted a request to the " + switches[0].upper() + " bucket with the name: "+lhs)
                    return
                else:
                    self.caller.msg("Invalid bucket.")
                    return