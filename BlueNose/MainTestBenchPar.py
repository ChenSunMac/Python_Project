# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:32:22 2017

Parallel Main Test Bench For BlueNose Project

- Extract and processing [2000*1] points from one reference .bin file
- TIME DOMAIN:
    - thickness calculation
    - energy calculation
- Frequency Domain:
    - thickness set calculation and picking
    - energy calculation
@author: chens
"""
import numpy as np
import os
import sys
import time
import AlgSet
import multiprocessing as mp
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
# BASIC INFORMATION OUTPUT


def job(file_name, return_dict):
    print(f'Process {os.getpid()} working on file {file_name}')
    bin_file_size = os.stat(file_name).st_size
    with open(file_name, "rb") as bin_file:
        ### Processing Bin File
        raw_data = np.fromfile(bin_file, dtype = np.uint8)
        signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
        ### CALLIPER MAP
        distance = AlgSet.calliperAlg(signal_matrices) 
        #np.save(file_name[0:15] + "TEST" , distance)
        return_dict[file_name] = distance
    print(f'Process {os.getpid()} done processing {file_name}')
    #return distance
    

    
if __name__ == "__main__":
    print(sys.version)
    test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"

    if os.path.exists(test_path):
        os.chdir(test_path)
        currentPath = os.getcwd()
        print(currentPath)

    FILENAME_YearMonthDate = "bn170614"
    FILENAME_HourMinute = "1429"
    FILENAME_Start = FILENAME_YearMonthDate + "-" + FILENAME_HourMinute

    file_index = 0
    # list files in one min
    bin_files = [f for f in os.listdir(test_path) if f.startswith(FILENAME_Start) and f.endswith(".bin")]
    #file_name = "bn170614-142902.bin" %timeit AlgSet.processBinFile(bin_file_size, raw_data)
    distance_map = np.zeros((96, 520*len(bin_files)),dtype = np.float64)
    
    ### PARALLEL SEGMENT
    start = time.time()
    manager = mp.Manager()
    return_dict = manager.dict()
    cpus = mp.cpu_count()
    process_list = []
    for i in range(cpus):
        p = mp.Process(target=job, args=(bin_files[i], return_dict, ))
        process_list.append(p)
        p.start()
        
    for proc in process_list:
        proc.join()

#    for file_name, start_index in zip(bin_files,  range(cpus)):
#        distance_map2[:, start_index * 520 : start_index * 520 + 520] = distance_map_par[start_index]

    print ('It took', time.time()-start, 'seconds. to finish all', cpus, 'files in par')
    
    ####
#    start_PROCESSING = time.time()
#    for file_name, start_index in zip(bin_files,  range(len(bin_files))):
#        distance_map[:, start_index * 520 : start_index * 520 + 520] = job(file_name)
##        bin_file_size = os.stat(file_name).st_size
##        rp_i = 0
##        with open(file_name, "rb") as bin_file:
##            raw_data = np.fromfile(bin_file, dtype = np.uint8)
##        start = time.time()
##
##        signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
##
##        print ('It took', time.time()-start, 'seconds. to finish parsing one Bin File')
##
##            ### CALLIPER MAP
##        start_CALLIPER = time.time()
##
##        distance = AlgSet.calliperAlg(signal_matrices)
##        print ('It took', time.time()-start_CALLIPER, 'seconds. to finish CALLIPER CALCULATION')            
#    print ('It took', time.time()-start_PROCESSING, 'seconds. to finish all 11 files in seq')
#    plt.imshow(distance_map, aspect='auto');
#    plt.colorbar()
#    plt.show()
#    plt.savefig('py.png')
