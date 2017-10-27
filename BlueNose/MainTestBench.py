# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:32:22 2017

Main Test Bench For BlueNose Project

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
#import matplotlib.pyplot as plt
# BASIC INFORMATION OUTPUT
print(sys.version)
test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
if os.path.exists(test_path):
    os.chdir(test_path)
currentPath = os.getcwd()
print(currentPath)

FILENAME_YearMonthDate = "bn170614"
FILENAME_HourMinute = "1429"
FILENAME_Start = FILENAME_YearMonthDate + "-" + FILENAME_HourMinute
start_TOTAL = time.time()
file_index = 0
# list files in one min
onlyfiles = [f for f in os.listdir(test_path) if f.startswith(FILENAME_Start) and f.endswith(".bin")]


def job(file_name):
    bin_file_size = os.stat(file_name).st_size
    with open(file_name, "rb") as bin_file:
        ### Processing Bin File
        raw_data = np.fromfile(bin_file, dtype = np.uint8)
        signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
        ### CALLIPER MAP
        distance = AlgSet.calliperAlg(signal_matrices) 
        #np.save(file_name[0:15] + "TEST" , distance)
    return distance

def job_queue(file_name, q):
    bin_file_size = os.stat(file_name).st_size
    with open(file_name, "rb") as bin_file:
        ### Processing Bin File
        raw_data = np.fromfile(bin_file, dtype = np.uint8)
        signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
        ### CALLIPER MAP
        distance = AlgSet.calliperAlg(signal_matrices) 
        #np.save(file_name[0:15] + "TEST" , distance)
    q.put(distance)
        
if __name__ == "__main__":
    start_TOTAL = time.time()
    file_name = "bn170614-142902.bin"
    file_index = 0
    job(file_name)
    results = []
    print ('It took', time.time()-start_TOTAL, 'seconds. to finish processing one bin files sequentially')      
    start_TOTAL = time.time()
    for f in onlyfiles[0:2]:
        job(f)
    print ('It took', time.time()-start_TOTAL, 'seconds. to finish processing 11 bin files sequentially')     
    
    start = time.time()
    q = mp.Queue()
    p1 = mp.Process(target = job_queue, args = (onlyfiles[1], q,))
    p2 = mp.Process(target = job_queue, args = (onlyfiles[2], q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    print ('It took', time.time()-start, 'seconds. to finish parallel 2')     
#    mp.freeze_support()
#    pool = mp.Pool()
#    cpus = mp.cpu_count()
#    for i in xrange(0,cpus):
#            result = pool.apply_async(job, args=(onlyfiles[i],))
#            results.append(result)
##    print(pool.map(job, onlyfiles))
#    pool.close()
#    pool.join()
#    print ('It took', time.time()-start_TOTAL, 'seconds. to finish processing 11 bin files using 8 cores')   
#    for result in results:
#            print(result.get())
    
#start_PROCESSING = time.time()
#bin_file_size = os.stat(file_name).st_size
#
#rp_i = 0
#with open(file_name, "rb") as bin_file:
#    raw_data = np.fromfile(bin_file, dtype = np.uint8)
#start = time.time()
#
#signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
#
#print ('It took', time.time()-start_PROCESSING, 'seconds. to finish parsing Bin File')
#
#### CALLIPER MAP
#start_CALLIPER = time.time()
#
#distance = AlgSet.calliperAlg(signal_matrices)
#print ('It took', time.time()-start_CALLIPER, 'seconds. to finish CALLIPER CALCULATION')            
            
            
#### PLOT
#x = np.linspace(1, 2000, 2000)
#y = signal_matrices[1,1,:]
#plt.figure(figsize=(8,4))
#plt.plot(x,y,label="signal from one channel",color="blue",linewidth=2)
#plt.xlabel("Time(s)")
#plt.ylabel("Normalized Amplitude")
#plt.title("Signal Plot")
#plt.ylim(-1,1)
#plt.legend()
#plt.show()
#x1 = np.linspace(1, 1001, 1001)
#test_signal = signal_matrices[1,1,:]
#fft_result =  np.fft.rfft(test_signal, n=None, axis=-1, norm=None)
#plt.plot(x1,fft_result,label="FFT RESULT",color="red",linewidth=2)
#plt.xlabel("frequency(s)")
#plt.ylabel("Normalized Amplitude")
#plt.title("Signal Plot")
#plt.ylim(-1,1)
#plt.legend()
#plt.show()




