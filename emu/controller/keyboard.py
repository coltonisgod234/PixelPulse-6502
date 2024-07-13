import pygame
from cpu.states import SystemControllerState

p1_key_mappings = {
    pygame.K_x: "a",
    pygame.K_z: "b",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

def tick_keyboard(keys_pressed: pygame.key.ScancodeWrapper, controller1: SystemControllerState) -> None:
    for key, button in p1_key_mappings.items():
        if keys_pressed[key]:
            controller1.press(button)
        else:
            controller1.release(button)