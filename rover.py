import pathlib
import threading
import time
from random import randint
from random import choice
from translate import *
from MapAndOrientation import Map,Orientation
from random import randint
from random import choice
from Token import SpecialBlock
import sys

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

# Rovers that exist
ROVER_1 = "Rover1"
ROVER_2 = "Rover2"
ROVER_3 = "Rover3"
ROVER_4 = "Rover4"
ROVER_5 = "Rover5"
ROVERS = [
    ROVER_1,
    ROVER_2,
    ROVER_3,
    ROVER_4,
    ROVER_5
]

# Command file is stored within the rover directory. Here we're building one file
# for each of the rovers defined above
ROVER_COMMAND_FILES = {
    rover_name: pathlib.Path(pathlib.Path(__file__).parent.resolve(), f"{rover_name}.txt")
    for rover_name in ROVERS
}
for _, file in ROVER_COMMAND_FILES.items():
    with file.open("w") as f:
        pass

# Constant used to store the rover command for parsing
ROVER_COMMAND = {
    rover_name: None
    for rover_name in ROVERS
}


def get_command(rover_name):
    """Checks, and gets a command from a rovers command file.

    It returns True when something was found, and False
    when nothing was found. It also truncates the contents
    of the file if it found something so that it doesn't
    run the same command again (unless it was re-run from
    the controller/main program).
    """
    fcontent = None
    with ROVER_COMMAND_FILES[rover_name].open() as f:
        fcontent = f.readlines()
    if fcontent is not None and fcontent:
        ROVER_COMMAND[rover_name] = fcontent
        with ROVER_COMMAND_FILES[rover_name].open("w+") as f:
            pass
        return True
    return False

