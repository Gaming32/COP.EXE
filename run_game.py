import sys

PYTHON_39 = (3, 9)
PYGAME_20 = (2, 0)


if sys.version_info[:2] < PYTHON_39:
    print('COP.EXE requires Python>=3.9')
    sys.exit(1)


have_pygame_20 = True

try:
    import pygame
except ImportError:
    have_pygame_20 = False
else:
    import pygame.version
    if pygame.version.vernum[:2] < PYGAME_20:
        have_pygame_20 = False

if not have_pygame_20:
    print('COP.EXE requires pygame>=2.0')
    sys.exit(2)


import cop_exe.__main__
