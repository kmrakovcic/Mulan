import tools
import tkinter as Tk
from itertools import count
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('fivethirtyeight')
# values for first graph
x_vals = []
y_vals = []
# values for second graph
y_vals2 = []
ser = tools.interface.open_serial_port()

index = count()
index2 = count()
global counts
counts = np.zeros(10)

def animate(i):
    # Generate values
    # Get all axes of figure
    global counts
    bins = np.linspace(0, 20000, 11)
    data = tools.interface.read_serial_port(ser) * 0.001
    hist, bins = np.histogram(data, bins=bins)
    counts = counts + hist
    ax1, ax2 = plt.gcf().get_axes()
    # Clear current data
    ax1.cla()
    ax2.cla()
    # Plot new data
    ax1.bar(bins[:-1], counts, width=1000)
    ax2.bar(bins[:-1], counts, width=1000)


# GUI
root = Tk.Tk()
label = Tk.Label(root, text="Realtime Animated Graphs").grid(column=0, row=0)

# graph 1
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().grid(column=0, row=1)
# Create two subplots in row 1 and column 1, 2
plt.gcf().subplots(1, 2)
ani = FuncAnimation(plt.gcf(), animate, interval=1000, blit=False, cache_frame_data=False)

Tk.mainloop()





##################################################################################################################33
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as pltlib
import Tkinter
from Tkinter import *
import numpy as np
import scipy as sc
#import matplotlib.pyplot as pltlib
# lmfit is imported becuase parameters are allowed to depend on each other along with bounds, etc.
from lmfit import minimize, Parameters, Minimizer



#Make object for application
class App_Window(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):
        button = Tkinter.Button(self,text="Open File",command=self.OnButtonClick).pack(side=Tkinter.TOP)
        self.canvasFig=pltlib.figure(1)
        Fig = matplotlib.figure.Figure(figsize=(5,4),dpi=100)
        FigSubPlot = Fig.add_subplot(111)
        x=[]
        y=[]
        self.line1, = FigSubPlot.plot(x,y,'r-')
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(Fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.resizable(True,False)
        self.update()
    def refreshFigure(self,x,y):
        self.line1.set_xdata(x)
        self.line1.set_ydata(y)
        self.canvas.draw()
    def OnButtonClick(self):
        # file is opened here and some data is taken
        # I've just set some arrays here so it will compile alone
        x=[]
        y=[]
        for num in range(0,1000):x.append(num*.001+1)
        # just some random function is given here, the real data is a UV-Vis spectrum
        for num2 in range(0,1000):y.append(sc.math.sin(num2*.06)+sc.math.e**(num2*.001))
        X = np.array(x)
        Y = np.array(y)
        self.refreshFigure(X,Y)

if __name__ == "__main__":
    MainWindow = App_Window(None)
    MainWindow.mainloop()