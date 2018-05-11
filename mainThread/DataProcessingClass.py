# coding: utf-8

import pandas as pd
import os
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf


class DataProcessing:
    def __init__(self):
        self.data = self.read_rawdata().ix[:, 1:5]
        self.baseline = np.array([])
        self.force = np.array([])
        self.peaks = np.zeros([np.shape(self.data)[1], 2])
        self.obj_force = np.array([])
        self.coord = np.array([])

    def read_rawdata(self):
        path = 'EdgeSensorDemo'
        files = os.listdir(path)
        for f in files:
            if 'txt' in f:
                return pd.read_table(''.join((path, '/', f)))

    def get_baseline(self):
        self.baseline = np.apply_along_axis(lambda x: self.baseline_als(x, 1e9, 0.01), 0, self.data)
        plt.plot(self.data)
        plt.plot(self.baseline)
        plt.show()
        plt.figure()
        self.force = np.array(self.data - self.baseline)

    def get_peaks(self):
        self.peaks[:, 0] = np.apply_along_axis(lambda x: np.argmax(x), 0, self.force)
        self.peaks[:, 1] = np.apply_along_axis(lambda x: np.max(x), 0, self.force)
        print(self.peaks)

    def fit_curves(self):
        mean_gap = np.mean(np.diff(np.sort(self.peaks[:, 0])))
        start = np.max((0, np.min(self.peaks[:, 0], 0) - 2.5 * mean_gap)).astype(np.int)
        end = np.min((np.shape(self.force)[0], np.max(self.peaks[:, 0], 0) + 2.5 * mean_gap)).astype(np.int)
        print(start, end)
        self.force = np.array(self.force)
        self.obj_force = self.force[start:end, :]
        self.coord = self.get_coord(range(np.shape(self.obj_force)[0]),
                                    np.min(self.peaks[:, 0], 0) - start,
                                    np.max(self.peaks[:, 0], 0) - start)
        params = self.calc_params()
        print(params)
        fitted_curve = np.array([self.rbf_func(self.coord, params[ii, 0], params[ii, 1], params[ii, 2])
                                 for ii in range(np.shape(self.obj_force)[1])])
        plt.figure()
        plt.plot(self.coord, self.obj_force)
        plt.plot(self.coord, fitted_curve.T)
        plt.show()

    @staticmethod
    def baseline_als(y, lam, p, niter=10):
        L = len(y)
        D = sparse.csc_matrix(np.diff(np.eye(L), 2))
        w = np.ones(L)
        z = 0
        for i in range(niter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D.dot(D.transpose())
            z = spsolve(Z, w * y)
            w = p * (y > z) + (1 - p) * (y < z)
        return z

    @staticmethod
    def preprocessing(data):
        return np.apply_along_axis(lambda x: x - x[0], 0, data)

    @staticmethod
    def get_coord(raw_coord, zero_pos, one_pos):
        return (raw_coord - zero_pos) / (one_pos - zero_pos)

    @staticmethod
    def rbf_func(x, alpha, beta, gamma):
        return alpha * np.exp(-(x - beta) ** 2 / (2 * gamma ** 2))

    def calc_params(self):
        params = np.apply_along_axis(lambda x: cf(self.rbf_func, self.coord, x)[0], 0, self.obj_force)
        return params.T


if __name__ == '__main__':
    dp = DataProcessing()
    dp.read_rawdata()
    dp.get_baseline()
    dp.get_peaks()
    dp.fit_curves()
