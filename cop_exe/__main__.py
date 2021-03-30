import shlex

from cop_exe.text_box import TextBox
from cop_exe import global_vars
from cop_exe.consts import *
from cop_exe.pygame_import import *
from cop_exe import __doc__ as START_TEXT
from cop_exe.assets import CREDITS, HELP_TEXT


fullscreen = False
screen = pygame.display.set_mode(WINDOW_SIZE)
global_vars.screen = screen
pygame.display.set_caption('COP.EXE')


global_vars.coroutines = []
global_vars.pressed_keys = set()


def start():
    global_vars.allow_typing = False
    yield from box.slow_print(START_TEXT.strip())
    box.print('\n>', end='')
    global_vars.allow_typing = True


def execute(func, *args, **kwargs):
    def wrapper():
        global_vars.allow_typing = False
        yield from func(*args, **kwargs)
        box.print('>', end='')
        global_vars.allow_typing = True
    global_vars.coroutines.append(wrapper())


pygame.key.set_repeat()
box = TextBox(Rect(660, 20, 600, 680))
global_vars.text_box = box
global_vars.coroutines.append(start())


clock = pygame.time.Clock()
typed = ''


running = True
while running:
    delta = clock.tick(FRAMERATE) / 1000
    global_vars.delta = delta

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            global_vars.pressed_keys.add(event.key)
            if global_vars.allow_typing:
                if event.key == K_BACKSPACE:
                    if len(box.text[-1]) > 1:
                        if event.mod & KMOD_CTRL:
                            pos = box.text[-1].rfind(' ')
                            if pos == -1:
                                pos = 1
                            box.text[-1] = box.text[-1][:pos]
                            typed = typed[:pos - 1]
                        else:
                            box.text[-1] = box.text[-1][:-1]
                            typed = typed[:-1]
                elif event.key == K_RETURN:
                    box.print()
                    try:
                        command = shlex.split(typed)
                    except Exception as e:
                        box.print('Parse error:', e)
                    else:
                        if not command:
                            box.text[-1] += '>'
                        elif command[0] == 'echo':
                            execute(box.slow_print, *command[1:])
                        elif command[0] == 'help':
                            execute(box.slow_print, HELP_TEXT)
                        elif command[0] == 'credits':
                            execute(box.slow_print, CREDITS)
                        else:
                            execute(box.slow_print, f'No command named "{command[0]}"')
                    typed = ''
        elif event.type == TEXTINPUT and global_vars.allow_typing:
            box.print(event.text, end='')
            typed += event.text
        elif event.type == KEYUP:
            global_vars.pressed_keys.discard(event.key)
            if event.key == K_F11:
                fullscreen = not fullscreen
                flags = (FULLSCREEN | SCALED) if fullscreen else 0
                pygame.display.quit()
                pygame.display.init()
                screen = pygame.display.set_mode(WINDOW_SIZE, flags)
                global_vars.screen = screen

    to_keep = []
    for coroutine in global_vars.coroutines:
        if next(coroutine, '__marker__') != '__marker__':
            to_keep.append(coroutine)
    global_vars.coroutines[:] = to_keep

    screen.fill(CLEAR_COLOR)
    box.render(screen)

    pygame.display.update()


pygame.quit()
