from pygame import Surface, image

CREDITS: str
with open('assets/credits.txt', 'r') as fp:
    CREDITS = fp.read().strip()


HELP_TEXT: str
with open('assets/help.txt', 'r') as fp:
    HELP_TEXT = fp.read().strip()


MAP_IMAGE: Surface
MAP_IMAGE = image.load('assets/map.png').convert_alpha()
