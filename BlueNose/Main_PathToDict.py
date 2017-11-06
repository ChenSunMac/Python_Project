# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:06:46 2017

Main Test Bench for parsing through a PATH
and RETURN a DICT(MAP) for the file list

INPUT: PATH -string
OUTPUT: DICT of list
    key: FILENAME_HOUR_MIN
    value: a LIST of files in this minute
    
>>>  test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
>>>  file_map = {
'bn170614-1429': ['bn170614-142902.bin',
                  'bn170614-142908.bin',
                  'bn170614-142913.bin',
                  'bn170614-142919.bin',
                  'bn170614-142924.bin',
                  'bn170614-142929.bin',
                  'bn170614-142935.bin',
                  'bn170614-142940.bin',
                  'bn170614-142946.bin',
                  'bn170614-142951.bin',
                  'bn170614-142956.bin',
                  'bn170614-143002.bin'],
'bn170614-1430': ['bn170614-143002.bin',
                  'bn170614-143002.bin',
                  'bn170614-143007.bin',
                  'bn170614-143013.bin',
                  'bn170614-143018.bin',
                  'bn170614-143023.bin',
                  'bn170614-143029.bin',
                  'bn170614-143034.bin',
                  'bn170614-143040.bin']}

@author: chens
"""


import os
import sys

import glob

if __name__ == "__main__":
    print(sys.version)
    test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
    
    if os.path.exists(test_path):
        os.chdir(test_path)
        currentPath = os.getcwd()
        print(currentPath)
    
    ## Filter .bin file and sort based on name
    file_list =  glob.glob('*.bin')
    file_list.sort()
    first_min = file_list[0][9:13]
    last_min = file_list[-1][9:13]
        
    total_files = len(file_list)
    
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
