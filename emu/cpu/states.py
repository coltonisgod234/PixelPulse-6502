from typing import SupportsIndex
import py65.devices.mpu65c02

# Define classes
class SystemControllerState:
    def __init__(self) -> None:
        self.buttons = ["up", "down", "left", "right", "a", "b"]
        self.pressed = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False
        }

    def press(self, buttonName: str) -> None:
        self.pressed[buttonName] = True
    
    def release(self, buttonName: str) -> None:
        self.pressed[buttonName] = False

    def convert_buttons_to_int(self) -> int:
        pressed_int = 0b00000000
        if self.pressed["right"]: pressed_int |= 0b00100000
        if self.pressed["left"]: pressed_int  |= 0b00010000
        if self.pressed["up"]: pressed_int    |= 0b00001000
        if self.pressed["down"]: pressed_int  |= 0b00000100
        if self.pressed["a"]: pressed_int     |= 0b00000010
        if self.pressed["b"]: pressed_int     |= 0b00000001

        self.pressed_as_int = pressed_int
        return pressed_int

class PixelStatusRegister:
    def __init__(self) -> None:
        self.status = 0

    def set_status(self, bit: int) -> None:
        status = self.status
        status = status | (1 << bit)
        self.status = status

    def clear_status(self, bit: int) -> None:
        status = self.status
        status = status &(1 << bit)
        self.status = status

    def get_status(self, bit: int) -> int:
        return (self.status >> bit) & 1
    
    def get_all_status(self) -> str:
        return bin(self.status)

def tick_controllers(cpu: py65.devices.mpu65c02.MPU, controller1: SystemControllerState, controller2: SystemControllerState) -> None:
    # Update The Controllers
    cpu.memory[0x3011] = controller1.convert_buttons_to_int()
    cpu.memory[0x3012] = controller2.convert_buttons_to_int()

def tick_PixelStatusRegister(cpu: py65.devices.mpu65c02.MPU, statusReg: PixelStatusRegister) -> PixelStatusRegister:
    statusReg.status = cpu.memory[0x3024]
    return statusReg