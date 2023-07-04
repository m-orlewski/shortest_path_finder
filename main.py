import tkinter as tk     
from tkinter import ttk

from tkinter import font as tkfont 

import matplotlib 
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import cv2 

import sys
import os

import functools

import drawer
import random
from skimage import morphology
from skan import csr
from pathfinder import find_and_draw_path
from width_finder import get_path_width

LARGE_FONT = ("Verdana", 12)

class Mapper(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        tk.Tk.wm_title(self, "Map and path generator")
        self.geometry("1400x1000")
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in ( PageMenu, PageFindPath, PageGenerateImage):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageMenu)

    def show_frame(self, page):
        '''Show a frame for the given page name'''
        frame = self.frames[page]
        frame.tkraise()

class PageMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.contoller = controller
        label = ttk.Label(self, text="Menu", font=LARGE_FONT)
        label.pack(side="top", pady=10, padx=10)

        button1 = ttk.Button(self, text="Find Path On Image", command=lambda: controller.show_frame(PageFindPath))
        button1.pack(side="top",fill='both',expand=True)

        button2 = ttk.Button(self, text="Generate Image", command=lambda: controller.show_frame(PageGenerateImage))
        button2.pack(side="top",fill='both',expand=True)

class PageFindPath(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.contoller = controller

        self.f = Figure(figsize=(4,4), dpi=100)
        self.ax = self.f.add_subplot(111)

        self.f2, self.axis = plt.subplots(1, 4, figsize=(4,4), dpi=100)

        self.start = 0
        self.destination = 1

        button1 = ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(PageMenu))
        button1.pack(side="top", fill="both",expand=True)

        button2 = ttk.Button(self, text="Load Image", command= self.load_image)
        button2.pack(side="top", fill="both",expand=True)
    
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(side="top", fill="y",expand=True)
        self.ax.plot()
        self.ax.set_title(f"Image")

        button3 = ttk.Button(self, text="Set start point", command= self.set_start)
        button3.pack(side="top", fill="both",expand=True)

        button4 = ttk.Button(self, text="Set destination point", command= self.set_destination)
        button4.pack(side="top", fill="both",expand=True)

        button5 = ttk.Button(self, text="Find path", command= self.find_path)
        button5.pack(side="top", fill="both",expand=True)

        self.canvas2 = FigureCanvasTkAgg(self.f2, self)
        self.canvas2.get_tk_widget().pack(side="top", fill="both",expand=True)
        for i, _ in enumerate(self.axis):
            self.axis[i].plot()


    def load_image(self):
        path = tk.filedialog.askopenfilename()
        self.image = cv2.imread(path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.binary = cv2.threshold(self.image, 175, 255, cv2.THRESH_BINARY)
        self.skeletonized = morphology.skeletonize(self.binary)
        self.skeleton = csr.Skeleton(self.skeletonized)
        self.ax.clear()
        self.ax.imshow(self.image)
        self.ax.set_title(f"Image")
        self.canvas.draw()

        self.axis[0].clear()
        self.axis[0].imshow(self.gray, cmap='gray')
        self.axis[0].set_title("Gray")

        self.axis[1].clear()
        self.axis[1].imshow(self.binary, cmap='gray')
        self.axis[1].set_title("Binary")

        self.axis[2].clear()
        self.axis[2].imshow(self.skeletonized, cmap='gray')
        self.axis[2].set_title("Skeletonized")

        self.axis[3].clear()
        self.axis[3].imshow(self.skeletonized, cmap='gray')
        self.axis[3].set_title("Nodes numbers")
        self.canvas2.draw()

    def set_start(self):
        self.start = tk.simpledialog.askinteger("New start point", "Enter number associated with start point:")

    def set_destination(self):
        self.destination = tk.simpledialog.askinteger("New destination point", "Enter number associated with destination point:")

    def find_path(self):
        nodes = {} # key: node number, value: (x_coord, y_coord)
        edges = [] # (x, y, w) - nodes connected + weight
        c = 0
        for i in range(self.skeleton.n_paths):
            path_coordinates = self.skeleton.path_coordinates(i)
            x1, y1 = path_coordinates[0][1], path_coordinates[0][0]
            x2, y2 = path_coordinates[-1][1], path_coordinates[-1][0]

            if (x1, y1) not in nodes.values():
                nodes[c] = (x1, y1)
                c += 1

            if (x2, y2) not in nodes.values():
                nodes[c] = (x2, y2)
                c += 1

            key_list = list(nodes.keys())
            val_list = list(nodes.values())

            pos1 = val_list.index((x1, y1))
            pos2 = val_list.index((x2, y2))
            
            edge_weight = len(path_coordinates) / get_path_width(self.binary, path_coordinates)
            edges.append((pos1, pos2, edge_weight))

        find_and_draw_path(nodes, edges, self.skeleton, self.ax, 0, 37, 'test')
        self.canvas.draw()

class PageGenerateImage(tk.Frame):
    resolution = 50
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.contoller = controller

        self.f = Figure(figsize=(5,5), dpi=100)
        self.ax = self.f.add_subplot(111)

        self.seed = 123
        button1 = ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(PageMenu))
        button1.pack(side="top", fill="both",expand=True)

        button2 = ttk.Button(self, text="Set Seed", command= self.set_seed)
        button2.pack(side="top", fill="both",expand=True)
    
        button3 = ttk.Button(self, text="Generate", command= self.generate)
        button3.pack(side="top", fill="both",expand=True)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(side="top", fill="y",expand=True)
        self.ax.plot()
        self.ax.set_title(f"Seed: {self.seed}")

        button4 = ttk.Button(self, text="Save", command= self.saveToFile)
        button4.pack(side="top", fill="both",expand=True)


    def set_seed(self):
        seed = tk.simpledialog.askinteger("New Seed", "Enter new seed:")
        self.seed = seed
        global SEED
        SEED = self.seed
        random.seed(self.seed)
        return 
    
    def generate(self):
        self.img = drawer.create_single_image()
        self.ax.clear()
        self.ax.imshow(self.img)
        self.ax.set_title(f"Seed: {self.seed}")
        self.ax.plot()
        self.canvas.draw()
        return
        
    def saveToFile(self):
        image_path = tk.filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("png files", '*.png')],
                initialdir="image_database",)
        cv2.imwrite(f'{image_path }.png', self.img)
        return 

app = Mapper()
app.mainloop()