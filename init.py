from board import Board, readFromFile, stats, makeMove

def main():
    # initialize test board
    # testBoard = Board("test.txt")
    pre, post = readFromFile("valid.txt")
    print(pre, post, sep="\n")
    # stats(pre, post)
    makeMove(pre, post)
    # invalid = Board("invalid.txt")
    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
