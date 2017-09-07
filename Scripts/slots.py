#!/usr/bin/env python


'''
$ ./slots.py <devices.lst

 reports information on the hardware in a particular slot in the DSLAM chassis
'''
import sys
from automgmt import *



# return a list of slot ids
def get_slots(data):
    slots = []
    for line in data:
       if re.compile("shelf").search(line):
           slot = line.split("}")[0] + " }"
           slots.append(slot)
    return slots

if __name__=='__main__':

    for stinger in sys.stdin.readlines():

        try:
            t = stcon(stinger.strip('\n'))
        except TelnetError, e:
            print "%s: %s" % (stinger, e.args)
            continue

        # get slots in chassis, populated
        # with cards, store as list
        output = t.do_cmd("show")
        slots = get_slots(output)

        # get info of each populated card slot
        for s in slots:
            slot_info = t.do_cmd("get slot-info " + s)
            for i in slot_info:
                print i

        t.close()