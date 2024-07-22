import pygame

from constants import APU_SAMPLERATE, DISPLAY_X_SIZE, DISPLAY_Y_SIZE
from controller.keyboard import p1_key_mappings
from audiovisual.avhelpers import draw_pixel
from helpers import get_high_nibble, get_low_nibble, pixel_print, is_multiple_of_2

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

def extract_pixel_at_location(x: int, y: int, vram: list) -> int:
    if is_multiple_of_2(x):
        return get_low_nibble(vram[y * DISPLAY_Y_SIZE + x])
    else:
        return get_high_nibble(vram[y * DISPLAY_Y_SIZE + x])

def tick_display(vram: list):
    
    # Handle drawing the pixels
    for x in range(DISPLAY_X_SIZE):  # Loop through all the pixels
        for y in range(DISPLAY_Y_SIZE):  # Loop through all the pixels
            if get_low_nibble(vram[y * DISPLAY_Y_SIZE + x]) == 0 and get_high_nibble(vram[y * DISPLAY_Y_SIZE + x]) == 0:
                continue

            col = get_low_nibble(vram[y * DISPLAY_Y_SIZE + x])
            draw_pixel(x, y, col)

            col = get_high_nibble(vram[y * DISPLAY_Y_SIZE + x])
            draw_pixel(x, y, col)
            
            #pixel_print(f"Bad pixel data. {e}", 2)