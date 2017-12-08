# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 13:44:49 2017

@author: Chens
"""

import os
import glob
import numpy as np
import numba as nb
import matplotlib.pyplot as plt
from detect_peaks import detect_peaks
from scipy import interpolate
import time
"""
Parameters:
"""
s = [-0.0729,   -0.2975,   -0.2346 ,   0.1057   , 0.8121  ,  0.5721  , -0.4512,   
     -0.7820  , -0.5137    , 0.4829    ,0.8867 ,  -0.0891 ,  -0.4474  ,-0.0875 ,   0.2159]

#trLayout = [1, 33, 17, 29, 13, 93, 49, 81, 65, 77, 61, 21, 25, 9, 41, 5, 37,
#            69, 73, 57, 89, 53, 85, 45, 2, 34, 18, 30, 14, 94, 50, 82, 66, 78,
#            62, 22, 26, 10, 42, 6, 38, 70, 74, 58, 90, 54, 86, 46, 3, 35, 19, 
#            31, 15, 95, 51, 83, 67, 79, 63, 23, 27, 11, 43, 7, 39, 71, 75, 59,
#            91, 55, 87, 47, 4, 36, 20, 32, 16, 96, 52, 84, 68, 80, 64, 24, 28,
#            12, 44, 8, 40, 72, 76, 60, 92, 56, 88, 48]

trLayout = np.linspace(1, 96, 96, dtype = 'uint')
trLayout =  np.asarray(trLayout) - 1

"""
Functions:
    
"""
def Dir_Parser(test_path):
    if os.path.exists(test_path):
        os.chdir(test_path)
        currentPath = os.getcwd()
        print(currentPath)
    
    ## Filter .bin file and sort based on name
    file_list =  glob.glob('*.bin')
    file_list.sort()
    first_min = file_list[0][9:13]
    last_min = file_list[-1][9:13]
    
    ## Construct a dictionary for mapping mins of data 
    file_map = dict()
    for file in  file_list:
        if file[:-6] in file_map:
            pass
        else:
            bn_YMDHM = file[:-6]
            file_map[bn_YMDHM] = [f for f in file_list if f.startswith(bn_YMDHM)]   
            
    if len(file_map) > 1:
        sorted_key_list = sorted(file_map.keys())
        for key, index in  zip(sorted_key_list, range(len(sorted_key_list))):
            if key[9:13] < last_min:
                file_map[key].append(file_map[sorted_key_list[index + 1]][0])
            if key[9:13] > first_min: 
                file_map[key].insert(0,file_map[sorted_key_list[index - 1]][-1])
                
    return file_map

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
def processBinFile(bin_file):
    raw_data = np.fromfile(bin_file, dtype = np.uint8)
    bin_file_size = len(raw_data)
    MATRICES_SIZE = (96, 520, 2000)
    ii = np.zeros((1,128), dtype=np.int)
    start_byte = 0
    rp_locs = np.zeros((260,1), dtype=np.int)
    fire_time_array = np.zeros(( 6240 , 1 ), dtype=np.uint)
    roll_r = np.zeros(( 260 , 1 ), dtype=np.uint16)
    rp_i = 0
    signal_matrices = np.zeros(MATRICES_SIZE)
    for i in range(0, int(bin_file_size/32096) ):
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
    return signal_matrices, roll_r

def processRoll_r (roll_r):
    tdcTr1 = 152

    TDC = roll_r /100+tdcTr1
    
    # Calculate transducer number @ TDC:
    transducer_TDC = TDC // 3.75 #np.around((TDC/3.75))
    
    transducer_TDC[transducer_TDC < 0] = transducer_TDC[transducer_TDC < 0] + 96
    transducer_TDC[transducer_TDC > 95] = transducer_TDC[transducer_TDC > 95] - 96
    
    transducer_TDC = np.interp(np.linspace(0, 519, 520, dtype = 'uint16'), 
                               np.linspace(0, 259, 260, dtype = 'uint16'), 
                               np.reshape(transducer_TDC, len(transducer_TDC)))
    return transducer_TDC

### calliper Algorithm using 60% of incline
# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@nb.jit
def calliperAlg(signal_matrices, EZ = False):
    skip_chn = 1
    skip_time_stamp = 1
    MAP_SIZE = (96, 520)
    if EZ == True:
        skip_chn = 2
        skip_time_stamp = 5
        MAP_SIZE = (int(96/skip_chn), int(520/skip_time_stamp))
    distance = np.zeros(MAP_SIZE)
    START_DELAY = 6601;
    TOTAL_CHN, TOTAL_ROUND, SIGNAL_LENGTH = signal_matrices.shape
    for chn in range(0, TOTAL_CHN, skip_chn):
        for rd in range(0, TOTAL_ROUND, skip_time_stamp):
            signal = signal_matrices[trLayout[chn], rd, :]
            #signal = signal_matrices[chn, rd, :]
            norm_signal = signal/np.max(np.absolute(signal))
            # USE Numpy.argmax instead of for loop to save time
            trigger = np.argmax(norm_signal > 0.594)
            if (trigger < 20) or (trigger > 1900):
                trigger = 20;
            else:
                pass
                #main_reflection = norm_signal[trigger - 20 : trigger + 280]
            chn = int(chn/skip_chn)
            rd = int(rd/skip_time_stamp)
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000;
    return distance

def plot_and_save(map_data, minute_key, transducer_TDC_map, IsThickness = False):
    map_name = 'Distance'
    plot_Trasducer_traspose = np.transpose(transducer_TDC_map)
    if IsThickness == True:
        map_name = 'Thickness'
    plt.figure(figsize=(8,4))        
    plt.imshow(map_data, aspect='auto', vmax= 0.3, vmin= 0.4)
    plt.plot(np.linspace(1, len(plot_Trasducer_traspose), len(plot_Trasducer_traspose)), plot_Trasducer_traspose, 'r-')
    plt.colorbar()   
    plt.xlabel('Time Stamps')
    plt.ylabel('Channels ()')
    plt.savefig( map_name + '_map' + minute_key +'.png')

if __name__ == "__main__":
    test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2\\testParallelData"
    file_map = Dir_Parser(test_path)
    start_PROCESSING = time.time()
 
    for minute_key, minute_file_list in file_map.items():
        index = 0
        distance_total_map = np.zeros((96, 520*len(minute_file_list)), dtype = np.float64)
        transducer_TDC_map = np.zeros( ( 1, 520*len(minute_file_list)) , dtype = np.uint16)
        for file_name in minute_file_list:       
            with open(file_name, "rb") as bin_file:
                signal_matrices, roll_r = processBinFile(bin_file)
                distance = calliperAlg(signal_matrices)
                distance_total_map [:, index * 520 :  index * 520 + 520] = distance
                trasducer_TDC =  processRoll_r (roll_r)
                transducer_TDC_map  [:, index * 520 :  index * 520 + 520] = np.asmatrix(trasducer_TDC)
                index += 1
                print("Work Finished at Min: " + minute_key + " File Count: " + str(index))
        print(minute_key + "Files has Finished!!!")
    plot_and_save(distance_total_map, minute_key, transducer_TDC_map)  
    print ('It took', time.time()-start_PROCESSING, 'seconds. to Finish all the Jobs')



