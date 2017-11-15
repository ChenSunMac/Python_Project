# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:08:36 2017
String and list Split and Strip Examples
@author: chens
"""
import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print '%s\t%s' % (word, 1)


string = "blah, lots  ,  of ,  spaces, here "

""" STRING -> LIST """
# split the string based on comma and strip all the white space store in List
StringResult0 = [x.strip() for x in string.split(',')]


print(StringResult0)


""" LIST -> STRING """

listresult0 = ','.join(StringResult0)
print(listresult0)