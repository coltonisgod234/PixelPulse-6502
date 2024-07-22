import argparse

import pygame
from cpu.cpuhelpers import config_cpu, get_instruction_from_memory
from cpu.states import SystemControllerState, PixelStatusRegister, tick_PixelStatusRegister
from audiovisual.video import after_instruction, before_instruction, tick_display, tick_events, config_video
from controller.keyboard import tick_keyboard
from audiovisual.audio import tick_audio
from cpu.cpu import tick_cpu
from helpers import pixel_print, get_execution_time
from constants import TARGET_CLOCK_RATE, TARGET_FPS, VRAM_LOCATION, VRAM_END_LOCATION

from time import monotonic, sleep

# Parse the arguments
parser = argparse.ArgumentParser(description="Emulator for the PixelPulse 6502")
parser.add_argument("cart", metavar="cartridge", type=str, help="the cartdrige to load")
parser.add_argument("--debug", action="store_true", help="Enalbe debug mode")
args = parser.parse_args()

# Initalize the components
cpu = config_cpu(args)

# Initalize the display and clock
display, clock = config_video()

# Initalize the pixel status register
pixelStatusReg = PixelStatusRegister()

# Initalize The Controllers
controller1 = SystemControllerState()
controller2 = SystemControllerState()

last_time = monotonic()

if __name__ == "__main__":
    last_time = monotonic()
    tick = 0

    while True:
        # Calculate elapsed time since last frame
        current_time = monotonic()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Calculate cycles to process based on delta time and target rate
        cycles_to_process = int(delta_time * TARGET_CLOCK_RATE)
        for _ in range(cycles_to_process):
            # Get key states
            keys = pygame.key.get_pressed()

            # Process CPU tasks
            tick_cpu(cpu)   # Step the CPU 
            tick_events()   # Tick the events
            pixelStatusReg = tick_PixelStatusRegister(cpu, pixelStatusReg)

            if pixelStatusReg.get_status(0):
                tick_keyboard(keys, controller1)    # Tick the keyboard
                tick_display(cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION])
                tick_audio(cpu)

                pixelStatusReg.clear_status(0) # Clear the status

            #tick += 1

            after_instruction()
        
            pixel_print(f"PC: {hex(cpu.pc): <5} | A: {cpu.a: <3} | X: {cpu.x: <3} | Y: {cpu.y: <3} | P: {bin(cpu.p): <10} | SP: {cpu.sp: <3} | P1: {bin(controller1.convert_buttons_to_int()): <8} | I: {get_instruction_from_memory(cpu.pc): <9} | C: {cpu.processorCycles: <3} | PS: {pixelStatusReg.get_all_status()}")

        # Cap the frame rate
        clock.tick(TARGET_FPS)