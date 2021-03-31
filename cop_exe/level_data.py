from typing import Optional

from pygame import Vector2


Coordinate = tuple[float, float]
Destination = Optional[Coordinate]
Option = tuple[Destination, Destination]


class Node:
    render: Vector2
    left: Optional[Option]
    right: Optional[Option]
    up: Optional[Option]
    down: Optional[Option]

    def __init__(self, render, *, left: Optional[Option] = None,
                                  right: Optional[Option] = None,
                                  up: Optional[Option] = None,
                                  down: Optional[Option] = None) -> None:
        self.render = Vector2(render)
        self.left = left
        self.right = right
        self.up = up
        self.down = down


MAX_COORDS = (4, 4)


LEVEL: dict[Coordinate, Node] = {
    # First row
    (0, 0): Node(
        (20, 24),
    ),
    (1, 0): Node(
        (180, 24),
    ),
    (2, 0): Node(
        (340, 24),
    ),
    (3, 0): Node(
        (500, 24),
        down = ((3, 0.5), None),
    ),
    (4, 0): Node(
        (620, 24),
    ),

    # Second row
    (0, 1): Node(
        (20, 200),
        right = ((1, 1), None),
    ),
    (1, 1): Node(
        (180, 200),
        right = (None, None),
        down = ((1, 2), (0, 3)),
    ),
    (2, 1): Node(
        (340, 200),
        left = (None, None),
    ),
    (3, 1): Node(
        (500, 200),
        left = ((2, 1), None),
        up = (None, None),
    ),
    (4, 1): Node(
        (620, 200),
    ),

    # Third row
    (0, 2): Node(
        (20, 380),
    ),
    (1, 2): Node(
        (180, 380),
        down = ((0, 3), None),
    ),
    (2, 2): Node(
        (321, 361),
    ),
    (3, 2): Node(
        (500, 380),
        up = ((3, 1), None),
    ),
    (4, 2): Node(
        (620, 380),
    ),

    # Fourth row
    (0, 3): Node(
        (20, 560),
        right = ((1, 2), None),
    ),
    (2, 3): Node(
        (340, 560),
        left = ((1.5, 3), None),
    ),
    (3, 3): Node(
        (500, 560),
        left = ((2, 3), (1.5, 3)),
    ),
    (4, 3): Node(
        (620, 560),
    ),

    # Fifth row
    (0, 4): Node(
        (20, 700),
    ),
    (1, 4): Node(
        (180, 700),
        up = ((1, 3.5), (1, 0)),
    ),
    (2, 4): Node(
        (340, 700),
    ),
    (3, 4): Node(
        (500, 700),
    ),
    (4, 4): Node(
        (620, 700),
    ),

    # Miscellaneous
    (3, 0.5): Node(
        (480, 91),
        up = ((3, 0), None),
        down = (None, None),
        left = (None, None),
        right = (None, None),
    ),
    (1.5, 3): Node(
        (212, 540),
        up = (None, None),
        down = (None, None),
        left = (None, None),
        right = ((2, 3), (3, 3)),
    ),
    (1, 3.5): Node(
        (160, 595),
        up = (None, None),
        down = ((1, 4), None),
        left = (None, None),
        right = (None, None),
    ),
}
