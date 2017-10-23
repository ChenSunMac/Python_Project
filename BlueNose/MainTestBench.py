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
#import matplotlib.pyplot as plt
# BASIC INFORMATION OUTPUT
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
        # FUTURE : add thickness and distance calculation here to save more time
        signal_matrices[channel_index, ii[0,channel_index], :] = raw_signal
        ii[0,channel_index] = ii[0,channel_index] + 1
    start_byte = start_byte +32096
print ('It took', time.time()-start, 'seconds. to finish parsing Bin File')

### CALLIPER MAP
(TOTAL_CHN, TOTAL_ROUND, SIGNAL_LENGTH) = signal_matrices.shape

for chn in range(TOTAL_CHN):
    for rd in range(TOTAL_ROUND):
        signal = signal_matrices[chn, rd, :]
        norm_signal = signal/np.max(np.absolute(signal))
        for timepoint in range(SIGNAL_LENGTH):
            
        

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




