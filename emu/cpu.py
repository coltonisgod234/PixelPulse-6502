import pygame

rom = [0x01,0xFF,0x00, 0x01,0x10,0x00] # Will Change To Argparse, Only Like This In Debug Mode.

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
            self.reg_flags.carry = True
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
                self.reg_flags.carry = True
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
        self.p1 = GameController()
        self.p2 = GameController()

        # Initalize The Registers
        self.reg_a = BinaryRegister()
        self.reg_x = BinaryRegister()
        self.reg_y = BinaryRegister()
        self.reg_flags = FlagsRegister() # This One Is Special (♪freinds♪)

        self.reg_programcounter = ConstrainedRegister(0, 32768, can_set_carry_flag=False)
        self.saved_pc = [ConstrainedRegister(0, 32768, can_set_carry_flag=False) for i in range(16)]
        self.saved_pc_count = ConstrainedRegister(0, 15)

        self.ram = [BinaryRegister() for i in range(32768)]

        print("*** CPU IS OKAY ***")

        print("*** RAM IS OKAY ***")

    def write_mem(self, address, data):
        try:
            self.ram[address].change(data.value)
        except IndexError:
            print("Invalid Or Bad Address", address)

    def read_mem(self, address):
        try:
            return self.ram[address].value
        except IndexError:
            print("Invalid Or Bad Address", address)

    def combine_address(self, high_byte, low_byte):
        # Combine the high byte and low byte into a 16-bit address
        address = (high_byte << 8) | low_byte
        return address

    def run_once(self, rom):
        opcode = rom[self.reg_programcounter.value]
        operand = rom[self.reg_programcounter.value + 1]
        address = self.combine_address(rom[self.reg_programcounter.value + 1], rom[self.reg_programcounter.value + 2])
        #print(opcode, operand)

        if opcode == 0x00: # NOP
            pass # Do Nothing
        elif opcode == 0x01: # LDA #
            self.reg_a.value = operand # Set Register A To The Operand
        elif opcode == 0x02: # LDY #
            self.reg_y.value = operand # Set Register Y To The Operand
        elif opcode == 0x03: # LDX #
            self.reg_x.value = operand # Set Register X To The Operand
        elif opcode == 0x04: # STA $
            self.write_mem(address, self.reg_a)
        elif opcode == 0x05: # STY $
            self.write_mem(address, self.reg_y)
        elif opcode == 0x06: # STX $
            self.write_mem(address, self.reg_x)
        elif opcode == 0x07: # ADD $
            self.reg_a.value = self.read_mem(address) + self.reg_a # Set The Value In Register A To The Sum Of A Value In RAM Plus Itself
        elif opcode == 0x08: # SUB $
            self.reg_a.value = self.read_mem(address) - self.reg_a # Set The Value In Register A To The Subtraction Of A Value In RAM Minus Itself
        elif opcode == 0x09: # AND $
            self.reg_a.value = self.read_mem(address) & self.reg_a # Set The Value In Register A To Itself Bitwise ANDed With A Value In RAM
        elif opcode == 0x0A: # ORA $
            self.reg_a.value = self.read_mem(address) | self.reg_a # Set The Value In Register A To Itself Bitwise ORed With A Value In RAM
        elif opcode == 0x0B: # EOR $
            self.reg_a.value = self.read_mem(address) ^ self.reg_a  # Set The Value In Register A To Itself Bitwise XORed With A Value In RAM
        elif opcode == 0x0C: # CMP $
            # Compare The Value In The A Register To A Value In RAM
            if self.reg_a.value == self.read_mem(address):
                # Set The Equal Flag
                self.reg_flags.equal = True
            else: self.reg_flags.equal = False
            
            # See If It's Less Than (For BMI)
            if self.reg_a.value < self.read_mem(address):
                # Set The Sign Flag
                self.reg_flags.sign = True
            else: self.reg_flags.sign = False
        
        elif opcode == 0x0D: # CPX $
            # Compare The Value In The X Register To A Value In RAM
            if self.reg_x.value == self.read_mem(address):
                # Set The Equal Flag
                self.reg_flags.equal = True
            else: self.reg_flags.equal = False
            
            # See If It's Less Than (For BMI)
            if self.reg_x.value < self.read_mem(address):
                # Set The Sign Flag
                self.reg_flags.sign = True
            else: 
                self.reg_flags.sign = False
        
        elif opcode == 0x0E: # CPY $
            # Compare The Value In The Y Register To A Value In RAM
            if self.reg_y.value == self.read_mem(address):
                # Set The Equal Flag
                self.reg_flags.equal = True
            else: 
                self.reg_flags.equal = False
            
            # See If It's Less Than (For BMI)
            if self.reg_y.value < self.read_mem(address):
                # Set The Sign Flag
                self.reg_flags.sign = True
            else: 
                self.reg_flags.sign = False
        
        elif opcode == 0x0F: # BEQ $
            # Branch To A Routine If Equal Flag Is Set
            if self.reg_flags.equal:
                self.reg_programcounter = address
            
            else:
                self.reg_flags.equal = False

        elif opcode == 0x10: # BNE $
            # Branch To A Routine If Equal Flag Is Not Set
            if not self.reg_flags.equal: 
                self.reg_programcounter = address

            else:
                self.reg_flags.equal = False
        
        elif opcode == 0x11: # BPS $
            # Branch To A Routine If Sign Flag Is Not Set
            if not self.reg_flags.sign:
                self.reg_programcounter = address

            else:
                self.reg_flags.sign = False

        elif opcode == 0x12: # BMI $
            # Branch To A Routine If Sign Flag Is Set
            if self.reg_flags.sign:
                self.reg_programcounter = address

            else:
                self.reg_flags.sign = False

        elif opcode == 0x13: # JMP $
            self.reg_programcounter = operand

        elif opcode == 0x14: # SPC
            self.write_mem(0x1A20, self.reg_programcounter.value)
            print("SAVED PROGRAM COUNTER AT 0x1A20")

        elif opcode == 0x15: # INT
            print("INTERUPT REQUEST NOT HANDLED")

        elif opcode == 0x16: # LDA $
            self.reg_a.value = self.ram[operand].value # Set Register A To A Value In Memory

        elif opcode == 0x17: # LDX $
            self.reg_x.value = self.ram[operand].value # Set Register X To A Value In Memory

        elif opcode == 0x18: # LDY $
            self.reg_y.value = self.ram[operand].value # Set Register Y To A Value In Memory

        elif opcode == 0x19: # LPC
            self.reg_programcounter.change(self.read_mem(0x1A20))

        print(f"PC:{self.reg_programcounter.value} | A:{self.reg_a.value} | X: {self.reg_x.value} | Y: {self.reg_y.value} | CARRY: {self.reg_flags.carry} | EQUAL: {self.reg_flags.equal} | SIGN: {self.reg_flags.sign}")
        self.reg_programcounter.change(self.reg_programcounter.value + 3)

# Initialize Pygame
pygame.init()
# Set up Pygame window
screen = pygame.display.set_mode((160, 240))
pygame.display.set_caption("PixelPulse 6502 Emulator")

print("********************* BOOTUP *************************")
print("* PIXELPULSE 6502 IS A FANTASY VIDEO GAME CONSOLE    *")
print("* THANK YOU TO __________ ON DISCORD AND THE PYGAME  *")
print("* PYGAME TEAM FOR HELPING MAKE THIS PROJECT POSSIBLE!*")
print("******************************************************")

emulated_cpu = cpu()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    if emulated_cpu.reg_programcounter.value > len(rom) - 2: running = False
    else: emulated_cpu.run_once(rom)