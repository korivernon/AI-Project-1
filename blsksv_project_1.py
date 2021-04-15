import copy
import math

BLANK = 0; LOWER = 0; UPPER = 3

class Board:
    def __init__(self, board, position=None):
        if position == None: #determine whether this is the first instance. if it is, then we
            self.pre = board #this stores the contents of the board on the first iteration
            self.parent = None # the parent is set to none by default if it is the first
            self.position = None # the position is set to None by default if it is the first
            self.g = 0 # this is the depth
            self.h = self.manhattan() #this is how the heuristic is calculated
            self.f = self.h + self.g # f(n) is calculated f = g + h
            self.blank,self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail
        else:
            self.pre = board.pre # on the second iteration, we are being passed the 2d tile list
            self.position = position #saving the last position
            self.move() #call the move function to use the position that was stored to move
            self.parent = copy.deepcopy(self.pre) #preserve the parent board
            self.g = board.g + 1 #increment the depth by one because we are going down
            self.h = self.manhattan() #call manhattan to get the manhattan distances between goal
            self.f = self.g + self.h #calculate f(n)
            self.blank,self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail

    def __str__(self):                              #this is for string representation to help with output
        st = ''
        for i in range(len(self.pre)):
            line = self.pre[i]
            st += "\t".join([str(x) for x in line])
            if i != len(self.pre)-1:
                st = st + '\n'
        return st

    def getBlank(self):#this obtains the blank space
        for tile in self.pre:
            if tile.val == 0:
                return tile

    def flatten(self):
        flatten = []  # flatten the list to easily parse
        for line in self.pre:
            flatten.extend(line)

        return flatten

    def manhattan(self): #this obtains the manhattan distances between tiles
        total = 0
        currTile = None; goalTile = None
        flat = self.flatten()
        for i in range(len(flat)):
            for tile in flat:
                if (tile.val == i):
                    currTile = tile #find the location of the tile
                if (tile.goal == i):
                    goalTile = tile # we can just use rise over run instead of absolute value x2-x1/y2-y1?
            total += abs(currTile.x - goalTile.x) + abs(currTile.y - goalTile.y) #how to alter for diag..?
        return total

    def move(self):
        self.blank, self.availability = getBlankTup(self.pre)  # get the blank dict if possible and determine avail
        try:
            after = self.availability[self.position] # tuple that has the location we want to swap with
        except KeyError:
            return
        self.swap_placement(self.blank, after)

    def swap_placement(self, before, after): #we want to swap the values at this point,
                                            # NOT the entire file, because we want the goal to remain static
        self.pre[before[0]][before[1]].val, self.pre[after[0]][after[1]].val = self.pre[after[0]][after[1]].val, self.pre[before[0]][before[1]].val

class Tile:
    def __init__(self, x, y, curr, goal = None): #when initializing the starting board, we will have to add the gaol at a later time
        self.x = x; self.y = y #get the x and y values
        self.val = curr; self.goal = goal #initialize the value and the goal

    def addGoal(self, goal): #if we need to add a goal, we have an option to do so
        self.goal = goal #add the goal later so we can keep track of both the goal and the value in the same ds

    def __str__(self): #string representation so in order to see exactly what is happening
        st = "x: {}, y: {}, val: {}, goal: {}\t\t|".format(self.x, self.y, self.val, self.goal)
        return st

def readAndLoadFromFile(filename):
    pre = []; goal = [] #pre represents the start, and goal represents the goal
    try:
        inFile = open(filename, "r") #we are first going to try to open the file
    except FileNotFoundError:
        return False #if we are unable to open the file, exit the code
    for y, line in enumerate(inFile): #using enumerate so we can keep track of the y value, as well as line elements
        elems = [] #adding line by line
        line = line.strip().split() #splitting by space and stripping new line character
        line = parseLine(line) #separate the line into a list of integers
        if y < 4:
            for x, item in enumerate(line): # create the two dimensional array
                curr = Tile(x,y, item) #add as a tile object where item == value
                elems.append(curr) #append to the elems == line
            pre.append(elems) #append the elems to the starting node
        elif y > 4:
            goal.append(line) #we can just append this to goal, then go back in the future and add it as a goal
    for y, line in enumerate(pre):
        for x, tile in enumerate(line):
            tile.addGoal(goal[y][x]) #adding the goal at goal[y][x]
    inFile.close() #closing file because we are done
    pre = Board(pre) #creating a board object to return
    return pre

def getBlankTup(cond): #this will get the blank tuple for us, storing the coordinates of the blank
    for i in range(len(cond)):
        for j in range(len(cond[i])):
            if cond[i][j].val == BLANK: #we want to see if the tile at this point is None
                avail = checkAvail((i, j)) #we are checking availability at this point
                return (i, j), avail #returning a tuple of the return objects
    return (-1, -1), {}

