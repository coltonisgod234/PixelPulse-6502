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
VOICES_COUNT = 4        # Amount of voices

APU_PITCH_TABLE = [0, 82, 110, 146, 246, 261, 293, 329, 349, 392, 440, 493, 525, 659, 880]
APU_SAMPLERATE = 44000
APU_LENGTH = 10 # The length of the sounds in the APU (not samples, just the individual pitches)

TARGET_FPS = 60             # The target FPS of the system, typically 24
TARGET_CLOCK_RATE = 4000    # The target clock rate in Hz, typically 4 MHz

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
