from function import *

class Board:
    def __init__(self, filename = ""):
        self.pre = []
        self.post = []
        self.valid = False
        self.availability = []
        if filename != "":
            self.filename = filename
            self.valid = readFromFile(filename, self.pre, self.post)
            if self.valid:
                self.blank = (getBlankTup(self.pre, self.availability), getBlankTup(self.post))
        else:
            self.filename = filename
            if self.valid == False:
                self.blank = (
                    (-1,-1),
                    (-1,-1)
                )
                print("Board init Failure: You have given an invalid file input.\n")

    def stats(self):
        print("==========Statistics==========")
        print("\t->Blank Location: {}".format(self.blank[0]))
        print("\t->Availability:")
        for i in range (len(self.availability)):
            print("\t\t\t{}".format(self.availability[i]))
        print("\t->h(x) = {}".format(compareBoard(self.pre, self.post)))
        print("=======End of Statistics=======")

    def loadBoard(self, filename):
        self.filename = filename
        self.valid = readFromFile(self.filename, self.pre, self.post)
        if self.valid:
            self.blank = (getBlankTup(self.pre), getBlankTup(self.post))

    def printPretty(self, mode= "pp"):
        '''
        Print 2D array prettily
        '''
        if self.valid == True:
            if mode == "pp":
                print("Printing Initial Condition:")
                printPretty(self.pre)
                print("Printing Post Condition:")
                printPretty(self.post)
            elif mode == "pre":
                print("Printing Initial Condition:")
                printPretty(self.pre)
            else:
                print("Printing Post Condition:")
                printPretty(self.post)
        else:
            print("printPretty() Error: Improper file input given.")


