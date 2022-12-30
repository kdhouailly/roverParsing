from enum import Enum

class Orientation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    def GetOrientation(actualOrientation,sens):
        if actualOrientation == Orientation.N and sens == -1:
            return Orientation.W
        elif actualOrientation ==  Orientation.W and sens == 1:
            return Orientation.N
        else:
            return Orientation(actualOrientation.value + sens)

class Map:
    def __init__(self, filename, rovers) -> None:
        self.matriceMap = []
        self.rovers = rovers
        print()
        for i in self.rovers:
            print(i)
        self.SetMap(filename)

    def printMap(self):
        #os.system("clear")
        print()
        for i in self.matriceMap:
            print("".join(i))
        print()

    def SetMap(self,filename):
        self.matriceMap = []

        file = open(filename,"r")
        code = file.readlines()
        file.close()

        for i in code:
            self.matriceMap.append(list(i.strip()))
        
        for rover in self.rovers:
            rover.SetMap(self)
    
    def IsRoverHere(self,x,y,killer):
        for rover in self.rovers:
            if rover.x == x and rover.y == y and rover != killer:
                return rover
        return None