"""
Audio
"""

from cpu.constants import (VOICES_COUNT, CHANNELS_COUNT, APU_LENGTH, APU_VOLUME_BASE,
                           APU_PITCH_BASE, APU_PITCH_STEP, APU_VOLUME_STEP)
from audiovisual.avhelpers import (generate_triangle_wave, generate_sawtooth_wave,
                       generate_sine_wave, generate_square_wave)

import pygame
from utils.helpers import get_low_nibble, get_high_nibble

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
    for voice in range(VOICES_COUNT):
        for channel in range(CHANNELS_COUNT):
            if voice == 0: # It's A Square Wave
                # Calculate freqencies and audios and stuff
                # I have no idea what this means, it's honestly just a mix of constants
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 4) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP
                buffer = generate_square_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                #sound.play(0)

            if voice == 1: # It's A Triangle Wave
                # Calculate freqencies and audios and stuff
                # I have no idea what this means, it's honestly just a mix of constants
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 8) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP
                buffer = generate_triangle_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)

            if voice == 2: # It's A Sawtooh Wave
                # Calculate freqencies and audios and stuff
                # I have no idea what this means, it's honestly just a mix of constants
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 12) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP
                buffer = generate_sawtooth_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)

            if voice == 3: # It's A Sine Wave
                # Calculate freqencies and audios and stuff
                # I have no idea what this means, it's honestly just a mix of constants
                freq = APU_PITCH_BASE + get_low_nibble(audio_ram[channel] + 16) * APU_PITCH_STEP
                vol = APU_VOLUME_BASE + get_high_nibble(audio_ram[channel]) * APU_VOLUME_STEP
                buffer = generate_sine_wave(APU_LENGTH, freq, vol)  # Buffer all that audio
                sound = pygame.mixer.Sound(buffer)  # Play it

                sound.play(0)
