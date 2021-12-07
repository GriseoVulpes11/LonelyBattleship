"""
Name: Cooper Brown
Date: 12/4/2021

Description: A Simple battleship game using tkinter against a moderately competent AI player

Sample runs: sample Photos on GitHub as well as a .exe file
https://github.com/GriseoVulpes11/LonelyBattleship/blob/master/README.md
Sources:
Heavy Use of Metallidogs tkinter strategies https://github.com/Metallidog/Battleship/blob/master/battleship.py
Functions:

I seperated
this project into two classes the first class is the one that creates the board  using the create player and create AI
boards, Both utilize a click handler function that is passed all information to initiate a recursive loop Data

The second class creates an AI that will fire at the player better than random chance and will place ships on its own
board . It seems to have a bias towards the top of the board  though. These are passed little information as little is
needed outside the class creation

Structures:

My program is extremely reliant on nested lists, the nested list is what determines the text on the buttons as well
as where the battleships are on both sides I utilize nested loops so often i created a function to create them called
create nested

Recent Topics:
Classes allow the recursive loop that allows the program to be responsive, as well as have the AI act intelligently
The GUI is what is used to play the game
"""


import copy
import random
from functools import partial
from tkinter import *
import tkinter.messagebox

root = Tk()
root.wm_title("SEA BATTLE")

class board :  # Class to create the board s
    def __init__(self, root, size, aiShips, playerShips):
        self.tk = root  # Defines the in class root value
        self.size = size  # Defines the size of the board
        self.__hiddenAiboard  = aiShips  # The board  for the AI battleships
        self.__hiddenPlayerboard  = playerShips  # The player board
        self.ocean = " "
        self.numOfPlayerShips = 0
        self.shotList = []
        self.AiHit = False
        """
        Creates a board  for the player on the top half of the screen, suing a for loop to create a grid and a click handler to regester clicks
        """

    def createPlayerboard (self, activeboard , playerChoose=False):
        def onClick(rowNum, colNum, activeboard , size, aiShips, playerShips, numOfPlayerShips):  # defines the click handler
            if not activeboard [rowNum][colNum] == "+":
                activeboard [rowNum][colNum] = "+"
            board (root, size, aiShips, playerShips).createPlayerboard (activeboard )

        # Creates board  in the space of the nested loop

        rowNum = 0
        for row in activeboard :
            colNum = 0
            for col in row:
                Button(self.tk, text=col, bg="sky blue",
                       command=partial(onClick, rowNum, colNum, activeboard , self.size, self.__hiddenAiboard ,
                                       self.__hiddenPlayerboard , self.numOfPlayerShips + 1 ),width=2).grid(
                    row=rowNum, column=colNum)
                colNum += 1
            Label(self.tk, text="    ").grid(row=self.size, column=rowNum)
            rowNum += 1

    """
    Creates A board  for the ai on the bottom half of the screen, this board  takes attacks,
    the click handler starts the ai attacking the player board  
    """

    def createAIboard (self, activeboard ):  # Creates board  in the space of the nested loop
        def onClick(rowNum, colNum, activeboard , size, aiShips, playerShips, shotList,
                    self):  # defines the click handler
            if aiShips[rowNum][colNum] == "+":
                activeboard [rowNum][colNum] = "X"
            else:
                activeboard [rowNum][colNum] = "O"
            ai = aiBehavor(None, size)
            aiShot = ai.aiShot(shotList, self.AiHit)

            if self.__hiddenPlayerboard [aiShot[-1][0]][aiShot[-1][1]] == "+":
                self.__hiddenPlayerboard [aiShot[-1][0]][aiShot[-1][1]] = "X"
                self.AiHit = True
            else:
                self.__hiddenPlayerboard [aiShot[-1][0]][aiShot[-1][1]] = "O"
                self.AiHit = False
            if not any('+' in x for x in self.__hiddenPlayerboard ):
                Label(root, text="YOU HAVE LOST")
            if not any('+' in x for x in aiShips):
                Label(root, text="YOU HAVE WON")
            board (root, size, aiShips, playerShips).createPlayerboard (self.__hiddenPlayerboard )
            board (root, size, aiShips, playerShips).createAIboard (activeboard )  # refreshes board

        rowNum = 0
        for row in activeboard :
            colNum = 0
            for col in row:
                Button(self.tk, text=col, bg="pale violet red",
                       command=partial(onClick, rowNum, colNum, activeboard , self.size, self.__hiddenAiboard ,
                                       self.__hiddenPlayerboard , self.shotList, self),width=2).grid(row=rowNum + self.size + 1,
                                                                                           column=colNum)
                colNum += 1
            rowNum += 1


"""
This class defines the behavor of the ai, placing ships and attacking the player mostly 
"""


