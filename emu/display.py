import tkinter as tk

class PixelPulseDisplay:
    def __init__(self):
        self.ready = False

        print("PixelPulse 6502: Display Is Initalizing")
        self.root = tk.Tk()
        self.root.title("PixelPulse 6502 - Debug Mode")

        self.canvas = tk.Canvas(self.root, width=140, height=260)
        self.canvas.pack()
        print("*** YOU ARE IN DEBUG MODE ***")
        self.ready = True
    
    def write_pixel(self,x,y,color):
        self.canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline=color)