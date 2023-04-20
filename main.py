from tkinter import *
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
import scipy


continueLive = False
continueFFwd = False
count_ffwd = 1

continueCollecting = False

shared_list = []
raw_data = []
data = []
time_distribution = {"tau": [], "tau_err": [], "w": [], "w_err": []}


def counter():
    global shared_list
    ser = tools.interface.open_serial_port()
    print("Starting to collect data...")
    while continueCollecting:
        data = tools.interface.read_serial_port(ser)
        shared_list += data.tolist()
    print("Stopped collecting data")


def writer(filename="data.csv"):
    global shared_list
    global raw_data

    print("Starting to write data...")
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass
    with open(filename, 'a') as f:
        while continueCollecting:
            time.sleep(1)
            if continueFFwd or continueLive:
                raw_data += shared_list
            if continueCollecting:
                for i in shared_list:
                    f.write(str(i) + '\n')
            shared_list[:] = []
    print("Stopped writing data")


def exit():
    global continueLive
    global continueFFwd
    global continueCollecting
    continueLive = False
    continueFFwd = False
    continueCollecting = False


def get_normal_distribution(mu, sigma, start=None, end=None):
    if start is None:
        start = mu - 3 * sigma
    if end is None:
        end = mu + 3 * sigma
    x = np.linspace(start, end, 100)
    x = np.append(x, [mu - sigma, mu, mu + sigma])
    x.sort()
    y = scipy.stats.norm.pdf(x, loc=mu, scale=sigma)
    return x, y


def create_tau_N_distribution(data, lower_cutoff, higher_cutoff):
    global time_distribution
    time_distribution = {"tau": [], "tau_err": [], "w": [], "w_err": [], "n": []}
    for n in range(len(data)):
        [w, tau], [w_err, tau_err] = analyze.maximum_likelihood_estimate(data[:n], lower_cutoff, higher_cutoff)
        time_distribution["tau"].append(tau)
        time_distribution["tau_err"].append(tau_err)
        time_distribution["w"].append(w)
        time_distribution["w_err"].append(w_err)
        time_distribution["n"].append(n)
    return time_distribution


def read_data(filename="data.csv"):
    data = np.array(pd.read_csv(filename)).reshape(-1)
    # data = np.random.exponential(1, 1000)
    return list(data)


