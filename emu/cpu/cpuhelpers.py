"""
Balls
"""

import py65
import py65.devices
import py65.devices.mpu65c02 as w65c02s
import py65.disassembler
import py65.monitor

from utils.helpers import pixel_print

# CPU helpers

cpu = py65.devices.mpu65c02.MPU()
def config_cpu(args) -> w65c02s.MPU:
    """
    Configure the systems CPU and load the program

    ...

    Arguments
    ---------
    args
        An object containing the arguments

    Returns
    -------
    py65.devices.mpu65c02.MPU
        The CPU with all attributes loaded in
    """
    try:
        f = open(args.cart, "rb")
    except FileNotFoundError:
        print(f"Cart File \"{args.cart}\" Not Found")
        quit(1)

    # After reading the file
    program_bytes = f.read()

    #for byte in enumerate(program_bytes):
    #    #print(f"{program_bytes[byte]:02X}", end=" ")
    #    program.append(int(program_bytes[byte]))
    pixel_print(f"Cart is {hex(len(program_bytes))} bytes.",  __name__, "config_cpu")

    # Don't ask... I don't even know...
    cpu.memory[0x0000:0xFFFF] = program_bytes
    cpu.pc = (program_bytes[0xfffd] << 8) | program_bytes[0xfffc]

    pixel_print(f"Loaded to {cpu.pc}", __name__, "config_cpu")

    return cpu

def get_instruction_from_memory(addr: int, cpu_instance: py65.devices.mpu65c02.MPU) -> str:
    """
    Load an instruction from memory and disasemble it

    ...

    Arguments
    ---------
    addr : int
        An integer representing the index into the CPU's memory

    cpu_instance : py65.devices.mpu65c02.MPU
        The CPU to dissaseble from

    Returns
    -------
    str
        A string representing the disassembled instruction
    """
    addr_parser = py65.disassembler.AddressParser()
    dasm = py65.disassembler.Disassembler(cpu_instance, addr_parser)

    i = dasm.instruction_at(addr)

    inst_fmt_opc = i[1]

    return inst_fmt_opc
