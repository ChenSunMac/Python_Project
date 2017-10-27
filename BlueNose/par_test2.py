# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:37:26 2017

@author: chens
"""

def foo(bar, baz):
  print ('hello {0}'.format(bar))
  return 'foo' + baz

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)

async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo

# do some other stuff in the main process

return_val = async_result.get() 