import pygame
from time import sleep

rom = [0x00,0x00,0x00,0x1,0xFF,0x00,0x1e,0x01,0x00,0x20,0x10,0x00,0xe,0x255,0x00]

class BinaryRegister:
    """
    Serves As A Base Class For All Numbers Used In The Emulator
    """
    def __init__(self, value=0, bitwidth=8):
        self.value = value
        self.bitwidth = bitwidth
    
    def change(self, value):
        if value > 2 ** self.bitwidth - 1:
            print("Register Overflow, Setting Overflow Flag And Resetting To 0")
            emulated_cpu.reg_flags.carry = True
            self.value = 0
        else:
            self.value = value

class ConstrainedRegister:
    """
    A Class For The Program Counter, Basically The Same As `BinaryRegister` But It Has A Max Value And A Minimum Value
    """
    def __init__(self, minvalue, maxvalue, value=0, can_set_carry_flag=True):
        self.value = value
        self.max = maxvalue
        self.min = minvalue
        self.allow_carry = can_set_carry_flag
    
    def change(self, value):
        if value > self.max:
            print("Register Overflow, Setting Overflow Flag And Resetting To 0")
            if self.allow_carry:
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

    def run_once(self, rom):
        opcode = rom[self.pc]
        operand = rom[self.pc + 1]
        operand2 = rom[self.pc + 2]

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
            if self.acc == self.read_mem(address): self.flags.equal = True
            else: self.flags.equal = False

            if self.acc < self.read_mem(address): self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0D: # CPX
            if self.x == operand: self.flags.equal = True
            else: self.flags.equal = False

            if self.x < operand: self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0E: # CPY
            if self.y == operand: self.flags.equal = True
            else: self.flags.equal = False

            if self.y < operand: self.flags.sign = True
            else: self.flags.sign = False

        elif opcode == 0x0F: # BEQ
            if self.flags.equal: self.pc.change(address)

        elif opcode == 0x10: # BNE
            if not self.flags.equal: self.pc.change(address)

        elif opcode == 0x11: # BPS
            if not self.flags.sign: self.pc.change(address)

        elif opcode == 0x12: # BMI
            if self.flags.sign: self.pc.change(address)


# Initialize Pygame
pygame.init()
# Set up Pygame window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("PixelPulse 6502 Emulator")

print("********************* BOOTUP *************************")
print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
print("* TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!       *")
print("******************************************************")

emulated_cpu = cpu()

running = True

colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128, 0, 128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

def draw_pixel(x,y,color):
    """
    Draws A Pixel To The Screen, X and Y and pixel coordinents (top left is 0,0) and color is a 3 value tuple containing an RGB colour
    """
    global screen
    rect = pygame.Rect(x,y,8,8)
    pygame.draw.rect(screen,color,rect,3)

def get_nibble_from_byte(byte,is_high_nibble):
    if is_high_nibble: return byte & 0x0F
    else: return (byte >> 4) & 0x0F

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            #print(emulated_cpu.vram)
            running = False
    
    screen.fill((0,0,0))

    #print(hex(len(emulated_cpu.vram)))

    for x in range(64):
        for y in range(64):
            col_index = get_nibble_from_byte(emulated_cpu.vram[y * 64 + x], False)
            draw_pixel(x,y,colors[col_index])

            col_index = get_nibble_from_byte(emulated_cpu.vram[y * 64 + x], True)
            draw_pixel(x,y,colors[col_index])

    pygame.display.flip()
    
    if emulated_cpu.reg_programcounter.value > len(rom) - 2: running = False
    else: emulated_cpu.run_once(rom)