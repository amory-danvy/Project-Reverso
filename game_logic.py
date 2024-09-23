# game_logic.py

import numpy as np

def init_random_board(N):
    """Returns a randomly initialized N x N board."""
    return np.random.randint(0, 2, (N, N))

def modify_board(c, T):
    """Modifies the board by flipping all cells around coordinate c."""
    x, y = c
    if x < 0 or y < 0:
        return
    directions = np.array([(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)])
    valid_indices = directions + [x, y]
    valid_indices = valid_indices[(valid_indices[:, 0] >= 0) & (valid_indices[:, 0] < T.shape[0]) &
                                  (valid_indices[:, 1] >= 0) & (valid_indices[:, 1] < T.shape[1])]
    T[valid_indices[:, 0], valid_indices[:, 1]] ^= 1

def point_to_coord(p, cell_size):
    """Returns the coordinate of the circle if point p is inside it, (-1, -1) otherwise."""
    i, j = p[1] // cell_size, p[0] // cell_size
    if (p[0] - (j * cell_size + cell_size // 2)) ** 2 + (p[1] - (i * cell_size + cell_size // 2)) ** 2 <= (cell_size // 2) ** 2:
        return i, j
    return -1, -1

def board_not_monochrome(T):
    """Returns True if the board is not monochrome."""
    return not np.all(T == T[0, 0])
