"spheres"

# Pylint does not shut up about my imports, so I've forced it to
# pylint: disable=import-error

import numpy as np
from cpu.constants import APU_SAMPLERATE
import pygame

def generate_triangle_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    triangle_wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return triangle_wave * volume

def generate_sawtooth_wave(length, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    sawtooth_wave = 2 * (t * frequency - np.floor(t * frequency))
    return sawtooth_wave * volume

def generate_square_wave(length: int, frequency: int, volume=1.0) -> bytes:
    # What does this do, I don't know but I think it makes a square wave
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    square_wave = np.sign(np.sin(2 * np.pi * frequency * t))
    
    # This scales the volume so it's not super quiet
    scaled_wave = square_wave * volume
    
    # This will convert it to 16-bit PCM format, apparently this is what I have to use
    pcm_wave = np.int16(scaled_wave * 32767)
    
    # Now we have to convert to bytes
    return pcm_wave.tobytes()

def generate_sine_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)

    return sine_wave * volume

def draw_pixel(x: int, y: int, col: int) -> None:
    display = pygame.display.get_surface()
    colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

    rect = pygame.rect.Rect(x, y, 4, 4)
    pygame.draw.rect(display, colors[col], rect)