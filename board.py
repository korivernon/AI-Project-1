from function import *
import copy
import numpy as np
BLANK = 0
import math

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

    def __str__(self):
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

    def manhattan(self):
        h = 0
        for i in range(len(self.pre)):
            for j in range(len(self.pre)):
                x, y = divmod(self.pre[i][j], 3)
                #print(x, y, len(self.pre))
                h += abs(x-i) + abs(y-j)
                h += abs(x-i) + abs(y-j)
        return h

def calculateManhattan(curr, goal):
    initial_config = curr.pre
    manDict = 0
    for i,item in enumerate(initial_config):
        prev_row,prev_col = int(i/ 4) , i % 4
        goal_row,goal_col = int(item /4),item % 4
        manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
    return manDict
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
    try:

        preBoard.pop(preBoard.index(BLANK)); postBoard.pop(postBoard.index(BLANK)) # try popping the blank space
        preBoard.sort(); postBoard.sort() # sort the lists then compare
        if not (preBoard == postBoard):
            inFile.close()
            return False
    except TypeError:
        pass
    try:
        lenBoard = len(postBoard)
    except IndexError:
        if lenBoard > 15:
            lenBoard = 'null'
    finally:
        # check if boards are valid
        pre = Board(pre); post = Board(post) # create board objects
        inFile.close()
        return pre, post #return tuple

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
