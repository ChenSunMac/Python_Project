# -*- coding: utf-8 -*-
"""
Created on Tue Oct 02 16:08:09 2017
- Took specific path and file name (.bin) file
- Processing it and output signal_matrices: 96 x 520 x 2000 mat (float64)
@author: chens
"""

import numpy as np
import os
import sys
import time

print(sys.version)
test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
file_name = "bn170614-142902.bin"
if os.path.exists(test_path):
    os.chdir(test_path)
currentPath = os.getcwd()
print(currentPath)

start = time.time()


bin_file_size = os.stat(file_name).st_size
round_per_read = bin_file_size/32096/12

MATRICES_SIZE = (96,520,2000)
signal_matrices = np.zeros(MATRICES_SIZE)
ii = np.zeros((1,128), dtype=np.int)
start_byte = 0
rp_i = 0;
with open(file_name, "rb") as bin_file:
    raw_data = np.fromfile(bin_file, dtype = np.uint8)
    
for i in range(1, bin_file_size/32096 + 1):
    raw_fire_time = raw_data[start_byte + 24:start_byte + 32]
    roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
    pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
    if((roll_b != 8224) | (pitch_b != 8224)):
        rp_i = rp_i + 1;
    
    for k in range(0, 8):
        raw_signal = raw_data[start_byte + k * 4008 + 40 : start_byte + k * 4008 + 4040].view('uint16')
        raw_signal = (raw_signal.astype("double")-32768)/32768;
        raw_signal = np.asmatrix(raw_signal)
        raw_first_ref = raw_data[start_byte+k*4008+32:start_byte +k*4008+34]
        first_ref = raw_first_ref.view('uint16')
        channel_index = raw_data[start_byte + k*4008 + 38].astype("int64")
        
        signal_matrices[channel_index, ii[0,channel_index], :] = raw_signal
        ii[0,channel_index] = ii[0,channel_index] + 1
    start_byte = start_byte +32096
print 'It took', time.time()-start, 'seconds.'
print ("DONE")
    


