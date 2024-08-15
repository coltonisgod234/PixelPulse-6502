from time import perf_counter, sleep, monotonic
PROGRAM_EXECUTIONTIME_START = perf_counter()

from re import DEBUG
import py65
import py65.devices
import py65.devices.mpu65c02

import argparse

import py65.disassembler
import py65.monitor
import pygame

import numpy as np

# Constants
CHANNELS_COUNT = 4  # Amount of channels
DISPLAY_X_SIZE = 64  # X size of display
DISPLAY_Y_SIZE = 64  # Y size of display
VRAM_LOCATION = 0x1000  # VRAM Location
VRAM_END_LOCATION = 0x2FFF  # VRAM end location

VOICES_COUNT = 4
APU_VOLUME_BASE = 0
APU_VOLUME_STEP = 0.05
APU_PITCH_BASE = 0
APU_PITCH_STEP = 512
APU_SAMPLE_RATE = 44100
APU_LENGTH = 10

TARGET_FPS = 60
TARGET_CLOCK_RATE = 4000

ERRRORLEVEL_TABLE = {
    0: "info",
    1: "debug",
    2: "warn",
    3: "error",
    4: "critical",
}

# Parse the arguments
parser = argparse.ArgumentParser(description="Emulator for the PixelPulse 6502")
parser.add_argument("cart", metavar="cartridge", type=str, help="the cartdrige to load")
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

DEBUG_MODE_MASK = args.debug

colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

try: 
    f = open(args.cart, "rb")
except FileNotFoundError: 
    print(f"Cart File \"{args.cart}\" Not Found")
    quit(1)

# After reading the file
program_bytes = f.read()

# We Reconstruct Our Program
program = []

for byte in range(len(program_bytes)):
    #print(f"{program_bytes[byte]:02X}", end=" ")
    program.append(int(program_bytes[byte]))
    
print(f"Cart is {len(program)} bytes.")

# Define classes
class GameController:
    def __init__(self) -> None:
        self.buttons = ["up", "down", "left", "right", "a", "b"]
        self.pressed = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False
        }

    def press(self, buttonName: str) -> None:
        self.pressed[buttonName] = True
    
    def release(self, buttonName: str) -> None:
        self.pressed[buttonName] = False

    def convert_buttons_to_int(self) -> int:
        pressed_int = 0b00000000
        if self.pressed["right"]: pressed_int |= 0b00100000
        if self.pressed["left"]: pressed_int  |= 0b00010000
        if self.pressed["up"]: pressed_int    |= 0b00001000
        if self.pressed["down"]: pressed_int  |= 0b00000100
        if self.pressed["a"]: pressed_int     |= 0b00000010
        if self.pressed["b"]: pressed_int     |= 0b00000001

        self.pressed_as_int = pressed_int
        return pressed_int

# Define utility functions

log = open("pixelpulse.log", "w+")
log.truncate(0)

def get_execution_time() -> float:
    now = perf_counter() - PROGRAM_EXECUTIONTIME_START
    return now

def pixel_print(msg: str, errorlevel=1):
    if errorlevel == 1 and not DEBUG_MODE_MASK: return 1  # We don't care about debug info if this is a release mode 
    formatted_msg = f"[{get_execution_time():>22}]  {ERRRORLEVEL_TABLE[errorlevel]: <8}    {msg}"
    log.write(f"{formatted_msg}\n")
    print(formatted_msg)
    return 0

def draw_pixel(x: int, y: int, col: int) -> None:
    rect = pygame.rect.Rect(x, y, 8, 8)
    pygame.draw.rect(display, colors[col], rect)

def get_high_nibble(x: int) -> int:
    return x >> 4

def get_low_nibble(x: int) -> int:
    return x & 0b1111

def generate_triangle_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    triangle_wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return triangle_wave * volume

