# AI-Project-1
Implement the A* Search Algorithm with Graph Search for solving the 15- puzzle problem as described below. Use sum of chessboard distances of tiles from their goal positions as heuristic function, where chessboard distance is defined as the maximum of the horizontal and vertical distances.

Partners: Bethany Saunders and Kori Vernon

## Instructions:

In order to run our program, you will need any modern Python compiler. There are multiple ways to run the program (We recommend IDLE). Once you open the file, execute it and then enter in the input file the form of a `*.txt` file. The input file will be loaded into the program, and it will perform the A* Algorithm using Manhattan Distance heuristic. If the user would like to quit the program before entering the filename they must type “q” to exit the program. Otherwise the program will run the provided text filename to perform the A* Search.

In order to compile the program, we suggest using the system module in python3.

## How this program works:

Our program takes in a 2-Dimensional list of `Tile` objects, which is passed to the `Board` class as the `board` parameter. In our Board class, we take in two parameters, `board`, and `position= None`. If the board being initialized is the root, we initialize this Board differently than if it is a child node, and we know that the board is the root if the default parameters are maintained. The Manhattan distances function is run, the depth is determined, f(n) is calculated, the blank is calculated, and a dictionary of valid places where the board can move is calculated. All of this occurs on the initialization of a `Board` object. 
  
## Shortfalls/Issues:

We are confident that we are on the right track in terms of the progression of the program. However, the `manhattan()` function does not work as expected. It calculates the Manhattan distance for Up, Down, Left, Right, but excludes the diagonal moves. Furthermore, the `search()` function in the `blsksv_project_1.py` file does not work as expected. The program does not progress, and instead stays stuck in a loop, going over the same element in the `openList`. We have followed the pseudo code in order to try to overcome this issue, however, to no avail. We continued the program and implemented the functions as we expected the code to work, should the `search()` and `manhattan()` functions work as expected. The output file text would be as expected in the instructions, however, due to the bug, there is no output. Please refer to the code for more information on how we implemented the A* algorithm. 

## Output File Text:
`<Nothing>`

