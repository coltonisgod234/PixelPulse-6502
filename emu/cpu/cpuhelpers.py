from time import perf_counter
from typing import SupportsIndex

from helpers import pixel_print

import py65
import py65.devices
import py65.devices.mpu65c02
import py65.disassembler
import py65.monitor

# CPU helpers

cpu = py65.devices.mpu65c02.MPU()
def config_cpu(args) -> py65.devices.mpu65c02.MPU:
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
        
    pixel_print(f"Cart is {hex(len(program))} bytes.")

    cpu.memory[0x0000:0xFFFF] = program
    cpu.pc = (program[0xfffd] << 8) | program[0xfffc]  # Don't ask... I don't even know...

    pixel_print(f"Loaded to {cpu.pc}")

    return cpu


def get_instruction_from_memory(addr: int) -> str:
    addr_parser = py65.disassembler.AddressParser()
    dasm = py65.disassembler.Disassembler(cpu, addr_parser)

    i = dasm.instruction_at(addr)

    inst_fmt_opc = i[1]

    return inst_fmt_opc