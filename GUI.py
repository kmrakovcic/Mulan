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
