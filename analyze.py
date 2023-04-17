import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt


def neg_log_likelihood(x, lower_cutoff=0.75, higher_cutoff=9):
    def function(parm):
        w = parm[0]
        tau = parm[1]
        y = w * 1/tau * 1/(np.exp(-lower_cutoff/tau)-np.exp(-higher_cutoff/tau)) * np.exp(-x/tau) + (1-w) * 1/(higher_cutoff-lower_cutoff)
        return -np.sum(np.log(y))
    return function


def exp_function(x, w, tau, lower_cutoff, higher_cutoff):
    y = w * 1/tau * 1/(np.exp(-lower_cutoff/tau)-np.exp(-higher_cutoff/tau)) * np.exp(-x/tau) + (1-w) * 1/(higher_cutoff-lower_cutoff)
    return y


def maximum_likelihood_estimate(data, lower_cutoff, higher_cutoff):
    popt = scipy.optimize.minimize(neg_log_likelihood(data, lower_cutoff, higher_cutoff), [0.2, 2.2], bounds=[(0, 1), (1, 3)])
    hessinv_matrix = np.asmatrix(popt.hess_inv.todense())
    values = popt.x
    errors = np.sqrt(np.diagonal(hessinv_matrix))
    return values, errors


def fit_and_calculate_histogram(data, n_bins, lower_cutoff=0.75, higher_cutoff=9):
    data = data[np.logical_and(data < higher_cutoff, data > lower_cutoff)]
    [w, tau], [w_err, tau_err] = maximum_likelihood_estimate(data, lower_cutoff, higher_cutoff)
    counts, bins = np.histogram(data, bins=n_bins)
    data.sort()
    x_fit = data
    y_fit = exp_function(data, w, tau, lower_cutoff, higher_cutoff)
    return counts, bins, x_fit, y_fit, w, tau, w_err, tau_err


def update_histogram(ax, counts, bins, x_fit=None, y_fit=None):
    ax.clear()
    if x_fit is not None:
        counts = (counts / x_fit.size) / (bins[1] - bins[0])
    ax.bar(bins[:-1] + (bins[1] - bins[0]) / 2, counts, width=bins[1] - bins[0])
    if x_fit is not None and y_fit is not None:
        ax.plot(x_fit, y_fit, color="r")
    return ax


if __name__ == '__main__':
    #data = np.random.exponential(2, 1000)
    data = np.array(pd.read_csv('test_data.csv'))
    counts, bins, x_fit, y_fit, w, tau, w_err, tau_err = fit_and_calculate_histogram(data, 100)
    fig, ax = plt.subplots(2, 1)
    ax[0] = update_histogram(ax[0], counts, bins, x_fit, y_fit)
    plt.show()
