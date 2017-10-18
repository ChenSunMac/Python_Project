# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:17:02 2017

@author: chens
"""

#Develop a service to help a client quickly find a manager who can resolve the conflict between two employees. When there is a conflict between two employees, the closest common manager should help resolve the conflict. The developers plan to test the service by providing an example reporting hierarchy to enable the identification of the closest common manager for two employees. Your goal is to develop an algorithm for IBM to efficiently perform this task. To keep things simple, they just use a single relationship "isManagerOf" between any two employees. For example, consider a reporting structure represented as a set of triples: 
#
#Tom isManagerOf Mary 
#Mary isManagerOf Bob 
#Mary isManagerOf Sam 
#Bob isManagerOf John 
#Sam isManagerOf Pete 
#Sam isManagerOf Katie 
#
#The manager who should resolve the conflict between Bob and Mary is Tom(Mary's manager). The manager who should resolve the conflict between Pete and Katie is Sam(both employees' manager). The manager who should resolve the conflict between Bob and Pete is Mary(Bob's manager and Pete's manager's manager). 
#
#Assumptions: 
#There will be at least one isManagerOf relationship. 
#There can be a maximum of 15 team member to a single manager 
#No cross management would exist i.e., a person can have only one manager 
#There can be a maximum of 100 levels of manager relationships in the corporation 
#
#Input: 
#R1,R2,R3,R4...Rn,Person1,Person2 R1...Rn - A comma separated list of "isManagerOf" relationships. Each relationship being represented by an arrow "Manager->Person". Person1,Person2 - The name of the two employee that have conflict 
#Output: 
#The name of the manager who can resolve the conflict Note: Please be prepared to provide a video follow-up response to describe your approach to this exercise. 
#
#Test 1: 
#Test Input 
#Frank->Mary,Mary->Sam,Mary->Bob,Sam->Katie,Sam->Pete,Bob->John,Bob,Katie 
#
#Expected Output 
#Mary 
#
#Test 2: 
#Test Input 
#Sam->Pete,Pete->Nancy,Sam->Katie,Mary->Bob,Frank->Mary,Mary->Sam,Bob->John,Sam,John 
#
#Expected Output 
#Mary
ip1="Sam->Pete,Pete->Nancy,Sam->Katie,Mary->Bob,Frank->Mary,Mary->Sam,Bob->John,Sam,John"
ip2="Frank->Mary,Mary->Sam,Mary->Bob,Sam->Katie,Sam->Pete,Bob->John,Bob,Katie"  
def conflict(conflict_1,conflict_2,book):
    # if conflict2 is the manager of conflict 1
    if(book.get(conflict_1)== conflict_2):
       return conflict_2
    # if conflict1 is the manager of conflict 2
    if(book.get(conflict_2)== conflict_1):
       return conflict_1
   # if conflict1 is boss
    if(book.get(conflict_1)== None):
       return conflict_1
   # if conflict2 is boss
    if(book.get(conflict_2)== None):
       return conflict_2   
   # if they have the same manager
    if(book.get(conflict_1)== book.get(conflict_2)):
       return book[conflict_1]
    else:
        # reversively goes up to check their manager who is the boss
       return conflict(book[conflict_1],book[conflict_2],book)
def main(ip1):
    sets=ip1.split(',')
    l=len(sets)
    conflict_1=sets[l-2]
    conflict_2=sets[l-1]
    i=0 
    book={}
    for i in range(l-2):
      [temp1,temp2]=sets[i].split('->')
      book[temp2]=temp1
    manager=conflict(conflict_1,conflict_2,book)
    print(manager)
   
  
main(ip1)
main(ip2)