class aiBehavor:
    def __init__(self, hiddenAiboard , size):
        self.ship_list = [5, 4, 3, 3, 2]  # List of ships the ai uses to place their ships
        self.numberboard  = copy.deepcopy(hiddenAiboard )  # a second board  used in placing battleships
        self.aiboard  = hiddenAiboard
        self.boardSize = size
        self.ocean = " "

    """
    Checks if the space in the ai board  defined as self.aiboard  is empty based on a given row and col 
    """

    def is_ocean(self, r, col):  # true if ocean

        if r < 0 or r >= self.boardSize:
            return 0
        elif col < 0 or col >= self.boardSize:
            return 0
        if self.aiboard [r][col] == self.ocean:
            return 1
        else:
            return 0

    """
    Places Ships
    """

    def placeShips(self, set_ship=None):
        import random
        def randomCol(orientation, size):  # puts the ship in a random col
            if orientation:
                return random.randint(0, size - 1)
            else:
                return random.randint(size - 1, size - 1)

        def randomRow(orientation, size):  # put the ship in a random row
            if orientation:
                return random.randint(0, size - size)
            else:
                return random.randint(0, size - 1)

        """lines 130 to 144 are checking if the board  is empty in certan spots to place each ship in the list of ships 
        defined in the __init__ function """

        for size in self.ship_list:
            orientation = random.randint(0, 2)
            occupied = True
            while occupied:
                occupied = False
                ship_row = randomRow(orientation, size)
                ship_col = randomCol(orientation, self.boardSize)
                if orientation:
                    for p in range(size):
                        if not aiBehavor.is_ocean(self, ship_row + p, ship_col):
                            occupied = True
                else:
                    for p in range(size):
                        if not aiBehavor.is_ocean(self, ship_row, ship_col - p):
                            occupied = True
            """
            The below codeblock places ships on the ai nested list 
            """
            if orientation:
                self.aiboard [ship_row][ship_col] = "+"
                self.aiboard [ship_row + size - 1][ship_col] = "+"
                if set_ship is not None:
                    self.numberboard [ship_row][ship_col] = set_ship
                    self.numberboard [ship_row + size - 1][ship_col] = set_ship
                for p in range(size - 2):
                    self.aiboard [ship_row + p + 1][ship_col] = "+"
                    if set_ship is not None:
                        self.numberboard [ship_row + p + 1][ship_col] = set_ship
            else:
                self.aiboard [ship_row][ship_col] = "+"
                self.aiboard [ship_row][ship_col - size + 1] = "+"
                if set_ship is not None:
                    self.numberboard [ship_row][ship_col] = set_ship
                    self.numberboard [ship_row][ship_col - size + 1] = set_ship
                for p in range(size - 2):
                    self.aiboard [ship_row][ship_col - p - 1] = "+"
                    if set_ship is not None:
                        self.numberboard [ship_row][ship_col - p - 1] = set_ship
        return self.aiboard

    def aiShot(self, shotList, aiHit):

        def checkAlready(shotsTaken, shotList):  # function to check if any instance in the list of shots randomly
            # found have already been taken
            returnList = []
            for cord in shotList:
                if cord in shotsTaken:
                    pass
                else:
                    returnList.append(cord)
            return returnList

        if aiHit:  # If there has been a hit the last turn the following is run
            hitShot = shotList[-1]
            shots = []
            for x in range(4):
                shots.append((hitShot[0] + 1, hitShot[1]))
                shots.append((hitShot[0] - 1, hitShot[1]))
                shots.append((hitShot[0], hitShot[1] + 1))
                shots.append((hitShot[0], hitShot[1] - 1))
            shots = checkAlready(shotList, shots)
            return shots[random.randint(1, len(shots) - 1)]

        if len(shotList) > 10:  # Creates a list of random cords to hit in a diagonal pattern returns one of them at
            # random; only runs if there have been less than 10 shots
            possibleDiagShots = []
            for x in range(self.boardSize):
                possibleDiagShots.append((x, x))
                possibleDiagShots.append((self.boardSize - x, x))
            diagShots = checkAlready(shotList, possibleDiagShots)
            Shot = diagShots[random.randint(1, len(possibleDiagShots) - 1)]
            shotList.append(Shot)
            return shotList

        else:  # creates a list of cords to hit in a checkerd pattern for after 10 shots
            try:
                checkersShots = []
                for x in range(self.boardSize):
                    if x % 2 == 0:
                        for i in range(self.boardSize):
                            if i % 2 == 0:
                                checkersShots.append((i, x))
                    else:
                        for i in range(self.boardSize):
                            if not i % 2 == 0:
                                checkersShots.append((i, x))
                checker = checkAlready(shotList, checkersShots)
                CheckerShot = checker[random.randint(1, len(checker) - 1)]
                shotList.append(CheckerShot)
                return shotList
            except: # Begins returning random spots, only runs after the above runs out of shots to take extremely
                # taxing to the computer
                backup = []
                for x in range(self.boardSize):
                    for i in range(self.boardSize):
                        backup.append(i, x)
                backup = checkAlready(shotList, backup)
                backupShot = backup[random.randint(1, len(checker) - 1)]
                shotList.append(backupShot)
                return shotList


def createNested(size):
    nested = []
    for x in range(size):
        l = []
        for i in range(size):
            l.append(" ")
        nested.append(l)
    return nested


size = 10

aiboard  = createNested(size)
hiddenPlayerboard  = createNested(size)
hiddenAiboard  = createNested(size)

ai = aiBehavor(hiddenAiboard , size)
aiShipboard  = ai.placeShips()

b = board (root, size, aiShips=aiShipboard , playerShips=hiddenPlayerboard )
b.createPlayerboard (hiddenPlayerboard , playerChoose=True)


def onIntroClick(): #Shows Intro Message
    tkinter.messagebox.showinfo("Welcome Sea Battle","First Place You battleships on the blue board wherever you want \nattack the AI by clicking in the red board \nBy Cooper Brown")

#Button To show intro message
Button(root, text="Show Intro Message",command=onIntroClick).grid(row=10, column=1000)

b.createAIboard (aiboard )

root.mainloop()
