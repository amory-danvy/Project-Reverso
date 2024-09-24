# main.py

import pygame
from menu import main_menu
from graphics import display_board
from audio import load_sound, load_music
from game_logic import init_random_board, modify_board, point_to_coord, board_not_monochrome

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Difficulty Selection Menu")
clock = pygame.time.Clock()

# Load Audio
pop_sound = load_sound('Audio/pop.wav')
menu_sound = load_sound('Audio/GmodSpawn.wav')
load_music('Audio/background_music.mp3')

# Main Menu - Select difficulty and get game settings
N, WINDOW_WIDTH, WINDOW_HEIGHT = main_menu(screen, clock, menu_sound)
CELL_SIZE = WINDOW_WIDTH // N

# Initialize the window and board
board = init_random_board(N)
f = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Reverso")

# Main Program - Display the initial board
display_board(board, f, CELL_SIZE)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coord = point_to_coord(pos, CELL_SIZE)
            if coord != (-1, -1):
                modify_board(coord, board)
                display_board(board, f, CELL_SIZE)
                if pop_sound:  # Play the pop sound if it was loaded successfully
                    pop_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Check win condition
    if not board_not_monochrome(board):
        print("The board is monochrome! Game over.")
        running = False

pygame.quit()

