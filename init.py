from board import Board, readFromFile, stats, makeMove

INP1 = "inp/Input1.txt"
INP2 = "inp/Input2.txt"
INP3 = "inp/Input3.txt"

def main():
    # initialize test board
    # testBoard = Board("test.txt")

    pre, post = readFromFile(INP1)
    print(pre, post, sep="\n\n")

    stats(pre, post)
    makeMove(pre, post)


    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