class Rover():
    def __init__(self, name):
        self.name = name
        self.id = name[-1]
        self.state = True
        self.nbD = 0

    def __IsPossibleToMoveHere(self,x,y):
        if self.state :
            if x>=0 and x < len(self.map.matriceMap) and y>=0 and y < len(self.map.matriceMap[0]):
                if self.map.matriceMap[x][y] != "X" and self.map.matriceMap[x][y] != self.id:
                    return True
            return False
        else:
            self.print("Rover is disable")
            return False

    def __ChangePosition(self,x,y):
        self.map.matriceMap[self.x][self.y] = self.oldCase
        self.x = x
        self.y = y
        self.oldCase = self.map.matriceMap[self.x][self.y]
        self.map.matriceMap[self.x][self.y] = self.id
        self.__IsSpecialBlock()
        self.map.printMap()

    def __InitPositionOrientation(self):
        self.orientation = choice(list(Orientation))
        while True:
            self.x = randint(0,len(self.map.matriceMap)-1)
            self.y = randint(0,len(self.map.matriceMap[0])-1)
            if self.map.matriceMap[self.x][self.y] == " ":
                break
        self.print(f"Init Map : {self.orientation} ; x = {self.x} ; y = {self.y} ; state = {self.state}")
        self.oldCase = self.map.matriceMap[self.x][self.y]
        self.map.matriceMap[self.x][self.y] = self.id
        self.map.printMap()
        
    def SetMap(self, map):
        self.map:Map = map
        self.__InitPositionOrientation()
        
    def print(self, msg):
        print(f"{self.name}: {msg}")
      
    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 1 second before trying to check for
            # content again
            #self.print("Waiting for command...")
            time.sleep(1)
            if get_command(self.name):
                self.print("Found a command...")
                self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                # try:
                #    self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                # except Exception as e:
                #     self.print(f"Failed to run command: {ROVER_COMMAND[self.name]}")
                #     self.print(traceback.format_exc())
                # finally:
                #     self.print("Finished running command.\n\n")

    def parse_and_execute_cmd(self, command):
        roverPythonCode = Translate.translate(ROVER_COMMAND[self.name])
        self.print ("Translated code: \n" + roverPythonCode)
        exec(roverPythonCode)
        #self.print("Erreur de synthaxe liée au pseudo code")
        
    

    def Info(self):
        self.print(f"{self.orientation} ; x = {self.x} ; y = {self.y} ; state = {self.state} ; nbD = {self.nbD}")
        
    def MoveForward(self):
        if self.orientation == Orientation.E or self.orientation == Orientation.W:
            if (self.orientation == Orientation.E):
                if self.__IsPossibleToMoveHere(self.x,self.y+1):
                    self.__ChangePosition(self.x,self.y+1)
                    return True 
                else:
                    return False
            else:
                if self.__IsPossibleToMoveHere(self.x,self.y-1):
                    self.__ChangePosition(self.x,self.y-1)
                    return True 
                else:
                    return False
        else:
            if (self.orientation == Orientation.N):
                if self.__IsPossibleToMoveHere(self.x-1,self.y):
                    self.__ChangePosition(self.x-1,self.y)
                    return True 
                else:
                    return False
            else:
                if self.__IsPossibleToMoveHere(self.x+1,self.y):
                    self.__ChangePosition(self.x+1,self.y)
                    return True 
                else:
                    return False

    def MoveBackward(self):
        if self.orientation == Orientation.E or self.orientation == Orientation.W:
            if (self.orientation == Orientation.E):
                if self.__IsPossibleToMoveHere(self.x,self.y-1):
                    self.__ChangePosition(self.x,self.y-1)
                    return True  
                else:
                    return False
            else:
                if self.__IsPossibleToMoveHere(self.x,self.y+1):
                    self.__ChangePosition(self.x,self.y+1)
                    return True 
                else:
                    return False
        else:
            if (self.orientation == Orientation.N):
                if self.__IsPossibleToMoveHere(self.x+1,self.y):
                    self.__ChangePosition(self.x+1,self.y)
                    return True 
                else:
                    return False
            else:
                if self.__IsPossibleToMoveHere(self.x-1,self.y):
                    self.__ChangePosition(self.x-1,self.y)
                    return True 
                else:
                    return False

    def TurnLeft(self):
        self.orientation = Orientation.GetOrientation(self.orientation,-1)
        self.print(f"Orientation = {self.orientation}")

    def TurnRight(self):
        self.orientation = Orientation.GetOrientation(self.orientation,1)
        self.print(f"Orientation = {self.orientation}")
    
    def MoveRight(self):
        self.TurnRight()
        self.MoveForward()

    def MoveLeft(self):
        self.TurnLeft()
        self.MoveForward()
    
    #The 5 added functions

    #As long as the rover can, the rover moves forward 
    def FullForward(self):
        while(self.MoveForward()):
            pass
    #As long as the rover can, the rover moves backward 
    def FullBackward(self):
        while(self.MoveBackward()):
            pass
    #The Rover changes its state from functional to disable or vice-versa
    def ChangeState(self, newstate=None):
        if newstate == None:
            self.state = not self.state
        else:
            self.state = newstate
    #If Rover goes over a D tile, the rover will get an extra life point
    def __IsSpecialBlock(self):
        match self.oldCase:
            case SpecialBlock.BlockD:
                self.nbD += 1
                self.print("D tile: " + self.nbD)
            case _:
                pass
    #The Rover shoots depending on its orientation
    def Shoot(self):
        self.print("Shoot")
        missed = True
        match self.orientation:
            case Orientation.N:
                for x in range(self.x, 0, -1):
                    rover:Rover = self.map.IsRoverHere(x,self.y,self)
                    if rover:
                        self.print(f"Kill Robot{rover.id}")
                        if self.nbD == 0:
                            rover.ChangeState(False)
                        else:
                            self.nbD -= 1
                        rover.Info()
                        missed = False
                        break
                if missed:
                    self.print("Oups the rover missed")
                    
            case Orientation.S:
                for x in range(self.x, len(self.map.matriceMap), 1):
                    rover:Rover = self.map.IsRoverHere(x,self.y,self)
                    if rover:
                        self.print(f"Kill Robot{rover.id}")
                        if self.nbD == 0:
                            rover.ChangeState(False)
                        else:
                            self.nbD -= 1
                        rover.Info()
                        missed = False
                        break        
                if missed:
                    self.print("Oups the rover missed")

            case Orientation.E:
                for y in range(self.y, len(self.map.matriceMap[0]), 1):
                    rover:Rover = self.map.IsRoverHere(self.x,y,self)
                    if rover:
                        self.print(f"Kill Robot{rover.id}")
                        if self.nbD == 0:
                            rover.ChangeState(False)
                        else:
                            self.nbD -= 1
                        rover.Info()
                        missed = False
                        break
                if missed:
                    self.print("Oups the rover missed")

            case Orientation.W:
                for y in range(self.y, 0, -1):
                    rover:Rover = self.map.IsRoverHere(self.x,y,self)
                    if rover:
                        self.print(f"Kill Robot{rover.id}")
                        if self.nbD == 0:
                            rover.ChangeState(False)
                        else:
                            self.nbD -= 1
                        rover.Info()
                        missed = False
                        break
                if missed:
                    self.print("Oups the rover missed")
                    


def main():
    # Initialize the rovers
    rover1 = Rover(ROVER_1)
    rover2 = Rover(ROVER_2)
    rover3 = Rover(ROVER_3)
    rover4 = Rover(ROVER_4)
    rover5 = Rover(ROVER_5)

    my_rovers = [rover1, rover2, rover3, rover4, rover5]
    
    map = Map("map.txt",my_rovers)

    # Run the rovers in parallel
    procs = []
    for rover in my_rovers:
        p = threading.Thread(target=rover.wait_for_command, args=())
        p.daemon = True
        p.start()
        procs.append(p)

    # Wait for the rovers to stop running (after MAX_RUNTIME)
    while True:
        time.sleep(MAX_RUNTIME)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
