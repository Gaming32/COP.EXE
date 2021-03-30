from typing import Generator
from pygame import Surface


delta: float
screen: Surface
allow_typing: bool
text_box = 'TextBox'
coroutines: list[Generator]
pressed_keys: set[int]
