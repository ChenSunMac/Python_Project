#!/usr/bin/env python

'''
$ ./info.py < devices.lst

read file contains a list of domains names of DSLAMs and output the stinger info
'''
import sys

from automgmt import *

def proc_info(data,t):
    dd = {'device' : t.stinger}
    for line in data:
        if re.search(':', line):
            key,value = line.split(':')
            dd[key.strip().lower()] = value.strip()
    return dd

if __name__=='__main__':

    info = []

    # read standard input
    for stinger in sys.stdin.readlines():

        # initiate Telnet session to DSLAM
        try:
            t = stcon(stinger.strip('\n'))
        except TelnetError, e:
            # if there's an error, report and
            # try next DSLAM
            print "%s: %s" % (stinger, e.args)
            continue

        # issue "info" command, store each
        # line of output in a list of lists
        info.append(t.do_cmd("info"))
        t.close()

    for dslam in info:
        for line in dslam:
            print line