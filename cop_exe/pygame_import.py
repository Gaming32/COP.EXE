import pygame

# These imports are necessary for PyLance to autocomplete for some reason
#isort:split
import pygame.display
import pygame.draw
import pygame.event
import pygame.key
import pygame.time

#isort:split
from pygame import *
from pygame.locals import *

pygame.init()


from pygame import midi
from typing import Optional
MIDI_DEVICE: Optional[midi.Output]
MIDI_ENABLED: bool

try:
    midi.init()
    MIDI_DEVICE = midi.Output(0)
    MIDI_ENABLED = True
except (pygame.error, midi.MidiException) as e:
    import sys
    print('Unable to load midi:', e, file=sys.stderr)
    MIDI_DEVICE = None
    MIDI_ENABLED = False
