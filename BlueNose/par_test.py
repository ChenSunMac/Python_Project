# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:03:27 2017

@author: chens
"""

import multiprocessing as mp
import time
import AlgSet
import numpy as np
import os
import sys

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
bin_file_names = []
bin_file_sizes = []
i = 0
raw_data = {}
for filename in onlyfiles:
    bin_file_size = os.stat(filename).st_size
    bin_file_sizes.append(bin_file_size)
    with open(filename, "rb") as bin_file:
        raw_data[i] = np.fromfile(bin_file, dtype = np.uint8)
        i += 1
        
#bin_file_names = [f for f in onlyfiles with open(file_name, "rb") as bin_file]

print(onlyfiles)
def job(q, n):
    res = 0;
    for i in range (n):
        res += i + i**2
    q.put(res)
   
def job_queue(q, bin_file_size,  raw_data):
    signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)
        ### CALLIPER MAP
    distance = AlgSet.calliperAlg(signal_matrices) 
        #np.save(file_name[0:15] + "TEST" , distance)
    q.put(distance)

if __name__ == "__main__":
    start = time.time()
    q = mp.Queue()
    n = 100000
    p1 = mp.Process(target = job, args = (q, n, ))
    p2 = mp.Process(target = job, args = (q,n,))
    p3 = mp.Process(target = job_queue, args = (q, bin_file_sizes[1], raw_data[1],))
    p4 = mp.Process(target = job_queue, args = (q, bin_file_sizes[2], raw_data[2],))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    res1 = q.get()
    res2 = q.get()
    res3 = q.get()
    res4 = q.get()
    print(res1 + res2)
    print ('It took', time.time()-start, 'seconds. to finish parallel')     
    start2 = time.time()
    p1 = mp.Process(target = job, args = (q,n, ))
    p2 = mp.Process(target = job, args = (q,n, ))
    p1.start()
    p1.join()
    p2.start()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print ('It took', time.time()-start2, 'seconds. to finish seq')     