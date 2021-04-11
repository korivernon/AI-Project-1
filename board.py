from function import *
import copy
BLANK = "BLANK"

class Board:
    def __init__(self, board = []):
        self.pre = board #pre refers to the board -> pre should be board. changing in the future
        self.availability = [] #list of tuples with available spaces that the space can move
        self.blank = getBlankTup(self.pre , self.availability) #get the blank tuple if possible and determine avail

    def __str__(self):
        st = ''
        for i in range(len(self.pre)):
            line = self.pre[i]
            st += "\t".join( [str(x) for x in line] )
            if i != len(self.pre)-1:
                st = st + '\n'
        return st

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.f = 0
        self.h = 0
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node, board):
    path = []
    no_rows, no_columns =
    result = [[-1 for i in range (no_columns)] for j in range (no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    start_value = 0
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result

def search(board, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0
    yet_to_visit_list = []
    visited_list = []
    yet_to_visit_list.append(start_node)
    outer_iterations = 0
    max_iterations = (len(board) // 2) ** 10

    #go up, go left, go down, go right
    move = [[-1,0],[0,-1], [1,0], [0,1]]

    no_rows, no_columns = np.shape(board)

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("Done pathfinding, too many iterations occurred")
            return return_path(current_node,board)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node, board)

        # Generate children from all adjacent squares
        children = []
        for new_position in move:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if (node_position[0] > (no_rows -1) or node_position[0] < 0 or node_position[1] > (no_columns-1) or node_position[1] < 0):
                continue

            if board[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

            for child in children:
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                child.g = current_node.g + cost
                child.h = (((child.position[0] - end_node.posiiton[0]) ** 2) +((child.position[1] - end_node.position[1]) ** 2))

                child.f = child.g + child.h

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
    preBoard, postBoard = [],[]
    inFile = open(filename, "r")
    count = 0
    pre =  [];post =[]
    for line in inFile:
        count += 1
        line = line.strip().split(); line = parseLine(line) #split by space and convert from string to integer
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
        preBoard.sort(); postBoard.sort() #sort the lists then compare
        if not (preBoard == postBoard ):
            inFile.close()
            return False
    except TypeError:
        pass
    try:
        lenBoard = len(postBoard)-1
    except IndexError:
        lenBoard = 'null'
    finally:
        # check if boards are valid
        pre = Board(pre); post = Board(post) #create board objects
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
        elif heur > nextHeur:
            boardList = [] # completely throw out the others
            boardList.append(temp)
            heur = nextHeur
        elif heur == nextHeur:
            boardList.append(temp)
    '''
    # well this took forever and a day
    for board in boardList:
        print(board)
    '''
    return boardList


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