import pygame

from constants import APU_SAMPLERATE, DISPLAY_X_SIZE, DISPLAY_Y_SIZE
from controller.keyboard import p1_key_mappings
from audiovisual.avhelpers import draw_pixel
from helpers import pixel_print

def config_video():
    clock = pygame.time.Clock()

    # Initalize The Pygame
    pygame.display.init()
    pygame.display.set_caption("PixelPulse 6502")
    pygame.mixer.init(APU_SAMPLERATE)
    display = pygame.display.set_mode((DISPLAY_X_SIZE*5, DISPLAY_Y_SIZE*5))
    return (display,clock)

def tick_events():
    # Handle The Pygame Things
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()

def before_instruction():
    # Handle resetting the screen
    display = pygame.display.get_surface()
    display.fill((0,0,0))

def after_instruction():
    # Handle flipping the buffers
    #display = pygame.display.get_surface()
    pygame.display.flip()

def tick_display(vram: list):
    # Handle drawing the pixels
    for x in range(DISPLAY_X_SIZE):  # Loop through all the pixels
        for y in range(DISPLAY_Y_SIZE):  # Loop through all the pixels
            try:
                col = vram[y * 64 + x]  # Locate them
                draw_pixel(x, y, col)  # Make 'em pulse (as in draw them)
            except IndexError as e:
                pixel_print(f"Bad pixel data. {e}", 4)