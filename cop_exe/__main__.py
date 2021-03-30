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


pygame.key.set_repeat()
box = TextBox(Rect(660, 20, 600, 680), START_TEXT.strip())
global_vars.allow_typing = True
global_vars.text_box = box


clock = pygame.time.Clock()


running = True
while running:
    delta = clock.tick(FRAMERATE) / 1000
    global_vars.delta = delta

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if global_vars.allow_typing:
                if event.key == K_BACKSPACE:
                    if len(box.text[-1]) > 1:
                        if event.mod & KMOD_CTRL:
                            pos = box.text[-1].rfind(' ')
                            if pos == -1:
                                pos = 1
                            box.text[-1] = box.text[-1][:pos]
                        else:
                            box.text[-1] = box.text[-1][:-1]
                elif event.key == K_RETURN:
                    global_vars.allow_typing = False
                    try:
                        command = shlex.split(box.text[-1].removeprefix('>'))
                    except Exception as e:
                        box.print('Parse error:', e)
                    else:
                        if not command:
                            pass
                        elif command[0] == 'echo':
                            box.print(*command[1:])
                        elif command[0] == 'help':
                            box.print(HELP_TEXT)
                        elif command[0] == 'credits':
                            box.print(CREDITS)
                        else:
                            box.print(f'No command called "{command[0]}"')
                    box.text[-1] += '>'
                    global_vars.allow_typing = True
        elif event.type == TEXTINPUT and global_vars.allow_typing:
            box.text[-1] += event.text
        elif event.type == KEYUP:
            if event.key == K_F11:
                fullscreen = not fullscreen
                flags = (FULLSCREEN | SCALED) if fullscreen else 0
                pygame.display.quit()
                pygame.display.init()
                screen = pygame.display.set_mode(WINDOW_SIZE, flags)
                global_vars.screen = screen

    screen.fill(CLEAR_COLOR)
    box.render(screen)

    pygame.display.update()


pygame.quit()
