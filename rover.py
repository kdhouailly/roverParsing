import multiprocessing
import pathlib
import time
import traceback
from enum import Enum
from random import randint
from random import choice
import os
from translate import *
from MapAndRotation import Map,Rotation
from random import randint
from random import choice

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

# Rovers that exist
ROVER_1 = "Rover1"
ROVER_2 = "Rover2"
ROVERS = [
    ROVER_1,
    ROVER_2,
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
    def __init__(self, name,map):
        self.name = name
        self.map = map
        self.actions = []
        self.__InitPositionRotation()

    def parse_and_execute_cmd(self, command):
        print ("Translated code: \n" + Translate.translate(ROVER_COMMAND[self.name]))

    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 1 second before trying to check for
            # content again
            self.print("Waiting for command...")
            time.sleep(1)
            if get_command(self.name):
                self.print("Found a command...")
                try:
                    self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                except Exception as e:
                    self.print(f"Failed to run command: {ROVER_COMMAND[self.name]}")
                    self.print(traceback.format_exc())
                finally:
                    self.print("Finished running command.\n\n")
    
    def __InitPositionRotation(self):
        self.rotation = choice(list(Rotation))
        while True:
            self.x = randint(0,len(self.map.matriceMap)-1)
            self.y = randint(0,len(self.map.matriceMap[0])-1)
            if self.map.matriceMap[self.x][self.y] != "X":
                break
        print(f"\nRotation = {self.rotation} ; x = {self.x} ; y = {self.y} ; Case = '{self.map.matriceMap[self.x][self.y]}'")
        self.oldCase = self.map.matriceMap[self.x][self.y]
        self.map.matriceMap[self.x][self.y] = "@"
        print("Init Map :")
        self.map.printMap()
    def MoveForward(self):
        if self.rotation == Rotation.E or self.rotation == Rotation.W:
            if (self.rotation == Rotation.E):
                if self.__IsPossibleToMoveHere(self.x,self.y+1):
                    self.__ChangePosition(self.x,self.y+1) 
                else:
                    print("Error")
            else:
                if self.__IsPossibleToMoveHere(self.x,self.y-1):
                    self.__ChangePosition(self.x,self.y-1)
                else:
                    print("Error")
        else:
            if (self.rotation == Rotation.N):
                if self.__IsPossibleToMoveHere(self.x-1,self.y):
                    self.__ChangePosition(self.x-1,self.y)
                else:
                    print("Error")
            else:
                if self.__IsPossibleToMoveHere(self.x+1,self.y):
                    self.__ChangePosition(self.x+1,self.y)
                else:
                    print("Error")
    def MoveBackward(self):
        if self.rotation == Rotation.E or self.rotation == Rotation.W:
            if (self.rotation == Rotation.E):
                if self.__IsPossibleToMoveHere(self.x,self.y-1):
                    self.__ChangePosition(self.x,self.y-1) 
                else:
                    print("Error")
            else:
                if self.__IsPossibleToMoveHere(self.x,self.y+1):
                    self.__ChangePosition(self.x,self.y+1)
                else:
                    print("Error")
        else:
            if (self.rotation == Rotation.N):
                if self.__IsPossibleToMoveHere(self.x+1,self.y):
                    self.__ChangePosition(self.x+1,self.y)
                else:
                    print("Error")
            else:
                if self.__IsPossibleToMoveHere(self.x-1,self.y):
                    self.__ChangePosition(self.x-1,self.y)
                else:
                    print("Error")
    def TurnLeft(self):
        self.rotation = Rotation.GetRotation(self.rotation,-1)
        print(f"\nRotation = {self.rotation}")
    def TurnRight(self):
        self.rotation = Rotation.GetRotation(self.rotation,1)
        print(f"\nRotation = {self.rotation}")
    def __IsPossibleToMoveHere(self,x,y):
        if x>=0 and x < len(self.map.matriceMap) and y>=0 and y < len(self.map.matriceMap[0]):
            if self.map.matriceMap[x][y] != "X":
                return True
        return False
    def AddAction(self,action):
        self.actions.append(action)
    def __ChangePosition(self,x,y):
        self.map.matriceMap[self.x][self.y] = self.oldCase
        self.x = x
        self.y = y
        self.oldCase = self.map.matriceMap[self.x][self.y]
        self.map.matriceMap[self.x][self.y] = "@"
        self.map.printMap()
    def Run(self):
        for action in self.actions:
            print("\n"+action.__name__)
            action(self)
    def Info(self):
        print(f"\nRotation = {self.rotation} ; x = {self.x} ; y = {self.y}")


def main():
    # Initialize the rovers
    map = Map("map.txt")
    rover1 = Rover(ROVER_1,map)
    rover2 = Rover(ROVER_2,map)
    my_rovers = [rover1, rover2]

    # Run the rovers in parallel
    procs = []
    for rover in my_rovers:
        p = multiprocessing.Process(target=rover.wait_for_command, args=())
        p.start()
        procs.append(p)

    # Wait for the rovers to stop running (after MAX_RUNTIME)
    for p in procs:
        p.join()


if __name__=="__main__":
    main()
