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

def find_coordinates(index):
    index = int(index)
    tblr = [0, 0, 0, 0]
    tblr[0] = index
    tblr[1] = index + 48
    tblr[2] = index - 24
    tblr[3] = index + 24
    if tblr[1] > 95:
        tblr[1] = tblr[1] - 96
    if tblr[2] < 0:
        tblr[2] = tblr[2] + 96
    if tblr[3] > 95:
        tblr[3] = tblr[3] - 96
    return tblr

    
    
    

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

        

start_TOTAL = time.time()
file_name = "bn170614-142902.bin"


start_PROCESSING = time.time()
bin_file_size = os.stat(file_name).st_size

rp_i = 0
with open(file_name, "rb") as bin_file:
    raw_data = np.fromfile(bin_file, dtype = np.uint8)

bin_file_size = len(raw_data)
MATRICES_SIZE = (96, 520, 2000)
ii = np.zeros((1,128), dtype=np.int)

start_byte = 0
rp_i = 0
signal_matrices = np.zeros(MATRICES_SIZE)

"""
Bin File is segmented in the following way:

||-header_files|-|.8 segments of sound data files..|-||.....||-header_files|-|.8 segments of sound data files..|-||
|-------------------32096 Bytes-----------------------|... 6240 instances of the data bags in total

Total Binary File Size is : 200279040 B
The Workers Need to Work On 200279040 B/ 32096 B = 6240 instances of Data Bags (i)
Each Data Bag Contains:
    |**HEADER DATA**|:
        raw_fire_time: {uint64}, update in each Data Bags [6240 in total]
        roll_b:{unit16}, update every 24 Data Bag instances [260 in total]


    |**SOUND DATA**|:
"""
rp_locs = np.zeros((260,1), dtype=np.int)
fire_time_array = np.zeros(( 6240 , 1 ), dtype=np.uint)
roll_r = np.zeros(( 260 , 1 ), dtype=np.uint16)
for i in range(0, int(bin_file_size/32096)):
    raw_fire_time = raw_data[start_byte + 24:start_byte + 32].view('uint64')
    fire_time_array[i] =  raw_fire_time
    roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
    pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
    if((roll_b != 8224) | (pitch_b != 8224)):
        rp_locs[rp_i] = i
        roll_r[rp_i] = roll_b
        rp_i = rp_i + 1
        
        
    for k in range(0, 8):
        raw_signal = raw_data[start_byte + k * 4008 + 40 : start_byte + k * 4008 + 4040].view('uint16')
        raw_signal = (raw_signal.astype("double")-32768)/32768
        raw_signal = np.asmatrix(raw_signal)
        #raw_first_ref = raw_data[start_byte+k*4008+32:start_byte +k*4008+34]
        #first_ref = raw_first_ref.view('uint16')
        channel_index = raw_data[start_byte + k*4008 + 38].astype("int64")
        # FUTURE : add thickness and distance calculation here to save more time
        signal_matrices[channel_index, ii[0,channel_index], :] = raw_signal
        ii[0,channel_index] = ii[0,channel_index] + 1
    start_byte = start_byte +32096


print ('It took', time.time()-start_PROCESSING, 'seconds. to read in  Bin File')

"""
Calliper:
"""
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
        if (trigger < 20) or (trigger > 1900):
            trigger = 20;
        else:
            pass
            #main_reflection = norm_signal[trigger - 20 : trigger + 280]
        distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000 



"""
Positioning:
    
"""
# roll reading when transducer 1 is facing up
tdcTr1 = 152

TDC = roll_r /100+tdcTr1

# Calculate transducer number @ TDC:
transducer_TDC = TDC // 3.75 #np.around((TDC/3.75))

transducer_TDC[transducer_TDC < 0] = transducer_TDC[transducer_TDC < 0] + 96
transducer_TDC[transducer_TDC > 95] = transducer_TDC[transducer_TDC > 95] - 96

