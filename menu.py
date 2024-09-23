# menu.py

import pygame
from graphics import draw_text, animate_title
from settings import EASY, MEDIUM, HARD, NORMAL_SCALE, MAX_SCALE, SCALE_SPEED, BASE_FONT_SIZE, BLACK

def main_menu(screen, clock, menu_sound):
    """Displays the main menu to choose difficulty with mouse interaction."""
    options = [
        {"text": "Easy (6x6)", "rect": pygame.Rect(200, 177, 200, 50), "scale": NORMAL_SCALE, "difficulty": EASY},
        {"text": "Medium (9x9)", "rect": pygame.Rect(200, 228, 200, 50), "scale": NORMAL_SCALE, "difficulty": MEDIUM},
        {"text": "Hard (12x12)", "rect": pygame.Rect(200, 280, 200, 50), "scale": NORMAL_SCALE, "difficulty": HARD},
    ]
    
    prev_option = None
    
    while True:
        screen.fill(BLACK)
        animate_title(screen, "Reverso", (300, 100), pygame.time.get_ticks())

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        for option in options:
            if option["rect"].collidepoint(mouse_pos):
                option["scale"] = min(MAX_SCALE, option["scale"] + SCALE_SPEED)
                
                if menu_sound and (prev_option != option):
                    menu_sound.play()
                    prev_option = option
                    
                if mouse_clicked:
                    return option["difficulty"]
            else:
                option["scale"] = max(NORMAL_SCALE, option["scale"] - SCALE_SPEED)

            draw_text(screen, option["text"], option["rect"].center, BASE_FONT_SIZE, option["scale"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
