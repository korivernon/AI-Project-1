from function import *
import copy
BLANK = "BLANK"
'''
there needs to be  a change... so basically, the boards should 
be loaded in... the self.post functionality has to be removed 
and implemented outside of the function so that we can refer to boards
arbitrarily INSTEAD of using a list... remove dual functionality in Board 
class
... fixed (:
'''
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
    print("\t->Blank Location: {}".format(curr.blank[0]))
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
        checker = compareBoard(temp, goal)
        if heur == -1:
            heur = checker
            boardList.append(temp)
        elif heur > checker:
            boardList = temp # completely throw out the  others
            heur = checker
        elif heur == checker:
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