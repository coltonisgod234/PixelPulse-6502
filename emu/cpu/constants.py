"""
Constants
"""

from time import perf_counter

DISPLAY_X_SIZE = 64     # X size of display
DISPLAY_Y_SIZE = 64     # Y size of display
VRAM_LOCATION = 0x1000  # VRAM Location
VRAM_END_LOCATION = 0x2FFF  # VRAM end location

CHANNELS_COUNT = 4      # Amount of channels
CHANNEL_OFFSETS = [0, 4, 8, 12]
# SHUT THE FUCK UP:
AUDIO_TABLE = {
    # Channel num
    0: [
        0x00, # Voice 1
        0x01, # Voice 2
        0x02, # Voice 3
        0x03  # ETC
    ],
    1: [
        0x04,
        0x05,
        0x06,
        0x07
    ],
    2: [
        0x08,
        0x09,
        0x0a,
        0x0b
    ],
    3: [
        0x0c,
        0x0d,
        0x0e,
        0x0f
    ]
}
VOICES_COUNT = 4        # Amount of voices

APU_PITCH_TABLE = [0, 82, 110, 146, 246, 261, 293, 329, 349, 392, 440, 493, 525, 659, 880, 1024, 2048, 3048, 3048]
APU_SAMPLERATE = 44000
APU_LENGTH = 10 # The length of the sounds in the APU (not samples, just the individual pitches)

TARGET_FPS = 24             # The target FPS of the system, typically 24
TARGET_CLOCK_RATE = 14000    # The target clock rate in Hz, typically 4 MHz
CYCLES_PER_FRAME = 1024

VERSION_INFO = "PixelPulse v0.4 prealpha"

# A table describing the diffrent error levels, info, debug, warn, error and critical
ERRRORLEVEL_TABLE = {
    0: "info",
    1: "debug",
    2: "warn",
    3: "error",
    4: "critical",
}

MAX_DIR_SEARCH_DEPTH = 4

# The time when execution of the emulator begins, used for logging, delta calculations, ETC
PROGRAM_EXECUTIONTIME_START = perf_counter()

BLACK_COLORS_LIST_INDEX = 0

# Open the logfile and reset it
LOGFILE = open("pixelpulse.log", "w+", encoding="utf-8")
LOGFILE.truncate(0)
