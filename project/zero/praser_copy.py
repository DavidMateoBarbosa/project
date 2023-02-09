from typing import *
from logic import *
from io import TextIOWrapper


class _Parser:
    logic: LogicAndGraphic
    script: TextIOWrapper | list
    vars: dict[str, Any]
    available_commands: dict[str, Callable[[Self, Any], Any]]
    def __init__(self, file: TextIOWrapper) -> None:
        self.logic = LogicAndGraphic()
        self.script = list(file)
        self.vars = {}
        self.procs = []
        self.available_commands = [
            'assingTo',
            'goto',
            'move',
            'turn',
            'face',
            'put',
            'pick',
            'moveToThe',
            'moveInDir',
            'jumpToThe',
            'jumpInDir',
        ]
        for _I in range(len(self.script)):
            self.script[_I] = self.script[_I].replace("\n", "")

        if self.script[0] != "ROBOT_R":
            raise TypeError()
        self.script = self.script[1:]
        
        self._parser()

    def _parser(self) -> None:
        self._is_in_vars = False
        self._is_in_procs = False
        self._is_in_defcommands = False
        self._is_in_commands = False
        for line in self.script:

            if line.startswith(" "):
                raise TypeError()
            if line.startswith("VARS "):
                self._is_in_vars = True
            if self._is_in_vars:
                self._vars(line)

            if line.startswith("PROCS"):
                self._is_in_procs = True
            if self._is_in_procs:
                self._procs(line)

            if line.replace(" ", "").replace("\n", "") == "[" or line.startswith("["):
                self._is_in_commands = True
            elif line.startswith("[ "):
                raise TypeError()
            if self._is_in_commands:
                self._commands(line)
        print(self.vars)
    
    #NOTE: start vars
    def _vars(self, line: str) -> None:
        line = line.replace(" ", "")
        if line.startswith("VARS"):
            line = line.replace("VARS", "")
        for var in line.split(","):
            self.vars[var.replace(";", "")] = None
        if line.endswith(";"):
            self._is_in_vars = False
    
    #NOTE: define proccess
    def _procs(self, line: str) -> None:
        if line.replace(" ","") == "PROCS": return
        
    #NOTE: define commands
    def _def_commands(self, line: str) -> None: ...

    #NOTE: run commands
    def _commands(self, line: str) -> None:
        if line.replace(" ", "").replace("\n", "") == "[" or line.replace(" ", "").replace("\n", "") == "]": return
        line = line.replace(" ", "").replace("\n", "")
        if not line.endswith(";"): raise TypeError()
        line = line[:-1]
        function, params = line.split(":")
        params = params.split(",")
        if function in self.available_commands:
            if function == 'put' or function == 'pick': eval(f"self.{function}({params[0]}, '{params[1]}')")
            else: eval(f"self.{function}({params[0]}, {params[1]})")
        if line.endswith("]"):
            self._is_in_commands = False

        


    def assingTo(self, n) -> ...: ...
    def goto(self, x, y) -> ...:
        self.logic.go_to((x, y))
    def move(self, n) -> ...:
        for _ in range(n):self.logic.move_forward()
    def turn(self, D) -> ...: ...
    def face(self, O) -> ...: ...
    def put(self, n, item) -> ...: 
        for _ in range(n):
            if item == "Balloon":self.logic.put_balloon()
            elif item == "Chip":self.logic.put_chip()
    def pick(self, n, item) -> ...:
        for _ in range(n):
            if item == "Balloon":self.logic.pick_balloon()
            elif item == "Chip":self.logic.pick_chip()
    def moveToThe(self, n, D) -> ...: ...
    def moveInDir(self, n, O) -> ...: ...
    def jumpToThe(self, n, D) -> ...: ...
    def jumpInDir(self, n, O) -> ...: ...



def parser(file: str) -> Literal["script and execution good request", "script good request, execution bad request", "script bad request"]:
    with open(file, mode='r', encoding='utf-8') as file:
            parse = _Parser(file)
    try:
        with open(file, mode='r', encoding='utf-8') as file:
            parse = _Parser(file)
        return "script and execution good request"
    except InvalidCommand:
        return "script good request, execution bad request"
    except TypeError:
        return "script bad request"
    
print(parser(r"C:\Users\LoganTaurus\Desktop\project\bot.txt"))