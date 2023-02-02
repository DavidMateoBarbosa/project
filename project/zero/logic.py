from typing import *
from bot import *
import pandas as pd
#from .._utils import InvalidCommand

class InvalidCommand(Exception): ...

CellState: TypeAlias = Literal[-1, 0, 1, 2]
ExceptionState: TypeAlias = bool

class Chip:
    position: Position
    def __init__(self, position: Position) -> None:
        self.position = position
    
    def prev_position(self) -> Position:
        "returns the inmediatly up posible position, used later in gravity methods"
        return self.position[0] - 1, self.position[1]

    def new_position(self) -> Position:
        "returns the inmediatly down posible position, used later in gravity methodss"
        return self.position[0] + 1, self.position[1]

    def update(self) -> None:
        "updates the current position using the scale property"
        self.position = self.new_position()

class Cell:
    state: CellState
    balloon_count: int
    _bot: Robot
    _chip: Chip
    def __init__(self) -> None:
        self.state = 0
        self.balloon_count = 0
        self._bot = None
        self._chip = None

    @property
    def bot(self) -> Robot: return self._bot
    @property
    def chip(self) -> Chip: return self._chip

    #info checkers
    def is_block(self) -> bool: return self.state == -1
    def is_blank(self) -> bool: return self.state == 0
    def is_balloon(self) -> bool: return self.state == 1
    def is_chip(self) -> bool: return self.state == 2

    #setters
    def set_block(self) -> None: self.state = -1
    def set_blank(self) -> None: self.state = 0

    #Ballon adder and remover
    def add_balloon(self) -> None:
        self.state = 1
        self.balloon_count += 1
    def remove_ballon(self) -> None:
        self.balloon_count -= 1
        if self.balloon_count == 0: self.state = 0

    #Chip setter and remover
    def set_chip(self, chip: Chip) -> None:
        self.state = 2
        self._chip = chip
    
    def unset_chip(self) -> Chip:
        self.state = 0
        _chip = self._chip
        self._chip = None
        return _chip
    
    #Robot setter and remover
    def set_bot(self, bot: Robot) -> None:
        self._bot = bot
    
    def unset_bot(self) -> Robot:
        _bot = self._bot
        self._bot = None
        return _bot

    def __repr__(self) -> str:
        if self.bot: return self.bot.__repr__()
        if self.is_block(): return "▩"
        if self.is_blank(): return "▢"
        if self.is_balloon(): return "◉"
        if self.is_chip(): return "▣"

