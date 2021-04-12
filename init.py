from board import Board, readFromFile, stats, makeMove, AStar

INP1 = "inp/Input1.txt"
INP2 = "inp/Input2.txt"
INP3 = "inp/Input3.txt"
SO = "inp/Sample_Output.txt"

left = 1;left_up = 2;up = 3; right_up = 4; right = 5; right_down = 6; down = 7; left_down = 8

def determine_move(prev,next):
    '''

    :param prev: the previous board
    :param next: the next board
    :return: the direction in which the play moved
    '''

    return None

def output(pre, post, nodes, len):
    outFile = "{}\n\n{}\n\n{}\n{}".format(pre, post, nodes, len)
    print(outFile)
'''
    Need to use a dictionary so that if flag = True, then we append 
        the dictionary key to a list, then return that list to init.py
    Need a function to compare the current node to the previous 
        constantly in the while t loop
'''
def compare():
    if (True):
        print("blah")

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
        prev = t
        while t:
            numMoves +=1
            #print(t.pre)
            t = t.parent
            next = t
            print("prev:\n{}\n\nnext:\n{}".format(prev, next))
            # try:
            #     continue
            #     print(t.f)
            # except AttributeError:
            #     continue
    output(pre, post, numMoves, nodes)

    # stats(pre, post)
    # makeMove(pre, post)


    # print pretty the pre and post condition
    # valid.printPretty()

    #runTests(testBoard)
main()
