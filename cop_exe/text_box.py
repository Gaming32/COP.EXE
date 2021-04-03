from cop_exe.consts import BLINK_TIME
import sys
from typing import Optional

from pygame import midi
from pygame.font import Font, SysFont

from cop_exe import global_vars
from cop_exe.co_utils import co_sleep
from cop_exe.pygame_import import *

OFFSET = Vector2(10, 10)
FONT = SysFont('Lucida Console', 20)
BLINK_CHAR = '_'
LINE_HEIGHT = 25
MAX_WIDTH = 49


class TextBox:
    rect: Rect
    text: list[str]
    skipped: bool

    def __init__(self, rect: Rect, start_text: Optional[str] = '') -> None:
        self.rect = rect
        self.text = start_text.split('\n')
        global_vars.blinked = 0
        global_vars.blink_on = True
        self.skipped = False

    def render(self, surf: Surface):
        global_vars.blinked += global_vars.delta
        if global_vars.blinked > BLINK_TIME:
            global_vars.blink_on = not global_vars.blink_on
            global_vars.blinked %= BLINK_TIME
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
            if i == len(self.text) - 1 and global_vars.blink_on:
                line += BLINK_CHAR
            rendered = FONT.render(line, True, (128, 255, 128), (0, 0, 0))
            surf.blit(rendered, destpos)
            curoffset.y += LINE_HEIGHT

    def print(self, *objs, sep: str = ' ', end: str = '\n'):
        value = sep.join(str(obj) for obj in objs) + end
        sys.stdout.write(value)
        xpos = len(self.text[-1]) + 1
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

    def reset_skipped(self):
        self.skipped = False

    def slow_print(self, *objs, sep: str = ' ', end: str = '\n', text_time: float = 0.05, midi_time: float = 0.005):
        curpressed = global_vars.pressed_keys.copy()
        value = sep.join(str(obj) for obj in objs) + end
        sys.stdout.write(value)
        xpos = len(self.text[-1]) + 1
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
                self.skipped = True
            if not self.skipped:
                if MIDI_ENABLED:
                    MIDI_DEVICE.note_on(90, 63)
                yield from co_sleep(midi_time)
                if MIDI_ENABLED:
                    MIDI_DEVICE.note_off(90, 63)
                yield from co_sleep(text_time - midi_time)
            xpos += 1
