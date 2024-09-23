# PixelPulse 6502
The PixelPulse 6502 Fantasy Computer is a fantasy computer inspired by the likes of the Apple ][e and the [Pico-8](https://www.lexaloffle.com/pico-8.php)

## What is it?
This is a [Fantasy Computer](https://en.wikipedia.org/wiki/Fantasy_video_game_console) (or fantasy video game console) designed for the development of retro games.

## Well... What Does it Do?
It Has a 65c02 microprocessor, 32KB of RAM, A 64x64 display with 4 bits per pixel and a versitile audio chip capible of producing 4 square waves, 4 triangle waves, 4 sin waves and 4 sawtooth waves!

# Installing The SDK

## Windows
First, install [Scoop](https://scoop.sh/), then open your start menu, search for "powershell" and press enter, then run:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser           
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```
Then install cc65:
```
scoop install cc65
```
If you don't have Python, install it with:
```
scoop install python
```
Ensure Python is version 3.10 or higher.

## Linux
Install the cc65 toolchain from your native package manager.
Ensure Python is installed and on version 3.10 or higher.

## MacOS
Sorry, MacOS isn't supported (offically) and probably won't ever as I don't own a Mac, please use a Linux or Windows system.

# Setting Up the Environment

## Creating a Virtual Environment
```
cd emu
python3 -m venv .venv
```
Activate the virtual environment:
- Windows: .venv/Scripts/activate
- macOS/Linux: source .venv/bin/activate
Install pip-tools:
```
pip install pip-tools
```
Generate requirements.txt if needed:
```
pip-compile ../requirements.in
```
Install project dependencies:
- Windows: ./.venv/Scripts/python.exe -m pip install -r ../requirements.txt
- Linux/macOS: ./.venv/bin/python -m pip install -r ../requirements.txt

# Compiling and Running

Run while in .\asm directory:
```
.\compile.ps1
```
Running The Emulator:
```
python main.py ../asm/out.bin
```

# Getting Started
1. Download the development kit (coming soon)
2. Download the PulseOS ROM Image (not available yet)
3. Check out [the wiki!](https://github.com/coltonisgod234/PixelPulse-6502/wiki/)
4. Start making games!

## How Do I Know Where To Start?
Start with a simple "HELLO WORLD" program that prints to the top left of the screen.

# Sharing Your Game
Post your game's ROM in the [Discussion](https://github.com/coltonisgod234/PixelPulse-6502/discussions/1) tab!

## License Info
This Is Licesnsed Under The [GNU GPL 3.0](https://github.com/coltonisgod234/PixelPulse-6502/blob/main/LICENSE)