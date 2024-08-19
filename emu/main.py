"""
The main thread for PixelPulse
"""

import argparse
from time import monotonic

import pygame
from audiovisual.audio import tick_audio
from audiovisual.video import (after_instruction, config_video, tick_display,
                               tick_events)

from controller.keyboard import tick_keyboard
from cpu.constants import (TARGET_CLOCK_RATE, TARGET_FPS, VRAM_END_LOCATION,
                           VRAM_LOCATION)
from cpu.cpu_emu import tick_cpu
from cpu.cpuhelpers import config_cpu, get_instruction_from_memory
from cpu.states import (PixelStatusRegister, SystemControllerState,
                        tick_pixel_status_register)

from utils.helpers import LocaleManager, pixel_print, print_locale

LocaleManager.load_locale(LocaleManager, "en", "CA")
pixel_print("Set locale to en-CA", __name__, "(init)")

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
SystemControllerState()
last_time = monotonic()

if __name__ == "__main__":
    last_time = monotonic()

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
            pixelStatusReg = tick_pixel_status_register(cpu, pixelStatusReg)

            if pixelStatusReg.get_status(0):
                tick_keyboard(keys, controller1)    # Tick the keyboard
                tick_display(cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION])
                tick_audio(cpu)

                pixelStatusReg.clear_status(0) # Clear the status

            after_instruction()
            print_locale("main.cpu_debug_registers_msg", __name__, "(MainLoop)",
                         [
                            cpu.pc,
                            cpu.a,
                            cpu.x,
                            cpu.y,
                            cpu.p,
                            cpu.sp,
                            controller1.convert_buttons_to_int(),
                            controller2.convert_buttons_to_int(),
                            get_instruction_from_memory(cpu.pc, cpu),
                            cpu.processorCycles,
                            pixelStatusReg.get_all_status()
                            ])

        # Cap the frame rate
        clock.tick(TARGET_FPS)
