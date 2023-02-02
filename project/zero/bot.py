from typing import *


N, S, E, W = "North", "South", "East", "West"
CardinalPoint: TypeAlias = Literal["North", "South", "East", "West"]
Position: TypeAlias = tuple[int, int]
Scale: TypeAlias = tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]

class Robot:
    "used to facilitate the logic"
    position: Position
    orientation: CardinalPoint
    scale: Scale
    def __init__(self, position: Position) -> None:
        self.position = position
        self.orientation = N

    @property
    def scale(self) -> Scale:
        "returns a Position modifier"
        if self.orientation == N: return 1, 0
        if self.orientation == S: return -1, 0
        if self.orientation == E: return 0, -1
        if self.orientation == W: return 0, 1    

    def update(self, position: Position) -> None:
        "updates the current position using the scale property"
        self.position = position

    @overload
    def new_position(self, multiplier: int = ...) -> Position: ...
    @overload
    def new_position(self) -> Position: ...

    def new_position(self, multiplier: int = 1) -> Position:
        "returns the new posible position"
        return self.position[0] + self.scale[0]*multiplier, self.position[1] + self.scale[1]*multiplier

    def rotate_left(self) -> None:
        "rotates to left"
        if self.orientation == N: self.orientation = W; return
        if self.orientation == W: self.orientation = S; return
        if self.orientation == S: self.orientation = E; return
        if self.orientation == E: self.orientation = N; return
    
    def rotate_right(self) -> None:
        "rotates to right"
        if self.orientation == N: self.orientation = E; return
        if self.orientation == E: self.orientation = S; return
        if self.orientation == S: self.orientation = W; return
        if self.orientation == W: self.orientation = N; return

    def __repr__(self) -> str:
        "the repr depends of the self orientation"
        if self.orientation == N: return "▾"
        if self.orientation == S: return "▴"
        if self.orientation == E: return "◂"
        if self.orientation == W: return "▸"