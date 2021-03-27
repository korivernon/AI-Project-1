from board import Board, readFromFile, stats

def main():
    # initialize test board
    # testBoard = Board("test.txt")
    pre, post = readFromFile("valid.txt")
    print(pre, post, sep="\n")
    stats(pre, post)
    # invalid = Board("invalid.txt")
    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
