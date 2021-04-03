from cop_exe.texts import ROBBER_HIDDEN, ROBBER_NOT_SHOWN, ROBBER_SHOWN, WIN
import random
from typing import Callable
import webbrowser

from pygame import Surface

from cop_exe.consts import CHARACTER_OPACITY, ENEMY_COLOR, PLAYER_COLOR
from cop_exe.level_data import LEVEL, MAX_COORDS, Coordinate, Node
from cop_exe.pygame_import import *


def get_movement(choices, name, cur, amnt):
    if choices is None:
        if name == 'left':
            return (cur[0] - amnt, cur[1])
        elif name == 'right':
            return (cur[0] + amnt, cur[1])
        elif name == 'up':
            return (cur[0], cur[1] - amnt)
        elif name == 'down':
            return (cur[0], cur[1] + amnt)


def get_enemy_move(node: Node, enemy: tuple, player: tuple, dirs: list, dir: str, amnt: int = 1, cnt: int = 3):
    choices = getattr(node, dir)
    if choices is None:
        next = get_movement(choices, dir, enemy, amnt)
    else:
        next = choices[amnt - 1]
    if next is not None and next != player:
        dirs.extend([next] * cnt)


class Game:
    player: Coordinate
    enemy: Coordinate
    commands: dict[str, Callable[..., None]]
    show_enemy: bool
    over: bool

    def __init__(self) -> None:
        self.enemy = (3, 3)
        self.player = (2, 1)
        self.commands = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down,
        }
        self.show_enemy = True
        self.over = False

    def command_wrapper(self, command: str, *args):
        func = self.commands.get(command)
        if func is None:
            yield from global_vars.text_box.slow_print(f'No command named "{command}"')
        argcount = func.__code__.co_argcount
        if len(args) != argcount - 1:
            yield from global_vars.text_box.slow_print(command, 'command requires exactly', argcount - 1, 'arguments')
            return
        argnames = func.__code__.co_varnames[1:argcount]
        argtypes = func.__annotations__
        args = list(args)
        for (i, arg) in enumerate(args):
            argname = argnames[i]
            if argname in argtypes:
                try:
                    args[i] = argtypes[argname](arg)
                except Exception:
                    disp = global_vars.text_box.slow_print(f'Invalid {argtypes[argname].__name__}: "{arg}"')
                    yield next(disp)
                    import traceback
                    traceback.print_exc()
                    yield from disp
                    return
        try:
            yield from self.commands[command](*args)
        except Exception as e:
            disp = global_vars.text_box.slow_print(f'Error in command "{command}": {e.__class__.__qualname__}:', e)
            yield next(disp)
            import traceback
            traceback.print_exc()
            yield from disp

    def render(self, surf: Surface):
        player_pos = LEVEL.get(self.player)
        enemy_pos = LEVEL.get(self.enemy)
        if global_vars.intro_part > 1:
            psurf = Surface(surf.get_size()).convert_alpha()
            psurf.fill((0, 0, 0, 0))
            if self.show_enemy and self.enemy == self.player:
                pygame.draw.circle(psurf, PLAYER_COLOR if global_vars.blink_on else ENEMY_COLOR, enemy_pos.render, 10)
            else:
                if self.show_enemy and enemy_pos is not None:
                    pygame.draw.circle(psurf, ENEMY_COLOR, enemy_pos.render, 10)
                if player_pos is not None:
                    pygame.draw.circle(psurf, PLAYER_COLOR, player_pos.render, 10)
            psurf.set_alpha(CHARACTER_OPACITY)
            surf.blit(psurf, (0, 0))

    def move_enemy(self):
        if self.player == self.enemy:
            self.over = True
            self.show_enemy = True
            yield from global_vars.text_box.slow_print(WIN)
            return
        curnode = LEVEL.get(self.enemy)
        if curnode is None:
            return
        dirs = []
        if self.enemy[0] > 0:
            get_enemy_move(curnode, self.enemy, self.player, dirs, 'left')
            if self.enemy[0] > 1:
                get_enemy_move(curnode, self.enemy, self.player, dirs, 'left', 2, 1)
        if self.enemy[0] < MAX_COORDS[0]:
            get_enemy_move(curnode, self.enemy, self.player, dirs, 'right')
            if self.enemy[0] < MAX_COORDS[0] - 1:
                get_enemy_move(curnode, self.enemy, self.player, dirs, 'right', 2, 1)
        if self.enemy[1] > 0:
            get_enemy_move(curnode, self.enemy, self.player, dirs, 'up')
            if self.enemy[1] > 1:
                get_enemy_move(curnode, self.enemy, self.player, dirs, 'up', 2, 1)
        if self.enemy[1] < MAX_COORDS[1]:
            get_enemy_move(curnode, self.enemy, self.player, dirs, 'down')
            if self.enemy[1] < MAX_COORDS[1] - 1:
                get_enemy_move(curnode, self.enemy, self.player, dirs, 'down', 2, 1)
        move = random.choice(dirs)
        self.enemy = move
        if self.show_enemy:
            self.show_enemy = False
            yield from global_vars.text_box.slow_print(random.choice(ROBBER_HIDDEN))
        elif random.random() < .33:
            self.show_enemy = True
            yield from global_vars.text_box.slow_print(random.choice(ROBBER_SHOWN))
        else:
            yield from global_vars.text_box.slow_print(random.choice(ROBBER_NOT_SHOWN))

    def player_move(self, name: str, amnt: int):
        if self.over:
            yield from global_vars.text_box.slow_print('The game is over! Go home!')
            webbrowser.open_new_tab('https://youtu.be/QRJ38y4Jn6k?t=8')
            return
        if amnt > 2:
            yield from global_vars.text_box.slow_print("Can't move", name, 'more than 2 blocks')
            return
        if amnt < 1:
            yield from global_vars.text_box.slow_print("Can't move", name, 'less than 1 block')
            yield from self.move_enemy()
            return
        node = LEVEL[self.player]
        choices = getattr(node, name)
        if choices is None:
            next = get_movement(choices, name, self.player, amnt)
        else:
            next = getattr(node, name)[amnt - 1]
        if next is None or next[0] > MAX_COORDS[0] or next[0] < 0 or next[1] > MAX_COORDS[1] or next[1] < 0:
            yield from global_vars.text_box.slow_print('There is no road leading in that direction')
            yield from self.move_enemy()
            return
        self.player = next
        yield from self.move_enemy()

    def move_left(self, amnt: int):
        yield from self.player_move('left', amnt)

    def move_right(self, amnt: int):
        yield from self.player_move('right', amnt)

    def move_up(self, amnt: int):
        yield from self.player_move('up', amnt)

    def move_down(self, amnt: int):
        yield from self.player_move('down', amnt)


from cop_exe import global_vars
from cop_exe.co_utils import *
