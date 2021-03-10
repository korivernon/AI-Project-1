class Board:
    def __init__(self, filename = ""):
        self.pre = []
        self.post = []
        if filename != "":
            self.filename = filename
            readFromFile(filename, self.pre, self.post)
        else:
            self.filename = filename
    def loadBoard(self, filename):
        self.filename = filename
        readFromFile(self.filename, self.pre, self.post)

def readFromFile(filename, pre, post):
    '''
    readFromFile is passed a filename in the format
    that we expect. Everything from the file
    will be stored in a two dimensional array.

    precondition -> filename
    postcondition -> 2D data array
    return: list
    '''
    inFile = open(filename, "r")
    count = 0
    for line in inFile:
        count += 1
        line = line.strip().split(" ")
        line = parseLine(line)
        if count < 5:
            pre.append(line)
        elif count > 5:
            post.append(line)
    inFile.close()
    return True

def parseLine(line):
    for i in range(len(line)):
        try:
            line[i] = int(line[i])
        except ValueError:
            line[i] = line[i]
    return line
def printPretty(param):
    if param != []:
        for i in range(len(param)):
            for j in range(len(param[i])):
                print(param[i][j] + " ", end="", sep=" ")
            print()

def main():
    testBoard = Board("test.txt")
    printPretty(testBoard.pre)
    printPretty(testBoard.post)
main()
