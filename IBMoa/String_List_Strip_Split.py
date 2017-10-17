# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:08:36 2017
String and list Split and Strip Examples
@author: chens
"""



string = "blah, lots  ,  of ,  spaces, here "

""" STRING -> LIST """
# split the string based on comma and strip all the white space store in List
StringResult0 = [x.strip() for x in string.split(',')]




print(StringResult0)


""" LIST -> STRING """

listresult0 = ','.join(StringResult0)
print(listresult0)