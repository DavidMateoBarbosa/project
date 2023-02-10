from typing import *
from logic import *
import io
import os



FileDescriptorOrPath: TypeAlias = int | str | bytes | os.PathLike[str] | os.PathLike[bytes]

ParseProcess: TypeAlias = None | NoReturn

class _Parser:
    def __init__(self, file: FileDescriptorOrPath) -> None:
        self.bot_logic: LogicAndGraphic = LogicAndGraphic()
        self.script: list[str] = self.open(file)
        self.vars: dict[str, Any] = {}
        self.builtin_funcs: dict[str, int] = {
            "assignTo": 2,
            "goto": 2,
            "move": 1,
            "turn": 1,
            "face": 1,
            "put": 2,
            "pick": 2,
            "moveToThe": 2,
            "moveInDir": 2,
            "jumpToThe": 2,
            "jumpInDir": 2,
            "nop": 0
        }
        self.builtin_logic: dict[str, int] = {
            "while,do": -1,
            "if,then": -1,
            "repeat": -1,
            "facing": 1,
            "canPut": 2,
            "canPick": 2,
            "canMoveInDir": 2,
            "canJumpInDir": 2,
            "canMoveToThe": 2,
            "canJumpToThe": 2,
            "not": 1
        }
        self.clean_unused()
        if self.script[0].replace("\n","").replace(" ", "") != "ROBOT_R":
            TypeError("all .rbt scripts need startswith ROBOT_R")
        self.script = self.script[1:]
        self.load_vars()
        self.load_process()
    

    def load_vars(self) -> None:
        line = self.script[0]
        line = line.replace("VARS", "").replace(" ", "")
        if not line.endswith(";"):
            raise TypeError("missing ';' at last int the line")
        for name in line.split(","):
            self.vars[name.replace(";", "")] = None
        self.script = self.script[1:]

    def load_process(self) -> None:
        if self.script[0] == "PROCS":
            self.script = self.script[1:]
            self.process: list[str] = []
            index = None
            for line in self.script:
                if not line.startswith("["):
                    self.process.append(line)
                else:
                    if index is None:
                        index = self.script.index(line)
            self.script = self.script[index:]
            self._wrap_process()
        elif self.script[0].startswith("[") or self.script[0] == "[":
            return None
        else:
            raise TypeError("function")

    def _wrap_process(self) -> None:
        process = ""
        for line in self.process:
            process += line.replace(" ", "")
        for index in range(len(process)):
            print(process)
            break


    def clean_unused(self) -> None:
        index = 0
        while index < len(self.script):
            self.script[index] = self.script[index].replace("\n", "")
            if self._is_void_str(self.script[index]):
                self.script.pop(index)
            else:
                if self.script[index].startswith(" "):
                    raise IndentationError("line never started with a space")
                index += 1
        
    def _is_void_str(self, string: str) -> bool:
        for char in string:
            if char != " ":
                return False
        return True

    def open(
        self,
        file: FileDescriptorOrPath,
        *args, **kwargs
    ) -> list[str]:
        name = file.split("/")
        if len(name) == 1:
            name = file.split("\\")
        name = name[-1]
        if not name.endswith(".rbt"):
            raise TypeError(f"wrong program extension, robot file must be endswith '.rbt', not '.{name.split('.')[-1]}'")
        with open(file, *args, **kwargs) as wraper:
            return list(wraper)


_Parser(r"C:\Users\LoganTaurus\Desktop\project\bot.rbt")

@overload
def parser(file: FileDescriptorOrPath = "needs abs path") -> ParseProcess: ...
def parser(file: FileDescriptorOrPath) -> ParseProcess:
    r"file must be ends in '.rbt'"
    _Parser(file)
