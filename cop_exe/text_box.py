import sys
from typing import Optional

from pygame.font import Font, SysFont
from cop_exe.pygame_import import *
from cop_exe import global_vars
from cop_exe.co_utils import co_sleep


OFFSET = Vector2(10, 10)
FONT = SysFont('Lucida Console', 20)
BLINK_TIME = 0.75
BLINK_CHAR = '_'
LINE_HEIGHT = 25
MAX_WIDTH = 49


class TextBox:
    rect: Rect
    text: list[str]
    blinked: float
    blink_on: bool

    def __init__(self, rect: Rect, start_text: Optional[str] = '') -> None:
        self.rect = rect
        self.text = start_text.split('\n')
        self.blinked = 0
        self.blink_on = True

    def render(self, surf: Surface):
        self.blinked += global_vars.delta
        if self.blinked > BLINK_TIME:
            self.blink_on = not self.blink_on
            self.blinked %= BLINK_TIME
        surf.fill((0, 0, 0), self.rect)
        curoffset = Vector2(OFFSET)
        height = (len(self.text) + 1) * LINE_HEIGHT
        if height > self.rect.height:
            movement = self.rect.height - height
            curoffset.y += movement
        for (i, line) in enumerate(self.text):
            destpos = self.rect.move(curoffset)
            if destpos.y < self.rect.y:
                curoffset.y += LINE_HEIGHT
                continue
            if i == len(self.text) - 1 and self.blink_on:
                line += BLINK_CHAR
            rendered = FONT.render(line, True, (255, 255, 255), (0, 0, 0))
            surf.blit(rendered, destpos)
            curoffset.y += LINE_HEIGHT

    def print(self, *objs, sep: str = ' ', end: str = '\n'):
        value = sep.join(str(obj) for obj in objs) + end
        sys.stdout.write(value)
        xpos = 1
        for char in value:
            if char == '\n':
                self.text.append('')
                xpos = 0
                continue
            elif xpos > MAX_WIDTH:
                self.text.append('')
                xpos = 0
            self.text[-1] += char
            xpos += 1

    def slow_print(self, *objs, sep: str = ' ', end: str = '\n', text_time: float = 0.05):
        curpressed = global_vars.pressed_keys.copy()
        skipped = False
        value = sep.join(str(obj) for obj in objs) + end
        sys.stdout.write(value)
        xpos = 1
        for char in value:
            if char == '\n':
                self.text.append('')
                xpos = 0
                continue
            elif xpos > MAX_WIDTH:
                self.text.append('')
                xpos = 0
            self.text[-1] += char
            curpressed.intersection_update(global_vars.pressed_keys)
            if global_vars.pressed_keys.difference(curpressed):
                skipped = True
            if not skipped:
                yield from co_sleep(text_time)
            xpos += 1
