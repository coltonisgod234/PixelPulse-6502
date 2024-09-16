"""
Audio
"""

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
    # Loop through all the channels
    for channel, voices in AUDIO_TABLE.items():
        # Loop through all voices in the current channel
        for voice_index, pitch_byte in enumerate(voices):
            if channel == 0:
                x = audio_ram[pitch_byte]
                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
                if frequency == 0:
                    continue

                audio = generate_square_wave(APU_LENGTH, frequency, 1.0)
                sound = pygame.mixer.Sound(audio)
                sound.play()

            if channel == 1:
                x = audio_ram[pitch_byte]
                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
                if frequency == 0:
                    continue

                audio = generate_triangle_wave(APU_LENGTH, frequency, 1.0)
                sound = pygame.mixer.Sound(audio)
                sound.play()

            if channel == 2:
                x = audio_ram[pitch_byte]
                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
                if frequency == 0:
                    continue

                audio = generate_sawtooth_wave(APU_LENGTH, frequency, 1.0)
                sound = pygame.mixer.Sound(audio)
                sound.play()
                
            if channel == 3:
                x = audio_ram[pitch_byte]
                frequency = APU_PITCH_TABLE[get_high_nibble(x)]
                if frequency == 0:
                    continue

                audio = generate_sine_wave(APU_LENGTH, frequency, 1.0)
                sound = pygame.mixer.Sound(audio)
                sound.play()