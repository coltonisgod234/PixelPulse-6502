"""
Hello
"""

import py65.devices.mpu65c02

# Define classes
class SystemControllerState:
    """
    A class to represent a controller

    ...

    Attributes
    ----------
    buttons : list[str]
        The names of all the buttons

    pressed : dict[str, bool]
        A dictionary where keys are button names (str) 
        and values are booleans indicating whether each button is pressed.

    Methods
    -------
    press(buttonName)
        Press a button
    
    release(buttonName)
        Release a button
    
    convert_buttons_to_int() -> int
        Prepare the pressed dictionary to be stored in the CPU's memory
    """
    def __init__(self) -> None:
        self.buttons = ["up", "down", "left", "right", "a", "b"] # Define a list of all buttons
        # Define a dictionary of pressed buttons
        self.pressed = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False
        }
        self.buttons_conversion_table = {
            "up":       0b00001000,
            "down":     0b00000100,
            "left":     0b00010000,
            "right":    0b00100000,
            "a":        0b00000010,
            "b":        0b00000001
        }

    def press(self, button_name: str) -> None:
        """ 
        Press a button on the controller

        ...

        Arguments
        ---------
        button_name : str
            The identifier in the dictionary of what button to press
        """
        # Set the button in the dictionary to true
        self.pressed[button_name] = True

    def release(self, button_name: str) -> None:
        """ 
        Release a button on the controller

        ...

        Arguments
        ---------
        button_name : str
            The identifier in the dictionary of what button to release
        """
        self.pressed[button_name] = False

    def convert_buttons_to_int(self) -> int:
        """ 
        Convert the buttons to a bitmapped integer to prepare it for use in the system's memory

        This method checks the state of each button (pressed or not) and uses a conversion table
        to generate a bitmapped integer where each bit represents the state of a button.

        ...

        Returns
        -------
        int
            A bitmapped integer representing the states of the buttons.
        """
        pressed_int = 0b00000000
        for button, bitmask in self.buttons_conversion_table.items():
            # If the button is pressed, OR its bitmask into the result
            if self.pressed.get(button, False):
                result |= bitmask

        return pressed_int



SystemControllerState()



class PixelStatusRegister:
    """
    A class implementing the PixelStatusRegister, a register
    allowing status communication between the program and the
    PixelPulse hardware
    
    ...
    
    Attributes
    ----------
    status : int
        A bitmapped integer representing the current status
        of the register
        
    Methods
    -------
    set_status(self, bit: int)
        Set a status bit to 1 based on it's index

    clear_status(self, bit: int)
        Clear a status bit to 0 bit based on it's index

    get_satus(self, bit: int) -> int
        Get a status bit based on it's index

    get_all_status(self) -> str
        Get all the status bits into a binary string, for display purposes only.
    """
    def __init__(self) -> None:
        self.status = 0

    def set_status(self, bit: int) -> None:
        """
        Set a status bit to 1 based on it's index
        
        ...
        
        Arguments
        ---------
        bit : int
            The index of the bit to set
        """
        status = self.status
        status = status | (1 << bit)
        self.status = status

    def clear_status(self, bit: int) -> None:
        """
        Clear a status bit to 0 based on it's index
        
        ...
        
        Arguments
        ---------
        bit : int
            The index of the bit to clear
        """
        status = self.status
        status = status &(1 << bit)
        self.status = status

    def get_status(self, bit: int) -> int:
        """
        Get a status bit based on it's index
        
        ...
        
        Arguments
        ---------
        bit : int
            The index of the bit to get

        Returns
        -------
        int
            The value of the requested bit
        """
        return (self.status >> bit) & 1

    def get_all_status(self) -> str:
        """
        Get all status bits into a binary format.
        For display purposes only
        
        ...
        
        Arguments
        ---------
        bit : int
            The index of the bit to set

        Returns
        -------
        str
            A binary string representing all bits (python '0b' string)
        """
        return bin(self.status)

def tick_controllers(cpu: py65.devices.mpu65c02.MPU, controller1: SystemControllerState,
                     controller2: SystemControllerState) -> None:
    """
    Updates CPU memory addresses involving controllers (0x3011 and 0x3012)
    Call once per tick.

    ...
    
    Arguments
    ---------
    cpu : py65.devices.mpu65c02.MPU
        The CPU instance to update
    controller1 : SystemControllerState
        Player 1's controller object
    
    controller2 : SystemControllerState
        Player 2's controller object
    """
    # Update The Controllers
    cpu.memory[0x3011] = controller1.convert_buttons_to_int()
    cpu.memory[0x3012] = controller2.convert_buttons_to_int()

def tick_pixel_status_register(cpu: py65.devices.mpu65c02.MPU,
                               status_reg: PixelStatusRegister) -> PixelStatusRegister:
    """
    Updates a PixelStatusRegister object and syncs with the CPU's memory

    ...

    Arguments
    ---------
    cpu : py65.devices.mpu65c02.MPU
        The CPU to sync with

    status_reg : PixelStatusRegister
        The PixelStatusRegister instance to sync with

    Returns
    -------
    PixelStatusRegister
        The synced PixelStatusRegister
    """
    # Slightly faster by not swapping the new one back into the CPUs memory
    # as the CPU already has the changes.
    status_reg.status = cpu.memory[0x3024]
    return status_reg
