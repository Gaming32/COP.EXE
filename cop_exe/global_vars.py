from __future__ import annotations

from typing import Generator

from pygame import Surface, Vector2

delta: float
screen: Surface
allow_typing: bool
text_box: TextBox
coroutines: list[Generator]
pressed_keys: set[int]
game: Game
intro_part: int
blinked: float
blink_on: bool


from cop_exe.game import Game
from cop_exe.text_box import TextBox
