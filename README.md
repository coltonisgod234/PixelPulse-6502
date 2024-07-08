# PixelPulse 6502
The PixelPulse 6502 Fantasy Computer is a fantasy computer inspired by the likes of the Apple ][e and the [Pico-8](https://www.lexaloffle.com/pico-8.php)

## License Info
This Is Licesnsed Under The [GNU GPL 3.0](https://github.com/coltonisgod234/PixelPulse-6502/blob/main/LICENSE)

## What is it?
This is a [Fantasy Computer](https://en.wikipedia.org/wiki/Fantasy_video_game_console) (or fantasy video game console) designed for the development of retro games.

## Well... What Does it Do?
It Has a 65c02 microprocessor, 32KB of RAM, A 64x64 display with 4 bits per pixel and a versitile audio chip capible of producing 4 square waves, 4 triangle waves, 4 sin waves and 4 sawtooth waves!

# How Should I Get Started With PixelPulse 6502?
Getting started is easy! Simply:
1. Download the development kit, this contains an assembler, an emulator and a linker! (Not Done Yet, It'll Be Done Really Soon I Promise!)
2. Download the PulseOS ROM Image (not available yet), (this part is not finished, come back later!)
3. Check out [the wiki!](https://github.com/coltonisgod234/PixelPulse-6502/wiki/)
4. Start making games!

## How Do I Know Where To Start?
Starting is hard, we all struggle with it. So I reccomend before trying anything to make a simple hello world program that just prints "HELLO WORLD" to the top left of the screen.

# Installing The SDK
## Windows
First you need the cc65 toolchain, I reccomend installing scoop, open your start menu, search for "powershell" and press enter, then run:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```
Then run `scoop install cc65`
Now if you don't have python on your system you can install it from scoop with `scoop install python`, if you don't then make sure it is up to date and on version 3.10 or higher (I haven't tested with anything older)
Now in the root directory of the project run `pip install -r requirements.txt` (it might be `requirements.in` sometimes, see [pip-compile](https://pip-tools.readthedocs.io/en/latest/cli/pip-compile/))

The SDK is now installed

## Linux
You need the cc65 toolchain, install it from your native package manager.
If you have python ensure it's on version 3.10 or higher, if not install it from your package manager and ensure it's on version 3.10 or higher
In the root directory of the project run `pip install -r requirements.txt` sometimes it'll be `requirements.in`, in that case see [pip-compile](https://pip-tools.readthedocs.io/en/latest/cli/pip-compile/)

The SDK is now installed

## MacOS
Sorry, MacOS isn't supported (offically) and probably won't ever as I don't own a Mac, please use a Linux or Windows system.

## I Made A Game, How Do I Share It?
Sharing Games Is Easy, Just Go Over To The [Discussion](https://github.com/coltonisgod234/PixelPulse-6502/discussions/1) And Post Your Game's ROM In The Issues Tab!
