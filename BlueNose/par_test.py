# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:03:27 2017

@author: chens
"""

import numpy as np
import threading
from numba import jit
import time
import os
@jit('void(double[:], double[:], int64, int64, double[:])', nopython=True, nogil=True)
def numba_f(x, y, S, N, res):
    for i in range(S, min(S+N, len(x))):
        res[i] = np.log(np.exp(x[i]) * np.log(y[i]))

@jit(nopython=True, nogil=True)
def open_file(file_name, i,  raw_data):
    test_path = "C:/Users/chens/Documents/gui-dev/SmallTempData/0.3_ft_Run2"
    #bin_file_size = os.stat(file_name).st_size
    #rp_i = 0
    #with open(test_path +"\\" + file_name, "rb") as bin_file:
    f = open(test_path +"/" + file_name, "rb")
    raw_data[i] = np.fromfile(f, dtype = np.uint8)




# number of threads
T = 8
# data size, 80 million items  8e7
N = int(8e7)
# data
x = np.random.uniform(0, 20., size=N)
y = np.random.uniform(0, 20., size=N)
# array for results
r = np.zeros(N)

# data size for each thread
chunk_N = N / T
# starting index for each thread
chunks = [i * chunk_N for i in range(T)]

start = time.time()
threads = [threading.Thread(target=numba_f, args=(x,y,chunk,chunk_N,r)) for chunk in chunks]
for thread in threads:
  thread.start()
for thread in threads:
  thread.join()
print ('It took', time.time()-start, 'seconds. to finish processing in parallel')        
print (r)   
# all threads have finished here
start = time.time()
# also run a 1-threaded version for comparison
numba_f(x, y, 0, N, r)
print ('It took', time.time()-start, 'seconds. to finish processing in one')  

###
test_path = "C:/Users/chens/Documents/gui-dev/SmallTempData/0.3_ft_Run2"

FILENAME_YearMonthDate = "bn170614"
FILENAME_HourMinute = "1429"
FILENAME_Start = FILENAME_YearMonthDate + "-" + FILENAME_HourMinute
start_TOTAL = time.time()
file_index = 0
# list files in one min
bin_files = [f for f in os.listdir(test_path) if f.startswith(FILENAME_Start) and f.endswith(".bin")]
start = time.time()
raw_data = np.zeros((len(bin_files), 200279040),dtype = np.uint8)
threads = [threading.Thread(target=open_file, args=(file_name, i,  raw_data))  for file_name, i in zip(bin_files, range(len(bin_files)))]
for thread in threads:
  thread.start()
for thread in threads:
  thread.join()
print ('It took', time.time()-start, 'seconds. to finish processing in parallel to open 11 files')    