class LogicAndGraphic:
    """
    >>> # NOTE: with_exceptions param determitaes if you want chckers to ignore invalid commands or not
    """
    with_exceptions: ExceptionState
    ground: pd.DataFrame
    robot: Robot
    def __init__(self, with_exceptions: ExceptionState = True) -> None:
        self.with_exceptions = with_exceptions
        self.ground = pd.DataFrame(
            [[Cell() for _ in range(8)] for _ in range(8)],
            index=list(range(1,9)),
            columns=list(range(1,9))
            )
        self.robot = Robot((0, 0))
        self._get_cell((0, 0)).set_bot(self.robot)
        self._load_obstacles()
        self.first = self.__repr__()

    #common internal info getters
    def _get_cell(self, position: Position) -> Cell:
        return self.ground.iloc[*position]

    def _limit_checker(self, position: Position) -> bool:
        return (0 <= position[0] <= 7) and (0 <= position[1] <= 7)

    def _load_obstacles(self) -> None:
        ">>> load in 4 random positons one obstacle"
        import random as rd
        obstacles = 4
        while obstacles > 0:
            pos = (rd.randint(0,7), rd.randint(0,7))
            if pos != (0, 0):
                self._get_cell(pos).set_block()
                obstacles -= 1
            if self._get_cell((1, 0)).is_block() and self._get_cell((0, 1)).is_block():
                pos = [(1, 0), (0, 1)]
                self._get_cell(rd.choice(pos)).set_blank()
                obstacles += 1

    # NOTE: Robot Movement
    def move_forward(self) -> None:
        """
        >>> move_forward()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> move once cell forward
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'move_forward' in 'GraphicLogic' out of limit")
            if not self._get_cell(self.robot.new_position()).is_blank(): raise InvalidCommand("method 'move_forward' in 'GraphicLogic' occuped cell")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if not self._get_cell(self.robot.new_position()).is_blank(): return
        self._get_cell(self.robot.new_position()).set_bot(self._get_cell(self.robot.position).unset_bot())
        self.robot.update(self.robot.new_position())

    def rotate_left(self) -> None:
        "rotates to left"
        self.robot.rotate_left()

    def rotate_right(self) -> None:
        "rotates to right"
        self.robot.rotate_right()

    def jump_to(self, squares: int) -> None:
        """
        >>> jump_to(squares: int)
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> move n cell/s to forward
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position(squares)): raise InvalidCommand("method 'jump_to' in 'GraphicLogic' out of limit")
            if not self._get_cell(self.robot.new_position(squares)).is_blank(): raise InvalidCommand("method 'jump_to' in 'GraphicLogic' occuped cell")
        else:
            if not self._limit_checker(self.robot.new_position(squares)): return
            if not self._get_cell(self.robot.new_position(squares)).is_blank(): return
        self._get_cell(self.robot.new_position(squares)).set_bot(self._get_cell(self.robot.position).unset_bot())
        self.robot.update(self.robot.new_position(squares))
    
    def go_to(self, position: Position) -> None:
        """
        >>> go_to(position: Position)
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> teleporting to [x, y] cell 
        """
        position = (position[0] - 1, position[1] - 1)
        if self.with_exceptions:
            if not self._limit_checker(position): raise InvalidCommand("method 'go_to' in 'GraphicLogic' out of limit")
            if not self._get_cell(position).is_blank(): raise InvalidCommand("method 'go_to' in 'GraphicLogic' occuped cell")
        else:
            if not self._limit_checker(position): return
            if not self._get_cell(position).is_blank(): return
        self._get_cell(position).set_bot(self._get_cell(self.robot.position).unset_bot())
        self.robot.update(position)

    # NOTE: actions with balloons
    def put_balloon(self) -> None:
        """
        >>> put_balloon()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> add a balloon on the next robot self cell
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'put_balloon' in 'GraphicLogic' objective cell out of limit")
            if self._get_cell(self.robot.new_position()).is_block() or self._get_cell(self.robot.new_position()).is_chip(): raise InvalidCommand("method 'put_balloon' in 'GraphicLogic' objective cell is already occuped")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if self._get_cell(self.robot.new_position()).is_block() or self._get_cell(self.robot.new_position()).is_chip(): return
        self._get_cell(self.robot.new_position()).add_balloon()

    def pick_balloon(self) -> None:
        """
        >>> pick_balloon()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> pick up a balloon on the next robot self cell
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'pick_balloon' in 'GraphicLogic' objective invalid position")
            if not self._get_cell(self.robot.new_position()).is_balloon(): raise InvalidCommand("method 'pick_balloon' in 'GraphicLogic' objective cell have not balloons or is occuped")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if not self._get_cell(self.robot.new_position()).is_balloon(): return
        self._get_cell(self.robot.new_position()).remove_ballon()

    def pop_balloon(self) -> None:
        """
        >>> pop_balloon()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> pop a balloon on the next robot self cell
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'pop_balloon' in 'GraphicLogic' objective cell invalid position")
            if not self._get_cell(self.robot.new_position()).is_balloon(): raise InvalidCommand("method 'pop_balloon' in 'GraphicLogic' objective cell have not balloons or (is empty or is occuped)")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if not self._get_cell(self.robot.new_position()).is_balloon(): return
        self._get_cell(self.robot.new_position()).remove_ballon()

    # NOTE: actions with chips
    def put_chip(self) -> None:
        """
        >>> put_chip()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> put a balloon on the next robot self cell
        >>> if a balloon is in the grvaity trip balloon will pop
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'put_chip' in 'GraphicLogic' objective cell out of limit")
            if not self._get_cell(self.robot.new_position()).is_blank(): raise InvalidCommand("method 'put_chip' in 'GraphicLogic' objective cell is already occuped")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if not self._get_cell(self.robot.new_position()).is_blank(): return
        chip = Chip(self.robot.new_position())
        self._get_cell(self.robot.new_position()).set_chip(chip)
        self._gravity(chip)

    def pick_chip(self) -> None:
        """
        >>> pick_chip()
        if self is with_exceptions:
        >>> Cheker 1: raise InvalidCommand if is True
        >>> Cheker 2: raise InvalidCommand if is True
        if self is not with_exceptions:
        >>> Cheker 1: pass if is True
        >>> Cheker 2: pass if is True
        Code:
        >>> pick up a balloon on the next robot self cell
        """
        if self.with_exceptions:
            if not self._limit_checker(self.robot.new_position()): raise InvalidCommand("method 'put_chip' in 'GraphicLogic' objective cell invalid position")
            if not self._get_cell(self.robot.new_position()).is_chip(): raise InvalidCommand("method 'pick_chip' in 'GraphicLogic' objective cell have not chip or (is empty or is occuped) ")
        else:
            if not self._limit_checker(self.robot.new_position()): return
            if not self._get_cell(self.robot.new_position()).is_chip(): return
        chip = self._get_cell(self.robot.new_position()).unset_chip()
        self._stack_gravity(chip)


    ## NOTE: chips gravity
    def _gravity(self, chip: Chip):
        """
        >>> gravity command for only a new chip
        """
        old_pos = chip.position
        while self._limit_checker(chip.new_position()):
            if self._get_cell(chip.new_position()).is_chip() or self._get_cell(chip.new_position()).is_block(): break
            chip.update()
        self._get_cell(chip.position).set_chip(self._get_cell(old_pos).unset_chip())

    def _stack_gravity(self, chip: Chip):
        """
        >>> gravity chain action
        """
        if not self._limit_checker(chip.prev_position()): return
        if not self._get_cell(chip.prev_position()).is_chip(): return self._get_cell(chip.position).unset_chip()
        self._get_cell(chip.position).set_chip(chip)    
        return self._stack_gravity(self._get_cell(chip.prev_position()).chip)

    def first_last_state(self) -> str:
        return  self.first + "\n" + self.__repr__()

    def __repr__(self) -> str:
        return self.ground.__repr__()