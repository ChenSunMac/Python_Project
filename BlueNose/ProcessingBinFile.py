#f = open('C:\Users\chens\Documents\gui-dev\SmallTempData\0.3_ft_Run2\bn170614-142902', 'r')
import os
test_path = "C:\\Users\\chens\\Documents\\gui-dev\\SmallTempData\\0.3_ft_Run2"
if os.path.exists(test_path):
    os.chdir(test_path)
currentPath = os.getcwd()
print(currentPath)

binFile = open("bn170614-142902.bin", "rb")
