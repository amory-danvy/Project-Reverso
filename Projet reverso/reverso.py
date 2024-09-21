import pygame
import math
from random import randint
# Difficultés
FACILE = (6, 480, 480)  # Grille 6x6, fenêtre 480x480
MOYEN = (9, 720, 720)   # Grille 8x8, fenêtre 720x720
DIFFICILE = (12, 960, 960)  # Grille 10x10, fenêtre 960x960

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Texte
base_font_size = 36

# Zoom text
scale_factor = 1  # Facteur de mise à l'échelle initial
max_scale = 3  # Facteur de mise à l'échelle maximal
min_scale = 1.5  # Facteur de mise à l'échelle minimal
scale_speed = 0.003  # Vitesse d'animation ajustée

# Initialisation de Pygame
pygame.init()

# Fenêtre du titre
title_screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Menu de Sélection de Difficulté")

# Variables d'animation
clock = pygame.time.Clock()

def draw_text(surface, text, pos, font_size, color=WHITE):
    """Affiche le texte sur la surface"""
    font = pygame.font.Font(None, font_size)  # Utilise une police par défaut
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)

def anime_title(surface, text, pos, time, color=WHITE):
    """zoom"""
    scale_factor = min_scale + (max_scale - min_scale) * (0.5 * (1 + math.sin(time * scale_speed)))

    # taille texte
    font_size = int(base_font_size * scale_factor)
    font = pygame.font.Font(None, font_size)

    # Rendu
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)

    # Affichage
    surface.blit(text_surface, text_rect)

def menu_principal():
    """Affiche le menu principal pour choisir la difficulté"""
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        title_screen.fill(BLACK)

        # titre anime
        anime_title(title_screen, "Reverso", (300, 100), current_time)

        # difficultés
        draw_text(title_screen, "1. Facile (6x6)", (300, 200), 36)
        draw_text(title_screen, "2. Moyen (9x9)", (300, 250), 36)
        draw_text(title_screen, "3. Difficile (12x12)", (300, 300), 36)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return FACILE
                elif event.key == pygame.K_2:
                    return MOYEN
                elif event.key == pygame.K_3:
                    return DIFFICILE

        pygame.display.update()
        clock.tick(60)  # Limiter à 60 FPS

def draw_fill_circle(surface, center, radius, color):
    pygame.draw.circle(surface, color, center, radius)

def draw_circle(surface, center, radius, color):
    pygame.draw.circle(surface, color, center, radius, 1)

def init_alea_plateau(T):
    """Génération aléatoire du plateau"""
    for i in range(len(T)):
        for j in range(len(T[i])):
            T[i][j] = randint(0, 1)  # Remplit chaque case avec 0 ou 1

def modif_plateau(c, T):
    """Modifie le plateau en inversant toutes les cases autour de la coordonnée c"""
    x, y = c
    if x >= 0 and y >= 0:
        # Inverser la case cliquée et les cases autour
        directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(T) and 0 <= ny < len(T[0]):
                T[nx][ny] = 1 - T[nx][ny]  # Inverser entre 0 et 1

def coord_to_centre(c, taille_case):
    """Renvoie les coordonnées du centre du cercle à la coordonnée c"""
    x = c[1] * taille_case + taille_case // 2
    y = c[0] * taille_case + taille_case // 2
    return (x, y)

def point_to_coord(p, taille_case, N):
    """Renvoie la coordonnée du cercle si le point p est dans celui-ci, (-1, -1) sinon"""
    for i in range(N):
        for j in range(N):
            x = j * taille_case + taille_case // 2
            y = i * taille_case + taille_case // 2
            if (p[0] - x) ** 2 + (p[1] - y) ** 2 <= (taille_case // 2) ** 2:
                return (i, j)
    return (-1, -1)

def affiche_plateau(T, f, taille_case):
    """Affiche le plateau par rapport au tableau T fourni"""
    f.fill(BLACK)
    for i in range(len(T)):
        for j in range(len(T[i])):
            center = coord_to_centre((i, j), taille_case)
            if T[i][j] == 0:
                draw_fill_circle(f, center, taille_case // 2, WHITE)
            else:
                draw_circle(f, center, taille_case // 2, WHITE)
    pygame.display.flip()

def plateau_non_monochrome(T):
    """Renvoie True si le plateau n'est pas monochrome (il existe encore des billes noires et blanches)"""
    first_value = T[0][0]
    for row in T:
        for val in row:
            if val != first_value:
                return True
    return False

# Menu
N, LARG_FEN, HAUT_FEN = menu_principal()
TAILLE_CASE = LARG_FEN // N

# Initialisation de la fenêtre et du plateau
plateau = [[0 for _ in range(N)] for _ in range(N)]
f = pygame.display.set_mode((LARG_FEN, HAUT_FEN))
pygame.display.set_caption("Jeu de Cercles")

# Programme principal
init_alea_plateau(plateau)
affiche_plateau(plateau, f, TAILLE_CASE)

# Boucle pour les events
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coord = point_to_coord(pos, TAILLE_CASE, N)
            modif_plateau(coord, plateau)
            affiche_plateau(plateau, f, TAILLE_CASE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False

    # check if win
    if not plateau_non_monochrome(plateau):
        print("Le plateau est monochrome ! Jeu terminé.")
        running = False

pygame.quit()
