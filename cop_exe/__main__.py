from cop_exe.utils import run_function
import shlex

from cop_exe import __doc__ as START_TEXT
from cop_exe import global_vars
from cop_exe.co_utils import *
from cop_exe.consts import *
from cop_exe.game import Game
from cop_exe.pygame_import import *
from cop_exe.text_box import TextBox

fullscreen = False
screen = pygame.display.set_mode(WINDOW_SIZE)
global_vars.screen = screen
pygame.display.set_caption('COP.EXE')
global_vars.game = Game()
global_vars.intro_part = 0


global_vars.coroutines = []
global_vars.pressed_keys = set()


def start():
    global_vars.allow_typing = False
    parts = START_TEXT.split('---NEXT---')
    for part in range(len(parts)):
        yield from box.slow_print(parts[part].strip() + '\n')
        global_vars.intro_part += 1
    box.print('>', end='')
    global_vars.text_box.reset_skipped()
    global_vars.allow_typing = True


def restart():
    global_vars.allow_typing = False
    global_vars.intro_part = 2
    global_vars.game = Game()
    box.text.clear()
    box.text.append('')
    *parts, intro = START_TEXT.split('---NEXT---')
    yield from box.slow_print(intro.strip() + '\n')
    global_vars.intro_part = 3
    box.print('>', end='')
    global_vars.text_box.reset_skipped()
    global_vars.allow_typing = True


pygame.key.set_repeat()
box = TextBox(Rect(660, 20, 600, 680))
global_vars.text_box = box
global_vars.coroutines.append(start())


clock = pygame.time.Clock()
typed = ''


from cop_exe.assets import CREDITS, HELP_TEXT, MAP_IMAGE

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
                        execute(box.slow_print, 'Parse error:', e)
                    else:
                        if not command:
                            box.print('>', end='')
                        elif command[0] == 'echo':
                            execute(box.slow_print, *command[1:])
                        elif command[0] == 'help':
                            execute(box.slow_print, HELP_TEXT)
                        elif command[0] == 'credits':
                            execute(box.slow_print, CREDITS)
                        elif command[0] == 'clear':
                            box.text.clear()
                            box.text.append('')
                            box.print('>', end='')
                        elif command[0] == 'quit':
                            running = False
                        elif command[0] == 'restart':
                            global_vars.coroutines.append(restart())
                        elif command[0] in global_vars.game.commands:
                            execute(global_vars.game.command_wrapper, *command)
                        else:
                            execute(box.slow_print, f'No command named "{command[0]}"')
                    typed = ''
        elif event.type == TEXTINPUT:
            if global_vars.allow_typing:
                box.print(event.text, end='')
                typed += event.text
            elif not box.skipped:
                box.backlog += event.text
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
    if global_vars.intro_part > 0:
        screen.blit(MAP_IMAGE, (0, 0))
    global_vars.game.render(screen)
    box.render(screen)

    pygame.display.update()


pygame.quit()
