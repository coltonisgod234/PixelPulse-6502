# pylint: disable=import-error

"""
Helpers
"""
import json
from pathlib import Path
from time import perf_counter

from cachetools import TTLCache

from cpu.constants import (ERRRORLEVEL_TABLE, LOGFILE, MAX_DIR_SEARCH_DEPTH,
                             PROGRAM_EXECUTIONTIME_START)

JSONcache = TTLCache(maxsize=100, ttl=300.0)
localeCache = TTLCache(maxsize=100, ttl=300.0)

def find_directory(project_root: str, target_dir: str):
    """
    Looks for a specified directory in the project folder
    
    ...
    
    Arguments
    ---------
    project_root : str
        The root of the proejct, 
        
    target_dir : str
        The directory to find

    Raises
    ------
    FileNotFoundError
        If the directory isn't found
        
    Returns
    -------
    str
        The full path to the target directory if found.
    """
    current_dir = Path(project_root).resolve()
    pixel_print(f"Searching for directory '{target_dir}'", __name__, "find_directory")

    # Maximum search depth of 4, if this loop exits the directory probably doesn't exist anywhere
    for _ in range(MAX_DIR_SEARCH_DEPTH):
        # Check if the directory exists in the current directory, if so then stop the search
        pixel_print(f"  Searching directory {current_dir}", __name__, "find_directory")

        potential_locale_dir = current_dir / target_dir
        if potential_locale_dir.is_dir():
            pixel_print(f"  Found directory {current_dir}")
            return potential_locale_dir

        # Move up one directory level
        parent_dir = current_dir.parent
        # * If we've reached the root directory without finding our target directory,
        # * Then we stop the search
        if parent_dir == current_dir:
            raise FileNotFoundError(f"{target_dir} directory not found")
        current_dir = parent_dir

    raise RecursionError("Max depth limit reached")

def load_json_path(json_file: dict, path: str):
    """
    Loads the path of a JSON seperated by dots
    
    ...
    
    Arguments
    ---------
    json_file : dict
        Dictionary representing the decoded JSON file
        
    path : str
        The dot-seperated string to use for the operation
        
    Returns
    -------
    Any
        varible representing the value at that path
    """
    #pixel_print(f"Searching for {resource_name}/{path}...",
    # __name__, f"load_JSON_path")
    keys = path.split(".") # Split by every dot
    try:
        return JSONcache[f"{json_file},{path}"] # If it's cached, just return the cached value
    except KeyError:
        for key in keys: # For every key, we go down one place

            #pixel_print(f"  Searching for {resource_name}/{path}, currently in {key}",
            # __name__, f"load_JSON_path")

            json_file = json_file.get(key, {})

        #pixel_print(f"Found matching {key} for {resource_name}/{path}",
        # __name__, f"load_JSON_path")

        JSONcache[f"{json_file},{path}"] = json
        return json_file # At the end we return the JSON

class LocaleManager:
    """
    Manages messages (provides multilingual support)
    """
    def __init__(self):
        self.locale_texts = None
        self.locale_file_path = None

    def load_locale(self, language: str, reigon: str):
        """
        Loads a locale file
        
        ...
        
        Arguments
        ---------
        language : str
            The ISO 639-1 code of the language, like \"en\" or \"jp\"
        
        reigon : str
            The reigon or subclass of the language, like \"CA\" or \"KANJI\"
        """
        # Find the locale directory
        locale_directory = find_directory(__file__, "locale")

        # Get the path to our file by combinding
        path = f"{locale_directory}/texts_{language}-{reigon}.json"

        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        fp.close()

        self.locale_texts = data
        self.locale_file_path = path

    def get_locale_path(self):
        """
        Returns the full path to the locale JSON file
        
        ...
        
        Returns
        -------
        str
            The full path to the currently loaded locale JSON file
        """
        return self.locale_file_path

    def get_locale_texts(self) -> dict:
        """
        Returns the full contents of the currently loaded locale JSON file
        
        ...
        
        Returns
        -------
        dict
            The full contents of the locale JSON file
        """
        return self.locale_texts

    def get_message(self, message: str, replacements: list):
        """
        Returns a message from the currently loaded locale
        
        Arguments
        ---------
        message : str
            The JSON path of the message seperated by dots
            
        replacements : list
            A list of values to replace the %-style placeholders with
            
        Returns
        -------
        str
            The requested message
        """
        try:
            # Try and retrieve the message in the cache, this causes a KeyError if it's
            # not in the cache and can be handled to retrieve the message from the filesystem
            text = localeCache[message] % (*replacements,)
            return text

        except KeyError:
            texts = self.get_locale_texts(self)
            text = load_json_path(texts, message)

            localeCache[message] = text

            text = text % (*replacements,)
            return text

