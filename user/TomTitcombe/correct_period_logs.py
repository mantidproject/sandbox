"""A script to correct erroneous periods in period_log"""
from __future__ import print_function

import numpy as np
import h5py

def correct_period_log(filename):
    """
    This function changes all period_log values to 1.
    Run this when the log periods/number is different to the periods 
    contained in framelog/period_log/value
    """
    # Open the file in read/write mode
    f = h5py.File(filename, "r+")

    # Loop through framelog/period_log/value and change any
    # non-1 values to 1
    value = f["raw_data_1"]["framelog"]["period_log"]["value"]
    for i in range(value.shape[0]):
        if value[i] != 1:
            value[i] = 1

    f.close()

    # Check that it has worked
    f = h5py.File(filename, "r")
    value = f["raw_data_1"]["framelog"]["period_log"]["value"]
    print("The maximum value present in period_log/value is now {}".format(np.max(value)))
    f.close()
    

filename = ""  # fill this in
correct_period_log(filename)