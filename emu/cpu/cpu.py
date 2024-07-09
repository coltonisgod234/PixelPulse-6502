import py65.devices.mpu65c02
from helpers import pixel_print

def tick_cpu(cpu: py65.devices.mpu65c02.MPU):
    cpu.step()

    if cpu.memory[cpu.pc] == 0x00:
            pixel_print("Encountered BRK instruction.")  # Tell the user, idk what to do here