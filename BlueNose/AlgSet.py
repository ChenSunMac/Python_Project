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
from numba import jit

def processBinFile(bin_file_size, raw_data):
    MATRICES_SIZE = (96, 520, 2000)
    ii = np.zeros((1,128), dtype=np.int)
    start_byte = 0
    rp_i = 0
    signal_matrices = np.zeros(MATRICES_SIZE)
    for i in xrange(1, bin_file_size/32096 + 1):
        raw_fire_time = raw_data[start_byte + 24:start_byte + 32]
        roll_b = raw_data[start_byte + 16:start_byte + 18].view('int16')
        pitch_b = raw_data[start_byte + 18:start_byte + 20].view('int16')
        if((roll_b != 8224) | (pitch_b != 8224)):
            rp_i = rp_i + 1;
    
        for k in xrange(0, 8):
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
    return signal_matrices

### calliper Algorithm using 60% of incline
# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@jit
def calliperAlg(signal_matrices):
    MAP_SIZE = (96, 520)
    distance = np.zeros(MAP_SIZE)
    START_DELAY = 6601;
    TOTAL_CHN, TOTAL_ROUND, SIGNAL_LENGTH = signal_matrices.shape
    for chn in xrange(TOTAL_CHN):
        for rd in xrange(TOTAL_ROUND):
            signal = signal_matrices[chn, rd, :]
            norm_signal = signal/np.max(np.absolute(signal))
            for time_point in xrange(SIGNAL_LENGTH):
                # OPTION 1 - incline on 0.6 of norm signal
                if np.absolute(norm_signal[time_point]) > 0.594 :
                    if (time_point > 20) and (time_point < 1900):
                        trigger = time_point;
                        #main_reflection = norm_signal[trigger - 20 : trigger + 280]
                        break
                    else:
                        trigger = 0;
                        #main_reflection = norm_signal[trigger - 20 : trigger + 280]
                        break
            distance[chn,rd] = (START_DELAY + trigger)*740.0/15000000;
    return distance