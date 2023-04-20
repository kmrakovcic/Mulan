import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt


def neg_log_likelihood(x, lower_cutoff=0.75, higher_cutoff=9):
    """
    Function to calculate the negative log likelihood of the data given the parameters w and tau.
    :param x:
    :param lower_cutoff:
    :param higher_cutoff:
    :return:
    """
    def function(parm):
        """
        Function to calculate the negative log likelihood of the data given the parameters w and tau.
        :param parm:
        :return:
        """
        w = parm[0]
        tau = parm[1]
        y = w * 1/tau * 1/(np.exp(-lower_cutoff/tau)-np.exp(-higher_cutoff/tau)) * np.exp(-x/tau) + (1-w) * 1/(higher_cutoff-lower_cutoff)
        if np.any(y <= 0):
            return 1e10
        else:
            return -np.sum(np.log(y))
    return function


def exp_function(x, w, tau, lower_cutoff, higher_cutoff):
    """
    Function to calculate the data distribution model given the parameters w and tau.
    :param x:
    :param w:
    :param tau:
    :param lower_cutoff:
    :param higher_cutoff:
    :return:
    """
    y = w * 1/tau * 1/(np.exp(-lower_cutoff/tau)-np.exp(-higher_cutoff/tau)) * np.exp(-x/tau) + (1-w) * 1/(higher_cutoff-lower_cutoff)
    return y


def estimate_standard_deviation(data, params, lower_cutoff=0.75, higher_cutoff=9):
    """
    Estimate the standard deviation of the parameters using the fact that the likelihood function is a parabola
    around the maximum likelihood estimate. The standard deviation is the distance from the maximum likelihood
    estimate to the point where the likelihood function is 0.5 below the maximum likelihood estimate.
    :param data:
    :param params:
    :param lower_cutoff:
    :param higher_cutoff:
    :return:
    """
    likelihood = neg_log_likelihood(data, lower_cutoff, higher_cutoff)
    init_like = likelihood(params)
    p_err = np.zeros(len(params))
    for i,parameter in enumerate(params):
        for k in range(-1, 5):
            continue_l = True
            while continue_l:
                new_params = np.zeros(len(params))
                new_params[i] = p_err[i] + 10 ** (-k)
                new_params = new_params + params
                p_like = likelihood(new_params)
                if (p_like - init_like) >= 0.5 or np.isnan(p_like - init_like) or p_err[i] > 10:
                    continue_l = False
                else:
                    p_err[i] += 10 ** (-k)
    return p_err


def maximum_likelihood_estimate(data, lower_cutoff, higher_cutoff):
    """
    Function to calculate the maximum likelihood estimate of the parameters w and tau.
    :param data:
    :param lower_cutoff:
    :param higher_cutoff:
    :return:
    """
    popt = scipy.optimize.minimize(neg_log_likelihood(data, lower_cutoff, higher_cutoff), [0.5, 2], bounds=[(0, 1), (1, 3)])
    values = popt.x
    errors = estimate_standard_deviation(data, values, lower_cutoff, higher_cutoff)
    return values, errors


def fit_and_calculate_histogram(data, n_bins, lower_cutoff=0.75, higher_cutoff=9):
    """
    Function to calculate the histogram of the data and fit the data distribution model to the histogram.
    :param data:
    :param n_bins:
    :param lower_cutoff:
    :param higher_cutoff:
    :return:
    """
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
