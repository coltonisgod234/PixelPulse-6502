"""
Manages video logic for the PixelPulse
"""

# Pylint does not shut up about my imports, so I've forced it to
# pylint: disable=import-error

import pygame
from cpu.constants import APU_SAMPLERATE, DISPLAY_X_SIZE, DISPLAY_Y_SIZE, BLACK_COLORS_LIST_INDEX

from audiovisual.avhelpers import draw_pixel
from utils.helpers import get_high_nibble, get_low_nibble, is_multiple_of_2


def config_video() -> tuple:
    """
    Configure the system's video
    
    ...

    Returns
    -------
    tuple
        A tuple containing the pygame display surface and the pygame clock instance
    """
    clock = pygame.time.Clock()

    # Initalize The Pygame
    pygame.display.init()
    pygame.display.set_caption("PixelPulse 6502")
    pygame.mixer.init(APU_SAMPLERATE)
    display = pygame.display.set_mode((DISPLAY_X_SIZE*8, DISPLAY_Y_SIZE*8))
    return (display,clock)

def tick_events():
    """
    Tick all pygame events
    """
    # Handle The Pygame Things
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

def before_instruction():
    """
    To be executed at the start of an instruction
    """
    # Handle resetting the screen
    display = pygame.display.get_surface()
    display.fill((0,0,0))

def after_instruction():
    """
    To be executed at the end of an instruction
    """
    # Handle flipping the buffers
    #display = pygame.display.get_surface()
    pygame.display.flip()

def extract_pixel_at_location(x: int, y: int, vram: list[int]) -> int:
    """
    Extracts the colour of the pixel at a location in video memory (VRAM)

    ...

    Arguments
    ---------
    x : int
        The X position of the pixel

    y : int
        The Y position of the pixel

    vram : list[int]
        The video memory to pull the pixel from

    Returns
    -------
    int
        An integer from 0-15 representing an index into the systems colour pallete
    """
    if is_multiple_of_2(x):
        return get_low_nibble(vram[y * DISPLAY_Y_SIZE + x])
    else:
        return get_high_nibble(vram[y * DISPLAY_Y_SIZE + x])

def tick_display(vram: list[int]):
    """
    Update the display
    
    ...
    
    Arguments
    ---------
    vram : list[int]
        The video memory to use
    """
    # Handle drawing the pixels
    for x in range(DISPLAY_X_SIZE):  # Loop through all the pixels
        for y in range(DISPLAY_Y_SIZE):  # Loop through all the pixels
            # The address will be the same, so compute it now, this will save a minuscule, 
            # but still nice amount of time
            addr = y * DISPLAY_Y_SIZE + x

            # Color 1
            col = get_low_nibble(vram[addr])

            # Optimization: only draw pixels that change the starting colour (black) of our canvas
            if col != BLACK_COLORS_LIST_INDEX:
                draw_pixel(x, y, col)

            # Color 2
            col = get_high_nibble(vram[addr])

            if col != BLACK_COLORS_LIST_INDEX: # Black
                draw_pixel(x+4, y, col)
            #pixel_print(f"Bad pixel data. {e}", 2)
