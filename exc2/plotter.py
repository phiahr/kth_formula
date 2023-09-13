import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axis import Axis
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import tkinter as tk
import time
import threading

def test():
    print('test')
class Plotter:

    def __init__(self
                #  , axes=["h(t)", "t"], t=10
                 ):
        self.running = False
        
        self.root = tk.Tk(className="KTH Formula")

        fig = Figure(figsize=(5, 4), dpi=100)
        self.t = [0]

        self.ax = fig.add_subplot()

        
        self.ax.set_xlabel("time [s]")
        self.ax.set_ylabel("f(t)")

        self.x_left, self.x_right = self.ax.get_xlim()
        self.y_left, self.y_right = self.ax.get_ylim()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        toolbar.update()

        button_frame = tk.Frame(self.root)

        quit_button = tk.Button(master=button_frame, text="Quit", command=self.root.destroy)
        reset_button = tk.Button(master=button_frame, text="Reset", command=self.reset)
        start_button = tk.Button(button_frame, text="Start", command=self.start)
        stop_button = tk.Button(button_frame, text="Stop", command=self.stop)

        x_slider = tk.Scale(self.root, from_=-9, to=10, orient=tk.HORIZONTAL,
                              command=self.x_zoom, label="Zoom x-axis")
        y_slider = tk.Scale(self.root, from_=-9, to=10, orient=tk.VERTICAL,
                                    command=self.y_zoom, label="Zoom y-axis")
        


        button_frame.pack(side=tk.BOTTOM)
        quit_button.pack(side=tk.RIGHT)
        reset_button.pack(side=tk.RIGHT)
        start_button.pack(side=tk.LEFT)
        stop_button.pack(side=tk.LEFT)

        slider_frame = tk.Frame(self.root)
        slider_frame.pack(side=tk.BOTTOM)


        x_slider.pack(side=tk.RIGHT)
        y_slider.pack(side=tk.RIGHT)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def run(self):
        self.root.mainloop()


    def update_plot(self):
        if self.running:
            t = time.time() - self.start_time
            print(t)
            self.t = np.append(self.t, t)
            print(self.t)
            data = self.calculate_function(self.t)
            self.ax.clear()
            self.ax.plot(self.t, data)
            self.ax.set_xlabel('t')
            self.ax.set_ylabel('h(t)')
            self.ax.set_title('Function Visualization')
            self.ax.grid(True)
            self.canvas.draw()
            self.root.after(100, self.update_plot)

    def calculate_function(self, t):
        lambda_t = 5 * np.sin(2 * np.pi * 1 * t)
        return 3 * np.pi * np.exp(-lambda_t)

    def start(self):
        self.start_time = time.time() - self.t[-1]

        self.running = True
        threading.Thread(target=self.update_plot).start()

    def stop(self):
        self.x_left, self.x_right = self.ax.get_xlim()
        self.y_left, self.y_right = self.ax.get_ylim()
        self.running = False

    def reset(self):
        self.ax.clear()
        self.canvas.draw()
        self.start_time = time.time() - self.t[-1]

        self.t = [0]

    def x_zoom(self, val):
        pos = int(val)
        if pos < 0:
            pos = 1+(pos/10)-0.1
    
        self.ax.set_xlim(self.x_left/pos, self.x_right/pos)
        
        self.canvas.draw()

    def y_zoom(self, val):
        pos = int(val)
        if pos < 0:
            pos = 1+(pos/10)-0.1
        
        self.ax.set_ylim(self.y_left/pos, self.y_right/pos)
        
        self.canvas.draw()


plotter = Plotter()

plotter.run()
