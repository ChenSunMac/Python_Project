# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:32:22 2017

Seq Main Test Bench For BlueNose Project

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

import matplotlib.pyplot as plt
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
bin_files = [f for f in os.listdir(test_path) if f.startswith(FILENAME_Start) and f.endswith(".bin")]
s = [-0.0729,   -0.2975,   -0.2346 ,   0.1057   , 0.8121  ,  0.5721  , -0.4512,   -0.7820  , -0.5137    , 0.4829    ,0.8867 ,  -0.0891 ,  -0.4474  ,-0.0875 ,   0.2159];

        
if __name__ == "__main__":
    start_TOTAL = time.time()
    file_name = "bn170614-142902.bin"

    
    start_PROCESSING = time.time()
    bin_file_size = os.stat(file_name).st_size
    
    rp_i = 0
    with open(file_name, "rb") as bin_file:
        raw_data = np.fromfile(bin_file, dtype = np.uint8)
        start = time.time()
    print ('It took', time.time()-start_PROCESSING, 'seconds. to read in  Bin File')
    signal_matrices = AlgSet.processBinFile(bin_file_size, raw_data)

    print ('It took', time.time()-start_PROCESSING, 'seconds. to finish parsing Bin File')

    ### CALLIPER MAP
#    start_CALLIPER = time.time()

#    distance = AlgSet.calliperAlg(signal_matrices)
#    print ('It took', time.time()-start_CALLIPER, 'seconds. to finish CALLIPER CALCULATION')   

    MAP_SIZE = (96, 520)
    distance = np.zeros(MAP_SIZE)
    START_DELAY = 6601;
    TOTAL_CHN, TOTAL_ROUND, SIGNAL_LENGTH = signal_matrices.shape
    for chn in range(TOTAL_CHN):
        for rd in range(TOTAL_ROUND):
            signal = signal_matrices[chn, rd, :]
            norm_signal = signal/np.max(np.absolute(signal))
            # USE Numpy.argmax instead of for loop to save time
            trigger = np.argmax(norm_signal > 0.594)
            if (trigger < 20) and (trigger > 1900):
                trigger = 0;
            else:
                pass
            main_reflection = norm_signal[trigger - 20 : trigger + 280]
            abs_conv_result = np.absolute(np.convolve(main_reflection, s))
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000;    
    



         
#    start_2 = time.time()
#    distance2  = AlgSet.processBinFileToDistanceMap2(bin_file_size, raw_data)
#    print ('It took', time.time()-start_2, 'seconds. to finish all in one function')   
    plt.imshow(distance, aspect='auto');
    plt.colorbar()
    plt.show()
    #plt.savefig('py.png')
            
            
#### PLOT
#    recovered, remainder = signal.deconvolve(main_reflection, s)    
#    xlen = len(recovered)
#    x = np.linspace(1, xlen, xlen)
#    y = recovered
#    plt.figure(figsize=(8,4))
#    plt.plot(x,y,label="signal from one channel",color="blue",linewidth=2)
#
#    plt.show()
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




