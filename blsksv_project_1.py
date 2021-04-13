from function import *
import copy
import numpy as np
import math
SO = "inp/Sample_Output.txt"

BLANK = 0
LOWER = 0
UPPER = 3

class Board:
    def __init__(self, board = [], parent= None, position = None):
        self.pre = board #pre refers to the board -> pre should be board. changing in the future
        self.availability = [] #list of tuples with available spaces that the space can move
        self.blank = getBlankTup(self.pre , self.availability) #get the blank tuple if possible and determine avail
        self.parent = parent
        self.position = position
        self.nodes = 0
        self.f = 0
        self.g = 0
        self.h = 0

    def __str__(self):                              #this is for string representation.
        st = ''
        for i in range(len(self.pre)):
            line = self.pre[i]
            st += "\t".join( [str(x) for x in line] )
            if i != len(self.pre)-1:
                st = st + '\n'
        return st

    def __repr__(self):
        st = ''
        for i in range(len(self.pre)):
            line = self.pre[i]
            st += "\t".join( [str(x) for x in line] )
            if i != len(self.pre)-1:
                st = st + '\n'
        return st

    def __eq__(self, other):
        return self.pre == other.pre

    def getAvailability(self):
        self.blank = getBlankTup(self.pre , self.availability) #get the blank tuple if possible and determine avail

class Tile:
    def __init__(self, x, y, curr, goal = None):
        self.x = x
        self.y = y
        self.val = curr
        self.goal = goal

    def addGoal(self, goal): #if we need to add a goal, we have an option to do so
        self.goal = goal
        return True

    def __str__(self):
        st = "x: {}, y: {}, val: {}, goal: {}".format(self.x, self.y, self.val, self.goal)
        return st

'''
Used for A* Implementation
   parent represents the parent of the current node
   position represents the current position of the node on the board
   g is cost from start to current node
   h is heuristic based estimated cost for the current node to end node
   f is total cost of present node i.e. : f(n) = g(n) + h(n)
'''
def readFromFile(filename):
    '''
    readFromFile is passed a filename in the format
    that we expect. Everything from the file
    will be stored in a two dimensional array.
    :return: ( <Board> , <Board> )
    '''
    preBoard, postBoard = [], []
    inFile = open(filename, "r")
    count = 0
    pre = [] ; post = []
    for line in inFile:
        count += 1
        line = line.strip().split() ; line = parseLine(line) # split by space and convert from string to integer
        if not checkLine(line):
            print("\n\t\tRow: {}".format(count))
            print("\tFilename with error present: {}\n".format(filename))
        if count < 5:
            pre.append(line)
            preBoard += line
        elif count > 5:
            post.append(line)
            postBoard += line
    # check if boards are valid
    pre = Board(pre); post = Board(post) # create board objects
    inFile.close()
    return pre, post #return tuple

def readAndLoadFromFile(filename):
    pre = []; goal = []
    inFile = open(filename, "r")
    for y, line in enumerate(inFile):
        elems = []
        line = line.strip().split()
        line = parseLine(line)

        if y < 4:
            for x, item in enumerate(line):
                curr = Tile(x,y, item)
                elems.append(curr)
            pre.append(elems)
        elif y > 4:
            goal.append(line)
    for y, line in enumerate(pre):
        for x, tile in enumerate(line):
            tile.addGoal(goal[y][x])
    inFile.close()
    pre = Board(pre)
    return pre

def stats(curr, goal):
    '''
    ouput the statistics of the current board with the goal board
    :param curr: current Board
    :param goal: goal Board
    :return:
    '''
    print("==========Statistics==========")
    print("\t->Blank Location: {}".format(curr.blank))
    print("\t->Availability:")
    for i in range(len(curr.availability)):
        print("\t\t\t{}".format(curr.availability[i]))
    print("\t->h(x) = {}".format(compareBoard(curr, goal)))
    print("=======End of Statistics======")

def makeMove(curr, goal):
    '''
    make a move based on the current state of the board
    and then return a list of the boards with the best
    heuristic.
    :param curr: current Board
    :param goal: goal Board
    :return: [ <Board> ]
    '''
    heur = -1
    boardList = []
    for tup in curr.availability:
        base = copy.deepcopy(curr.pre) # create a copy
        temp = swap(base, curr.blank, tup)
        nextHeur = compareBoard(temp, goal)
        if heur == -1:
            heur = nextHeur
            boardList.append(temp)
            curr.nodes += 1
        elif heur > nextHeur:
            boardList = [] # completely throw out the others
            boardList.append(temp)
            curr.nodes += 1
            heur = nextHeur
        elif heur == nextHeur:
            boardList.append(temp)
            curr.nodes += 1
    return boardList

def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if(item.f < f):
            f = item.f
            index  = i

    return openList[index], index

def swap(cond, before, after):
    '''
    swaps the position when passed a conditon, the before tuple, and the after tuple
    :param cond: list
    :param before: tuple containing before coordinates
    :param after: tuple containing after coordinates
    :return: <Board>
    '''
    cond[before[0]][before[1]], cond[after[0]][after[1]] = cond[after[0]][after[1]], cond[before[0]][before[1]]
    temp = Board(cond)
    return temp

def compare(curr, goal):
    return curr.pre == goal.pre

def AStar(start, goal):
    openList = []
    closedList = []
    print("start\n" + str(start))
    #print(type(start))
    openList.append(start)

    numNodes = 0
    while openList:
        print(openList[0])
        current, index = best_fvalue(openList)
        if compare(current, goal):
            #print(numNodes)
            return current, numNodes
        openList.pop(index)
        closedList.append(current)

        X = makeMove(current, goal)
        for move in X:
            numNodes+=1
            ok = False   #checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:              #not in closed list
                newG = current.g + 1
                present = False

                #openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan()
                    #print(move.h)
                    move.f = move.g + move.h
                    move.parent = current
                    openList.append(move)

    return None, numNodes

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
    retDict = {}

    #check upZ
    up = loc[0] > LOWER
    down = loc[0] < UPPER
    left = loc[1] > LOWER
    right = loc[1] < UPPER
    if up:
        retLst.append(
            (loc[0]-1, loc[1])
        )
        retDict[3] = retLst[-1]
    #check down
    if down:
        retLst.append(
            (loc[0]+1, loc[1])
        )
        retDict[7] = retLst[-1]
    #check left
    if left:
        retLst.append(
            (loc[0], loc[1]-1)
        )
        retDict[1] = retLst[-1]
    #check right
    if right:
        retLst.append(
            (loc[0], loc[1]+1)
        )
        retDict[5] = retLst[-1]
    # check left up
    if up and left:
        retLst.append(
            (loc[0] - 1, loc[1] -1 )
        )
        retDict[2] = retLst[-1]
    #check right up
    if up and right:
        retLst.append(
            (loc[0] - 1, loc[1] + 1 )
        )
        retDict[4] = retLst[-1]
    # check left down
    if down and left:
        retLst.append(
            (loc[0] + 1, loc[1] - 1)
        )
        retDict[8] = retLst[-1]
    #check right down
    if down and right:
        retLst.append(
            (loc[0] + 1, loc[1] + 1)
        )
        retDict[6] = retLst[-1]
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

def main():
    pre = readFromFile(SO)
    print(pre)
    pre = readAndLoadFromFile(SO)
    print(pre)
main()
