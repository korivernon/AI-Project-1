from board import Board, readFromFile, stats, makeMove, AStar

INP1 = "inp/Input1.txt"
INP2 = "inp/Input2.txt"
INP3 = "inp/Input3.txt"
SO = "inp/Sample_Output.txt"

left = 1;left_up = 2;up = 3; right_up = 4; right = 5; right_down = 6; down = 7; left_down = 8

'''
    Need to use a dictionary so that if flag = True, then we append 
        the dictionary key to a list, then return that list to init.py
    Need a function to compare the current node to the previous 
        constantly in the while t loop
'''

def main():
    # initialize test board
    # testBoard = Board("test.txt")

    pre, post = readFromFile(SO)
    print(pre, post, sep="\n\n")

    result, nodes= AStar(pre, post)
    numMoves = 0

    print("goal:\n{}\npre:\n{}".format(post, pre))


    if (not result):
        print("No soln")
    else:
        print(result.pre)

        t = result.parent
        prev = t
        while t:
            numMoves +=1
            t = t.parent

    output(pre, post, numMoves, nodes)

    stats(pre, post)
    makeMove(pre, post)


    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
