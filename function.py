BLANK = 0
LOWER = 0
UPPER = 3
import copy
from board import *

def compareBoard(curr, post):
    '''
    get the heuristic of the current board when compared to the
    board at the end
    :param curr: pre condition/current board
    :param post: post condition/goal board
    :return: int
    '''
    count = 0
    for i in range(len(curr.pre)):
        for j in range(len(curr.pre[i])):
            if curr.pre[i][j] != post.pre[i][j]:
                count +=1
    return count

def getBlankTup(cond, avail = None):
    '''
    get the precondition or post condition tuple when passed the
    :param cond: precondition tuple
    :return: tuple with the coordinates of the blank space
    '''
    for i in range(len(cond)):
        for j in range(len(cond[i])):
            if cond[i][j] == BLANK:
                if (avail != None):
                    #check all sides
                    avail = checkAvail( (i,j) , avail)
                return (i, j)
    return (-1,-1)

def checkAvail(loc, retLst ):
    '''
    :param loc: this is the location that we are checking
    :param cond: this is the condition, either pre or post
    :param lst: this is the return list
    :return: None
    '''

    #check up
    up = loc[0] > LOWER
    down = loc[0] < UPPER
    left = loc[1] > LOWER
    right = loc[1] < UPPER
    if up:
        retLst.append(
            (loc[0]-1, loc[1])
        )
    #check down
    if down:
        retLst.append(
            (loc[0]+1, loc[1])
        )
    #check left
    if left:
        retLst.append(
            (loc[0], loc[1]-1)
        )
    #check right
    if right:
        retLst.append(
            (loc[0], loc[1]+1)
        )
    # check left up
    if up and left:
        retLst.append(
            (loc[0] - 1, loc[1] -1 )
        )
    #check right up
    if up and right:
        retLst.append(
            (loc[0] - 1, loc[1] + 1 )
        )
    # check left down
    if down and left:
        retLst.append(
            (loc[0] + 1, loc[1] - 1)
        )
    #check right down
    if down and right:
        retLst.append(
            (loc[0] + 1, loc[1] + 1)
        )
    return retLst

def checkLine(line):
    retBool = True
    for i in range(len(line)):
        num = line[i]
        try:
            if not (num <= 15 and num >= 0):
                print("readFromFile() Error:\n\tIncorrect value(s) given on:\n\t\tColumn: {}".format(i+1), end="")
                retBool = False
        except TypeError:
            continue
    return retBool

def parseLine(line):
    '''
    Given a line, parse the line and
    convert all of the items to integers
    if possible
    precondition -> lst(string)
    postcondition -> lst(int) if possible
    return: lst(int) if possible
    '''
    for i in range(len(line)):
        try:
            line[i] = int(line[i])
            if line[i] == 0:
                line[i] = BLANK
        except ValueError:
            line[i] = line[i]
    return line

def printPretty(cond):
    '''
    Print 2D array prettily
    :param cond pre or post condition
    '''
    try:
        if cond != []:
            for i in range(len(cond)):
                try:
                    for j in range(len(cond[i])):
                        print(str(cond[i][j]) + "\t", end="", sep="\t")
                    print()
                except TypeError:
                    return
    except AttributeError:
        return
