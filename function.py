BLANK = "BLANK"
LOWER = 0
UPPER = 3

def getBlankTup(cond, avail = None):
    '''
    get the precondition or post condition tuple when passed the
    :param cond: precondition tuple
    :return: tuple with the coordinates of the blank space
    '''
    for i in range(len(cond)):
        for j in range(len(cond[i])):
            if cond[i][j] == BLANK:
                if (avail != None):
                    #check all sides
                    checkAvail( (i,j) , cond, avail)
                return (i, j)
    return (-1,-1)

def checkAvail(loc, cond, lst ):
    '''
    :param loc: this is the location that we are checking
    :param cond: this is the condition, either pre or post
    :param lst: this is the return list
    :return: None
    '''
    #check up
    if loc[0] > LOWER:
        lst.append(
            (loc[0]-1, loc[1])
        )
    #check down
    if loc[0] < UPPER:
        lst.append(
            (loc[0]+1, loc[1])
        )
    #check left
    if loc[1] > LOWER:
        lst.append(
            (loc[0], loc[1]-1)
        )
    #check right
    if loc[1] < UPPER:
        lst.append(
            (loc[0], loc[1]+1)
        )

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

def printPretty(cond):
    '''
    Print 2D array prettily
    :param cond pre or post condition
    '''
    try:
        if cond != []:
            for i in range(len(cond)):
                try:
                    for j in range(len(cond[i])):
                        print(str(cond[i][j]) + "\t", end="", sep="\t")
                    print()
                except TypeError:
                    return
    except AttributeError:
        return