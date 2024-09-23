# graphics.py

import pygame
import math
import numpy as np
from settings import WHITE, BLACK, BASE_FONT_SIZE, MAX_TITLE_SCALE, MIN_TITLE_SCALE, TITLE_SCALE_SPEED, FONT_PATH

font_cache = {}

def get_font(size):
    """Returns a font object of the specified size, caching it if necessary."""
    if size not in font_cache:
        try:
            font_cache[size] = pygame.font.Font(FONT_PATH, size)
        except FileNotFoundError:
            print(f"Error: Font '{FONT_PATH}' not found. Using default font.")
            font_cache[size] = pygame.font.Font(None, size)
    return font_cache[size]

def draw_text(surface, text, pos, font_size, scale=1):
    """Draws text on the given surface with optional scaling."""
    font = get_font(int(font_size * scale))
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, text_surface.get_rect(center=pos))

def animate_title(surface, text, pos, time):
    """Animates text with a zoom effect."""
    scale_factor = MIN_TITLE_SCALE + (MAX_TITLE_SCALE - MIN_TITLE_SCALE) * (0.5 * (1 + math.sin(time * TITLE_SCALE_SPEED)))
    draw_text(surface, text, pos, BASE_FONT_SIZE, scale_factor)

def display_board(T, f, cell_size):
    """Displays the board based on the provided grid T."""
    f.fill(BLACK)
    centers = np.indices(T.shape).T.reshape(-1, 2) * cell_size + cell_size // 2
    for (i, j), center in zip(np.ndindex(T.shape), centers):
        pygame.draw.circle(f, WHITE, tuple(center), cell_size // 2, 0 if T[i, j] == 0 else 1)
    pygame.display.flip()
