from board import Board, printPretty


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
    # print pretty the pre and post condition

    runTests(testBoard)
main()
