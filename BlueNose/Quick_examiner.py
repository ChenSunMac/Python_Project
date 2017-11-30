# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:29:36 2017
Down Sample Quick Examine


@author: chens
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
trLayout = [1, 33, 17, 29, 13, 93, 49, 81, 65, 77, 61, 21, 25, 9, 41, 5, 37,
            69, 73, 57, 89, 53, 85, 45, 2, 34, 18, 30, 14, 94, 50, 82, 66, 78,
            62, 22, 26, 10, 42, 6, 38, 70, 74, 58, 90, 54, 86, 46, 3, 35, 19, 
            31, 15, 95, 51, 83, 67, 79, 63, 23, 27, 11, 43, 7, 39, 71, 75, 59,
            91, 55, 87, 47, 4, 36, 20, 32, 16, 96, 52, 84, 68, 80, 64, 24, 28,
            12, 44, 8, 40, 72, 76, 60, 92, 56, 88, 48]
trLayout =  np.asarray(trLayout) - 1

coating = False
need_thickness = False

timeFlight = 59
DOWN_SAMPLE = False # Down Sample still needs to be approved, Please use False for now

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

def processBinFile(bin_file):
    raw_data = np.fromfile(bin_file, dtype = np.uint8)
    bin_file_size = len(raw_data)
    MATRICES_SIZE = (96, 520, 2000)
    ii = np.zeros((1,128), dtype=np.int)
    start_byte = 0
#    rp_i = 0
    signal_matrices = np.zeros(MATRICES_SIZE)
    for i in range(1, int(bin_file_size/32096) + 1):
        #raw_fire_time = raw_data[start_byte + 24:start_byte + 32]
#        roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
#        pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
#        if((roll_b != 8224) | (pitch_b != 8224)):
#            rp_i = rp_i + 1;
    
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
    return signal_matrices

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

### calliper Algorithm using 60% of incline
# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@nb.jit
def Thickness_CalliperAlg(signal_matrices, EZ = False):
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
    thickness_map = np.zeros(MAP_SIZE) + timeFlight
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
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000;
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
            chn = int(chn/skip_chn)
            rd = int(rd/skip_time_stamp)
            if (coating == False):
                if ( len(peak_diff) > 2 ):
                    thickness_point = np.median(peak_diff)
                    if thickness_point <  timeFlight * 1.2:
                        thickness_map[chn,rd] = thickness_point
                else:
                    thickness_map[chn,rd] = timeFlight
    return distance, thickness_map


def plot_and_save(map_data, minute_key, IsThickness = False):
    map_name = 'Distance'
    if IsThickness == True:
        map_name = 'Thickness'
    plt.figure(figsize=(8,4))        
    plt.imshow(distance_total_map, aspect='auto');
    plt.colorbar()
    plt.xlabel('Time Stamps')
    plt.ylabel('Channels ()')
    plt.savefig( map_name + '_map' + minute_key +'.png')
              
if __name__ == "__main__":
    test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
    file_map = Dir_Parser(test_path)
    start_PROCESSING = time.time()
 
    for minute_key, minute_file_list in file_map.items():
        index = 0
        distance_total_map = np.zeros((96, 520*len(minute_file_list)),dtype = np.float64)
        thickness_total_map = np.zeros((96, 520*len(minute_file_list)),dtype = np.float64)
        if  DOWN_SAMPLE == True:
            skip_chn = 2
            skip_time_stamp = 5
            chns = int(96/skip_chn)
            rounds = int(520/skip_time_stamp)
            distance_total_map = np.zeros(( chns, rounds*len(minute_file_list)),dtype = np.float64)
            thickness_total_map = np.zeros((chns, rounds*len(minute_file_list)),dtype = np.float64)
        for file_name in minute_file_list:       
            with open(file_name, "rb") as bin_file:
                signal_matrices = processBinFile(bin_file)
                if need_thickness == False:      
                    distance = calliperAlg(signal_matrices, DOWN_SAMPLE)
                    if DOWN_SAMPLE == True:
                        distance_total_map [:, index * int(520/skip_time_stamp) :  index * int(520/skip_time_stamp) + int(520/skip_time_stamp)] = distance
                    else:
                        distance_total_map [:, index * 520 :  index * 520 + 520] = distance
                else:
                    distance, thickness_map = Thickness_CalliperAlg(signal_matrices, DOWN_SAMPLE)
                    if DOWN_SAMPLE == True:
                        distance_total_map [:, index * int(520/skip_time_stamp) :  index * int(520/skip_time_stamp) + int(520/skip_time_stamp)] = distance
                        thickness_total_map  [:, index * int(520/skip_time_stamp) :  index * int(520/skip_time_stamp) + int(520/skip_time_stamp)] = thickness_map
                    else:
                        distance_total_map [:, index * 520 :  index * 520 + 520] = distance
                        thickness_total_map  [:, index * 520 :  index * 520 + 520] = thickness_map
                index += 1
        
        plot_and_save(distance_total_map, minute_key)        
        if need_thickness == True:
            plot_and_save(thickness_total_map, minute_key, need_thickness)
            
    print ('It took', time.time()-start_PROCESSING, 'seconds. to Finish all the Jobs')
        
