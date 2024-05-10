import py65
import py65.devices
import py65.devices.mpu65c02

import argparse

import py65.disassembler
import pygame

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

    def press(self, buttonName):
        self.pressed[buttonName] = True
    
    def release(self, buttonName):
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

colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128, 0, 128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

def draw_pixel(x, y, col):
    rect = pygame.rect.Rect(x, y, 8, 8)
    pygame.draw.rect(display, colors[col], rect)

def update_io():
    # Update The Controllers
    cpu.memory[0x3011] = controller1.convert_buttons_to_int()
    cpu.memory[0x3012] = controller2.convert_buttons_to_int()

    # Play The Sounds
    pass # A Placeholder

    # Update The Pallete
    pass # A PLACEHOLDER

    # Draw The Display
    vram = cpu.memory[0x1000:0x2000]
    for x in range(64):
        for y in range(64):
            try:
                col = vram[y * 64 + x]
                draw_pixel(x, y, col)
            except IndexError:
                print("BAD PIXEL DATA. PROBABLY READ PAST VRAM")

#program = [
#    0xA9, 0x05, # LDA #$05
#    0x8D, 0x00, 0x15, # STA $1500
#    0x4C, 0x00, 0x80 # JMP $8000
#]

# Initalize The CPU
cpu = py65.devices.mpu65c02.MPU()
cpu.memory[0x8000:0x8000+len(program)] = program

cpu.pc = 0x8000

# Initalize The Controllers
controller1 = GameController()
controller2 = GameController()

# Initalize The Pygame
pygame.display.init()
display = pygame.display.set_mode((128, 128))

# Hi!!!
#print("********************* BOOTUP *************************")
#print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
#print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
#print("* TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!       *")
#print("******************************************************")
#print("the above is blacked out, this person wishes for their privacy until the full release")


def get_instruction_from_memory(addr):
    addr_parser = py65.disassembler.AddressParser()
    dasm = py65.disassembler.Disassembler(cpu, addr_parser)

    i = dasm.instruction_at(addr)

    inst_fmt_opc = i[1]
    inst_fmt_opr = i[0]

    return [inst_fmt_opc, inst_fmt_opr]

running = True

frame_counter = 0

if __name__ == "__main__":
    while running:
        # Handle The Pygame Things
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: controller1.press("a")
                elif event.key == pygame.K_z: controller1.press("b")
                elif event.key == pygame.K_UP: controller1.press("up")
                elif event.key == pygame.K_DOWN: controller1.press("down")
                elif event.key == pygame.K_LEFT: controller1.press("left")
                elif event.key == pygame.K_RIGHT: controller1.press("right")

                elif event.key == pygame.K_d: dbg_con_open = ~dbg_con_open
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_x: controller1.release("a")
                elif event.key == pygame.K_z: controller1.release("b")
                elif event.key == pygame.K_UP: controller1.release("up")
                elif event.key == pygame.K_DOWN: controller1.release("down")
                elif event.key == pygame.K_LEFT: controller1.release("left")
                elif event.key == pygame.K_RIGHT: controller1.release("right")
        
        # Execute The Instruction
        cpu.step()

        # Check if the instruction is a breakpoint (BRK instruction)
        if cpu.memory[cpu.pc] == 0x00:
            print("BREAK")
            break

        display.fill((0, 0, 0))

        pygame.display.flip()

        frame_counter += 1

        if frame_counter == 2048:
            frame_counter = 0
            #print("UPDATING IO")
            update_io()

        print(f"PC: {cpu.pc: <5} | A: {cpu.a: <3} | X: {cpu.x: <3} | Y: {cpu.y: <3} | P: {bin(cpu.p): <8} | SP: {cpu.sp: <3} | P1: {bin(controller1.convert_buttons_to_int()): <8} | INSTRUCTION: {get_instruction_from_memory(cpu.pc)[0]}")