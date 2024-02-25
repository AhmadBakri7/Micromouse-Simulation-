import API
import sys

TOP = 0 
RIGHT = 1 
BOTTOM = 2 
LEFT =3
mouseFace = {
    0:"Top",
    1:"Right" ,
    2:"Bottom",
    3:"Left" } 

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    COLUMN=0 
    ROW=0
    currentDirection = 0

    while True:
        if COLUMN == 7 and ROW == 7:
            API.setColor(COLUMN,ROW, "G")
            API.setText(COLUMN,ROW,"GOAL")
            break
        if not API.wallLeft():
            API.turnLeft()
            currentDirection = (currentDirection-1) %4
        while API.wallFront():
            API.turnRight()
            currentDirection = (currentDirection+1) %4            
        API.moveForward()

        if currentDirection == RIGHT:
            COLUMN +=1
        elif currentDirection == TOP:
            ROW +=1
        elif currentDirection == BOTTOM:
            ROW -=1
        elif currentDirection == LEFT:
            COLUMN -=1
        log("Current Direction: " + mouseFace.get(currentDirection) + " Current Position : (" +  str(COLUMN) + ","+ str(ROW)+ ")")

if __name__ == "__main__":
    main()