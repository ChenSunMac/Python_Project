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
from scipy import interpolate
import os
import sys
import time
import AlgSet
from detect_peaks import detect_peaks
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
s = [-0.0729,   -0.2975,   -0.2346 ,   0.1057   , 0.8121  ,  0.5721  , -0.4512,   
     -0.7820  , -0.5137    , 0.4829    ,0.8867 ,  -0.0891 ,  -0.4474  ,-0.0875 ,   0.2159];
coating = False
trLayout = [1, 33, 17, 29, 13, 93, 49, 81, 65, 77, 61, 21, 25, 9, 41, 5, 37,
            69, 73, 57, 89, 53, 85, 45, 2, 34, 18, 30, 14, 94, 50, 82, 66, 78,
            62, 22, 26, 10, 42, 6, 38, 70, 74, 58, 90, 54, 86, 46, 3, 35, 19, 
            31, 15, 95, 51, 83, 67, 79, 63, 23, 27, 11, 43, 7, 39, 71, 75, 59,
            91, 55, 87, 47, 4, 36, 20, 32, 16, 96, 52, 84, 68, 80, 64, 24, 28,
            12, 44, 8, 40, 72, 76, 60, 92, 56, 88, 48]

trLayout =  np.asarray(trLayout) - 1

        
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
    start_CalliperAndThickness = time.time()
    timeFlight = 59
    MAP_SIZE = (96, 520)
    distance = np.zeros(MAP_SIZE)
    thickness_map = np.zeros(MAP_SIZE) + timeFlight
    START_DELAY = 6601;
    TOTAL_CHN, TOTAL_ROUND, SIGNAL_LENGTH = signal_matrices.shape
    for chn in range(TOTAL_CHN):        
        for rd in range(TOTAL_ROUND):
            signal = signal_matrices[trLayout[chn], rd, :]
            norm_signal = signal/np.max(np.absolute(signal))
            # USE Numpy.argmax instead of for loop to save time
            trigger = np.argmax(norm_signal > 0.594)
            if (trigger < 20) or (trigger > 1900):
                trigger = 20
            else:
                pass
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000   
            main_reflection = norm_signal[trigger - 20 : trigger + 280]
            abs_conv_result = np.absolute(np.convolve(main_reflection, s))
            peaks_locs = detect_peaks(abs_conv_result, mph = None, mpd = 20, 
                                      show=False)
            peaks_value = abs_conv_result[peaks_locs]
            envelopObject = interpolate.interp1d(peaks_locs, peaks_value, kind='quadratic')
            xnew = np.linspace(peaks_locs[0], peaks_locs[-1], num=peaks_locs[-1] - peaks_locs[0] + 1)
            envelop = envelopObject(xnew)
            filtered_peaks_locs = detect_peaks(envelop, mph = None, mpd = 20, 
                                      show=False)        
            peak_diff = np.diff(filtered_peaks_locs)
            if (coating == False):
                if ( len(peak_diff) > 2 ):
                    thickness_point = np.median(peak_diff)
                    if thickness_point <  timeFlight * 1.2:
                        thickness_map[chn,rd] = thickness_point
                else:
                    thickness_map[chn,rd] = timeFlight / 3
    print ('It took', time.time()- start_CalliperAndThickness, 'seconds. to finish 2 maps')   

         
#    start_2 = time.time()
#    distance2  = AlgSet.processBinFileToDistanceMap2(bin_file_size, raw_data)
#    print ('It took', time.time()-start_2, 'seconds. to finish all in one function')   
    plt.figure(figsize=(8,4))        
    plt.imshow(distance, aspect='auto');
    plt.colorbar()
    plt.show()
    #plt.savefig('py.png')
    plt.figure(figsize=(8,4))        
    plt.imshow(thickness_map, aspect='auto');
    plt.colorbar()
    plt.show()            
            
#### PLOT
#    recovered, remainder = signal.deconvolve(main_reflection, s)    
#    xlen = len(envelop)
#    x = np.linspace(1, xlen, xlen)
#    y = envelop
#    plt.figure(figsize=(8,4))
#    plt.plot(x,y,label="signal from one channel",color="blue",linewidth=2)
##
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




