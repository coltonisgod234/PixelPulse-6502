import pygame
from time import sleep
import time
import argparse

parser = argparse.ArgumentParser(description="Emulator For The PixelPulse 6502")
parser.add_argument("Cartridge", metavar="cart", type=str, help="cartridge To Boot From")
parser.add_argument("-D", action="store_true", help="when true, the system will run in debug mode")
args = parser.parse_args()

print(args)

if args.D:
    print("*** THE SYSTEM IS RUNNING IN DEBUG MODE ***")
    print("THIS MEANS YOU CAN USE DEBUG COMMANDS BY USING A CONSOLE")
    print("PRESS THE \"D\" KEY FOR A DEBUG CONSOLE")
    print("")
    print("AVALIBLE DEBUG COMMANDS:")
    print("f: Freezes time")
    print("rw (step): Rewinds time by (step) many instructions")
    print("s (step): Step forwards in time (step) many instructions")
    print("peek (addr): peeks an address in memory")
    print("poke (addr), (data): sets an address in memory to (data)")
    print("search (value): seaches memory for (value) and prints whatever is found")

    sleep(1)

rom = [0x00,0x00,0x00,0x1,0xFF,0x00,0x1e,0x01,0x00,0x20,0x10,0x04,0xe,0x255,0x00,0x10,0x00,0x00,0x1c,0x01,0x00,0x13,0x00,0x00]

class BinaryRegister:
    """
    Serves As A Base Class For All Numbers Used In The Emulator
    """
    def __init__(self, value=0, bitwidth=8, cpu_emu=None):
        self.value = value
        self.bitwidth = bitwidth
        self.cpu = cpu_emu
    
    def change(self, value):
        if value > 2 ** self.bitwidth - 1:
            print("Register Overflow, Setting Overflow Flag And Resetting To 0")
            if self.cpu != None: self.cpu_emu.flags.carry = True
            else: print("Can't Set Carry Flag. CPU is Nonetype or undefined")
            self.value = 0
        else:
            self.value = value

class ConstrainedRegister:
    """
    A Class For The Program Counter, Basically The Same As `BinaryRegister` But It Has A Max Value And A Minimum Value
    """
    def __init__(self, minvalue, maxvalue, value=0, can_set_carry_flag=True, cpu_emu=None):
        self.value = value
        self.max = maxvalue
        self.min = minvalue
        self.allow_carry = can_set_carry_flag
    
    def change(self, value):
        if value > self.max:
            print("Register Overflow, Setting Overflow Flag And Resetting To 0")
            if self.allow_carry and self.cpu != None:
                emulated_cpu.reg_flags.carry = True
            
            self.value = 0
        elif value < self.min:
            print("Register Underflow, Overflowing To Maximim")
            self.value = self.max
        else:
            self.value = value

class FlagsRegister:
    def __init__(self, carry=False,equal=False,sign=False,res=False):
        self.carry = carry
        self.equal = equal
        self.sign = sign
        self.reserved = res

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

