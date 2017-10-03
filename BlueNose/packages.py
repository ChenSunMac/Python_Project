# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 15:04:40 2017

@author: chens
"""
from scipy.interpolate import interp1d

def findEnvelopeUsingDiff(signal):
    """
    Generate a envelope for input signal based on diff
    
    keyword arguments:
    signal -- input 1-D array
    """
    d = np.diff(signal)
    n = d.size
    d1 = d[0 : n - 1]
    d2 = d[1 : n]
    t = np.linspace(1, n, n)
    indmax = np.where((d1*d2 <= 0) & (d1  > 0))
    envTop =  interp1d  (t[indmax], signal[indmax], kinid = 'slinear')
    