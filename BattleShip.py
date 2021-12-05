import copy
import random
from functools import partial
from tkinter import *

root = Tk()
root.wm_title("SEA BATTLE")


class Bord:
    def __init__(self, root, size, aiShips, playerShips):
        self.tk = root  # Defines the in class root value
        self.size = size
        self.__hiddenAiBord = aiShips
        self.__hiddenPlayerBord = playerShips
        self.ocean = " "
        self.numOfPlayerShips = 0
        self.shotList = []
        self.AiHit = False

    def createPlayerBord(self, activeBord,playerChoose = False):
        def onClick(rowNum, colNum, activeBord, size, aiShips, playerShips,numOfPlayerShips,playerChoose):  # defines the click handler
                if not activeBord[rowNum][colNum]== "+":
                    activeBord[rowNum][colNum] = "+"
                Bord(root, size, aiShips, playerShips).createPlayerBord(activeBord)

        # Creates bord in the space of the nested loop
        
        rowNum = 0
        for row in activeBord:
            colNum = 0
            for col in row:
                Button(self.tk, text=col, bg="sky blue",
                       command=partial(onClick, rowNum, colNum, activeBord, self.size, self.__hiddenAiBord,
                                       self.__hiddenPlayerBord,self.numOfPlayerShips+1,playerChoose)).grid(row=rowNum, column=colNum)
                colNum += 1
            Label(self.tk, text="    ").grid(row=self.size, column=rowNum)
            rowNum += 1

    def createAIBord(self, activeBord):  # Creates bord in the space of the nested loop
        def onClick(rowNum, colNum, activeBord, size, aiShips, playerShips,shotList,self):  # defines the click handler
            if aiShips[rowNum][colNum] == "+":
                activeBord[rowNum][colNum] = "X"
            else:
                activeBord[rowNum][colNum] = "O"
            ai = aiBehavor(None,size)
            aiShot = ai.aiShot(shotList,self.AiHit)

            if self.__hiddenPlayerBord[aiShot[-1][0]][aiShot[-1][1]]== "+":
                self.__hiddenPlayerBord[aiShot[-1][0]][aiShot[-1][1]] = "X"
                self.AiHit = True
            else:
                self.__hiddenPlayerBord[aiShot[-1][0]][aiShot[-1][1]] = "O"
                self.AiHit = False
            if not any('+' in x for x in self.__hiddenPlayerBord):
                Label(root,text= "YOU HAVE LOST")
            if not any('+' in x for x in aiShips):
                Label(root,text="YOU HAVE WON")
            Bord(root,size,aiShips,playerShips).createPlayerBord(self.__hiddenPlayerBord)
            Bord(root, size, aiShips, playerShips).createAIBord(activeBord)  # refreshes bord

        rowNum = 0
        for row in activeBord:
            colNum = 0
            for col in row:
                Button(self.tk, text=col, bg="pale violet red",
                       command=partial(onClick, rowNum, colNum, activeBord, self.size, self.__hiddenAiBord,
                                       self.__hiddenPlayerBord,self.shotList,self)).grid(row=rowNum + self.size + 1,
                                                                      column=colNum)
                colNum += 1
            rowNum += 1


