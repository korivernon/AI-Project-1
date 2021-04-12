from board import Board, readFromFile, stats, makeMove, AStar

INP1 = "inp/Input1.txt"
INP2 = "inp/Input2.txt"
INP3 = "inp/Input3.txt"
SO = "inp/Sample_Output.txt"

def output(pre, post, nodes, len):
    outFile = "{}\n\n{}\n\n{}\n{}".format(pre, post, nodes, len)
    print(outFile)
def main():
    # initialize test board
    # testBoard = Board("test.txt")

    pre, post = readFromFile(SO)
    #print(pre, post, sep="\n\n")

    result, nodes= AStar(pre, post)
    numMoves = 0


    if (not result):
        print("No soln")
    else:
        #print(result.pre)
        t = result.parent
        while t:
            numMoves +=1
            print(t.pre)
            t = t.parent
            try:
                continue
                print(t.f)
            except AttributeError:
                continue
    output(pre, post, nodes, numMoves)

    # stats(pre, post)
    # makeMove(pre, post)


    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
