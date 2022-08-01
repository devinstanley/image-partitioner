import tkinter as tk

from image_input import InputPage
from image_display import DispImage
from rgb_channels import RGBChannels

from image_functions import *

LARGEFONT = ("Verdana", 35)

# Page Dictionary
page_dic = {
    0: InputPage,
    1: DispImage,
    2: RGBChannels
}

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
         
        # Frame Container
        container = tk.Frame(self, bg="gray") 
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # Create Frames Dict
        self.frames = {} 
  
        # Fill Frames Array with Initialized Pages
        for F in (InputPage, DispImage, RGBChannels):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        # Display Home Page
        self.show_frame(0)
  
    # Display Frame of ID Passed
    def show_frame(self, id):
        cont = page_dic[id]
        frame = self.frames[cont]
        frame.tkraise()

    # Pass Image Data to Page Frame Class
    def pass_image(self, id, img):
        cont = page_dic[id]
        frame = self.frames[cont]
        frame.set_img(img)

# Driver Code
app = tkinterApp()
app.mainloop()