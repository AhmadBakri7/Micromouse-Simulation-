TOP_DIR = 0 
RIGHT_DIR = 1 
BOTTOM_DIR = 2 
LEFT_DIR =3

SLEEP_TIME = 0

mouseFace = {
    0:"Top",
    1:"Right" ,
    2:"Bottom",
    3:"Left" 
}

class Position:
    def __init__(self, COLUMN, ROW):
        self.COLUMN = COLUMN
        self.ROW = ROW
        self.visited = 0
        self.TOP = False
        self.BOTTOM = False
        self.RIGHT = False
        self.LEFT = False
        self.floodValue = 0
        self.turns = 0
        self.traversed = False
        self.editWalls = True



    def printMyInfo(self):
        return "(" + str(self.COLUMN) + "," +str(self.ROW) + ")" #Flood=" + str(self.floodValue)  + " Top=["+ str(self.TOP)+"] Bottom =["+ str(self.BOTTOM) + "] Right=[" + str(self.RIGHT ) + "] Left=["+ str(self.LEFT)  + "]"

    def setWalls(self, Direction, FRONT, BACK, RIGHT, LEFT):
        if self.editWalls == False:
            return
        
        if Direction == TOP_DIR:
            if  RIGHT:
                self.RIGHT = True
            if  LEFT:
                self.LEFT = True
            if  FRONT:
                self.TOP = True
            if  BACK:
                self.BOTTOM = True
        elif Direction == RIGHT_DIR:
            if  RIGHT:
                self.BOTTOM = True
            if  LEFT:
                self.TOP = True
            if  FRONT:
                self.RIGHT = True
            if  BACK:
                self.LEFT = True
        elif Direction == LEFT_DIR:
            if  RIGHT:
                self.TOP= True
            if  LEFT:
                self.BOTTOM = True
            if  FRONT:
                self.LEFT = True
            if  BACK:
                self.RIGHT = True               
        elif Direction == BOTTOM_DIR:
            if  RIGHT:
                self.LEFT = True
            if  LEFT:
                self.RIGHT = True
            if  FRONT:
                self.BOTTOM = True
            if  BACK:
                self.TOP = True
        self.editWalls = False