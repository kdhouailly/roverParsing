from Token import *

class Translate:
    @staticmethod
    def __find_between_r(s, first, last ):
        try:
            start = s.find(first) + 1
            end = s.rindex(last)
            return s[start:end]
        except ValueError:
            return ""
    
    @staticmethod
    def translate (lines):
        code = ""
        indent = ""
        nbLine = 1
        for line in lines:
            line = line.replace("true","True")
            line = line.replace("false","False")
            line = line.strip().split()
            if len(line) == 1 and (line[0] == "{" or line[0] == "}"):
                if indent != "":
                    tamp = list(indent)
                    tamp.pop()
                    indent = "".join(tamp)
            elif len(line)>1 and line[1] == PythonVocab.AFFECTATION:
                code += indent + " ".join(line).replace(";","") + "\n"
            elif line[0] == PythonKeyWord.WHILE:
                code += indent + str(PythonKeyWord.WHILE) + Translate.__find_between_r(" ".join(line),"(",")").replace("&&","and").replace("||","or") + ":\n"
                indent += "\t"
            elif line[0] == PythonKeyWord.IF:
                code += indent + str(PythonKeyWord.IF) + Translate.__find_between_r(" ".join(line),"(",")").replace("&&","and").replace("||","or") + ":\n"
                indent += "\t"
            elif line[0] == PythonKeyWord.ELSE:
                code += indent + str(PythonKeyWord.ELSE) + ":\n"
                indent += "\t"
            elif line[0] == PythonKeyWord.BREAK:
                code += indent + str(PythonKeyWord.BREAK) + "\n"
            elif line[0] == PythonKeyWord.RETURN:
                code += indent + str(PythonKeyWord.RETURN) + " " + line[1] +"\n"
            elif line[0] == PythonKeyWord.ROVER:
                if line[2] == PythonFunctionRobot.MAPCHANGE:
                    code += (indent + "self.map." + "".join(line).replace(";","") + "\n").replace(".rover","")
                else:
                    code += (indent + "".join(line).replace(";","") + "\n").replace("rover","self")
            elif PythonType.has_value(line[0]):
                pass
            # elif line[0] == PythonFunctionRobot.MAPCHANGE:
            #     code += indent + "self.map." + "".join(line).replace(";","") + "\n"
            elif line[0] == "#":
                # Debug
                code += indent + ("".join(line).replace("#","").replace(";",""))
            else:
                print(f"Traduction error in line {nbLine}")
                
            nbLine += 1

        return code