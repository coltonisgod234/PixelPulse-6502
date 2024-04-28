rom = "\x00\x00\x01\xFF" # Will Change To Argparse, Only Like This In Debug Mode.

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
            reg_flags[0] = True
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
                reg_flags[0] = True
            self.value = 0
        elif value < self.min:
            print("Register Underflow, Overflowing To 255")
            self.value = 255
        else:
            self.value = value

def getRamValue(address):
    """
    Fetches A Value In Ram As A `BinaryRegister` Object
    Example use:
    `getRamObject(3000) = 255`
    """
    return ram[address].value

# Initalize The Registers
reg_a = BinaryRegister()
reg_x = BinaryRegister()
reg_y = BinaryRegister()
reg_flags = [False, False, False, False] # This One Is Special (♪freinds♪)
#           Carry, Equal, Sign,  Reserved

reg_programcounter = ConstrainedRegister(0, 32768, can_set_carry_flag=False)

ram = [BinaryRegister() for i in range(32768)]

while reg_programcounter.value < len(rom):
    opcode = rom[reg_programcounter.value]
    operand = rom[reg_programcounter.value + 1]

    if opcode == "\x00": # NOP
        print("0x00 | NOP: Do Nothing")
    elif opcode == "\x01": # LDA #
        print("0x01 | LDA #: Load accumulator with a value.")
        reg_a.value = operand
    elif opcode == "\x02": # LDY #
        reg_y.value = operand
    elif opcode == "\x03": # LDX #
        reg_x.value = operand
    elif opcode == "\x04": # STA $
        ram[operand].value = reg_a.value
    elif opcode == "\x05": # STY $
        ram[operand].value = reg_y.value
    elif opcode == "\x06": # STX $
        ram[operand].value = reg_x.value
    elif opcode == "\x07": # ADD $
        reg_a.value = ram[operand].value + reg_a
    elif opcode == "\x08": # SUB $
        reg_a.value = ram[operand].value - reg_a
    elif opcode == "\x09": # AND $
        reg_a.value = ram[operand].value & reg_a
    elif opcode == "\x0A": # ORA $
        reg_a.value = ram[operand].value | reg_a
    elif opcode == "\x0B": # EOR $
        reg_a.value = ram[operand].value ^ reg_a

    # I'll Finish This Later.
    

    reg_programcounter.change(reg_programcounter.value + 2)
    print(reg_programcounter.value)

print("Program Ended, No More Instructions To Run")