class aiBehavor:
    def __init__(self, hiddenAiBord, size):
        self.ship_list = [5, 4, 3, 3, 2]
        self.numberBord = copy.deepcopy(hiddenAiBord)
        self.aiBord = hiddenAiBord
        self.BordSize = size
        self.ocean = " "

    def is_ocean(self, r, col):  # true if ocean

        if r < 0 or r >= self.BordSize:
            return 0
        elif col < 0 or col >= self.BordSize:
            return 0
        if self.aiBord[r][col] == self.ocean:
            return 1
        else:
            return 0

    def placeShips(self, set_ship=None):
        import random
        def randomCol(orientation, size):
            if orientation:
                return random.randint(0, size - 1)
            else:
                return random.randint(size - 1, size - 1)

        def randomRow(orientation, size):
            if orientation:
                return random.randint(0, size - size)
            else:
                return random.randint(0, size - 1)

        for size in self.ship_list:
            orientation = random.randint(0, 2)
            occupied = True
            while occupied:
                occupied = False
                ship_row = randomRow(orientation, size)
                ship_col = randomCol(orientation, self.BordSize)
                if orientation:
                    for p in range(size):
                        if not aiBehavor.is_ocean(self, ship_row + p, ship_col):
                            occupied = True
                else:
                    for p in range(size):
                        if not aiBehavor.is_ocean(self, ship_row, ship_col - p):
                            occupied = True
            if orientation:
                self.aiBord[ship_row][ship_col] = "+"
                self.aiBord[ship_row + size - 1][ship_col] = "+"
                if set_ship is not None:
                    self.numberBord[ship_row][ship_col] = set_ship
                    self.numberBord[ship_row + size - 1][ship_col] = set_ship
                for p in range(size - 2):
                    self.aiBord[ship_row + p + 1][ship_col] = "+"
                    if set_ship is not None:
                        self.numberBord[ship_row + p + 1][ship_col] = set_ship
            else:
                self.aiBord[ship_row][ship_col] = "+"
                self.aiBord[ship_row][ship_col - size + 1] = "+"
                if set_ship is not None:
                    self.numberBord[ship_row][ship_col] = set_ship
                    self.numberBord[ship_row][ship_col - size + 1] = set_ship
                for p in range(size - 2):
                    self.aiBord[ship_row][ship_col - p - 1] = "+"
                    if set_ship is not None:
                        self.numberBord[ship_row][ship_col - p - 1] = set_ship
        return self.aiBord

    def aiShot(self, shotList,aiHit):

        def checkAlready(shotsTaken, shotList):
            returnList = []
            for cord in shotList:
                if cord in shotsTaken:
                    pass
                else:
                    returnList.append(cord)
            return returnList
        if aiHit:
            hitShot = shotList[-1]
            shots = []
            for x in range(4):
                shots.append((hitShot[0]+1,hitShot[1]))
                shots.append((hitShot[0]-1,hitShot[1]))
                shots.append((hitShot[0] , hitShot[1]+1))
                shots.append((hitShot[0] , hitShot[1]-1))
            shots = checkAlready(shotList,shots)
            return shots[random.randint(1,len(shots)-1)]

        if len(shotList) > 10:
            possibleDiagShots = []
            for x in range(self.BordSize):
                possibleDiagShots.append((x, x))
                possibleDiagShots.append((self.BordSize - x, x))
            diagShots = checkAlready(shotList, possibleDiagShots)
            Shot = diagShots[random.randint(1, len(possibleDiagShots) - 1)]
            shotList.append(Shot)
            return shotList

        else:
            try:
                checkersShots = []
                for x in range(self.BordSize):
                    if x % 2 == 0:
                        for i in range(self.BordSize):
                            if i % 2 == 0:
                                checkersShots.append((i, x))
                    else:
                        for i in range(self.BordSize):
                            if not i % 2 == 0:
                                checkersShots.append((i, x))
                checker = checkAlready(shotList, checkersShots)
                CheckerShot = checker[random.randint(1, len(checker) - 1)]
                shotList.append(CheckerShot)
                return shotList
            except:
                backup = []
                for x in range(self.BordSize):
                    for i in range(self.BordSize):
                        backup.append(i,x)
                backup = checkAlready(shotList,backup)
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

aiBord = createNested(size)
hiddenPlayerbord = createNested(size)
hiddenAiBord = createNested(size)

ai = aiBehavor(hiddenAiBord, size)
aiShipbord = ai.placeShips()

b = Bord(root, size, aiShips=aiShipbord, playerShips=hiddenPlayerbord)
b.createPlayerBord(hiddenPlayerbord,playerChoose=True)

Label(root,text="welcome to SEA BATTLE,\n the blue bord is the player bord  \n you can place your battleships  however you want ").grid(row=1,column=1000)
Label(root,text="click to place your battleships they will appear as a + \n  the ai will place ships according to theoriginal game").grid(row=4,column=1000)
Label(root, text="Click in the red spaces to attack the other ships").grid(row=10,column=1000)


b.createAIBord(aiBord)

root.mainloop()
