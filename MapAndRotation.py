from enum import Enum


class Rotation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    def GetRotation(actualrotation,sens):
        if actualrotation == Rotation.N and sens == -1:
            return Rotation.W
        elif actualrotation ==  Rotation.W and sens == 1:
            return Rotation.N
        else:
            return Rotation(actualrotation.value + sens)

class Map:
    def __init__(self, filename, rovers) -> None:
        self.matriceMap = []
        self.rovers = rovers
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
            print(self)
            rover.SetMap(self)
    
    def IsRoverHere(self,x,y,killer):

        for i in range(0,len(self.rovers)):
            if self.rovers[i].x == x and self.rovers[i].y == y and self.rovers[i] != killer:
                print(self.rovers[i])
                return self.rovers[i]
        return None