import py65
import py65.devices
import py65.devices.mpu65c02

import argparse

import py65.disassembler
import pygame

import numpy as np

# Constants
CHANNELS_COUNT = 4 # Amount Of Voices
DISPLAY_X_SIZE = 64
DISPLAY_Y_SIZE = 64
VRAM_LOCATION = 0x1000
VRAM_END_LOCATION = 0x2FFF

VOICES_COUNT = 4
APU_VOLUME_BASE = 0.0
APU_VOLUME_STEP = 0.05
APU_PITCH_BASE = 500
APU_PITCH_STEP = 150
APU_SAMPLE_RATE = 2048
APU_LENGTH = 10

parser = argparse.ArgumentParser(description="Emulator for the PixelPulse 6502")
parser.add_argument("cart", metavar="cartridge", type=str, help="the cartdrige to load")
args = parser.parse_args()

try: f = open(args.cart, "rb")
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
    
print(len(program))

#print(repr(program))

# Print each byte in hexadecimal format
#for byte in program:
#    print(f"{byte:02X}", end=" ")

class GameController:
    def __init__(self):
        self.buttons = ["up", "down", "left", "right", "a", "b"]
        self.pressed = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False
        }

    def press(self, buttonName: str):
        self.pressed[buttonName] = True
    
    def release(self, buttonName: str):
        self.pressed[buttonName] = False

    def convert_buttons_to_int(self):
        pressed_int = 0
        if self.pressed["right"]: pressed_int |= 0b00100000
        if self.pressed["left"]: pressed_int |= 0b00010000
        if self.pressed["up"]: pressed_int |= 0b00001000
        if self.pressed["down"]: pressed_int |= 0b00000100
        if self.pressed["a"]: pressed_int |= 0b00000010
        if self.pressed["b"]: pressed_int |= 0b00000001

        self.pressed_as_int = pressed_int
        return pressed_int

colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

def draw_pixel(x: int, y: int, col: int):
    rect = pygame.rect.Rect(x, y, 8, 8)
    pygame.draw.rect(display, colors[col], rect)

def get_high_nibble(x: int):
    return x >> 4

def get_low_nibble(x: int):
    return x & 0b1111

def generate_triangle_wave(length, frequency, volume=1.0):
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    triangle_wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return triangle_wave * volume

def generate_sawtooth_wave(length, frequency, volume=1.0):
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    sawtooth_wave = 2 * (t * frequency - np.floor(t * frequency))
    return sawtooth_wave * volume

def generate_square_wave(length, frequency, volume=1.0):
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    square_wave = np.sign(np.sin(2 * np.pi * frequency * t))
    return square_wave * volume

def generate_sine_wave(length, frequency, volume=1.0):
    t = np.linspace(0, length, int(length * APU_SAMPLE_RATE), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    return sine_wave * volume

def update_io():
    # Update The Controllers
    cpu.memory[0x3011] = controller1.convert_buttons_to_int()
    cpu.memory[0x3012] = controller2.convert_buttons_to_int()

    # Play The Sounds
    audio_ram = cpu.memory[0x3000:0x3010]
    for voice in range(VOICES_COUNT):
        for channel in range(CHANNELS_COUNT):
            if voice == 0: # It's A Square Wave
                # Calculate freqencies and audios and stuff
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel]) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_PITCH_STEP
                buffer = generate_square_wave(APU_LENGTH, freq, vol)
                sound = pygame.mixer.Sound(buffer)

                sound.play(0)
            
            if voice == 1: # It's A Triangle Wave
                # Calculate freqencies and audios and stuff
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel]) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_PITCH_STEP
                buffer = generate_triangle_wave(APU_LENGTH, freq, vol)
                sound = pygame.mixer.Sound(buffer)

                sound.play(0)

            if voice == 2: # It's A Sawtooh Wave
                # Calculate freqencies and audios and stuff
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel]) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_PITCH_STEP
                buffer = generate_sawtooth_wave(APU_LENGTH, freq, vol)
                sound = pygame.mixer.Sound(buffer)

                sound.play(0)
            
            if voice == 3: # It's A Sine Wave
                # Calculate freqencies and audios and stuff
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel]) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_PITCH_STEP
                buffer = generate_sine_wave(APU_LENGTH, freq, vol)
                sound = pygame.mixer.Sound(buffer)

                sound.play(0)

    # Update The Pallete
    pass # A PLACEHOLDER

    # Draw The Display
    vram = cpu.memory[VRAM_LOCATION:VRAM_END_LOCATION]
    for x in range(DISPLAY_X_SIZE):
        for y in range(DISPLAY_Y_SIZE):
            try:
                col = vram[y * 64 + x]
                draw_pixel(x, y, col)
            except IndexError:
                print("BAD PIXEL DATA. PROBABLY READ PAST VRAM")

    # Audio Format: SQW1,SQW2,SQW3,SQW4 (pitch+=15), TRW1,TRW2,TRW3,TRW4, (pitch+=15), ETC, ETC.
    # Byte Format: VVVV:PPPP

#program = [
#    0xA9, 0x05, # LDA #$05
#    0x8D, 0x00, 0x15, # STA $1500
#    0x4C, 0x00, 0x80 # JMP $8000
#]

# Initalize The CPU
cpu = py65.devices.mpu65c02.MPU()
cpu.memory[0x0000:0xFFFF] = program

# We've Gotta Check The Reset Vector
print(cpu.memory[0xFFFC:0xFFFD])

# Initalize The Controllers
controller1 = GameController()
controller2 = GameController()

# Initalize The Pygame
pygame.display.init()
pygame.mixer.init(APU_SAMPLE_RATE)
display = pygame.display.set_mode((128, 128))

# Hi!!!
#print("********************* BOOTUP *************************")
#print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
#print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
#print("* TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!       *")
#print("******************************************************")
#print("the above is blacked out, this person wishes for their privacy until the full release")


def get_instruction_from_memory(addr: int):
    addr_parser = py65.disassembler.AddressParser()
    dasm = py65.disassembler.Disassembler(cpu, addr_parser)

    i = dasm.instruction_at(addr)

    inst_fmt_opc = i[1]
    inst_fmt_opr = i[0]

    return [inst_fmt_opc, inst_fmt_opr]

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
        
        # Execute The Instruction
        cpu.step()

        # Check if the instruction is a breakpoint (BRK instruction)
        if cpu.memory[cpu.pc] == 0x00:
            print("BREAK")
            break

        display.fill((0, 0, 0))

        pygame.display.flip()

        frame_counter += 1

        if frame_counter == 1024: 
           frame_counter = 0
           print("UPDATING IO")
           update_io()

        print(f"PC: {cpu.pc: <5} | A: {cpu.a: <3} | X: {cpu.x: <3} | Y: {cpu.y: <3} | P: {bin(cpu.p): <10} | SP: {cpu.sp: <3} | P1: {bin(controller1.convert_buttons_to_int()): <8} | INSTRUCTION: {get_instruction_from_memory(cpu.pc)[0]: >3}")