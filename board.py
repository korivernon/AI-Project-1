from function import *
import copy
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
        self.pre = board
        self.availability = []
        self.blank = getBlankTup(self.pre , self.availability)

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

    precondition -> filename
    postcondition -> 2D data array
    return: list
    '''
    preBoard, postBoard = [],[]
    inFile = open(filename, "r")
    count = 0
    pre =  [];post =[]
    for line in inFile:
        count += 1
        line = line.strip().split(" ")
        line = parseLine(line) #convert from string to integer


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
    pre = Board(pre)
    post = Board(post)

    try:
        # try popping the blank space

        preBoard.pop(preBoard.index(BLANK)); postBoard.pop(postBoard.index(BLANK))
        preBoard.sort(); postBoard.sort()
        # print(preBoard) ; print(postBoard)
        if not (preBoard == postBoard ):
            inFile.close()
            return False
    except TypeError:
        doNothing = ""
    finally:
        inFile.close()
        return pre, post

def stats(pre, goal):
    print("==========Statistics==========")
    print("\t->Blank Location: {}".format(pre.blank[0]))
    print("\t->Availability:")
    for i in range(len(pre.availability)):
        print("\t\t\t{}".format(pre.availability[i]))
    print("\t->h(x) = {}".format(compareBoard(pre, goal)))
    print("=======End of Statistics=======")

def makeMove(curr, post):
    heur = -1
    boardList = []
    for tup in curr.availability:
        base = copy.deepcopy(curr.pre) # create a copy
        temp = swap(base, curr.blank, tup)
        checker = compareBoard(temp, post)
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


def swap(cond, before, after):
    cond[before[0]][before[1]], cond[after[0]][after[1]] = cond[after[0]][after[1]], cond[before[0]][before[1]]
    temp = Board(cond)

    return temp