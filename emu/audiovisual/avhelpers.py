import numpy as np
from constants import APU_SAMPLERATE
import pygame

def generate_triangle_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    triangle_wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return triangle_wave * volume

def generate_sawtooth_wave(length, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    sawtooth_wave = 2 * (t * frequency - np.floor(t * frequency))
    return sawtooth_wave * volume

def generate_square_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    square_wave = np.sign(np.sin(2 * np.pi * frequency * t))
    return square_wave * volume

def generate_sine_wave(length: int, frequency: int, volume=1.0) -> np.ndarray:
    t = np.linspace(0, length, int(length * APU_SAMPLERATE), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    return sine_wave * volume

def draw_pixel(x: int, y: int, col: int) -> None:
    display = pygame.display.get_surface()
    colors = [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),(0,128,128),(192,192,192),(128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]

    rect = pygame.rect.Rect(x, y, 8, 8)
    pygame.draw.rect(display, colors[col], rect)