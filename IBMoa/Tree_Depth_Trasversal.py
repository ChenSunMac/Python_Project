# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:22:50 2017
Tree Type Questions
- Min Depth 
- Max Depth

- Traversal: (order depends on whether root node is pre, in or post)
    pre-oder
    in-oder
    post-oder

    DFS
    BFS

@author: Chens
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
#------------------------------------------------------------------------------
def preOrderTraverseRecur(root):
    """
    @param : {Node} root
    
    @return: Preorder in ArrayList which contains node values.
    """    
    results = []
    traverse(root, results)
    return results
    
def traverse(root, results):
    """
    @param : {Node} root
    @param : {[]} result   

    @return: None
    - Helper function for Recursive Traverse functions 
        (Toggle sequence to implement pre, in and post order traverse)
    """    
    if root is None:
        return
    results.append(root.data)
    traverse(root.left, results)
    traverse(root.right, results)

def preOrderTraversal(root):
    if root is None:
        return []
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result
    
#------------------------------------------------------------------------------

def inOrderTraverseStrack(root):
    """
    @param: {Node} root
    
    @return: {[data]} list of node values 
        Use Iterative method
    """    
    p = root
    stack = []
    results = []
    if root is None:
        return results
    while stack or p:
        while p:
            stack.append(p)
            p = p.left
        p = stack.pop()
        results.append(p.data)
        p = p.right
    return results

#------------------------------------------------------------------------------
def dfs(root):
    """
    @param: {Node} root
    
    @return: {[data]} list of node values 
        Use Iterative method(STACK) to Deep First Trasversal the tree    
    """
    if root is None:
        return []
    visited, stack = [], [root]
    while stack:
        node = stack.pop()
        visited.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
        return visited
    
def bfs(root):
    """
    @param: {Node} root
    
    @return: {[data]} list of node values 
        Use Iterative method(QUEUE)  to Breadth First Traversal the tree    
    """
    if root is None:
        return []
    visited, queue = [], [root]
    while queue:
        node = queue.pop(0)
        visited.append(node)
        if node.left:
            queue.append(node.left)        
        if node.right:
            queue.append(node.right)
        return visited

#------------------------------------------------------------------------------
#　　　　　　　　　　　　　　　　1
#
#　　　　　　　　　　　　　　　/　  \
#
#　　　　　　　　　　　　　　 2       3
#
#　　　　　　　　　　　　　 /    \    /   \
#
#　　　　　　　　　　　　　4     5  6      7        
# Return list of list 
#       ordered by level(pre-order with level):
#            breadth dirst traverse
#       zig zag order (reverse at every odd level):          
#           breadth dirst traverse + flag to reverse list

def LevelOrder(root):
    """
    @param: {Node} root
    
    @return: {[data]} list of node values 
        Use Iterative method(QUEUE)  to Breadth First Trasversal the tree    
    """
    if root is None:
        return []
    res, temp, queue = [], [], [root]
    while queue:
        for i in range(len(queue)):
            node = queue.pop(0)
            temp += [node.data]
            if node.left:
                queue += [node.left]
            if node.right:
                queue += [node.right]
        res += [temp[::]]
        temp = []
    return res


def zigzagLevelOrder(root):
    if root is None:
        return []
    res, temp, queue, flag = [], [], [root], 1
    while queue:
        for i in range(len(queue)):
            node = queue.pop(0)
            temp += [node.data]
            if node.left:
                queue += [node.left]
            if node.right:
                queue += [node.right]
        res += [temp[::flag]]
        temp = []
        flag* = -1
    return res 


#------------------------------------------------------------------------------
def minDepthRecursive(root):
    """
    @param: {Node} root
    
    @return: {int} minDepth 
        Use Recursive method to search leaf node level by level
    """
    if root is None:
        return 0
    
    # found the leaf, this is it
    if root.left == None and root.right == None:
        return 1
    
    # in order to find the leaf
    if root.left == None:
        return minDepthRecursive(root.right) + 1
    
    # in order to find the leaf
    if root.right == None:
        return minDepthRecursive(root.left) + 1
    
    return min(minDepthRecursive(root.left), minDepthRecursive(root.right)) + 1

def minDepthQueue(root):
    """
    @param: {Node} root
    
    @return: {int} minDepth 
        Use Level Order Traversal and Queue to search for the leaf with min Depth
    """
    if root is None:
        return 0
    
    queue = []
    queue.append({'node' : root, 'depth' : 1})
    
    while (len(queue) > 0):
        queueItem = queue.pop(0)
        # Get details of the removed item
        node = queueItem['node']
        depth = queueItem['depth']        

        # If this is the first leaf node seen so far
        # then return its depth as answer
        if node.left is None and node.right is None:    
            return depth
        # If left subtree is not None, add it to queue
        if node.left is not None:
            queue.append({'node' : node.left , 'depth' : depth+1})
 
        # if right subtree is not None, add it to queue
        if node.right is not None:  
            queue.append({'node': node.right , 'depth' : depth+1})


def maxDepthRecur(root):
    """
    @param: {Node} root
    
    @return: {int} maxDepth 
        Use Recursive method to search the maximum depth
    """
    if root is None:
        return 0
    return max(maxDepthRecur(root.left), maxDepthRecur(root.right)) + 1
    

def maxDepthStack(root):
    """
    @param: {Node} root
    
    @return: {int} maxDepth 
        Use Stack instead of recursion
    """    
    if root == None:
        return 0
    
    stack = []
    stack.append({"node" : root, "depth" : 0})
    maxDepth = 0
    while (len(stack) > 0):
        stackItem = stack.pop()
        # Get details of the removed item
        node = stackItem["node"]
        
        depth = stackItem["depth"]            
        maxDepth = maxDepth if maxDepth > depth else depth
        if node is None:
            return depth
        
        if node.left is not None:
            stack.append({'node' : node.left , 'depth' : depth+1})
        
        if node.right is not None:
            stack.append({'node' : node.right , 'depth' : depth+1})

    return maxDepth + 1
    
# Driver Program 
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
print minDepthRecursive(root)
print minDepthQueue(root)
print maxDepthRecur(root)
print maxDepthStack(root)

print inOrderTraverseStrack(root)

results = []
print preOrderTraverseRecur(root)