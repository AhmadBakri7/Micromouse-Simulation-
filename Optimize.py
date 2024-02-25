import API
import sys
from Position import Position
import time
from queue import Queue
TOP = 0 
RIGHT = 1 
BOTTOM = 2 
LEFT =3

SLEEP_TIME = 0

mouseFace = {
    0:"Top",
    1:"Right" ,
    2:"Bottom",
    3:"Left" 
}

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def getOptions(currentDirection, COLUMN, ROW):
    options = []
    if currentDirection == TOP:
        if not API.wallRight():
            options.append((COLUMN+1, ROW, RIGHT))
        if not API.wallLeft():
            options.append((COLUMN-1, ROW, LEFT))
        if not API.wallFront():
            options.append((COLUMN, ROW+1, TOP))
        if not (COLUMN == 0 and  ROW == 0):
            options.append((COLUMN, ROW-1, BOTTOM))
    elif currentDirection == RIGHT:
        if not API.wallRight():
            options.append((COLUMN, ROW-1, RIGHT))
        if not API.wallLeft():
            options.append((COLUMN, ROW+1,LEFT))
        if not API.wallFront():
            options.append((COLUMN+1, ROW, TOP))
        options.append((COLUMN-1, ROW, BOTTOM))
    elif currentDirection == LEFT:
        if not API.wallRight():
            options.append((COLUMN, ROW+1, RIGHT))
        if not API.wallLeft():
            options.append((COLUMN, ROW-1, LEFT))
        if not API.wallFront():
            options.append((COLUMN-1, ROW, TOP))
        options.append((COLUMN+1, ROW, BOTTOM))
    elif currentDirection == BOTTOM:
        if not API.wallRight():
            options.append((COLUMN-1, ROW, RIGHT))
        if not API.wallLeft():
            options.append((COLUMN+1, ROW, LEFT))
        if not API.wallFront():
            options.append((COLUMN, ROW-1, TOP))
        options.append((COLUMN, ROW+1, BOTTOM))
    return options

def getBestOption(maze, currentDirection, COLUMN, ROW):
    currentPosition = maze[str(COLUMN) + "_" + str(ROW)]
    options = []
    if currentDirection == TOP:
        if not  currentPosition.RIGHT :
            options.append((maze[str(COLUMN+1) + "_" + str(ROW)], 1))
        if not currentPosition.LEFT:
            options.append((maze[str(COLUMN-1) + "_" + str(ROW)], 3))
        if not currentPosition.TOP:
            options.append((maze[str(COLUMN) + "_" + str(ROW+1)], 0))
        if not currentPosition.BOTTOM:
            options.append((maze[str(COLUMN) + "_" + str(ROW-1)], 2))

    if currentDirection == BOTTOM:
        if not  currentPosition.RIGHT :
            options.append((maze[str(COLUMN+1) + "_" + str(ROW)], 3))
        if not currentPosition.LEFT:
            options.append((maze[str(COLUMN-1) + "_" + str(ROW)], 1))
        if not currentPosition.TOP:
            options.append((maze[str(COLUMN) + "_" + str(ROW+1)], 2))
        if not currentPosition.BOTTOM:
            options.append((maze[str(COLUMN) + "_" + str(ROW-1)], 0))

    if currentDirection == RIGHT:
        if not  currentPosition.RIGHT :
            options.append((maze[str(COLUMN+1) + "_" + str(ROW)], 0))
        if not currentPosition.LEFT:
            options.append((maze[str(COLUMN-1) + "_" + str(ROW)], 2))
        if not currentPosition.TOP:
            options.append((maze[str(COLUMN) + "_" + str(ROW+1)], 3))
        if not currentPosition.BOTTOM:
            options.append((maze[str(COLUMN) + "_" + str(ROW-1)], 1))

    if currentDirection == LEFT:
        if not  currentPosition.RIGHT :
            options.append((maze[str(COLUMN+1) + "_" + str(ROW)], 2))
        if not currentPosition.LEFT:
            options.append((maze[str(COLUMN-1) + "_" + str(ROW)], 0))
        if not currentPosition.TOP:
            options.append((maze[str(COLUMN) + "_" + str(ROW+1)], 1))
        if not currentPosition.BOTTOM:
            options.append((maze[str(COLUMN) + "_" + str(ROW-1)], 3))
    

    options.sort(key = lambda x : x[0].floodValue)
    return options[0][1]

