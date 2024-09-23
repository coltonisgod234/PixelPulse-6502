"""
The main thread for PixelPulse
"""

import argparse
from time import monotonic

# Pylint does not shut up about my imports, so I've forced it to
# pylint: disable=import-error

import pygame
from audiovisual.audio import tick_audio
from audiovisual.video import (after_instruction, config_video, tick_display,
                               tick_events)
from controller.keyboard import tick_keyboard
from cpu.constants import (TARGET_CLOCK_RATE, TARGET_FPS, VRAM_END_LOCATION,
                           VRAM_LOCATION, APU_SAMPLERATE, CYCLES_PER_FRAME)
from cpu.cpu_emu import tick_cpu
from cpu.cpuhelpers import config_cpu, get_instruction_from_memory
from cpu.states import (PixelStatusRegister, SystemControllerState,
                        tick_pixel_status_register)
from utils.helpers import LocaleManager, pixel_print, print_locale
from cpu.timer import Timer, tick_timer

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
last_time = monotonic()

PITtimer = Timer()

pygame.mixer.init(frequency=APU_SAMPLERATE, size=-16, channels=16)

pixel_print("Initalization done!")
print("Cool people!")
print("     Thanks to my coding instructor kevin for teaching me python")
print("     Thanks to my friend lagthecat for at least TRYING to help")
print("Cool libraries!")
print("     py65       : emulation of the w65c02s")
print("     argparse   : argument parsing")
print("     pygame     : audiovisual engine")
print("     numpy      : math, generation of audio")
print("     scipy      : math, wave generation")
print("     pytest     : unit testing, debugging")
print("     cachetools : caching")

#if __name__ == "__main__":
#    last_time = monotonic()
#
#    while True:
#        # Calculate elapsed time since last frame
#        current_time = monotonic()
#        delta_time = current_time - last_time
#        last_time = current_time
#
#        # Calculate cycles to process based on delta time and target rate
#        cycles_to_process = int(delta_time * TARGET_CLOCK_RATE)
#        for _ in range(cycles_to_process):
#            # Get key states
#            keys = pygame.key.get_pressed()
#
#            # Process CPU tasks
#                #tick_cpu(cpu)   # Step the CPU
#            for _ in range(24):
#                cpu.step()
#                print(f"PC={cpu.pc:<10} A={hex(cpu.a):<5} X={hex(cpu.x):<5} Y={hex(cpu.y)} P={bin(cpu.p):>20} SP={cpu.sp:<5} I={get_instruction_from_memory(cpu.pc, cpu):<20}")
#
#            tick_events()   # Tick the events
#
#            pixelStatusReg = tick_pixel_status_register(cpu, pixelStatusReg)
#
#            if pixelStatusReg.get_status(0) == 1:
#                tick_keyboard(keys, controller1)    # Tick the keyboard
#                tick_display(cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION])
#                tick_audio(cpu)
#
#                print("Flushed hardware")
#
#                pixelStatusReg.clear_status(0)
#
#            after_instruction()
            #print_locale("main.cpu_debug_registers_msg", __name__, "(AfterMainLoop)",
            #             [
            #                cpu.pc,
            #                hex(cpu.a),
            #                hex(cpu.x),
            #                hex(cpu.y),
            #                bin(cpu.p),
            #                cpu.sp,
            #                controller1.convert_buttons_to_int(),
            #                controller2.convert_buttons_to_int(),
            #                get_instruction_from_memory(cpu.pc, cpu),
            #                cpu.processorCycles,
            #                pixelStatusReg.get_all_status(),
            #                PITtimer.counter
            #                ])


if __name__ == "__main__":
    last_time = monotonic()

    while True:
        current_time = monotonic()
        delta_time = current_time - last_time
        last_time = current_time

        cycles_to_process = int(delta_time * TARGET_CLOCK_RATE)

        if cycles_to_process <= 0:
            continue  # Skip processing if no cycles are available

        for _ in range(cycles_to_process):
            # Get key states
            keys = pygame.key.get_pressed()

            # Process CPU tasks
                #tick_cpu(cpu)   # Step the CPU
            for _ in range(24):
                cpu.step()

            tick_events()

            pixelStatusReg = tick_pixel_status_register(cpu, pixelStatusReg)

            if pixelStatusReg.get_status(0) == 1:
    
                #print("Flushing hardware")

                tick_keyboard(keys, controller1)    # Tick the keyboard
                tick_display(cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION])
                tick_audio(cpu)

                print(clock.get_time(), clock.get_fps())

                clock.tick(TARGET_FPS)

                pixelStatusReg.clear_status(0)

            after_instruction(clock)