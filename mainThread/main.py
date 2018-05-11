# coding: utf-8


from pylab import *
import os
from matplotlib.patches import Ellipse, Circle
import time
from mpl_toolkits.mplot3d import Axes3D
import sys
from scipy.spatial import Delaunay
from scipy.optimize import leastsq
import AdminPhoneClass
import DataProcessingClass


def warning(str):
    print('\033[31;0m')
    print(str)
    print('\033[0m')


def switch(var, ap, dp):
    return {'0': lambda ap, dp: sys.exit(),
            '1': lambda ap, dp: ap.export_data(),
            '2': lambda ap, dp: ap.clear_data(),
            '3': lambda ap, dp: dp.get_baseline(),
            '4': lambda ap, dp: dp.get_peaks(),
            '5': lambda ap, dp: dp.fit_curves(),
            }[var](ap, dp)


def choose_what_to_do(ap, dp):
    do_no = input('choose which you want to do:\n'
                  '0. Exit this programme\n'
                  '1. Export data from phone\n'
                  '2. Clear all the data inside phone\n'
                  '3. Get baselines\n'
                  '4. Get peaks\n'
                  '6. Fit curves\n'
                  '7. Draw cloud map\n'
                  '8. Validate')
    switch(do_no, ap, dp)


if __name__ == '__main__':
    ap = AdminPhoneClass.AdminPhone()
    dp = DataProcessingClass.DataProcessing()
    while True:
        choose_what_to_do(ap, dp)
        time.sleep(1)
