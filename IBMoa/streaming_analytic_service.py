# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:38:33 2017
IBM OA - streaming analytic service for online retailor data anlytic
Each line of the input includes a string 'date,number,item'
The output would be 'data,totalNumberOfAllItems,average,NumberOfCategories'
Example Input:
    '2017-06-02,5,Apples\n2017-06-02,2,pears\n2017-06-03,3,pineapples'
Example Output:
    '2017-06-02,7,3.5,2\n2017-06-03,3,3.00,1'
Use Dict, split and so on
Note one can use round(float number, 2) to result a number less than 2 decimal digits
One can use print("%.2f" % float number) to get a exact 2 decimal digits form 
@author: chens
"""

test_input = '2017-06-02,5,Apples\n2017-06-02,2,pears\n2017-06-03,3,pineapples'
Data_map = dict()
segment_list = test_input.split('\n')
#segment_list = ['2017-06-02,5,Apples', '2017-06-02,2,pears', '2017-06-03,3,pineapples']
"""MAPPER PART"""
for line in segment_list:
    date_num_item = line.split(',')
    # if new Date, then create a instance in the dict.
    if date_num_item[0] not in Data_map:
        # construct the dict for the entry
        Data_map[date_num_item[0]] = {date_num_item[2].lower() : int(date_num_item[1])}
        # initialize the 'TOTAL_NUMBER' part for each new entry
        Data_map[date_num_item[0]]['TOTAL_NUMBER'] = 0
        Data_map[date_num_item[0]]['TOTAL_NUMBER'] += int(date_num_item[1])
        # initialize the 'ITEMS_NUMBER' part for each new entry
        Data_map[date_num_item[0]]['ITEMS_NUMBER'] = 1
    # if has such Date, then we need to insert the data in the dict
    else:
        # if item not exist
        if date_num_item[2].lower() not in Data_map[date_num_item[0]]:
            Data_map[date_num_item[0]][date_num_item[2].lower()] = int(date_num_item[1])
            Data_map[date_num_item[0]]['TOTAL_NUMBER'] += int(date_num_item[1])
            Data_map[date_num_item[0]]['ITEMS_NUMBER'] += 1
            # if item already exist
        else:
            Data_map[date_num_item[0]][date_num_item[2].lower()] += int(date_num_item[1])
            Data_map[date_num_item[0]]['TOTAL_NUMBER'] += int(date_num_item[1])
        
            
"""REDUCER PART"""

for key in sorted(Data_map.keys()):
    total_number = Data_map[key]['TOTAL_NUMBER']
    item_number = Data_map[key]['ITEMS_NUMBER']
    average = float(total_number)/float(item_number)
    print("%s,%d,%.2f,%d" % (key, total_number, average, item_number))



