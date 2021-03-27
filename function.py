BLANK = "BLANK"

def getBlankTup(cond):
    '''
    get the precondition or post condition tuple when passed the
    :param cond: precondition tuple
    :return: tuple with the coordinates of the blank space
    '''
    for i in range(len(cond)):
        for j in range(len(cond[i])):
            if cond[i] == BLANK:
                return (i, j)

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
        line = parseLine(line) #convert from string to integer
        if not checkLine(line):
            print("\n\tRow: {}".format(count))
            print("Filename with error present: {}\n".format(filename))
        if count < 5:
            pre.append(line)
        elif count > 5:
            post.append(line)
    inFile.close()
    return True

def checkLine(line):
    retBool = True
    for i in range(len(line)):
        num = line[i]
        try:
            if not (num <= 15 and num >= 1):
                print("Incorrect value(s) given on:\n\tColumn: {}".format(i+1), end="")
                retBool = False
        except TypeError:
            continue
    return retBool

def parseLine(line):
    '''
    Given a line, parse the line and
    convert all of the items to integers
    if possible
    precondition -> lst(string)
    postcondition -> lst(int) if possible
    return: lst(int) if possible
    '''
    for i in range(len(line)):
        try:
            line[i] = int(line[i])
            if line[i] == 0:
                line[i] = BLANK
        except ValueError:
            line[i] = line[i]
    return line

def printPretty(param):
    '''
    Print 2D array prettily
    '''
    try:
        if param != []:
            for i in range(len(param)):
                try:
                    for j in range(len(param[i])):
                        print(str(param[i][j]) + "\t", end="", sep="\t")
                    print()
                except TypeError:
                    return
    except AttributeError:
        return