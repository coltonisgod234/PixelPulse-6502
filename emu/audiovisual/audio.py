"""
Audio
"""

# pylint: disable=import-error,unused-import

from cpu.constants import (VOICES_COUNT, CHANNELS_COUNT, APU_LENGTH, APU_PITCH_TABLE,
                           CHANNEL_OFFSETS, AUDIO_TABLE)
from audiovisual.avhelpers import (generate_triangle_wave, generate_sawtooth_wave,
                       generate_sine_wave, generate_square_wave)

import pygame
from utils.helpers import get_low_nibble, get_high_nibble, pixel_print


# Fucking peice of shit

#def tick_audio(cpu) -> None:
#    """
#    Ticks the audio systems
#
#    ...
#
#    Arguments
#    ---------
#    cpu : py65.devices.65c02.MPU
#        The CPU to update
#    """
#    # Play The Sounds
#    audio_ram = cpu.memory[0x3000:0x3010]
#    # Loop through all the channels
#    for channel, voices in AUDIO_TABLE.items():
#        # Loop through all voices in the current channel
#        for voice_index, pitch_byte in enumerate(voices):
#            if channel == 0:
#                offset = AUDIO_TABLE[channel][voice_index]
#                x = audio_ram[offset]
#                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
#
#                audio = generate_square_wave(APU_LENGTH, frequency, 1.0)
#                sound = pygame.mixer.Sound(audio)
#                sound.play()
#
#            if channel == 1:
#                offset = AUDIO_TABLE[channel][voice_index]
#                x = audio_ram[offset]
#                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
#
#                audio = generate_triangle_wave(APU_LENGTH, frequency, 1.0)
#                sound = pygame.mixer.Sound(audio)
#                sound.play()
#
#            if channel == 2:
#                offset = AUDIO_TABLE[channel][voice_index]
#                x = audio_ram[offset]
#                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
#
#                audio = generate_sawtooth_wave(APU_LENGTH, frequency, 1.0)
#                sound = pygame.mixer.Sound(audio)
#                sound.play()
#
#            if channel == 3:
#                offset = AUDIO_TABLE[channel][voice_index]
#                x = audio_ram[offset]
#                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
#
#                audio = generate_sine_wave(APU_LENGTH, frequency, 1.0)
#                sound = pygame.mixer.Sound(audio)
#                sound.play()

def find_pitch_and_volume_of_byte(byte: int) -> tuple[int, int]:
    """
    Finds the pitch and volume of a given byte and returns them

    ...

    Arguments
    ---------
    byte : int
        The byte to extract data from

    Returns
    -------
    tuple[int, int]
        A tuple containing:
        - pitch (int): The pitch value extracted from the byte.
        - volume (int): The volume value extracted from the byte.
    """
    # If the byte is 0 we can just return zero
    if byte == 0:
        return (0, 0)

    # Otherwise, get the pitch
    pitch = get_high_nibble(byte)
    pitch = APU_PITCH_TABLE[pitch]

    volume = get_low_nibble(byte)

    return (pitch, volume)

def play_sound(channel: int, byte: int):
    """
    Takes a channel and byte, then plays said sound according to the audio chip
    
    ...
    
    Arguments
    ---------
    channel : int
        The channel to play the sound on, refer to the audio chip's table
        to get the right channel for your wave
        
    byte : int
        The byte containing pitch and volume data for that channel
    """
    pitch, volume = find_pitch_and_volume_of_byte(byte)
    if channel in [0, 6]: # Square wave
        wave = generate_square_wave(1.0, pitch, volume)
    elif channel in [1, 7]: # Triangle wave
        wave = generate_triangle_wave(1.0, pitch, volume)
    elif channel in [2]: # Sine wave
        wave = generate_sine_wave(1.0, pitch, volume)

    else:
        return  # Skip unsupported channels

    pygame.mixer.Channel(channel).play(pygame.mixer.Sound(wave))

def tick_audio(cpu) -> None:
    """
    Ticks the audio systems
    
    ...
    
    Arguments
    ---------
    cpu : py65.devices.65c02.MPU
        The CPU to update"""
    audio_ram = cpu.memory[0x3000:0x3010]
    for channel, byte in enumerate(audio_ram):
        play_sound(channel, byte)

# SEP 16

#def tick_audio(cpu) -> None:
#    """
#    Ticks the audio systems
#
#    ...
#
#    Arguments
#    ---------
#    cpu : py65.devices.65c02.MPU
#        The CPU to update
#    """
#    # Play The Sounds
#    audio_ram = cpu.memory[0x3000:0x3010]
#    # Loop through all the channels
#    for channel, byte in enumerate(audio_ram):
#        print(channel, byte)
#        # If the channel is a square wave, run the square wave code
#        if channel in [0, 6]: # Square wave
#            # Get the pitch and volume
#            pitch, volume = find_pitch_and_volume_of_byte(byte)
#            # Optimization: Makes sure we only generate the wave if it actually matters
#            #if pitch == 0 and volume == 0:
#            #    continue
#
#            wave = generate_square_wave(1.0, pitch, volume)
#
#            sound = pygame.mixer.Sound(wave)
#            sound.play()
#
#        if channel in [1, 7]: # Triangle waves
#            # Get the pitch and volume
#            pitch, volume = find_pitch_and_volume_of_byte(byte)
#            # Optimization: Makes sure we only generate the wave if it actually matters
#            #if pitch == 0 and volume == 0:
#            #    continue
#
#            wave = generate_sawtooth_wave(1.0, pitch, volume)
#
#            sound = pygame.mixer.Sound(wave)
#            sound.play()
#
#        if channel == 2: # Sine wave
#            # Get the pitch and volume
#            pitch, volume = find_pitch_and_volume_of_byte(byte)
#
#            # Optimization: Makes sure we only generate the wave if it actually matters
#            if pitch == 0 and volume == 0:
#                continue
#
#            wave = generate_square_wave(1.0, pitch, volume)
#
#            sound = pygame.mixer.Sound(wave)
#            sound.play()
#
#        if channel == 3: # Noise
#            pass
#
#
