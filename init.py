from board import Board, readFromFile, stats, makeMove

def main():
    # initialize test board
    # testBoard = Board("test.txt")
    pre, post = readFromFile("inp/input1.txt")
    print(pre, post, sep="\n\n")

    stats(pre, post)
    makeMove(pre, post)

    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
