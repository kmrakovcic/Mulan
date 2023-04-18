from tkinter import *
from random import randint

# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading
import numpy as np
import pandas as pd
import analyze
import tools.interface
import os
import multiprocessing

continuePlotting = False
shared_list = []
raw_data = []

def counter():
    global shared_list
    global continuePlotting
    ser = tools.interface.open_serial_port()
    while continuePlotting:
        data = tools.interface.read_serial_port(ser)
        shared_list += data.tolist()


def writer(filename="data.csv", lower_cutoff=0.75, higher_cutoff=9):
    global shared_list
    global continuePlotting
    global raw_data
    event_counter = 0
    mion_counter = 0
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass
    with open(filename, 'a') as f:
        while continuePlotting:
            time.sleep(1)
            raw_data += shared_list
            for i in shared_list:
                event_counter += 1
                if (i < higher_cutoff) and (i > lower_cutoff):
                    mion_counter += 1
                f.write(str(i) + '\n')
            print("\r counts:"+str(event_counter*2)+" mion:"+str(mion_counter), end="")
            shared_list[:] = []

def change_state(path="data.csv"):
    global continuePlotting
    global raw_data
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True
        if os.path.exists(path):
            raw_data = read_data(path)


def read_data(filename="data.csv"):
    data = np.array(pd.read_csv(filename)).reshape(-1)
    #data = np.random.exponential(1, 1000)
    return list(data)


def app(filename="data.csv"):
    #lower_cutoff = 0.75
    lower_cutoff = 0.25
    higher_cutoff = 7
    # initialise a window.
    root = Tk()
    root.config(background='white')
    root.geometry("1000x700")

    lab = Label(root, text="Live Plotting", bg='white').pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel(r"t[$\mu s$]")
    ax.set_ylabel("counts")
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            ax.set_xlabel(r"t[$\mu s$]")
            ax.set_ylabel("counts")
            raw_data_tmp = np.array(raw_data).copy()
            data = raw_data_tmp[np.logical_and(raw_data_tmp < higher_cutoff, raw_data_tmp > lower_cutoff)]
            if data.size > 0:
                counts, bins, x_fit, y_fit, w, tau, w_err, tau_err = analyze.fit_and_calculate_histogram(data, 100, lower_cutoff=lower_cutoff, higher_cutoff=higher_cutoff)
                y_fit = y_fit * (bins[1] - bins[0]) * x_fit.size
                #counts = (counts / x_fit.size) / (bins[1] - bins[0])
                ax.bar(bins[:-1] + (bins[1] - bins[0]) / 2, counts, width=bins[1] - bins[0])
                ax.plot(x_fit, y_fit, color="r")
            else:
                ax.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center')
            graph.draw()
            time.sleep(1)

    def gui_handler():
        change_state(filename)
        threading.Thread(target=counter).start()
        threading.Thread(target=writer, args=(filename, lower_cutoff, higher_cutoff)).start()
        threading.Thread(target=plotter).start()

    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop()



if __name__ == '__main__':
    app()

