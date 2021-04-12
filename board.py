from function import *
import copy
#from functools import reduce
#from operator import mul
import numpy as np
BLANK = 0

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
                h += abs(x-i) + abs(y-j)
        return h

'''
Used for A* Implementation
   parent represents the parent of the current Node
   position represents the current position of the Node on the board
   g is cost from start to current Node
   h is heuristic based estimated cost for the current Node to end Node
   f is total cost of present node i.e. : f(n) = g(n) + h(n)
'''

# return_path function will return the path of the search
def return_path(curr_node, board):
    path = []

    rows, columns = np.shape(board.pre)

    #initializing the result board maze with -1 in every position
    result = [[-1 for i in range (columns)] for j in range (rows)]
    current = curr_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # return the reversed path to show start to end
    path = path[::-1]
    start_value = 0
    # updating the path of the A* implementation by incrementing by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result

# search function will return a list of tuples as a path from given start to end
def search(board, cost, start, end):
    # initializing values of g, h, and f
    start_node = Board(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Board(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # all nodes that have yet to be visited will be placed here
    yet_to_visit_list = []

    # all nodes that have already been visited will be placed here to avoid redundancy
    visited_list = []

    # adding the start nde to the beginning
    yet_to_visit_list.append(start_node)

    # stop condition to avoid an infinite loop
    outer_iterations = 0
    max_iterations = (len(board) // 2) ** 10

    # this represents the search movements of every position : go up, go left, go down, go right, diagonals
    move = [[-1, 0], [0, -1], [1, 0], [0, 1],
            [-1, -1], [-1, 1], [1, -1], [1, 1]]

    # assigns the dimension of the board to rows and columns
    rows, columns = np.shape(board.pre)

    # loop that will continue until it reaches the end of the board
    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

        # current node
        curr_node = yet_to_visit_list[0]
        curr_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < curr_node.f:
                curr_node = item
                curr_index = index

        if outer_iterations > max_iterations:
            print("Done pathfinding, too many iterations occurred")
            return return_path(curr_node,board)

        # removing the current node from yet_to_visit_list
        yet_to_visit_list.pop(curr_index)
        # appending it to the visited list to avoid visting that node again
        visited_list.append(curr_node)

        # if the goal has been reached then return the path, otherwise keep going
        if curr_node == end_node:
            return return_path(curr_node, board)

        # Generate children from all adjacent squares
        children = []
        for new_position in move:

            # Node position
            node_position = (curr_node.position[0] + new_position[0],
                             curr_node.position[1] + new_position[1])

            # Checking if they are within range or not
            if (node_position[0] > (rows -1) or node_position[0] < 0
                    or node_position[1] > (columns-1) or node_position[1] < 0):
                continue

            if board[node_position[0]][node_position[1]] != 0:
                continue

            # creating a new node and appending it to children
            new_node = Board(curr_node, node_position)
            children.append(new_node)

            # Iterate through children
            for child in children:
                # If child is in visited_list then search
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                # once again initializing f,g, and h values
                child.g = curr_node.g + cost

                # calculating the heuristic cost
                child.h = (((child.position[0] - end_node.posiiton[0]) ** 2) +
                           ((child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h

                # If child is already in yet_to_visit_list and g cost is lower, append
                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue
                yet_to_visit_list.append(child)


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
    '''
    # well this took forever and a day
    for board in boardList:
        print(board)
    '''
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
    openList.append(start)

    numNodes = 0
    while openList:
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
                    move.f = move.g + move.h
                    move.parent = current
                    openList.append(move)

    return None, numNodes
