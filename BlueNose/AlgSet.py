# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:45:40 2017
### Algorithm Set for Bluenose Data Processing

# 

# calliperAlg 
    INPUT: m * n * 2000 signal matrices
    OUTPUT : m * n calliper MAP

@author: chens
"""
import numpy as np
import numba as nb
from scipy import interpolate
from detect_peaks import detect_peaks
#@nb.jit
def processBinFile(bin_file_size, raw_data):
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
def calliperAlg(signal_matrices):
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
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000;
    return distance

@nb.jit
def CalliperAndThicknessNoCoating(signal_matrices, coating, s, trLayout):
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
            envelopObject = interpolate.interp1d(peaks_locs, peaks_value, kind='slinear')
            xnew = np.linspace(peaks_locs[0], peaks_locs[-1], num=peaks_locs[-1] - peaks_locs[0] + 1)
            envelop = envelopObject(xnew)
            filtered_peaks_locs = detect_peaks(envelop, mph = None, mpd = 20, 
                                      show=False)        
            peak_diff = np.diff(filtered_peaks_locs)
            if (coating == False):
                if ( len(peak_diff) > 2 ):
                    thickness_map[chn,rd] = np.median(peak_diff)
                else:
                    thickness_map[chn,rd] = timeFlight / 3
    return  distance, thickness_map



@nb.jit
def processBinFileToDistanceMap(bin_file_size, raw_data):
    MAP_SIZE = (96, 520)
    distance = np.zeros(MAP_SIZE)
    ii = np.zeros((1,128), dtype=np.int)
    start_byte = 0
    START_DELAY = 6601;    
#    rp_i = 0
    for i in range(1, int(bin_file_size/32096) + 1):
        #raw_fire_time = raw_data[start_byte + 24:start_byte + 32]
#        roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
#        pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
#        if((roll_b != 8224) | (pitch_b != 8224)):
#            rp_i = rp_i + 1;
    
        for k in range(0, 8):
            raw_signal = raw_data[start_byte + k * 4008 + 40 : start_byte + k * 4008 + 4040].view('uint16')
            raw_signal = (raw_signal.astype("double")-32768)/32768
            #raw_signal = np.asmatrix(raw_signal)
            norm_signal = raw_signal/np.max(np.absolute(raw_signal))
            #raw_first_ref = raw_data[start_byte+k*4008+32:start_byte +k*4008+34]
            #first_ref = raw_first_ref.view('uint16')
            channel_index = raw_data[start_byte + k*4008 + 38].astype("int64")
            trigger = np.argmax(norm_signal > 0.594)
            if (trigger < 20) or (trigger > 1900):
                trigger = 20;
                #main_reflection = norm_signal[trigger - 20 : trigger + 280]
            distance[channel_index, ii[0,channel_index]] = (START_DELAY + trigger)*740.0/15000000;
            ii[0,channel_index] = ii[0,channel_index] + 1
        start_byte = start_byte +32096
    return distance



@nb.jit
def processBinFileToDistanceMap2(bin_file_size, raw_data):
    MAP_SIZE = (96, 520)
    distance = np.zeros(MAP_SIZE)
    ii = np.zeros((1,128), dtype=np.int)
    start_byte = 0
    START_DELAY = 6601;    
#    rp_i = 0
    for i in range(1, int(bin_file_size/32096) + 1):
        #raw_fire_time = raw_data[start_byte + 24:start_byte + 32]
#        roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
#        pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
#        if((roll_b != 8224) | (pitch_b != 8224)):
#            rp_i = rp_i + 1;
    
        for k in range(0, 8):
            raw_signal = raw_data[start_byte + k * 4008 + 40 : start_byte + k * 4008 + 4040].view('uint16')
            raw_signal = (raw_signal.astype("double")-32768)/32768
            #raw_signal = np.asmatrix(raw_signal)
            norm_signal = raw_signal/np.max(np.absolute(raw_signal))
            #raw_first_ref = raw_data[start_byte+k*4008+32:start_byte +k*4008+34]
            #first_ref = raw_first_ref.view('uint16')
            channel_index = raw_data[start_byte + k*4008 + 38].astype("int64")
            trigger = np.argmax(norm_signal > 0.594)
            if (trigger < 20) or (trigger > 1900):
                trigger = 20;
                #main_reflection = norm_signal[trigger - 20 : trigger + 280]
            distance[channel_index, ii[0,channel_index]] = (START_DELAY + trigger)*740.0/15000000;
            ii[0,channel_index] = ii[0,channel_index] + 1
        start_byte = start_byte +32096
    return distance