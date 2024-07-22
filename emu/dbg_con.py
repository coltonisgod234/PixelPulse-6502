from typing import Any
from cpu.cpuhelpers import config_cpu, get_instruction_from_memory
import pygame
from time import sleep, monotonic

import argparse

parser = argparse.ArgumentParser(description="Emulator for the PixelPulse 6502")
parser.add_argument("cart", metavar="cartridge", type=str, help="the cartdrige to load")
parser.add_argument("--debug", action="store_true", help="Enalbe debug mode")
args = parser.parse_args()

pygame.quit()

cpu = config_cpu(args)

breakpoints = {}
traces = []

def trace():
        print("AC    | RX    | RY    | PC    |   NV-BDIZC | SP    | IR")
        for trace in traces:
            print(f"{trace["a"]: <5} | {trace["x"]: <5} | {trace["y"]: <5} | {trace["pc"]: <5} | {bin(trace["p"]): <8} | {trace["sp"]: <5} | {trace["disassembled"]: <13}")

def registers():
    print("AC | RX | RY | PC   |   NV-BDIZC | SP | IR")
    print(f"{cpu.a:02X} | {cpu.x:02X} | {cpu.y:02X} | {cpu.pc:02X} | {bin(cpu.p):<10} | {cpu.sp:02X} | {get_instruction_from_memory(cpu.pc):<13}")

def step():
    cpu.step()

def dump_memory(start_address, end_address, bytes_per_line):
    current_address = start_address
    while current_address <= end_address:
        # Format the address in hexadecimal
        print(f"${current_address:04X}: ", end="")

        # Fetch and format 16 bytes of data
        for i in range(bytes_per_line):
            if i > 0 and i % 8 == 0:
                print(" ", end="")
            print(f"{cpu.memory[current_address]:02X}", end=" ")

            current_address += 1

        print()

def dbg_console():
    # Commands: (s:step|t:trace|bp:breakpoint|rmbp:remove_breakpoint|r:registers|ec:execute-custom|q:quit|rbp:run-until-bp|d:disassemble|lbp:bps:list-bps)
    cmd = input(".").lower().split()
    if cmd[0] in ["q", "quit", "exit"]:
        quit(0)
    if cmd[0] in ["s", "step"]:
        registers()
        step()

    if cmd[0] in ["r", "registers"]:
        registers()

    if cmd[0] in ["d"]:
        try:
            addr = int(cmd[1], 16)
            print(get_instruction_from_memory(addr))
        except IndexError:
            print(get_instruction_from_memory(cpu.pc))
    
    if cmd[0] in ["dr"]:
        start = int(cmd[1], 16)
        end = int(cmd[2], 16)
        for i in range(start, end):
            print(get_instruction_from_memory(i))
    
    if cmd[0] in ["bp"]:
        if cmd[1] in breakpoints.keys():
            print(f"A breakpoint with the name {cmd[1]} already exists")
            return 1
        else:
            breakpoints[cmd[1]] = cmd[2]
    
    if cmd[0] in ["lbp", "list-bps", "bps"]:
        print("Name           Value")
        print("--------------------")
        for key, value in breakpoints.items():
            print(f"{key: <15}{value: <15}")

    if cmd[0] in ["rbp"]:
        print("Stepping until breakpoint")
        while str(cpu.pc) not in breakpoints.values():
            step()
            registers()

        # We hit something, but we wanna know what
        for key, value in breakpoints.items():
            if value == str(cpu.pc): # If the value is the same as the program counter. Conversion to string is nessasary as breakpoints.items() contains strings no matter the type
                print(f"Hit breakpoint '{key}' at address {value}!") # Tell the user
                return 0
            
    if cmd[0] in ["mp", "peek"]:
        print(cpu.memory[cmd[1]])

    if cmd[0] in ["ms", "poke"]:
        cpu.memory[cmd[1]] = cmd[2]

    if cmd[0] in ["ss", "show-stack"]:
        dump_memory(0x0100, 0x01FF, 16)

    if cmd[0] in ["m", "memory"]:
        dump_memory(int(cmd[1], 16), int(cmd[2], 16), 16)
            
    if cmd[0] in ["t", "trace"]:
        trace()

while True: 
    try:
        dbg_console()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("exception", e)