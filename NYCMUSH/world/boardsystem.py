'''
Created on Jan 26, 2017

@author: CodeKitty
'''

from evennia import default_cmds
from evennia import DefaultScript
from evennia import create_script
from evennia.utils import search
from collections import OrderedDict
from textwrap import wrap
from evennia import DefaultCharacter
import time
class BoardCommand(default_cmds.MuxCommand):
    """
    This command is used to access the board system. It's designed to work similar to boards on many other MUSHes,
    simply for familiarity's sake.
    
    Usage:
        +bbread <Board number> Shows the messages on a given board, provided you can access it.
        +bbread <Board Number>/<Message Number> Shows a message on the board indicated.
        +bbpost <Board Number>/<Title>=<Message> Posts to a certain board with the given title and message.
        +bbremove <Board Number>/<Message Number> As implied, removes a message that you posted from a board.
    """
    key = "+bbread"
    lock = "cmd:all()"
    help_category = "OOC"
    aliases = ["+bbpost","+boards","+board","+bbremove"]
    
    def func(self):
        boardsearch = search.scripts('BoardSystem')
        if not boardsearch:
            create_script("world.boardsystem.BBS",key="BoardSystem",persistent=True)
            self.caller.msg("Board system initialized.")
            boardsearch = search.scripts('BoardSystem')[0]
        else:
            boardsearch = boardsearch[0]
        if self.cmdstring == "+bbread":
            if not self.args:
                board_rows = ""
                boardmessage = "/" + "-" * 36 + "BBS" + "-" * 37 + "\\\n"
                if len(boardsearch.db.boardnames) == 0:
                    board_rows = "||" + " " * 36 + "None" + " " * 36 + "||\n"
                else:
                    hideboard = True
                    boardrow = ""
                    boardrow = ""
                    boardmessage += "|| #" + "  " + " " * 3 + " " * 5 + "Board Title" + " " * 6 + "  Posts  " + " " * 4 + "Last Poster" + " " * 4 + " " * 4 + "Last Post" + " " * 6 + "||\n"
                    for name in boardsearch.db.boardnames.keys():
                        boardrow += "||"
                        if boardsearch.db.boardnames[name] > 9:
                            pass
                        else:
                            boardrow += " "
                        boardrow += str(boardsearch.db.boardnames[name])
                        if len(boardsearch.db.boardperms[int(boardsearch.db.boardnames[name]) - 1]) > 0:
                            for lock in boardsearch.db.boardperms:
                                if boardsearch.db.boardperms.index(lock) == (boardsearch.db.boardnames[name] - 1):
                                    if "see" in lock:
                                        postlock = lock.split(":")[1]
                                        self.caller.msg(postlock)
                                        if self.caller.locks.check_lockstring(self, "dumm:"+postlock) or self.caller.IsAdmin():
                                            hideboard = False
                                            break
                            if hideboard == True:
                                hideboard = False
                                continue
                        try:
                            for item in boardsearch.db.board[boardsearch.db.boardnames[name] - 1]:
                                if item[1] == self.caller.name:
                                    break
                                elif len(self.caller.db.readmessages[boardsearch.db.boardnames[name] - 1]) < len(boardsearch.db.board[boardsearch.db.boardnames[name] - 1]):
                                    boardrow += "  U  "
                                    break
                                elif not (boardsearch.db.board[boardsearch.db.boardnames[name]].index(item) in self.caller.db.readmessages[boardsearch.db.boardnames[name]]):
                                    boardrow += "  U  "
                                    break
                            if not ("U" in boardrow):
                                boardrow += "     "
                        except IndexError:
                            boardrow += "  U  "
                        boardrow += " " * (10 - (len(name)/2)) + name + " " * (10 - (len(name)/2))
                        try:
                            boardrow += " " * (5 - len(boardsearch.db.board[boardsearch.db.boardnames[name]-1])) + str(len(boardsearch.db.board[boardsearch.db.boardnames[name]-1]))
                            boardrow += " " * (4 - len(boardsearch.db.board[boardsearch.db.boardnames[name]-1]))
                        except IndexError:
                            boardrow += " " * 4 + str(0)
                            boardrow += " " * 4
                        try:
                            boardrow += (" " * (12 - (len(boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][1])/2)) + 
                                         str(boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][1])+
                                         " " * (12 - (len(boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][1])/2)))
                        except IndexError:
                            boardrow += " " * 8 + "None" + " " * 12
                        try:
                            boardrow += " " * (6 - (len(boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][2])/2)) + boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][2] +  " " * (10 - (len(boardsearch.db.board[boardsearch.db.boardnames[name]-1][len(boardsearch.db.board) - 1][2])/2))
                        except IndexError:
                            boardrow += " " * 2 + "Never" + " " * 7
                        boardrow += "||\n"
                        board_rows += boardrow
                        boardrow = ""
                    boardmessage += "+" + "-" * 76 + "+\n"
                boardfooter = "\\" + "-" * 76 + "/"
                self.caller.msg(boardmessage + board_rows + boardfooter)
            else:
                boardmessage = ""
                try:
                    int(self.args)
                    boardrow = ""
                    board_rows = ""
                    lockboard = True
                    boardnamelist = list(boardsearch.db.boardnames.keys())
                    for name in boardnamelist:
                        if len(boardsearch.db.boardperms[int(boardsearch.db.boardnames[name]) - 1]) > 0:
                            for lock in boardsearch.db.boardperms:
                                if boardsearch.db.boardperms.index(lock) == (boardsearch.db.boardnames[name] - 1):
                                    if "see" in lock or "post" in lock or "read" in lock:
                                        postlock = lock.split(":")[1]
                                        if self.caller.locks.check_lockstring(self, "dumm:"+postlock) or self.caller.IsAdmin():
                                            lockboard = False
                                            break
                                
                                if lockboard == True:
                                    self.caller.msg("You can't read this board!")
                                    return
                    try:
                        boardnames = boardsearch.db.boardnames
                        boardname = list(boardsearch.db.boardnames)[int(self.args) - 1]
                        boardindex = boardnames[boardname]
                        thisboard = boardsearch.db.board[boardnames[boardname] - 1]
                        if len(boardname) % 2 == 0:
                            boardmessage += "/" + "-" * (38 - len(boardname)/2) +  boardname + "-" * (38 - len(boardname)/2) + "\\\n"
                        else:
                            boardmessage += "/" + "-" * (38 - len(boardname)/2) +  boardname + "-" * (37 - len(boardname)/2) + "\\\n"
                        boardmessage += "||  #      " + " " * 13 + "Post Name" + " " * 13 + " " * 7 + "Poster" + " " * 7 + " " * 4 + "Date" + " " * 4 + "||\n"
                        boardmessage += "+" + "-"  * 76 + "+\n"
                        try:
                            for post in thisboard:
                                boardrow += "|| " + str(boardindex) + "/"+str(thisboard.index(post) + 1)
                                if thisboard.index(post) + 1 in self.caller.db.readmessages[boardindex - 1] or thisboard[thisboard.index(post)][1] == self.caller.name:
                                    boardrow += " " * (9 - len(boardrow))
                                else:
                                    boardrow += "U" + " " * (9 - len(boardrow))
                                    
                                if len(thisboard[thisboard.index(post)][0]) % 2 == 0:
                                    boardrow += " " * (19 - len(thisboard[thisboard.index(post)][0])/2) + thisboard[thisboard.index(post)][0] + " " * (16 - len(thisboard[thisboard.index(post)][0])/2)
                                else:
                                    boardrow += " " * (28 - len(thisboard[thisboard.index(post)][0])/2) + thisboard[thisboard.index(post)][0] + " " * (16 - len(thisboard[thisboard.index(post)][0])/2)
                                if len(thisboard[thisboard.index(post)][1]) % 2 == 0:
                                    boardrow += " " * (11 - len(thisboard[thisboard.index(post)][1])/2) + thisboard[thisboard.index(post)][1] + " " * (9 - len(thisboard[thisboard.index(post)][1])/2)
                                else:
                                    boardrow += " " * (11 - len(thisboard[thisboard.index(post)][1])/2) + thisboard[thisboard.index(post)][1] + " " * (8 - len(thisboard[thisboard.index(post)][1])/2)
                                if len(thisboard[thisboard.index(post)][2]) % 2 == 0:
                                    boardrow += " " * (7 - len(thisboard[thisboard.index(post)][2])/2) + thisboard[thisboard.index(post)][2] + " " * (4 - len(thisboard[thisboard.index(post)][2])/2)
                                else:
                                    boardrow += " " * (6 - len(thisboard[thisboard.index(post)][2])/2) + thisboard[thisboard.index(post)][2] + " " * (4 - len(thisboard[thisboard.index(post)][2])/2)
                                boardrow += "  ||\n"  
                                board_rows += boardrow
                                boardrow = ""
                        except IndexError:
                            pass
                        boardfooter = "\\" + "-" * 76 +"/"
                        self.caller.msg(boardmessage + board_rows + boardfooter)
                    except IndexError:
                        self.caller.msg("Invalid board.")
                        return
                except ValueError:
                    if "/" in self.args:
                        try:
                            boardnames = boardsearch.db.boardnames
                            boardlist = boardsearch.db.board
                            boardkeys = list(boardnames.keys())
                            boardindex = int(self.args.split("/")[0]) - 1
                            postindex = int(self.args.split("/")[1]) - 1
                            postbody = ""
                            try:
                                posttitle = boardkeys[boardindex]
                                posttext = wrap(boardlist[boardindex][postindex][3],76)
                                postauthor = boardlist[boardindex][postindex][1]
                                postdate = boardlist[boardindex][postindex][2]
                                if len(posttitle) % 2 == 0:
                                    postheader = "/" + "-" * (38 - len(posttitle)/2) + posttitle + "-" * (38 - len(posttitle)/2) + "\\\n"
                                else:
                                    postheader = "/" + "-" * (37 - len(posttitle)/2) + posttitle + "-" * (38 - len(posttitle)/2) + "\\\n"
                                postheader += "|| Post: " + str(boardindex+1) + "/" + str(postindex+1)
                                if len(posttitle) % 2 == 0:
                                    postheader +=  " " * (9 - len(boardlist[boardindex][postindex][0])/2) + "Title: " +boardlist[boardindex][postindex][0] + " " * (11 - len(boardlist[boardindex][postindex][0])/2)
                                else:
                                    postheader += " " * (8 - len(boardlist[boardindex][postindex][0])/2) + "Title: " +boardlist[boardindex][postindex][0] + " " * (11 - len(boardlist[boardindex][postindex][0])/2)
                                if len(postauthor) % 2 == 0:
                                    postheader += " " * (4 - len(postauthor)/2) + "Author: "+ postauthor + " " * (7 - len(postauthor)/2)
                                else:
                                    postheader += " " * (4 - len(postauthor)/2) + "Author: "+postauthor + " " * (7 - len(postauthor)/2)
                                postheader += "Date: " + postdate
                                postheader += " " * (157 - len(postheader)) + "||\n"
                                postheader += "+" + "-" * 76 + "+\n"
                                for item in posttext:
                                    if len(item) == 76:
                                        postbody += "||" + item + "||\n"
                                    else:
                                        postbody += "||" + item + " " * (76 - len(item)) + "||\n"
                                postfooter = "\\" + "-" * 76 + "/"
                                self.caller.msg(postheader + postbody + postfooter)
                                return
                            except ValueError:
                                self.caller.msg("Invalid message index.")
                                return
                        except ValueError:
                            self.caller.msg("Invalid board and message combination.")
                            return
                    else:
                        self.caller.msg("This isn't a valid number to search for.")
                        return
        elif self.cmdstring == "+bbremove":
            if "/" in self.args:
                mainindex = int(self.args.split("/")[0]) - 1
                boardlist = boardsearch.db.board
                try:
                    postindex = int(self.args.split("/")[1]) - 1
                    charactersearch = search.objects(boardlist[mainindex][postindex][1])[0]
                    if charactersearch.account == self.caller.account or self.caller.IsAdmin():
                        self.caller.msg("The message titled "+boardlist[mainindex][postindex][0]+" has been removed.")
                        del boardlist[mainindex][postindex]
                        return
                    else:
                        self.caller.msg("You can't remove a post you didn't create.")
                        return
                except IndexError:
                    self.caller.msg("You need to select a post within a board, if you're going to remove it.")
                    return
                except ValueError:
                    self.caller.msg("That's not a valid post to remove.")
                    return
        elif self.cmdstring == "+bbpost":
        #Quick note. The posts are stored in the format as follows, within a tuple. Title,poster name,date,body.
            if "=" in self.args:
                if len(self.args.split("=")[1]) == 0:
                    self.caller.msg("Your message can't be empty.")
                    return
                if "/" in self.args:
                    board = int(self.args.split("/")[0]) - 1
                    lockboard = True
                    boardnames = list(boardsearch.db.boardnames.keys())
                    for name in boardnames:
                        if len(boardsearch.db.boardperms[int(boardsearch.db.boardnames[name]) - 1]) > 0:
                            for lock in boardsearch.db.boardperms:
                                if boardsearch.db.boardperms.index(lock) == (boardsearch.db.boardnames[name] - 1):
                                    if "see" in lock or "post" in lock:
                                        postlock = lock.split(":")[1]
                                        if self.caller.locks.check_lockstring(self, "dumm:"+postlock) or self.caller.IsAdmin():
                                            lockboard = False
                                            break
                                
                                if lockboard == True:
                                    self.caller.msg("You can't post to this board!")
                                    return
                    date = time.strftime("%a") + " " + time.strftime("%b") + " " + time.strftime("%d")
                    try:
                        boardsearch.db.board[board].append(tuple([self.args.split("/")[1].split("=")[0],self.caller.name,date,self.args.split("/")[1].split("=")[1]]))
                    except IndexError:
                        boardsearch.db.board.append([board].append(tuple([self.args.split("/")[1].split("=")[0],self.caller.name,date,self.args.split("/")[1].split("=")[1]])))
                        try:
                            boardsearch.db.board[board].append(tuple([self.args.split("/")[1].split("="),[0],self.caller.name,date,self.args.split("/")[1].split("=")[1]]))
                        except IndexError:
                            self.caller.msg("Invalid board to post to.")
                            return
                        self.caller.msg("Message posted to "+boardnames[int(self.args.split("/")[0]) - 1] + " as post number " + str(len(boardsearch.db.board[board])))
                        charlist = DefaultCharacter.objects.filter_family()
                        for char in charlist:
                            if char == self.caller:
                                continue
                            elif char.has_account:
                                boardindex = int(self.args.split("/")[0]) - 1
                                if len(boardsearch.db.boardperms[boardindex]) == 0:
                                    char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                    continue
                                for lock in boardsearch.db.boardperms:
                                    if boardindex == boardsearch.db.boardperms.index(lock):
                                        if "see" in lock:
                                            lockeval = lock.split(":")[1]
                                            if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                                char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                                break
                                        elif "post"in lock:
                                            lockeval = lock.split(":")[1]
                                            if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                                char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                                break
                                        elif "read" in lock:
                                            lockeval = lock.split(":")[1]
                                            if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                                char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                                break
                                
                        return
                    self.caller.msg("Message posted to "+boardnames[int(self.args.split("/")[0]) - 1] + " as post number " + str(len(boardsearch.db.board[board])))
                    charlist = DefaultCharacter.objects.filter_family()
                    for char in charlist:
                        if char == self.caller:
                            continue
                        elif char.has_account:
                            boardindex = int(self.args.split("/")[0]) - 1
                            if len(boardsearch.db.boardperms[boardindex]) == 0:
                                char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                continue
                            for lock in boardsearch.db.boardperms:
                                if boardindex == boardsearch.db.boardperms.index(lock):
                                    if "see" in lock:
                                        lockeval = lock.split(":")[1]
                                        if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                            char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                            break
                                    elif "post"in lock:
                                        lockeval = lock.split(":")[1]
                                        if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                            char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                            break
                                    elif "read" in lock:
                                        lockeval = lock.split(":")[1]
                                        if char.locks.check_lockstring(self, "dumm:"+lockeval):
                                            char.msg(self.caller.name +" has posted a new message to "+boardnames[boardindex] + " titled: " + self.args.split("/")[1].split("=")[0])
                                            break
                    return
                else:
                    self.caller.msg("You need to select a title for your message.")
                    return
            else:
                self.caller.msg("You need to have a message in your post.")
        elif self.cmdstring == "+board" or self.cmdstring == "+boards":
            if self.switches:
                if self.caller.IsAdmin():
                    if self.switches[0] == "create":
                        if self.args:
                            try:
                                boardtest = boardsearch.db.boardnames[self.args]
                                self.caller.msg("A board with that name already exists.")
                                return
                            except KeyError:
                                boardsearch.db.boardnames[self.args] = len(boardsearch.db.boardnames) + 1
                                boardsearch.db.boardperms.append([])
                                boardsearch.db.board.append([])
                                self.caller.msg("A board with the name, '"+self.args+"' has been created as board number "+str(len(boardsearch.db.boardnames)))
                                return
                        else:
                            self.caller.msg("Please enter the name of the board you wish to create.")
                            return
                    elif self.switches[0] == "delete" or self.switches[0] == "destroy":
                        if self.args:
                            try:
                                del boardsearch.db.boardnames[self.args]
                                del boardsearch.db.board[boardsearch.db.boardnames[self.args]]
                                self.caller.msg(self.args + " deleted.")
                                return
                            except KeyError:
                                self.caller.msg("There is no such board with that name.")
                                return
                    elif self.switches[0] == "desc":
                        if "=" in self.args:
                            try:
                                boardsearch.db.boarddesc[self.lhs] = self.rhs
                                self.caller.msg("Description for " + self.lhs + " set to " + self.rhs)
                            except KeyError:
                                self.caller.msg("That board doesn't exist.")
                                return
                        else:
                            self.caller.msg("Please enter a description for the board, after an equals sign.")
                            return
                    elif self.switches[0] == "lock":
                        if "=" in self.args:
                            try:
                                boardindex = int(self.args.split("=")[0])
                                boardsearch.db.boardperms[boardindex].append(self.args.split("=")[1])
                                self.caller.msg("Lock added. Format: "+self.args.split("=")[1])
                                return
                            except IndexError:
                                self.caller.msg("You need to select a lock to add.")
                                return
                            except ValueError:
                                self.caller.msg("You need to select a valid board to lock.")
                                return
                        else:
                            self.caller.msg("You need to select a lock to add.")
                            return
                    elif self.switches[0] == "unlock":
                        if "=" in self.args:
                            try:
                                boardindex = int(self.args.split("=")[0]) - 1
                                removelock = str(self.args.split("=")[1])
                                boardnames = boardsearch.db.boardnames.keys()
                                for perm in boardsearch.db.boardperms:
                                    if perm.lower().strip() == removelock.lower().strip():
                                        if boardindex == boardsearch.db.boardperms.index(perm):
                                            boardsearch.db.boardperms[boardindex].remove(perm)
                                            self.caller.msg(perm + " removed.")
                                            return
                                self.caller.msg("Permission not found.")
                            except IndexError:
                                self.caller.msg("You have to input a lock or locks to remove.")
                                return
                        else:
                            self.caller.msg("You have to input a lock or locks to remove.")
                            return
                    
class BBS(DefaultScript):
    
    def at_script_creation(self):
        self.db.board = [[]]
        self.db.boardnames = OrderedDict()
        self.db.boarddesc = OrderedDict()
        self.db.boardperms = [[]]