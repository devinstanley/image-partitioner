import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2

LARGEFONT =("Verdana", 35)

# Input Page and Home Page
class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        # Header Label
        label = ttk.Label(self, text ="Upload Image", font = LARGEFONT)
        label.grid(row = 0, column = 0, padx = 10, pady = 10)
  
        # Upload Image
        button1 = ttk.Button(self, text ="Select File",
            command = lambda : self.read_input(controller))
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)

    # Reads Input and Passes Information to Image Display Page
    def read_input(self, controller):
        # Read Image
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        # Change Page If Image Read Successfully
        if 'img' in locals():
            controller.pass_image(1, img)
            controller.pass_image(2, img)
            controller.show_frame(1)