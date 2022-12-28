from enum import Enum

class PythonDetection(Enum):
    @classmethod
    def has_value(cls,value):
        return value in cls._value2member_map_
    def __eq__(cls, other):
        return cls.value == other
    def __str__(self):
        return str(self.value)

class PythonVocab(PythonDetection):
    AFFECTATION = "="

class PythonType(PythonDetection):
    INT = "int"
    BOOl = "bool"
    DOUBLE = "double"
    CHAR = "char"

class PythonKeyWord(PythonDetection):
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    BREAK = "break"
    RETURN = "return"
    ROBOT = 'robot'

class PythonFunctionRobot(PythonDetection):
    INFO = "INFO"
    MAPCHANGE = "MapChange"
    TURNLEFT = "TurnLeft"
    TURNRIGHT = "TurnRight"
    MOVEFORWARD = "MoveForward"
    MOVEBACKWARD = "MoveBackward"
    ISPOSSIBLE = "IsPossible"
    DRILLING = "Drilling"
