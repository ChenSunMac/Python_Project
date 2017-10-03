# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 11:08:09 2017

@author: chens
"""
import sys
sys.path.append('C:\\Users\\chens\\Documents\\GitHub\\Python_Project\\BlueNose') 
import ProcessingBinFile
import configs
import matplotlib.pyplot as plt

configs

ProcessingBinFile

for chn in range(0, 96):
    
    for i in range(0, round_per_read):
        signal = signal_matrices[chn,i,0 : SIGNAL_END]
        signal = signal/(max(abs(signal)))
        for j in range (0, SIGNAL_END):
            if (j > 20) & ( j < (SIGNAL_END - 280) ):
                trigger = j - 20
                main_reflection = signal[ trigger : trigger + 300]
                break
            else:
                main_reflection = signal[0 : 300]
                break
        C = abs(np.convolve( main_reflection, reference_input ))
    

x = np.linspace(1, 2000, 2000)
y = signal_matrices[1,1,:]
#z = np.cos(x**2)
start = time.time()
plt.figure(figsize=(8,4))
plt.plot(x,y,label="$sin(x)$",color="blue",linewidth=2)

plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(-1,1)
plt.legend()
plt.show()
print 'It took', time.time()-start, 'seconds for figure showing'