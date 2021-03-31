from __future__ import annotations

from typing import Generator

from pygame import Surface, Vector2

delta: float
screen: Surface
allow_typing: bool
text_box: TextBox
coroutines: list[Generator]
pressed_keys: set[int]
camera: Vector2
game: Game


from cop_exe.text_box import TextBox
from cop_exe.game import Game
