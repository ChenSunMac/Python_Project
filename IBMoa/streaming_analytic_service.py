# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:38:33 2017
IBM OA - streaming analytic service for online retailor data anlytic
Each line of the input includes a string 'date,number,item'
The output would be 'data,totalNumberOfAllItems,average,NumberOfCategories'
Example Input:
    '2017-06-02,5,Apples\n2017-06-02,2,pears,2017-06-03,3,pineapples'
Example Output:
    '2017-06-02,7,3.5,2\n2017-06-03,3,3.00,1'
Use Dict, split and so on
Note one can use round(float number, 2) to result a number less than 2 decimal digits
One can use print("%.2f" % float number) to get a exact 2 decimal digits form 
@author: chens
"""

