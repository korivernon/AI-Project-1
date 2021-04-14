from function import *
import copy
import numpy as np
import math
SO = "inp/Sample_Output.txt"
import sys

BLANK = 0
LOWER = 0
UPPER = 3

class Board:
    def __init__(self, board, position=None):
        if (isinstance(board, list)): #determine whether this is the first instance. if it is, then we
            self.pre = board
            self.parent = None
            self.position = None
            self.g = 0
            self.h = self.manhattan()
            self.f = self.h + self.g
            self.blank,self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail
            print(self.blank)
        else:
            self.position = position #saving the last position
            self.move()
            self.parent = copy.deepcopy(self.pre) #preserve the parent board
            self.g = board.g + 1
            self.h = self.manhattan()
            self.f = self.g + self.h
            self.blank,self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail

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

    def getBlank(self):
        for tile in self.pre:
            if tile.val == 0:
                return tile

    def flatten(self):
        flatten = []  # flatten the list to easily parse
        for line in self.pre:
            flatten.extend(line)

        return flatten

    def manhattan(self):
        total = 0
        currTile = None
        goalTile = None
        flat = self.flatten()
        for i in range(len(flat)):
            for tile in flat:
                if (tile.val == i):
                    currTile = tile
                if (tile.goal == i):
                    goalTile = tile
            total += abs(currTile.x - goalTile.x) + abs(currTile.y - goalTile.y) #how to alter for diag..?
        return total

    def move(self):
        self.blank, self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail
        after = self.availability[self.position] # tuple that has the location we want to swap with
        swap_placement(self.blank, after)

    def swap_placement(self, before, after):
        self.pre[before[0]][before[1]], self.pre[after[0]][after[1]] = self.pre[after[0]][after[1]], self.pre[before[0]][before[1]]

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
        st = "x: {}, y: {}, val: {}, goal: {}\t\t|".format(self.x, self.y, self.val, self.goal)
        return st

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

def swap_placement(cond, before, after):
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

def getBlankTup(cond ):
    '''
    get the precondition or post condition tuple when passed the
    :param cond: precondition tuple
    :return: tuple with the coordinates of the blank space
    '''
    avail = {}
    for i in range(len(cond)):
        for j in range(len(cond[i])):
            if cond[i][j].val == BLANK:
                if (avail != None):
                    #check all sides
                    avail = checkAvail( (i,j) )
                return (i, j), avail
    return (-1,-1) , {}

def checkAvail(loc ):
    retLst = []
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
    return retDict

def search(start):
    numNodes = 1 #initial number of nodes created starts with root node
    openList = [start] #initializes an open list with the initial board
    while len(openList) > 0:
        currBoard = openList[0] #assigning a default board
        for board in openList:
            if board.f < currBoard.f:
                currBoard = board # if the f(n) value is more favorable, replace it
            elif board.f == currBoard.f and board.h < currBoard.h: # if the same f(n) is present, but h is deeper, swap priority
                currBoard = board
            openList.remove(currBoard) #remove the board from the openList
            if currBoard.h == 0:
                return currBoard, numNodes
            for key, value in currBoard.items():
                newBoard = Board(currBoard, key)         #creates new node
                openList.append(newBoard)
                numNodes += 1
    return None, None

def findBestf(board):
    f_lst = []
    positions = []
    curr = board
    while curr.parent != None:
        f_lst.append(curr.f)
        positions.append(curr.positions)
        curr = curr.parent # go back by one node and traverse

    f_lst.append(curr.f); f_lst.reverse()
    positions.reverse()
    return f_lst, positions

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

def init_board_with_file_and_run(filename):
    start = readAndLoadFromFile(filename)
    goal, numNodes = search(start) # starts the search
    f_lst, positions = findBestf(goal)
    st = output(board, board.g, numNodes, positions, f_lst)

    newFilename = filename[:filename.find(".")] + "_ASTAR_OUTPUT.txt"
    print(st, newFilename)

    return True

def output(board, shallowest_node, numNodes, directions, f_lst):
    st = ""
    # output the starting board
    for y, line in enumerate(board):
        line = board[y]
        st += "\t".join([str(x.val) for x in line])
        if i != len(self.pre)-1:
            st = st + '\n'
    st += '\n' #output the new line character
    for y, line in enumerate(board):
        line = board[y]
        st += "\t".join([str(x.goal) for x in line])
        if i != len(self.pre)-1:
            st = st + '\n'
    ending = "{}\n{}\n{}\n{}".format(shallowest_node, numNodes, " ".join(directions), " ".join(f_lst))
    st += ending
    return st

def valid_filename(filename):
    cond = filename[-4:-1] == ".txt" or filename == "q"
    if cond:
        return True
    return True

def main():

    while 1:
        filename = input("Please enter the filename you would like to perform the A Star Search on (q to quit): ")
        while not valid_filename(filename):
            filename = input("Please enter the filename you would like to perform the A Star Search on (q to quit): ")
        if filename == "q":
            break
        init_board_with_file_and_run(filename)
main()
