"""
Keyboard
"""

import pygame
from cpu.states import SystemControllerState, tick_controllers
from utils.helpers import pixel_print

p1_key_mappings = {
    "a": pygame.K_x,
    "b": pygame.K_z,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

def tick_keyboard(keys_pressed: pygame.key.ScancodeWrapper,
                  controller1: SystemControllerState, controller2: SystemControllerState):
    """
    Ticks the keyboard

    ...

    Arguments
    ---------
    keys_pressed : pygame.key.ScancodeWrapper
        A pygame ScancodeWrapper object containing all keys state
    
    controller1 : SystemControllerState
        A SystemControllerState object representing what buttons are 
        pushed on the emulated controller
    """
    for button, key in p1_key_mappings.items():
        if keys_pressed[key]:
            #pixel_print(f"  Ticking button {button}, key {key} ({keys_pressed[key]}): Pressed")
            controller1.press(button)
        else:
            #pixel_print(f"  Ticking button {button}, key {key} ({keys_pressed[key]}): No Pressed")
            controller1.release(button)
