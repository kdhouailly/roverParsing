# roverParsing
CS403: Rapport Final Project




Description of the project:

	For this project, I built a game where 5 Rovers spawn on a map. They can move (forward, backward, left, right, full forward, full backward), get life point by passing over a D tile and shoot. Initially each rover has no life point and get disable if it get shoot, however it will still be active if it has life points (D). The rovers can also teleport on a new map (ex: rover . SetMap ( “map2.txt” )). 

Information about the pseudo-code:

The syntax to send instructions to the rovers is the following:
1/ The pseudo-code must start with “{“ and end with “}”
2/ The pseudo-code must be separate by blanks and each line must end with “;”

An exemple of pseudo-code is in the file parsing-tests.txt.

How the project works:

The code was built over the skeleton project. When “python rover.py” is called the following process will start:
The file rover.py sets up the Rovers, and the map and calls the function  wait_for_command to make them wait for the pseudo-code to be parsed in a rover’s text file and check every second if the pseudo-code has been parsed. The Rovers are set using threads instead of multiprocessing for a memory issue. Using multiprocessing, the Rovers use separate memories within different processes for each rovers. Therefore, I instead used thread in order to be able to execute tasks within the same process and thus, sharing the same memory and be able to share the same variables. 
With the command “python sender.py prgm.txt Rover1/2/3/4/5”, the program in the sender.py file will pass (if correctly written) the pseudo-code to the rover’s text file.
Then, the function wait_for_command will detect the pseudo-code and then call the function parse_and_execute_cmd which will “translate” the pseudo-code in python and run it using the class Translate contained in the file translate.py.
Using the token classes, the translate class will “translate” the pseudo-code in python.
Finally, the function parse_and_execute_cmd will execute the translated code.




Attributes of the class Rover:

The class Rover has the following attributes:
a name
an id (1, 2, …)
a state (either activate or deactivate). If disabled the rover cannot perform any action
a D counter that will define if a Rover gets shoot whether it will get deactivated (number of D = 0) or lose a D


Functions of the class Rover:

The Class Rover in the rover.py file contains the functions:
IsPossibleToMoveHere → to check if possible to move to a defined position
ChangePosition → to set up the new position in order to make the rover move
SetMap → is called by the function SetMap in MapAndOrientation file to set up the map for each Rovers and call InitPositionOrientation to set up the rover’s orientation in the map
InitPositionOrientation → to set up the initial rover’s orientation
print → to print 
wait_for_command
parse_and_execute_cmd
Info → to print all rover’s info (orientation, position, state, D’s number)
MoveForward/Backward → to check and execute if possible to move forward/backward depending on the rover’s orientation.
TurnLeft/Right → to make the rover change its orientation.
MoveLeft/Right → to make the rover move left/right.
FullForward/Backward → to make the rover move forward/backward until it reaches a limit.
ChangeState → to make the rover change its state from functional to disable or vice-versa.
IsSpecialBlock → to check if the rover is on a D tile and if yes upgrade the D counter.
Shoot → to check if a rover is on the rover’s orientation, and if yes will shoot the rover and make it disable.

 
Python version 3.10 is required.

