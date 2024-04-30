import argparse

parser = argparse.ArgumentParser(description="Assembler For The PixelPulse 6502 CPU")
parser.add_argument("input", metavar="input", type=str, help="Input File To Assemble")
parser.add_argument("output", metavar="output", type=str, help="Filename To Assemble To (If it isn't provided it will default to a.py)", default="a.py")
parser.add_argument("-f", metavar="format", type=str, help="Format To Assemble To (Supported formats are: py)", default="py")

args = parser.parse_args()

instructions = {
    "nop": 0x00,
    "lda": 0x01,
    "ldy": 0x02,
    "ldx": 0x03,
    "sta": 0x04,
    "sty": 0x05,
    "stx": 0x06,
    "add": 0x07,
    "sub": 0x08,
    "and": 0x09,
    "ora": 0x0A,
    "eor": 0x0B,
    "cmp": 0x0C,
    "cpx": 0x0D,
    "cpy": 0x0E,
    "beq": 0x0F,
    "bne": 0x10,
    "bps": 0x11,
    "bmi": 0x12,
    "jmp": 0x13,
    "spc": 0x14,
    "int": 0x15,
    "lda_m": 0x16,
    "ldx_m": 0x17,
    "ldy_m": 0x18,
    "lpc": 0x19
}


try:
    code_filepointer = open(args.input)
except FileNotFoundError:
    print("The Input File Specified Doesn't Exist")
    quit(1)

try:
    output_filepointer = open(args.output, "w")
except FileNotFoundError:
    print("The Output File Specified Doesn't Exist")

code = code_filepointer.readlines()
output = []

output_filepointer.write("rom = [0x00,0x00,0x00")

for i in range(len(code)):
    line = code[i].split()
    print(line)
    if len(line) < 2: # It's A Subroutine Then
        print(f"{line} is a subroutine")
    else: # It's An Instruction
        # Handle The Opcode
        inst = instructions[line[0]]
        operand = line[1]
        #print(inst)
        output_filepointer.write(f",{hex(inst)}")

        # And Then Handle The Operand
        if len(operand) == 2:
            # Then This Is An Immideate Value
            hexvalue = operand.strip()
            output_filepointer.write(f",0x{hexvalue}")
            output_filepointer.write(",0x00")
        elif len(operand) == 1:
            print("Implied Instruction, We Do Not Care")
        else: # This Is A Memory Instruction
            print(line, "is memory")
            part1 = operand[:2]
            part2 = operand[2:]
            output_filepointer.write(f",0x{part1},0x{part2}")

output_filepointer.write("]")