transducer_TDC = np.interp(np.linspace(0, 519, 520, dtype = 'uint16'), 
                           np.linspace(0, 259, 260, dtype = 'uint16'), 
                           np.reshape(transducer_TDC, len(transducer_TDC)))

# Find Pipe Diver Center at Each Ring:
ring_set = {"ring1":np.arange(0, 96, 6), "ring2":np.arange(3, 96, 6),
            "ring3":np.arange(1, 96, 6), "ring4":np.arange(4, 96, 6),
            "ring5":np.arange(2, 96, 6), "ring6":np.arange(5, 96, 6)}
ring_counter = 0
index_ring_TDC_pool = np.zeros((6 , 520), dtype='uint')
xAxis = np.zeros((6 , 520), dtype='float')
yAxis = np.zeros((6 , 520), dtype='float')
drift = np.zeros((6 , 520), dtype='float')

for ring, ring_tdc_value in ring_set.items():
    
    for shot_index in range(0, 520):
        cur_tdc_list = np.absolute(ring_tdc_value - transducer_TDC[shot_index])
        min_value = np.amin(cur_tdc_list)
        index_ring_TDC_pool[ring_counter, shot_index] = np.argmin(cur_tdc_list)
        ring_aprox_tdc = ring_tdc_value[index_ring_TDC_pool[ring_counter, shot_index]]
        topIndex = transducer_TDC[shot_index]
        tblr_match = find_coordinates(topIndex)
        tblrAprxTDC = find_coordinates(ring_aprox_tdc)
        
        # TDC on this ring
        if min_value == 0:
            xAxis[ring_counter, shot_index] = -(distance[tblr_match[2], shot_index] - distance[tblr_match[3], shot_index])/2
            yAxis[ring_counter, shot_index] = -(distance[tblr_match[0], shot_index] - distance[tblr_match[1], shot_index])/2
            drift[ring_counter, shot_index] = (xAxis[ring_counter, shot_index]**2 + yAxis[ring_counter, shot_index]**2)**0.5
            continue
        
        if transducer_TDC[shot_index] > ring_tdc_value[index_ring_TDC_pool[ring_counter, shot_index]] :
            if index_ring_TDC_pool[ring_counter, shot_index] + 2 >  len(ring_tdc_value):
                top_neighbour = ring_tdc_value[0]
            else:
                top_neighbour = ring_tdc_value[index_ring_TDC_pool[ring_counter, shot_index] + 2]
        else:
            if index_ring_TDC_pool[ring_counter, shot_index]  == 0:
                top_neighbour = ring_tdc_value[-1]
            else:
                top_neighbour = ring_tdc_value[index_ring_TDC_pool[ring_counter, shot_index]]
        tblrNeighbor = find_coordinates(top_neighbour)
        
        intrplDistance = distance[tblrAprxTDC,shot_index] + abs(tblr_match[0] - tblrAprxTDC[0])/6 * (distance[tblrNeighbor,shot_index] -  distance[tblrAprxTDC,shot_index])
        xAxis[ring_counter, shot_index] = (intrplDistance[3] - intrplDistance[2]) / 2
        yAxis[ring_counter, shot_index] = (intrplDistance[1] - intrplDistance[0]) / 2
        drift[ring_counter, shot_index] = (xAxis[ring_counter, shot_index]**2 + yAxis[ring_counter, shot_index]**2)**0.5    
    ring_counter += 1

tilt = np.arctan((drift[0,:]-drift[5,:])/0.1397)

#    start_2 = time.time()
#    distance2  = AlgSet.processBinFileToDistanceMap2(bin_file_size, raw_data)
#    print ('It took', time.time()-start_2, 'seconds. to finish all in one function')   
plt.figure(figsize=(8,4))        
plt.imshow(distance, aspect='auto')
plt.plot(np.linspace(1, len(transducer_TDC), len(transducer_TDC)), transducer_TDC, 'r-')
plt.colorbar()
plt.show()
#    #plt.savefig('py.png')
#    plt.figure(figsize=(8,4))        
#    plt.imshow(thickness_map, aspect='auto');
#    plt.colorbar()
#    plt.show()            
            
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




