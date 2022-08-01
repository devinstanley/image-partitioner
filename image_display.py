import tkinter as tk
from tkinter import ttk
from skimage.measure import shannon_entropy
from PIL import Image, ImageTk
from image_functions import *

LARGEFONT = 'verdana 35'
LABELFONT = 'Verdana 10 bold'

# Image Display Class
class DispImage(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Image Partitioner", font = LARGEFONT)
        label.grid(row = 0, column = 0, columnspan=3, padx = 10, pady = 10)
  
        # Select New Image
        button1 = ttk.Button(self, text ="Select New Image",
            command = lambda : controller.show_frame(0))
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)
  
        # Reset Image
        button2 = ttk.Button(self, text ="Reset Image",
            command = lambda : self.set_img(self.img))
        button2.grid(row = 1, column = 1, padx = 10, pady = 10)

        # Show RGB Channels
        button2 = ttk.Button(self, text ="Show Channels",
            command = lambda : controller.show_frame(2))
        button2.grid(row = 1, column = 2, padx = 10, pady = 10)


    # Setter to Receive Information from Input Page
    def set_img(self, img):
        self.img = img
        self.split_iter = 0
        self.orig_ent = shannon_entropy(img)
        self.ent_thresh = self.orig_ent*(.75) # Set Default Threshold
        self.photo_img = arr2im(self.img, (800, 800))
        self.show_image()

    # Create Button From Image and Display
    def show_image(self):
        im_b = ttk.Button(self, image=self.photo_img, command=lambda: self.split_image(self))
        im_b.grid(row=3,column=0, columnspan=3, rowspan=120)

        direc = tk.Label(self, text="Click Image to Partition One Step")
        direc.grid(row=2, column = 0, columnspan=3)

        # Show Base Entropy Information
        l0 = tk.Label(self, text="Original Image Entropy", font=LABELFONT)
        l0.grid(row=3, column=4)
        e0 = tk.Label(self, text=self.orig_ent)
        e0.grid(row=4, column=4)

        # Show Number of Iterations
        i0 = tk.Label(self, text="# of Partition Iterations", font=LABELFONT)
        i0.grid(row=5, column=4)
        i1 = tk.Label(self, text=self.split_iter)
        i1.grid(row=6, column=4)


    # Calculates and Displays Measures of Entropy for Image
    def show_image_information(self, window):
        # Entropy Labels
        l1 = tk.Label(window, text="Average Partition Entropy", font=LABELFONT)
        l1.grid(row=7, column=4)
        l2 = tk.Label(window, text="Maximum Partition Entropy", font=LABELFONT)
        l2.grid(row=9, column=4)
        l3 = tk.Label(window, text="Minimum Partition Entropy", font=LABELFONT)
        l3.grid(row=11, column=4)


        # Calculate Entropy
        self.ave_ent = np.average(get_entropy(self.parent))
        e1 = tk.Label(window, text=self.ave_ent)
        e1.grid(row=8, column=4)

        self.max_ent = max(get_entropy(self.parent))
        e2 = tk.Label(window, text=self.max_ent)
        e2.grid(row=10, column=4)

        self.min_ent = min(get_entropy(self.parent))
        e3 = tk.Label(window, text = self.min_ent)
        e3.grid(row=12, column=4)


    # Splits and Reconstructs Image
    def split_image(self, window):
        self.split_iter += 1

        if self.split_iter == 1:
            self.parent = split(Node(self.img))
            reconstructed = reconstructor(self.parent)
        else:
            self.parent = deconstructor(self.parent, self.ent_thresh)
            reconstructed = reconstructor(self.parent)

        self.photo_img = arr2im(reconstructed, (800, 800))

        self.show_image()

        self.show_image_information(window)