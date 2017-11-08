# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:59:06 2017

@author: Chens
"""

import time 
from joblib import Parallel, delayed 
import AlgSet
import os
import numpy as np
import matplotlib.pyplot as plt

def job(file_name):
    print(f'Process {os.getpid()} working on file {file_name}')
    bin_file_size = os.stat(file_name).st_size
    with open(file_name, "rb") as bin_file:
        ### Processing Bin File
        raw_data = np.fromfile(bin_file, dtype = np.uint8)
        signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
        ### CALLIPER MAP
        distance = AlgSet.calliperAlg(signal_matrices) 
        #np.save(file_name[0:15] + "TEST" , distance)
    print(f'Process {os.getpid()} done processing {file_name}')
    return distance

# A function that can be called to do work:

def work(arg):    
    print ("Function receives the arguments as a list:", arg)
    # Split the list to individual variables:
    i, j = arg    
    # All this work function does is wait 1 second...
    time.sleep(1)    
    # ... and prints a string containing the inputs:
    print ("%s_%s" % (i, j))
    return "%s_%s" % (i, j)

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    # List of arguments to pass to work():
    arg_instances = [(1, 1), (1, 2), (1, 3), (1, 4)]
    # Anything returned by work() can be stored:
    results = Parallel(n_jobs=4, verbose=1)(map(delayed(work), arg_instances))
    print (results)
    
    test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"

    if os.path.exists(test_path):
        os.chdir(test_path)
        currentPath = os.getcwd()
        print(currentPath)

    FILENAME_YearMonthDate = "bn170614"
    FILENAME_HourMinute = "1429"
    FILENAME_Start = FILENAME_YearMonthDate + "-" + FILENAME_HourMinute
    # list files in one min
    bin_files = [f for f in os.listdir(test_path) if f.startswith(FILENAME_Start) and f.endswith(".bin")]
    print (bin_files)
    resultss = Parallel(n_jobs = 4, verbose=1) (map(delayed(job), bin_files[0:8]))
    
    plt.figure(figsize=(8,4))        
    plt.imshow(resultss[1], aspect='auto');
    plt.colorbar()
    plt.show()

