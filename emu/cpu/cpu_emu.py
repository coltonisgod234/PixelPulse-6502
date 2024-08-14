"""
Balls
"""

import py65.devices.mpu65c02
from utils.helpers import pixel_print

def tick_cpu(cpu: py65.devices.mpu65c02.MPU):
    """
    Ticks the CPU logic every cycle
    
    ...
    
    Arguments
    ---------
    cpu : py65.devices.mpu65c02.MPU
        The CPU to run the logic on
    """
    cpu.step()

    if cpu.memory[cpu.pc] == 0x00:
        # Tell the user, idk what to do here
        pixel_print("Encountered BRK instruction.", __name__, "tick_cpu")
