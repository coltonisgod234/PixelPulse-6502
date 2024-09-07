"""
Audio
"""

from cpu.constants import (VOICES_COUNT, CHANNELS_COUNT, APU_LENGTH, APU_PITCH_TABLE,
                           CHANNEL_OFFSETS)
from audiovisual.avhelpers import (generate_triangle_wave, generate_sawtooth_wave,
                       generate_sine_wave, generate_square_wave)

import pygame
from utils.helpers import get_low_nibble, get_high_nibble


# Fucking peice of shit

def tick_audio(cpu) -> None:
    """
    Ticks the audio systems
    
    ...
    
    Arguments
    ---------
    cpu : py65.devices.65c02.MPU
        The CPU to update
    """
    # Play The Sounds
    audio_ram = cpu.memory[0x3000:0x3010]
    for channel in range(CHANNELS_COUNT):
        for voice in range(VOICES_COUNT):
            if voice == 0:
                