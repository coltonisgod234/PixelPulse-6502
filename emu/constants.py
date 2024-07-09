from time import perf_counter

DISPLAY_X_SIZE = 64         # X size of display
DISPLAY_Y_SIZE = 64         # Y size of display
VRAM_LOCATION = 0x1000      # VRAM Location
VRAM_END_LOCATION = 0x2FFF  # VRAM end location

CHANNELS_COUNT = 4          # Amount of channels
VOICES_COUNT = 4            # Amount of voices

APU_VOLUME_BASE = 0         # Base volume of APU (a 0h in volume equals this)
APU_VOLUME_STEP = 0.05      # How much volume to step of from the base
APU_PITCH_BASE = 0          # Base pitch of APU (a 0h in pitch equals this)
APU_PITCH_STEP = 512        # How much pitch to step up from the base
APU_SAMPLERATE = 44100     # The sample rate of sounds in the APU
APU_LENGTH = 10             # The length of the sounds in the APU (not samples, just the individual pitches)

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

DEBUG_MODE_MASK = False     # Wether the system is in debug mode, this is configured later.

PROGRAM_EXECUTIONTIME_START = perf_counter()    # The time when execution of the emulator begins, used for logging, delta calculations, ETC

# Open the logfile and reset it
LOGFILE = open("pixelpulse.log", "w+")
LOGFILE.truncate(0)

# Now we can configure constants
def configure_constants(args):
    global DEBUG_MODE_MASK
    DEBUG_MODE_MASK = True if args.debug else False