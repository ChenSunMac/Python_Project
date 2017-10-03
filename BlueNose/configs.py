# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 13:50:07 2017
config parameters

@author: chens
"""
import numpy as np

import time

start = time.time()


SIGNAL_END = 1400

reference_input = np.array([-0.0729,   -0.2975,   -0.2346,    0.1057,    0.8121,    0.5721,   -0.4512,   -0.7820,   -0.5137,     0.4829 ,   0.8867  , -0.0891  , -0.4474   ,-0.0875  ,  0.2159]);
t = np.linspace(1, 315, 315); 


print 'It took', time.time()-start, 'seconds to config.'
    
