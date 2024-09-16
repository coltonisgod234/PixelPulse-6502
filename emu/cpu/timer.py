"""
Routines for interupting the CPU
Required for the PIC chip
"""

import py65
import py65.devices
import py65.devices.mpu65c02 as w65c02
from time import perf_counter
from utils.helpers import combine_integers, split_integers

class Timer:
    def __init__(self):
        self.counter = None
        self.interrupt_flag = False

    def update(self, cycles: int):
        if isinstance(self.counter, int):
            if self.counter <= 0:
                self.counter -= cycles

                self.interrupt_flag = True
                self.counter = None

    def reset(self, cycles):
        self.counter = cycles
        self.interrupt_flag = False

def tick_timer(cpu: w65c02.MPU, timer: Timer):
    timer.update(1)
    timer_RAM = cpu.memory[0x3025:0x302F]
    timer_data = combine_integers(timer_RAM[0x01], timer_RAM[0x00])
    timer_command = timer_RAM[0x02]
    timer_source = timer_RAM[0x03]
    timer_status = timer_RAM[0x04]

    if timer_command == 0x01:
        timer.reset(timer_data)

    if timer.interrupt_flag:
        timer_status |= 0b01000000
        cpu.nmi()

    cpu.memory[0x3025+0x02] = timer_command
    cpu.memory[0x3025+0x03] = timer_source
    cpu.memory[0x3025+0x04] = timer_status