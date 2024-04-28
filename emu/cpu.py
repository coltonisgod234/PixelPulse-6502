import display
import threading

rom = "\x00\x00\x01\xFE" # Will Change To Argparse, Only Like This In Debug Mode.

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
            reg_flags.carry = True
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
                reg_flags.carry = True
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

p1 = GameController()
p2 = GameController()

# Initalize The Registers
reg_a = BinaryRegister()
reg_x = BinaryRegister()
reg_y = BinaryRegister()
reg_flags = FlagsRegister() # This One Is Special (♪freinds♪)

reg_programcounter = ConstrainedRegister(0, 32768, can_set_carry_flag=False)
saved_pc = [ConstrainedRegister(0, 32768, can_set_carry_flag=False) for i in range(16)]
saved_pc_count = ConstrainedRegister(0, 15)

ram = [BinaryRegister() for i in range(32768)]

print("*** CPU IS OKAY ***")

print("*** RAM IS OKAY ***")

print("*** INITING DISPLAY ***")

def tkinter_thread(threading_ready_event):
    pixelPulseDisplayInstance = display.PixelPulseDisplay()
    threading_ready_event.set() # It's Safe You Can Continue Now
    pixelPulseDisplayInstance.root.mainloop()

# Initalize The Display
display_ready_event = threading.Event()

pixelPulseDisplayInstanceThread = threading.Thread(target=tkinter_thread, args=(display_ready_event,))
pixelPulseDisplayInstanceThread.start()

# Now We Wait Around Until It's ready
display_ready_event.wait()

while reg_programcounter.value < len(rom):
    opcode = rom[reg_programcounter.value]
    operand = rom[reg_programcounter.value + 1]

    if opcode == "\x00": # NOP
        pass # Do Nothing
    elif opcode == "\x01": # LDA #
        reg_a.value = operand # Set Register A To The Operand
    elif opcode == "\x02": # LDY #
        reg_y.value = operand # Set Register Y To The Operand
    elif opcode == "\x03": # LDX #
        reg_x.value = operand # Set Register X To The Operand
    elif opcode == "\x04": # STA $
        ram[operand].value = reg_a.value # Set A Value In Memory To Register A
    elif opcode == "\x05": # STY $
        ram[operand].value = reg_y.value # Set A Value In Memory To Register Y
    elif opcode == "\x06": # STX $
        ram[operand].value = reg_x.value # Set A Value In Memory To Register X
    elif opcode == "\x07": # ADD $
        reg_a.value = ram[operand].value + reg_a # Set The Value In Register A To The Sum Of A Value In RAM Plus Itself
    elif opcode == "\x08": # SUB $
        reg_a.value = ram[operand].value - reg_a # Set The Value In Register A To The Subtraction Of A Value In RAM Minus Itself
    elif opcode == "\x09": # AND $
        reg_a.value = ram[operand].value & reg_a # Set The Value In Register A To Itself Bitwise ANDed With A Value In RAM
    elif opcode == "\x0A": # ORA $
        reg_a.value = ram[operand].value | reg_a # Set The Value In Register A To Itself Bitwise ORed With A Value In RAM
    elif opcode == "\x0B": # EOR $
        reg_a.value = ram[operand].value ^ reg_a  # Set The Value In Register A To Itself Bitwise XORed With A Value In RAM
    elif opcode == "\x0C": # CMP $
        # Compare The Value In The A Register To A Value In RAM
        if reg_a.value == ram[operand].value:
            # Set The Equal Flag
            reg_flags.equal = True
        else: reg_flags.equal = False
        
        # See If It's Less Than (For BMI)
        if reg_a.value < ram[operand].value:
            # Set The Sign Flag
            reg_flags.sign = True
        else: reg_flags.sign = False
    
    elif opcode == "\x0D": # CPX $
        # Compare The Value In The X Register To A Value In RAM
        if reg_x.value == ram[operand].value:
            # Set The Equal Flag
            reg_flags.equal = True
        else: reg_flags.equal = False
        
        # See If It's Less Than (For BMI)
        if reg_x.value < ram[operand].value:
            # Set The Sign Flag
            reg_flags.sign = True
        else: reg_flags.sign = False
    
    elif opcode == "\x0E": # CPY $
        # Compare The Value In The Y Register To A Value In RAM
        if reg_y.value == ram[operand].value:
            # Set The Equal Flag
            reg_flags.equal = True
        else: reg_flags.equal = False
        
        # See If It's Less Than (For BMI)
        if reg_y.value < ram[operand].value:
            # Set The Sign Flag
            reg_flags.sign = True
        else: reg_flags.sign = False
    
    elif opcode == "\x0F": # BEQ $
        # Branch To A Routine If Equal Flag Is Set
        if reg_flags.equal: 
            saved_pc[saved_pc_count.value] = reg_programcounter.value
            saved_pc_count.change(saved_pc_count.value + 1)
            reg_programcounter = operand

        reg_flags.equal = False

    elif opcode == "\x10": # BNE $
        # Branch To A Routine If Equal Flag Is Not Set
        if not reg_flags.equal: 
            saved_pc[saved_pc_count.value] = reg_programcounter.value
            saved_pc_count.change(saved_pc_count.value + 1)
            reg_programcounter = operand

        reg_flags.equal = False
    
    elif opcode == "\x11": # BPS $
        # Branch To A Routine If Sign Flag Is Not Set
        if not reg_flags.sign:
            saved_pc[saved_pc_count.value] = reg_programcounter.value
            saved_pc_count.change(saved_pc_count.value + 1)
            reg_programcounter = operand

        reg_flags.sign = False

    elif opcode == "\x12": # BMI $
        # Branch To A Routine If Sign Flag Is Set
        if reg_flags.sign:
            saved_pc[saved_pc_count.value] = reg_programcounter.value
            saved_pc_count.change(saved_pc_count.value + 1)
            reg_programcounter = operand

        reg_flags.sign = False

    elif opcode == "\x13": # JMP $
        saved_pc = reg_programcounter.value
        saved_pc_count.change(saved_pc_count.value + 1)
        reg_programcounter = operand

    elif opcode == "\x14": # RET
        saved_pc_count.change(saved_pc_count.value - 1)
        reg_programcounter = saved_pc[saved_pc_count.value]

    elif opcode == "\x15": # INT
        print("INTERUPT REQUEST NOT HANDLED")

    elif opcode == "\x16": # LDA $
        reg_a.value = ram[operand].value # Set Register A To A Value In Memory

    elif opcode == "\x17": # LDX $
        reg_x.value = ram[operand].value # Set Register X To A Value In Memory

    elif opcode == "\x18": # LDY $
        reg_y.value = ram[operand].value # Set Register Y To A Value In Memory

    print(f"PC:{reg_programcounter.value} | A:{reg_a.value} | X: {reg_x.value} | Y: {reg_y.value} | CARRY: {reg_flags.carry} | EQUAL: {reg_flags.equal} | SIGN: {reg_flags.sign}")
    reg_programcounter.change(reg_programcounter.value + 2)
    

print("Program Ended, No More Instructions To Run")
pixelPulseDisplayInstanceThread.join()