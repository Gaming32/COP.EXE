from pygame import Surface, Vector2

from cop_exe.consts import CHARACTER_OPACITY, ENEMY_COLOR, PLAYER_COLOR
from cop_exe.pygame_import import *


class Game:
    player: Vector2
    enemy: Vector2

    def __init__(self) -> None:
        # Vector2(320, 360)
        self.enemy = Vector2(500, 560)
        self.player = Vector2(340, 200)
        self.commands = {
            'debug move': self.debug_move,
            'left': self.move_left
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
                args[i] = argtypes[argname](arg)
        try:
            yield from self.commands[command](*args)
        except Exception as e:
            disp = global_vars.text_box.slow_print(f'Error in command "{command}": {e.__class__.__qualname__}:', e)
            yield next(disp)
            import traceback
            traceback.print_exc()
            yield from disp

    def render(self, surf: Surface):
        if global_vars.intro_part > 1:
            psurf = Surface(surf.get_size()).convert_alpha()
            psurf.fill((0, 0, 0, 0))
            pygame.draw.circle(psurf, ENEMY_COLOR, self.enemy, 10)
            pygame.draw.circle(psurf, PLAYER_COLOR, self.player, 10)
            psurf.set_alpha(CHARACTER_OPACITY)
            surf.blit(psurf, (0, 0))

    def debug_move(self, x: int, y: int):
        self.player += (x, -y)
        yield

    def move_left(self):
        self.player.x -= 160
        yield


from cop_exe.co_utils import *
from cop_exe import global_vars