class cpu:
    def __init__(self):
        """
        Class For The PixelPulses' Central Processing Unit (CPU)
        """
        self.p1 = GameController()
        self.p2 = GameController()

        self.acc = BinaryRegister()
        self.x = BinaryRegister()
        self.y = BinaryRegister()
        self.pc = BinaryRegister(bitwidth=16)
        self.flags = FlagsRegister()

        self.ram = [BinaryRegister() for i in range(2**16-1)]
        self.vram = [BinaryRegister() for i in range(0x1000,0x2FFF)]

    def write_mem(self, address, data):
        """
        Write To The Memory Of The PixelPulse. Address and data are both integers
        """
        try:
            self.ram[address].change(data)
        except IndexError:
            print("BAD MEMORY INDEX OR VALUE")
        
    def read_mem(self, address):
        """
        Read From The Memory Of The PixelPulse. Address is an integer
        """
        try:
            if address > 0xFFFF:
                # We Read Out Of Bounds, So We Need To Return ROM Instead
                return self.rom[address] # ROM Is An Integer, Because I Hate People
            else:
                return self.ram[address].value

        except IndexError:
            print("BAD MEMORY INDEX OR VALUE")

    def merge_address(self, low_byte, high_byte):
        address = (high_byte << 8) | low_byte
        return address
    
    def update_IO(self):
        i = 0
        for byte in range(0x1000, 0x2FFF):
            self.vram[i] = self.read_mem(byte) # This Should Be A BinaryRegister, If It Is Not Something Is Wrong
            if not isinstance(self.vram[i], BinaryRegister):
                #print("Non BinaryRegister VRAM Object, Correcting...")
                self.vram[i] = BinaryRegister(value=self.vram[i], bitwidth=8) # Correct It To A BinaryRegister
            i += 1
            #print("instance binary register", type(emulated_cpu.vram[i]), self.vram[i].value)

    def run_once(self, rom):
        opcode = rom[self.pc.value]
        operand = rom[self.pc.value + 1]
        operand2 = rom[self.pc.value + 2]

        address = self.merge_address(operand, operand2)

        if opcode == 0x00: pass

        elif opcode == 0x01: self.acc.change(operand) # LDA
        elif opcode == 0x02: self.y.change(operand) # LDY
        elif opcode == 0x03: self.x.change(operand) # LDX
        elif opcode == 0x04: self.write_mem(address, self.acc) # STA
        elif opcode == 0x05: self.write_mem(address, self.y) # STY
        elif opcode == 0x06: self.write_mem(address, self.x) # STX
        elif opcode == 0x07: self.acc.change(self.acc.value + self.read_mem(address)) # ADD
        elif opcode == 0x08: self.acc.change(self.acc.value - self.read_mem(address)) # SUB
        elif opcode == 0x09: self.acc.change(self.acc.value & self.read_mem(address)) # AND
        elif opcode == 0x0A: self.acc.change(self.acc.value | self.read_mem(address)) # ORA
        elif opcode == 0x0B: self.acc.change(self.acc.value ^ self.read_mem(address)) # EOR
        elif opcode == 0x0C: # CMP
            if self.acc.value == self.read_mem(address): self.flags.equal = True
            else: self.flags.equal = False

            if self.acc.value < self.read_mem(address): self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0D: # CPX
            if self.x.value == operand: self.flags.equal = True
            else: self.flags.equal = False

            if self.x.value < operand: self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0E: # CPY
            if self.y.value == operand: self.flags.equal = True
            else: self.flags.equal = False

            if self.y.value < operand: self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0F: # BEQ
            if self.flags.equal: self.pc.change(address)

        elif opcode == 0x10: # BNE
            if not self.flags.equal: self.pc.change(address)

        elif opcode == 0x11: # BPS
            if not self.flags.sign: self.pc.change(address)

        elif opcode == 0x12: # BMI
            if self.flags.sign: self.pc.change(address)
        
        elif opcode == 0x13: # JMP
            self.pc.change(address)

        elif opcode == 0x14: print("RESERVED OPCODE, WHAT ARE YOU TRYING TO DO?") # RES 

        elif opcode == 0x15: # INT
            print("BIOS INTERUPTS NOT HANDLED YET, SORRY")

        elif opcode == 0x16: self.acc.change(self.read_mem(address)) # LDA_M
        elif opcode == 0x17: self.x.change(self.read_mem(address)) # LDX_M
        elif opcode == 0x18: self.y.change(self.read_mem(address)) # LDY_M
        elif opcode == 0x19: self.acc.change(self.read_mem(address)) # LDA_M
        elif opcode == 0x1A: self.write_mem(address + self.x.value) # SOX
        elif opcode == 0x1B: self.write_mem(address + self.y.value) # SOY
        elif opcode == 0x1C: self.x.change(self.x.value + operand) # INX
        elif opcode == 0x1D: self.x.change(self.x.value - operand) # DEX
        elif opcode == 0x1E: self.y.change(self.y.value + operand) # INY
        elif opcode == 0x1F: self.y.change(self.y.value - operand) # DEY
        elif opcode == 0x20: self.write_mem(address + self.x.value + self.y.value, self.acc.value)

        print(f"PC:{self.pc.value: <5} | A:{self.acc.value: <3} | X:{self.x.value: <3} | Y:{self.y.value: <3}")
        self.pc.change(self.pc.value + 3)


# Initialize Pygame
pygame.init()
# Set up Pygame window
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("PixelPulse 6502 Emulator")

print("********************* BOOTUP *************************")
print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
print("* TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!       *")
print("******************************************************")
print("the above is blacked out, this person wishes for their privacy until the full release")

emulated_cpu = cpu()

running = True

colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128, 0, 128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

def draw_pixel(x,y,color):
    """
    Draws A Pixel To The Screen, X and Y and pixel coordinents (top left is 0,0) and color is a 3 value tuple containing an RGB colour
    """
    global screen
    rect = pygame.Rect(x,y,10,10)
    pygame.draw.rect(screen,color,rect,3)

def draw_screen():
    for x in range(64):
        for y in range(64):
            try:
                col_index = emulated_cpu.vram[y * 64 + x].value
                draw_pixel(x,y,colors[col_index])
            except IndexError:
                print("BAD PIXEL DATA. PROBABLY READ PAST VRAM")
#instructions = 0
while running:
    #start_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            #print(emulated_cpu.vram)
            running = False
    
    screen.fill((0,0,0))

    #print(hex(len(emulated_cpu.vram)))

    pygame.display.flip()
    
    if emulated_cpu.pc.value > len(rom) - 2: running = False
    else: 
        try:
            emulated_cpu.run_once(rom)
            emulated_cpu.update_IO()
        except IndexError:
            print("END OF PROGRAM. QUITING")
            quit(1)
    
    if emulated_cpu.pc.value % 1024 == 0:
        draw_screen()
        print("DREW SCREEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    #instructions += 1
    
    #end_time = time.time()
    #etime = end_time - start_time
    #print(instructions)