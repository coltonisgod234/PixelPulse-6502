from time import perf_counter

from constants import (DEBUG_MODE_MASK, ERRRORLEVEL_TABLE, LOGFILE,
                       PROGRAM_EXECUTIONTIME_START)


def get_execution_time() -> float:
    now = perf_counter() - PROGRAM_EXECUTIONTIME_START
    return now

def pretty_float(f: float, length=24) -> str:
    return str(f).rjust(20, "0")

def pixel_print(msg: str, errorlevel=1) -> None:
    try:
        if errorlevel == 1 and DEBUG_MODE_MASK: return  # We don't care about debug info if this is a release mode 
        formatted_msg = f"[{pretty_float(get_execution_time(), 22):>22}]  {ERRRORLEVEL_TABLE[errorlevel]: <8}    {msg}"
        LOGFILE.write(f"{formatted_msg}\n")
        print(formatted_msg)
    
    except IOError as e:
        print(f"[{get_execution_time():>22}]  {ERRRORLEVEL_TABLE[2]: <8}    Error writing to logfile: {e}")

    finally:
        return

def get_high_nibble(x: int) -> int:
    return x >> 4

def get_low_nibble(x: int) -> int:
    return x & 0b1111