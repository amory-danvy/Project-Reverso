# audio.py

import pygame
from settings import POP_SOUND_PATH, MENU_SOUND_PATH, BACKGROUND_MUSIC_PATH

def load_sound(path):
    """Loads a sound effect from the specified path."""
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"Error: Sound file '{path}' not found.")
        return None

def load_music(path):
    """Loads and plays background music from the specified path."""
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except pygame.error:
        print(f"Error: Music file '{path}' not found. No background music will play.")