def generate_sawtooth_wave(length, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    sawtooth_wave = 2 * (t * frequency - np.floor(t * frequency))
    return sawtooth_wave * volume

def generate_square_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    square_wave = np.sign(np.sin(2 * np.pi * frequency * t))
    return square_wave * volume

def generate_sine_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    return sine_wave * volume

# Define other functions

def update_io() -> None:
    # Update The Controllers
    cpu.memory[0x3011] = controller1.convert_buttons_to_int()
    cpu.memory[0x3012] = controller2.convert_buttons_to_int()

    # Play The Sounds
    audio_ram = cpu.memory[0x3000:0x3010]
    for voice in range(VOICES_COUNT):
        for channel in range(CHANNELS_COUNT):
            if voice == 0: # It's A Square Wave
                # Calculate freqencies and audios and stuff (I have no idea what this means, it's honestly just a mix of constants)
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 4) * APU_PITCH_STEP  # Step the pitch
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP  # Step the volume
                buffer = generate_square_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                #sound.play(0)
            
            if voice == 1: # It's A Triangle Wave
                # Calculate freqencies and audios and stuff (I have no idea what this means, it's honestly just a mix of constants)
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 8) * APU_PITCH_STEP  # Step the pitch
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP  # Step the volume
                buffer = generate_triangle_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)

            if voice == 2: # It's A Sawtooh Wave
                # Calculate freqencies and audios and stuff (I have no idea what this means, it's honestly just a mix of constants)
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 12) * APU_PITCH_STEP  # Step the pitch
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP  # Step the volume
                buffer = generate_sawtooth_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)
            
            if voice == 3: # It's A Sine Wave
                # Calculate freqencies and audios and stuff (I have no idea what this means, it's honestly just a mix of constants)
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 16) * APU_PITCH_STEP  # Step the pitch
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP  # Step the volume
                buffer = generate_sine_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)

    # Update The Palette
    palette_ram = cpu.memory[0x3013:0x3023]  # Fill up the palette memory so it's accessable
    colors = palette_ram  # Set the colors to this

    # Draw The Display
    vram = cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION]
    for x in range(DISPLAY_X_SIZE):  # Loop through all the pixels
        for y in range(DISPLAY_Y_SIZE):  # Loop through all the pixels
            try:
                col = vram[y * 64 + x]  # Locate them
                draw_pixel(x, y, col)  # Make 'em pulse (as in draw them)
            except IndexError:
                pixel_print("Bad pixel data.", 4)

# Initalize The CPU
cpu = py65.devices.mpu65c02.MPU()
cpu.memory[0x0000:0xFFFF] = program

# Initalize The Controllers
controller1 = GameController()
controller2 = GameController()

# Initalize The Pygame
pygame.display.init()
pygame.display.set_caption("PixelPulse 6502")
pygame.mixer.init(APU_SAMPLE_RATE)
display = pygame.display.set_mode((DISPLAY_X_SIZE*5, DISPLAY_Y_SIZE*5))

# Hi!!!
#print("********************* BOOTUP *************************")
#print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
#print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
#print("* TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!       *")
#print("******************************************************")
#print("the above is blacked out, this person wishes for their privacy until the full release")


def get_instruction_from_memory(addr: int) -> str:
    addr_parser = py65.disassembler.AddressParser()
    dasm = py65.disassembler.Disassembler(cpu, addr_parser)

    i = dasm.instruction_at(addr)

    inst_fmt_opc = i[1]

    return inst_fmt_opc

running = True

frame_counter = 0

key_mappings = {
    pygame.K_x: "a",
    pygame.K_z: "b",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

clock = pygame.time.Clock()

cpu.pc = (program[0xfffd] << 8) | program[0xfffc]  # Don't ask... I don't even know...
pixel_print(f"Loaded to {cpu.pc}")

if __name__ == "__main__":
    while running:
        # Handle The Pygame Things
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        # Poll For Input
        keys = pygame.key.get_pressed()
        for key, button in key_mappings.items():
            if keys[key]:
                controller1.press(button)
            else:
                controller1.release(button)
        
        # Start timing (To get a delta time)
        instruction_execution_start = monotonic()

        # Execute The Instruction
        cpu.step()

        # Check if the instruction is a break (BRK instruction)
        if cpu.memory[cpu.pc] == 0x00:
            pixel_print("Encountered BRK instruction.")  # Tell the user, idk what to do here

        instruction_execution_end = monotonic()  # End timing
        delta = instruction_execution_end - instruction_execution_start  # Compute the delta

        # Clear the display
        display.fill((0, 0, 0))

        frame_counter += 1  # I would use modulo but that's really slow and kills preformance, division = slow everyone!
        if frame_counter == (TARGET_CLOCK_RATE // TARGET_FPS):
            frame_counter = 0  # Reset our frame count
            pixel_print("Updating IO") # Log it
            update_io()  # Update the IO
            pygame.display.set_caption(f"PixelPulse-6502: {clock.get_fps()}")  # Set the caption to our current FPS

        pygame.display.flip()  # We can update our display now!
        

        pixel_print(f"PC: {hex(cpu.pc): <5} | A: {cpu.a: <3} | X: {cpu.x: <3} | Y: {cpu.y: <3} | P: {bin(cpu.p): <10} | SP: {cpu.sp: <3} | P1: {bin(controller1.convert_buttons_to_int()): <8} | I: {get_instruction_from_memory(cpu.pc): <9} | C: {cpu.processorCycles}")
        sleep(delta)