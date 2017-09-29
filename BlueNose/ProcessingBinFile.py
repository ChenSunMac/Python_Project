#f = open('C:\Users\chens\Documents\gui-dev\SmallTempData\0.3_ft_Run2\bn170614-142902', 'r')
import numpy as np
import os

test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
file_name = "bn170614-142902.bin"
if os.path.exists(test_path):
    os.chdir(test_path)
currentPath = os.getcwd()
print(currentPath)

binFile = open(file_name, "rb")
statinfo = os.stat(file_name)
print(statinfo)

#for byte in binFile:
#    print(byte)

data = np.arange(100, dtype=np.int)
data.tofile("temp")  # save the data

f = open("temp", "rb")  # reopen the file
f.seek(256, os.SEEK_SET)  # seek

x = np.fromfile(f, dtype=np.int)  # read the data into numpy
print ("x")