from board import Board, printPretty
PRE = "pre"
POST = "post"

def runTests(board):
    '''
    Test the output of the board
    '''
    print("Printing Initial Condition:")
    printPretty(board.pre)
    print("Printing Goal Condition:")
    printPretty(board.post)

def main():
    # initialize test board
    testBoard = Board("test.txt")
    valid = Board("valid.txt")
    # print pretty the pre and post condition
    valid.stats()

    #runTests(testBoard)
main()
