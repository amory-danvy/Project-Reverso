import pygame
import math
import numpy as np  # Efficient array manipulations

# Constants
FACILE = (6, 480, 480)
MOYEN = (9, 720, 720)
DIFFICILE = (12, 960, 960)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASE_FONT_SIZE = 36
MAX_SCALE = 1.3
MAX_TITLE_SCALE = 3
MIN_TITLE_SCALE = 1.5
NORMAL_SCALE = 1
SCALE_SPEED = 0.1
TITLE_SCALE_SPEED = 0.003
FONT_PATH = 'Font/Stimcard.ttf'  # Path to the custom font
POP_SOUND_PATH = 'Audio/pop.wav'  # Path to the pop sound effect
MENU_SOUND_PATH = 'Audio/GmodSpawn.wav' # Path to the menu sound effect
BACKGROUND_MUSIC_PATH = 'Audio/background_music.mp3'  # Path to the background music

# Pygame Initialization
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects and music
title_screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Menu de Sélection de Difficulté")
clock = pygame.time.Clock()

# Load sound effect
try:
    pop_sound = pygame.mixer.Sound(POP_SOUND_PATH)
except pygame.error:
    print(f"Error: Sound file '{POP_SOUND_PATH}' not found.")
    pop_sound = None  # Set to None if loading fails to prevent crashes
    
# Load menu sound effect
try:
    menu_sound = pygame.mixer.Sound(MENU_SOUND_PATH)
except pygame.error:
    print(f"Error: Sound file '{MENU_SOUND_PATH}' not found.")
    menu_sound = None  # Set to None if loading fails to prevent crashes

# Load and play background music
try:
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)  # Loop indefinitely
except pygame.error:
    print(f"Error: Music file '{BACKGROUND_MUSIC_PATH}' not found. No background music will play.")

# Preloaded fonts and surfaces for static texts
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

def menu_principal():
    """Displays the main menu to choose difficulty with mouse interaction."""
    options = [
        {"text": "Easy (6x6)", "rect": pygame.Rect(200, 177, 200, 50), "scale": NORMAL_SCALE, "difficulty": FACILE},
        {"text": "Medium (9x9)", "rect": pygame.Rect(200, 228, 200, 50), "scale": NORMAL_SCALE, "difficulty": MOYEN},
        {"text": "Hard (12x12)", "rect": pygame.Rect(200, 280, 200, 50), "scale": NORMAL_SCALE, "difficulty": DIFFICILE},
    ]
    
    sound_played = False  # Variable pour suivre si le son a déjà été joué

    while True:
        title_screen.fill(BLACK)
        anime_title(title_screen, "Reverso", (300, 100), pygame.time.get_ticks())

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        for option in options:
            if option["rect"].collidepoint(mouse_pos):
                option["scale"] = min(MAX_SCALE, option["scale"] + SCALE_SPEED)
                
                if menu_sound and not sound_played:  # Vérifie si le son n'a pas encore été joué
                    menu_sound.play()
                    sound_played = True  # Marque que le son a été joué

                if mouse_clicked:
                    return option["difficulty"]
            else:
                option["scale"] = max(NORMAL_SCALE, option["scale"] - SCALE_SPEED)

            # Réinitialise sound_played après avoir vérifié tous les rectangles
            sound_played = False if not any(option["rect"].collidepoint(mouse_pos) for option in options) else sound_played

            draw_text(title_screen, option["text"], option["rect"].center, BASE_FONT_SIZE, option["scale"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)

def anime_title(surface, text, pos, time):
    """Animates text with a zoom effect."""
    scale_factor = MIN_TITLE_SCALE + (MAX_TITLE_SCALE - MIN_TITLE_SCALE) * (0.5 * (1 + math.sin(time * TITLE_SCALE_SPEED)))
    draw_text(surface, text, pos, BASE_FONT_SIZE, scale_factor)

def init_alea_plateau(N):
    """Returns a randomly initialized N x N board."""
    return np.random.randint(0, 2, (N, N))

def modif_plateau(c, T):
    """Modifies the board by flipping all cells around coordinate c."""
    x, y = c
    if x < 0 or y < 0:
        return
    # Using NumPy indexing to flip cells efficiently
    directions = np.array([(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)])
    valid_indices = directions + [x, y]
    valid_indices = valid_indices[(valid_indices[:, 0] >= 0) & (valid_indices[:, 0] < T.shape[0]) &
                                  (valid_indices[:, 1] >= 0) & (valid_indices[:, 1] < T.shape[1])]
    T[valid_indices[:, 0], valid_indices[:, 1]] ^= 1

def point_to_coord(p, taille_case):
    """Returns the coordinate of the circle if point p is inside it, (-1, -1) otherwise."""
    i, j = p[1] // taille_case, p[0] // taille_case
    if (p[0] - (j * taille_case + taille_case // 2)) ** 2 + (p[1] - (i * taille_case + taille_case // 2)) ** 2 <= (taille_case // 2) ** 2:
        return i, j
    return -1, -1

def affiche_plateau(T, f, taille_case):
    """Displays the board based on the provided grid T."""
    f.fill(BLACK)
    centers = np.indices(T.shape).T.reshape(-1, 2) * taille_case + taille_case // 2
    for (i, j), center in zip(np.ndindex(T.shape), centers):
        pygame.draw.circle(f, WHITE, tuple(center), taille_case // 2, 0 if T[i, j] == 0 else 1)
    pygame.display.flip()

def plateau_non_monochrome(T):
    """Returns True if the board is not monochrome."""
    return not np.all(T == T[0, 0])

# Main Menu
N, LARG_FEN, HAUT_FEN = menu_principal()
TAILLE_CASE = LARG_FEN // N

# Initialize the window and board
plateau = init_alea_plateau(N)
f = pygame.display.set_mode((LARG_FEN, HAUT_FEN))
pygame.display.set_caption("Reverso ")

# Main Program
affiche_plateau(plateau, f, TAILLE_CASE)

# Event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coord = point_to_coord(pos, TAILLE_CASE)
            if coord != (-1, -1):
                modif_plateau(coord, plateau)
                affiche_plateau(plateau, f, TAILLE_CASE)
                if pop_sound:  # Play the pop sound if it was loaded successfully
                    pop_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Check win condition
    if not plateau_non_monochrome(plateau):
        print("Le plateau est monochrome ! Jeu terminé.")
        running = False

pygame.quit()