def app(filename="data.csv"):
    global count_ffwd
    lower_cutoff = 0.25
    higher_cutoff = 7
    n_bins = 100

    def plotter():
        global count_ffwd
        global data
        print("Starting to plot data...")
        lower_cutoff = 0.25
        higher_cutoff = 7
        recalculate_time_distribution = True
        time_distribution = {"tau": [], "tau_err": [], "w": [], "w_err": [], "n": []}
        while continueLive or continueFFwd:
            if lower_cutoff != slider_lower_bounds.get() or higher_cutoff != slider_higher_bounds.get():
                lower_cutoff = slider_lower_bounds.get()
                higher_cutoff = slider_higher_bounds.get()
                recalculate_time_distribution = True
            n_bins = slider_n_bins.get()
            if continueLive:
                live_label.config(text="LIVE MODE")
            elif continueFFwd:
                live_label.config(text="FAST FORWARD MODE")
            elif continueCollecting:
                live_label.config(text="COLLECTING DATA MODE")
            else:
                live_label.config(text="Idle")
            ax.cla()
            ax.grid()
            ax.set_xlabel(r"t[$\mu s$]")
            ax.set_ylabel("Number of decays")
            ax.title.set_text("Decay time histogram")

            ax1.cla()
            ax1.set_xlabel(r"$\tau$")
            ax1.set_yticks([0, 1])
            ax1.set_ylim(bottom=0, top=1.1)
            ax1.title.set_text("Muon lifetime estimation")

            ax2.cla()
            ax2.set_xlabel(r"w")
            ax2.set_yticks([0, 1, 2])
            ax2.set_ylim(bottom=0, top=1.1)
            ax2.title.set_text("Signal ratio estimation")

            ax3.cla()
            ax3.set_xlabel(r"n")
            ax3.set_ylabel(r"$\tau$")

            raw_data_tmp = np.array(raw_data).copy()
            if continueFFwd:
                where_mions = np.argwhere(np.logical_and(raw_data_tmp < higher_cutoff, raw_data_tmp > lower_cutoff)).reshape(-1)
                if where_mions.size < count_ffwd:
                    count_ffwd = 1
                    time_distribution = {"tau": [], "tau_err": [], "w": [], "w_err": [], "n": []}
                else:
                    raw_data_tmp = raw_data_tmp[:where_mions[count_ffwd]]
                    count_ffwd += np.random.randint(1, 20)
            data = raw_data_tmp[np.logical_and(raw_data_tmp < higher_cutoff, raw_data_tmp > lower_cutoff)]
            count_lab1.config(text=str(raw_data_tmp.size))
            count_lab2.config(text=str(data.size))
            if data.size > 0:
                counts, bins, x_fit, y_fit, w, tau, w_err, tau_err = analyze.fit_and_calculate_histogram(data, n_bins, lower_cutoff=lower_cutoff, higher_cutoff=higher_cutoff)
                time_distribution["tau"].append(tau)
                time_distribution["tau_err"].append(tau_err)
                time_distribution["w"].append(w)
                time_distribution["w_err"].append(w_err)
                time_distribution["n"].append(data.size)
                y_fit = y_fit * (bins[1] - bins[0]) * x_fit.size
                ax.bar(bins[:-1] + (bins[1] - bins[0]) / 2, counts, width=(bins[1] - bins[0]))
                ax.plot(x_fit, y_fit, color="r")

                x, y = get_normal_distribution(tau, tau_err, start=min(2.2-1, tau-tau_err), end=max(2.2+1, tau+tau_err))
                ax1.plot(x, y)
                ax1.set_xlabel(r"$\tau = \left("+str(round(tau, 2)) + r"\pm" + str(round(tau_err, 2)) + r"\right) \mu s$")
                ax1.fill_between(x[np.logical_and(x >= (tau-tau_err), x <= (tau+tau_err))],
                                 y[np.logical_and(x >= (tau-tau_err), x <= (tau+tau_err))], 0, alpha=.6, color='orange')
                ax1.vlines(x=tau, ymin=0, ymax=scipy.stats.norm.pdf(tau, tau, tau_err), color='r', linestyle='-', linewidth=1)
                ax1.vlines(x=tau-tau_err, ymin=0, ymax=scipy.stats.norm.pdf(tau-tau_err, tau, tau_err), color='r', linestyle='--', linewidth=1)
                ax1.vlines(x=tau+tau_err, ymin=0, ymax=scipy.stats.norm.pdf(tau+tau_err, tau, tau_err), color='r', linestyle='--', linewidth=1)
                ax1.set_ylim(bottom=0, top=1.1*y.max())
                graph.draw()

                x, y = get_normal_distribution(w, w_err, start=0, end=1.5)
                ax2.plot(x, y)
                ax2.set_xlabel(r"$w = \left(" + str(round(w, 2)) + r"\pm" + str(round(w_err, 2)) + r"\right)$")
                ax2.fill_between(x[np.logical_and(x >= (w-w_err), x <= (w+w_err))],
                                 y[np.logical_and(x >= (w-w_err), x <= (w+w_err))], 0, alpha=.6, color='orange')
                ax2.vlines(x=w, ymin=0, ymax=scipy.stats.norm.pdf(w, w, w_err), color='r', linestyle='-', linewidth=1)
                ax2.vlines(x=w-w_err, ymin=0, ymax=scipy.stats.norm.pdf(w-w_err, loc=w, scale=w_err), color='r', linestyle='--', linewidth=1)
                ax2.vlines(x=w+w_err, ymin=0, ymax=scipy.stats.norm.pdf(w+w_err, loc=w, scale=w_err), color='r', linestyle='--', linewidth=1)
                ax2.set_ylim(bottom=0, top=1.1*y.max())
                graph1.draw()
                if recalculate_time_distribution:
                    ax3.set_xlabel(r"n")
                    ax3.set_ylabel(r"$\tau$")
                    ax3.text(0.5, 0.5, "Calculating", horizontalalignment='center', verticalalignment='center')
                    graph2.draw()
                    time_distribution = create_tau_N_distribution(data, lower_cutoff, higher_cutoff)
                    recalculate_time_distribution = False
                ax3.clear()
                ax3.set_xlabel(r"n")
                ax3.set_ylabel(r"$\tau$")
                ax3.set_ylim(top=3.2, bottom=1.2)
                ax3.fill_between(time_distribution["n"],
                                 np.array(time_distribution["tau"])+np.array(time_distribution["tau_err"]),
                                 np.array(time_distribution["tau"])-np.array(time_distribution["tau_err"]), alpha=.6, color='orange')
                ax3.plot(time_distribution["n"], time_distribution["tau"], color="r", linestyle="-", linewidth=1, label=r"$\tau$")
                ax3.hlines(y=2.2, xmin=0, xmax=time_distribution["n"][-1], color='b', linestyle='--', linewidth=1, label=r"$\tau_{exp}$")
                ax3.legend()
                graph2.draw()
            else:
                ax.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center')
                ax1.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center')
                ax2.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center')
                ax3.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center')
                graph.draw()
                graph1.draw()
                graph2.draw()
            if continueFFwd:
                time.sleep(0.1)
            else:
                time.sleep(1)

        ax.cla()
        ax.grid()
        ax.set_xlabel(r"t[$\mu s$]")
        ax.set_ylabel("Number of decays")
        ax.title.set_text("Decay time histogram")
        ax.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

        ax1.cla()
        ax1.set_xlabel(r"$\tau$")
        ax1.set_yticks([0, 1])
        ax1.set_ylim(bottom=0, top=1.1)
        ax1.title.set_text("Muon lifetime estimation")
        ax1.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

        ax2.cla()
        ax2.set_xlabel(r"w")
        ax2.set_yticks([0, 1, 2])
        ax2.set_ylim(bottom=0, top=1.1)
        ax2.title.set_text("Signal ratio estimation")
        ax2.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

        ax3.cla()
        ax3.set_xlabel(r"n")
        ax3.set_ylabel(r"$\tau$")
        ax3.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

        count_lab1.config(text="Idle")
        count_lab2.config(text="Idle")

        live_label.config(text="Idle")

        graph.draw()
        graph1.draw()
        graph2.draw()
        print("Plotter stopped")

    def start_live():
        global continueFFwd
        global continueLive
        global count_ffwd
        global raw_data
        thread_plotter = threading.Thread(target=plotter)
        b_live["state"] = "disabled" if continueFFwd else "normal"
        if continueLive:
            continueLive = False
            raw_data = []
            time.sleep(1)
            b_live.config(text="Start Live", bg="green", fg="white")
            b_ffwd["state"] = "normal"
            b_exit["state"] = "normal"

        else:
            continueLive = True
            continueFFwd = False
            b_live.config(text="Stop Live", bg="red", fg="white")
            if os.path.exists(filename) and (os.path.getsize(filename) > 0):
                raw_data = read_data(filename)
            b_ffwd["state"] = "disabled"
            b_exit["state"] = "disabled"
            thread_plotter.start()

    def start_ffwd():
        global continueFFwd
        global continueLive
        global count_ffwd
        global raw_data
        thread_plotter = threading.Thread(target=plotter)
        if continueFFwd:
            continueFFwd = False
            count_ffwd = 1
            raw_data = []
            time.sleep(0.1)
            b_ffwd.config(text="Start FFwd", bg="green", fg="white")
            b_live["state"] = "normal"
            b_exit["state"] = "normal"
        else:
            continueFFwd = True
            continueLive = False
            b_ffwd.config(text="Stop FFwd", bg="red", fg="white")
            if os.path.exists(filename) and (os.path.getsize(filename) > 0):
                raw_data = read_data(filename)
            b_live["state"] = "disabled"
            b_exit["state"] = "disabled"
            thread_plotter.start()

    def start_collecting():
        global continueCollecting
        thread_counter = threading.Thread(target=counter)
        thread_writer = threading.Thread(target=writer, args=(filename,))
        if continueCollecting:
            continueCollecting = False
            b_collect.config(text="Start Collecting", bg="green", fg="white")
            b_exit["state"] = "normal"
        else:
            continueCollecting = True
            b_collect.config(text="Stop Collecting", bg="red", fg="white")
            thread_counter.start()
            thread_writer.start()
            b_exit["state"] = "disabled"

    def exit_button():
        global continueCollecting
        global continueFFwd
        global continueLive
        continueCollecting = False
        continueFFwd = False
        continueLive = False
        root.destroy()
    # initialise a window.
    root = Tk()
    root.config(background='white')
    # root.geometry("1800x800")
    root.attributes('-fullscreen', True)
    # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.geometry("%dx%d+0+0" % (w, h))
    root.title("Muon Detector")
    # create a label.
    live_label = Label(root, text="Idle", bg='white', font=("Helvetica", 16))
    live_label.pack()

    # create a canvas.
    frame_plots = Frame(root)
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(r"t[$\mu s$]")
    ax.set_ylabel("Number of decays")
    ax.grid()
    ax.title.set_text("Decay time histogram")
    ax.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

    graph = FigureCanvasTkAgg(fig, master=frame_plots)
    graph.get_tk_widget().pack(side="left", fill="both", expand=True)

    frame_plots1 = Frame(frame_plots)
    fig2 = Figure()
    ax1 = fig2.add_subplot(121)
    ax1.set_xlabel(r"$\tau$")
    ax1.set_yticks([])
    ax1.set_ylim(bottom=0, top=1.1)
    ax1.title.set_text("Muon lifetime estimation")
    ax1.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')

    ax2 = fig2.add_subplot(122)
    ax2.set_xlabel(r"w")
    ax2.set_yticks([])
    ax2.set_ylim(bottom=0, top=1.1)
    ax2.title.set_text("Signal ratio estimation")
    ax2.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')
    fig2.tight_layout()

    graph1 = FigureCanvasTkAgg(fig2, master=frame_plots1)
    graph1.get_tk_widget().pack(side="top", fill="both", expand=True)

    fig3 = Figure(figsize=(5, 2))
    ax3 = fig3.add_subplot(111)
    ax3.set_xlabel(r"n")
    ax3.set_ylabel(r"$\tau$")
    ax3.set_yticks([])
    ax3.set_ylim(bottom=0, top=1.1)
    ax3.text(0.5, 0.5, "Idle", horizontalalignment='center', verticalalignment='center')
    fig3.tight_layout()
    graph2 = FigureCanvasTkAgg(fig3, master=frame_plots1)
    graph2.get_tk_widget().pack(side="bottom", fill="both", expand=True)

    frame_plots1.pack(side="right", fill="both", expand=True)

    count_frame = Frame(root)
    count_lab1 = Label(count_frame, text="Idle", bg='white', font=20)
    muons_lab1 = Label(count_frame, text="Muons", bg='white', font=("Arial", 25))
    muons_lab1.pack(side="top", fill="both", expand=False)
    count_lab1.pack(side="top", fill="both", expand=False)

    decayed_lab1 = Label(count_frame, text="Decayed", bg='white', font=("Arial", 25))
    count_lab2 = Label(count_frame, text="Idle", bg='white', font=20)

    decayed_lab1.pack(side="top", fill="both", expand=False)
    count_lab2.pack(side="top", fill="both", expand=False)

    sliders = Frame(root)
    slider_lower_bounds = Scale(sliders, from_=0, to=2, resolution=0.01, orient=HORIZONTAL, label="Lower bound",
                                bg='white')
    slider_lower_bounds.set(lower_cutoff)
    slider_higher_bounds = Scale(sliders, from_=1, to=100, resolution=1, orient=HORIZONTAL, label="Higher bound",
                                 bg='white')
    slider_higher_bounds.set(higher_cutoff)
    slider_n_bins = Scale(sliders, from_=10, to=1000, resolution=10, orient=HORIZONTAL, label="Number of bins",
                          bg='white')
    slider_n_bins.set(n_bins)
    slider_lower_bounds.pack(side="top", fill="both", expand=False)
    slider_higher_bounds.pack(side="top", fill="both", expand=False)
    slider_n_bins.pack(side="top", fill="both", expand=False)

    b_exit = Button(count_frame, text="Exit", command=exit_button, bg="red", fg="white")
    b_exit.pack(side="bottom", fill='none', expand=False)
    b_live = Button(count_frame, text="Start Live", command=start_live, bg="green", fg="white")
    b_live.pack(side="bottom", fill='none', expand=False)
    b_ffwd = Button(count_frame, text="Start FFwd", command=start_ffwd, bg="green", fg="white")
    b_ffwd.pack(side="bottom", fill='none', expand=False)
    b_collect = Button(count_frame, text="Start collecting", command=start_collecting, bg="green", fg="white")
    b_collect.pack(side="bottom", fill='none', expand=False)

    sliders.pack(side="bottom", fill="both", expand=False)
    count_frame.pack(side="right", fill="both", expand=False)
    frame_plots.pack(side="right", fill="both", expand=True)

    root.mainloop()
    exit()


if __name__ == '__main__':
    app("data.csv")
