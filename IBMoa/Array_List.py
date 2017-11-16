# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:22:50 2017
Array and List

- Kth Smallest and Largest element in an array

@author: Chens
"""
from heapq import heappush, heappop


"""
Kth largest(or smallest) elements in an array
"""

def  kthSmallest(k, nums):
    """
    @param: {int/float}, k
    @param: {[int/float]}, nums
    
    @return: {int/float} kth smallest element
    """    
    min_heap = []
    # Construct a min_heap for the inputs O(n)
    for num in nums:
        heappush(min_heap, num)
    # Perform Extract k times 
    for i in xrange(k):
        result = heappop(min_heap)
    return result

def kthSmallestQuickSelect(k, nums):
    """
    @param: {int/float}, k
    @param: {[int/float]}, nums
    
    @return: {int/float} kth smallest element
    """        
    return quickSelect(nums, 0, len(nums)-1, k-1)

def quickSelect(nums, start, end, k):
    if start == end:
            return nums[start]
    left, right = start, end
    pivot = nums[(left + right) / 2]
    while left <= right:
        while left <= right and nums[left] < pivot:
            left += 1
        while left <= right and nums[right] > pivot:
            right -= 1
        if left <= right:
            temp = nums[left]
            nums[right] = temp
            left += 1
            right -= 1
        if right >= k and start <= right:
            return quickSelect(nums, start, right, k)
        elif left <= k and end >= left:
            return quickSelect(nums, left, end, k)
        else:
            return nums[k]
    

nums = [2,3,4,6,8,9,12,34,5,65,234,1,2,4]
print kthSmallest(2, nums)

print kthSmallestQuickSelect(0, nums)