def floodFill(mazeArray, startColumn, startRow):
    queue = Queue()
    queue.put((startColumn, startRow))

    while not queue.empty():
        col, row = queue.get()
    
        currentBlock = mazeArray[str(col) + "_" + str(row)]
        rightIndex = str(col+1) + "_" + str(row)
        leftIndex = str(col-1) + "_" + str(row)
        topIndex = str(col) + "_" + str(row+1)
        bottomIndex = str(col) + "_" + str(row-1)

        if rightIndex in mazeArray.keys() and (mazeArray[rightIndex].traversed) == False and (currentBlock.RIGHT == False):
            mazeArray[rightIndex].traversed = True
            mazeArray[rightIndex].floodValue = currentBlock.floodValue +1
            queue.put((col+1, row))
        if leftIndex in mazeArray.keys() and (mazeArray[leftIndex].traversed == False) and (currentBlock.LEFT == False):
            mazeArray[leftIndex].traversed = True
            mazeArray[leftIndex].floodValue = currentBlock.floodValue +1
            queue.put((col-1, row))
        if topIndex in mazeArray.keys() and (mazeArray[topIndex].traversed == False) and (currentBlock.TOP == False):
            mazeArray[topIndex].traversed = True
            mazeArray[topIndex].floodValue = currentBlock.floodValue +1
            queue.put((col, row+1))
        if bottomIndex in mazeArray.keys() and (mazeArray[bottomIndex].traversed == False) and (currentBlock.BOTTOM == False):
            mazeArray[bottomIndex].traversed = True
            mazeArray[bottomIndex].floodValue = currentBlock.floodValue +1
            queue.put((col, row-1))


def main():

    COLUMN=0 
    ROW=0
    currentDirection = 0
    maze = {}
    for i in range(API.mazeHeight()):
        for j in range(API.mazeWidth()):
            maze[str(j) + "_" + str(i)]  = Position( COLUMN=j, ROW = i)

    uniqueAddresses = []
    numberOfCells = API.mazeHeight() * API.mazeWidth()
    
    while True:
        isOrigin = (COLUMN == 0 and ROW == 0)
        currentIndex = str(COLUMN) + "_" + str(ROW)
        if (COLUMN,ROW) not in uniqueAddresses:
            uniqueAddresses.append((COLUMN,ROW))

        maze[currentIndex].visited+=1
        maze[currentIndex].setWalls(currentDirection, API.wallFront(), isOrigin, API.wallRight(), API.wallLeft())
        if len(uniqueAddresses) == numberOfCells:
            for i in range(16):
                for j in range(16):
                    maze[str(i) + "_" + str(j)].traversed = False
                    maze[str(i) + "_" + str(j)].floodValue = 0
            maze["0_0"].traversed = True
            floodFill(maze, 0,0)
            maze["0_0"].floodValue = 0
            
            for i in range(16):
                for j in range(16):
                    API.setText(j,i, str(maze[str(j) + "_" + str(i)].floodValue))

            API.clearAllColor()
            while COLUMN !=0 or ROW !=0:
                turns = getBestOption(maze, currentDirection, COLUMN, ROW)
                API.setColor(COLUMN, ROW, "r")
                for i in range(turns):
                    API.turnRight()
                    currentDirection = (currentDirection+1) % 4
                API.moveForward()
                if currentDirection == RIGHT:
                    COLUMN +=1
                elif currentDirection == TOP:
                    ROW +=1
                elif currentDirection == BOTTOM:
                    ROW -=1
                elif currentDirection == LEFT:
                    COLUMN -=1
                if COLUMN == 0 and ROW == 0 : break


            for i in range(16):
                for j in range(16):
                    maze[str(i) + "_" + str(j)].traversed = False
                    maze[str(i) + "_" + str(j)].floodValue = 0

            maze["7_7"].traversed = True
            floodFill(maze,7,7)
            API.clearAllColor()
            for i in range(16):
                for j in range(16):
                    API.setText(j,i, str(maze[str(j) + "_" + str(i)].floodValue))
            currentColumn = 0 
            currentRow = 0
            while currentColumn !=7 or currentRow !=7:
                API.setColor(currentColumn, currentRow, "g")
                bestOption = getBestOption(maze, currentDirection, currentColumn, currentRow)
                
                turns = bestOption
                for i in range(turns):
                    API.turnRight()
                    currentDirection = (currentDirection+1) % 4
                API.moveForward()
                if currentDirection == RIGHT:
                    currentColumn +=1
                elif currentDirection == TOP:
                    currentRow +=1
                elif currentDirection == BOTTOM:
                    currentRow -=1
                elif currentDirection == LEFT:
                    currentColumn -=1
            
            API.setColor(7,7 ,"g")
            API.setText(7,7,"GOAL")
            break


        API.setText(maze[currentIndex].COLUMN, maze[currentIndex].ROW, currentIndex)
        API.setColor(maze[currentIndex].COLUMN, maze[currentIndex].ROW, "B")
        options = getOptions(currentDirection, COLUMN, ROW)
        optionObjects =[]
        for option in options:
            position = maze[str(option[0]) + "_" + str(option[1])]
            position.turns = option[2]
            optionObjects.append(position)
        
        optionObjects.sort(key = lambda x : x.visited)

        bestOption = optionObjects[0]

        for i in range(bestOption.turns):
            API.turnRight()
            currentDirection = (currentDirection+1) % 4
        time.sleep(SLEEP_TIME)
        API.moveForward()

        if currentDirection == RIGHT:
            COLUMN +=1
        elif currentDirection == TOP:
            ROW +=1
        elif currentDirection == BOTTOM:
            ROW -=1
        elif currentDirection == LEFT:
            COLUMN -=1

if __name__ == "__main__":
    main()