def print_locale(msg: str, mod: str, func: str, replacements: list,
                 errorlevel=1, identation_level=0):
    """
    Wrapper over pixel_print() that prints a message from the locale
    """
    msg = LocaleManager.get_message(LocaleManager, msg, replacements)
    pixel_print(f"{' '*identation_level}{msg}", mod, func, errorlevel)

def extract_bit(x: int, bit: int) -> int:
    return (x >> bit) & 1

def get_execution_time() -> float:
    """
    Returns how long the program has been running for

    ...

    Returns
    -------
    float
        A float representing how many seconds the program has been running for
    """
    now = perf_counter() - PROGRAM_EXECUTIONTIME_START
    return now

def pretty_float(f: float, length=24) -> str:
    """
    Makes a float look a little nicer,
    only meant for terminal output, not operations

    ...

    Arguments
    ---------
    f : float
        The float to preform the operation on

    length : int
        The maximum length to fill with the placeholder character
        Default: 24

    Returns
    -------
    str
        The given float, but nicer
    """
    return str(f).rjust(length, "0")

def pixel_print(msg: str, mod="Undefined", function="Undefined", errorlevel=1) -> None:
    """
    Function for logging out to the terminal and to a file

    Arguments
    ---------
    msg : str
        The message to print
    
    mod : str
        The name of the module that is printing this message
    
    function : str
        The name of the function that is printing this message

    errorlevel : int
        The level of error that this message is (will soon move to str)
        Default: 1
    """
    try:
        #if errorlevel == 1:
        #    return # We don't care about debug info if this is a release mode
        formatted_msg = f"[{pretty_float(get_execution_time(),22):>22}] [{function:>17}@{mod:<17}] {ERRRORLEVEL_TABLE[errorlevel]:<6}    {msg}"
        format(formatted_msg)
        LOGFILE.write(f"{formatted_msg}\n")
        print(formatted_msg)
    except IOError as e:
        print(f"[{get_execution_time():>22}] {ERRRORLEVEL_TABLE[2]: <8} Error writing to logfile: {e}")

def get_high_nibble(x: int) -> int:
    """
    Returns the high nibble of an 8-bit byte
    
    ...
    
    Arguments
    ---------
    x : int
        The byte to preform the operation on
        
    Returns
    -------
    int
        The high 4-bit nibble of the given byte `x`
    """
    return x >> 4

def get_low_nibble(x: int) -> int:
    """
    Returns the low nibble of an 8-bit byte
    
    ...
    
    Arguments
    ---------
    x : int
        The byte to preform the operation on
        
    Returns
    -------
    int
        The low 4-bit nibble of the given byte `x`
    """
    return x & 0b1111

def is_multiple_of_2(n: int) -> bool:
    """
    Checks if a varible is a multiple of 2
    
    Arguments
    ---------
    n : int
        The (whole) number to check
        
    Returns
    -------
    bool
        A boolean representing if it is a multiple of 2
        Returns True if it is a multiple of 2, otherwise returns false
    """
    return (n & 1) == 0

def combine_integers(high: int, low: int):
    # Determine bit length required for high and low
    high_bits = high.bit_length()
    low_bits = low.bit_length()

    # Shift high part by the number of bits in the low part
    combined = (high << low_bits) | low
    return combined

def split_integers(combined, high_bits, low_bits):
    # Extract the high part by shifting right and masking
    high = (combined >> low_bits) & ((1 << high_bits) - 1)
    
    # Extract the low part by masking
    low = combined & ((1 << low_bits) - 1)