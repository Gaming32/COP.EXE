from cop_exe.level_data import Coordinate, LEVEL, MAX_COORDS
from pygame import Surface, Vector2

from cop_exe.consts import CHARACTER_OPACITY, ENEMY_COLOR, PLAYER_COLOR
from cop_exe.pygame_import import *


class Game:
    player: Coordinate
    enemy: Coordinate

    def __init__(self) -> None:
        self.enemy = (3, 3)
        self.player = (2, 1)
        self.commands = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down,
        }

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
            if enemy_pos is not None:
                pygame.draw.circle(psurf, ENEMY_COLOR, enemy_pos.render, 10)
            if player_pos is not None:
                pygame.draw.circle(psurf, PLAYER_COLOR, player_pos.render, 10)
            psurf.set_alpha(CHARACTER_OPACITY)
            surf.blit(psurf, (0, 0))
    
    def player_move(self, name: str, amnt: int):
        if amnt > 2:
            yield from global_vars.text_box.slow_print("Can't move", name, 'more than 2 blocks')
            return
        if amnt < 1:
            yield from global_vars.text_box.slow_print("Can't move", name, 'less than 1 block')
            return
        node = LEVEL[self.player]
        choices = getattr(node, name)
        if choices is None:
            if name == 'left':
                next = (self.player[0] - amnt, self.player[1])
            elif name == 'right':
                next = (self.player[0] + amnt, self.player[1])
            elif name == 'up':
                next = (self.player[0], self.player[1] - amnt)
            elif name == 'down':
                next = (self.player[0], self.player[1] + amnt)
        else:
            next = getattr(node, name)[amnt - 1]
        if next is None or next[0] > MAX_COORDS[0] or next[0] < 0 or next[1] > MAX_COORDS[1] or next[1] < 0:
            yield from global_vars.text_box.slow_print('There is no road leading in that direction')
            return
        self.player = next

    def move_left(self, amnt: int):
        yield from self.player_move('left', amnt)

    def move_right(self, amnt: int):
        yield from self.player_move('right', amnt)

    def move_up(self, amnt: int):
        yield from self.player_move('up', amnt)

    def move_down(self, amnt: int):
        yield from self.player_move('down', amnt)


from cop_exe.co_utils import *
from cop_exe import global_vars