def checkAvail(loc ):
    retLst = []
    retDict = {}
    up = loc[0] > LOWER #so we can check to see if the upper is clear
    down = loc[0] < UPPER #so we can check to see if the lower is clear
    left = loc[1] > LOWER #so we can check to see if the left is clear
    right = loc[1] < UPPER # so we can check to see if the right is clear
    #check up
    if up:
        retLst.append(
            (loc[0]-1, loc[1])
        )
        retDict[3] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    #check down
    if down:
        retLst.append(
            (loc[0]+1, loc[1])
        )
        retDict[7] = retLst[-1]  #simply taking the value at -1 index and adding to the dictionary with the directional value
    #check left
    if left:
        retLst.append(
            (loc[0], loc[1]-1)
        )
        retDict[1] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    #check right
    if right:
        retLst.append(
            (loc[0], loc[1]+1)
        )
        retDict[5] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    # check left up
    if up and left:
        retLst.append(
            (loc[0] - 1, loc[1] -1 )
        )
        retDict[2] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    #check right up
    if up and right:
        retLst.append(
            (loc[0] - 1, loc[1] + 1 )
        )
        retDict[4] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    # check left down
    if down and left:
        retLst.append(
            (loc[0] + 1, loc[1] - 1)
        )
        retDict[8] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    #check right down
    if down and right:
        retLst.append(
            (loc[0] + 1, loc[1] + 1)
        )
        retDict[6] = retLst[-1] #simply taking the value at -1 index and adding to the dictionary with the directional value
    return retDict

def search(start):
    numNodes = 1 #initial number of nodes created starts with root node
    openList = [start] #initializes an open list with the initial board
    while len(openList) > 0:
        currBoard = openList[0] #assigning a default board
        for i, board in enumerate(openList):
            if board.f < currBoard.f:
                currBoard = board # if the f(n) value is more favorable, replace it
            elif board.f == currBoard.f and board.h < currBoard.h: # if the same f(n) is present, but h is deeper, swap priority
                currBoard = board
            for b in openList: #remove the board from the list
                if b.pre == currBoard.pre:
                    openList.remove(b)
                    break
            if currBoard.h == 0:
                return currBoard, numNodes
            for key, value in currBoard.availability.items():
                newBoard = Board(currBoard, key)         #creates new node
                openList.append(newBoard)
                numNodes += 1
    return None, None

def findBestf(board):
    f_lst = [] #have a list to store the f values
    positions = [] #list to store positions
    curr = board #set the current to the board
    while curr.parent != None: #continue until we reach the root
        f_lst.append(curr.f) #append the current f value
        positions.append(curr.positions)
        curr = curr.parent # go back by one node and traverse
    f_lst.append(curr.f); f_lst.reverse() #reverse the the positions list so we go forward
    positions.reverse() #reverse the the positions list so we go forward
    return f_lst, positions #return the tuple

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

def init_board_with_file_and_run(filename):
    start = readAndLoadFromFile(filename)
    if start == False:
        return False
    goal, numNodes = search(start) # starts the search
    f_lst, positions = findBestf(goal) #obtain the output from backtrack
    st = output(board, board.g, numNodes, positions, f_lst) #this will give us our intended output in the form of a string

    newFilename = filename[:filename.find(".")] + "_ASTAR_OUTPUT.txt" #have a set output name for ease of use
    print(st, newFilename) #print the value of the string to the filename

    return True

def output(board, shallowest_node, numNodes, directions, f_lst):
    st = ""
    # output the starting board
    for y, line in enumerate(board):
        line = board[y]
        st += "\t".join([str(x.val) for x in line])
        if i != len(self.pre)-1:
            st = st + '\n'
    st += '\n' #output the new line character
    for y, line in enumerate(board):
        line = board[y]
        st += "\t".join([str(x.goal) for x in line])
        if i != len(self.pre)-1:
            st = st + '\n'
    ending = "{}\n{}\n{}\n{}".format(shallowest_node, numNodes, " ".join(directions), " ".join(f_lst))
    st += ending
    return st

def valid_filename(filename):
    cond = filename[-4:-1] == ".txt" or filename == "q" # we want to check to see if we received a valid input
    if cond:
        return True
    return True

def main():
    while 1:
        filename = input("Please enter the filename you would like to perform the A Star Search on (q to quit): ")
        while not valid_filename(filename):
            filename = input("Please enter the filename you would like to perform the A Star Search on (q to quit): ")
            print()
        if filename == "q": #if you want to quit then return break the loop
            print("\nGoodbye.")
            break
        if not init_board_with_file_and_run(filename):
            print("Invalid input given.") #if this function returns false, this is an invalid input
            print()
        else:
            print("Output given in {}".format(filename[:filename.find(".")] + "_ASTAR_OUTPUT.txt")) # this is where the output is given
main()
