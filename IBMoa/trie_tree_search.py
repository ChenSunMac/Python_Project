# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:12:06 2017
Trie Tree Porblem: Trie is an efficient information reTrieval data structure.
Using Trie, we can search the key in O(M) time. However the penalty is on Trie storage requirements.
Example: 
                       root
                    /   \    \
                    t   a     b
                    |   |     |
                    h   n     y
                    |   |  \  |
                    e   s  y  e
                 /  |   |
                 i  r   w
                 |  |   |
                 r  e   e
                        |
                        r
@author: chens
"""
import sys

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()
    
    def addChild(self, key, data=None):
        # new character goes into the first branch
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word):
        current_node = self.head
        word_finished = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break
        
        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
        
        # Store the full word at the end node so we don't need to
        # travel back up the tree to reconstruct the word
        current_node.data = word
    
    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        
        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        
        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if current_node.data == None:
                exists = False
        
        return exists
    
    def start_with_prefix(self, prefix):
        """ Returns a list of all words in tree that start with prefix """
        words = list()
        if prefix == None:
            raise ValueError('Requires not-Null prefix')
        
        # Determine end-of-prefix node
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                # Prefix not in tree, go no further
                return words
        
        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.iteritems()]
        else:
            queue = [top_node]
        # Perform a Depth first search under the prefix
        # will return a list of words ordered by appearance?
        # need to check
        while queue:
            current_node = queue.pop(-1)
            if current_node.data!=None:
                words.append(current_node.data)
            queue = queue +  [node for key,node in current_node.children.iteritems()]
#        # Perform a breadth first search under the prefix
#        # A cool effect of using BFS as opposed to DFS is that BFS will return
#        # a list of words ordered by increasing length
#        while queue:
#            # pop in defaults pop the last element in the list
#            current_node = queue.pop()
#            if current_node.data != None:
#                # Isn't it nice to not have to go back up the tree?
#                words.append(current_node.data)
#            
#            queue = [node for key,node in current_node.children.iteritems()] + queue
        
        return words
    
    def getData(self, word):
        """ This returns the 'data' of the node identified by the given word """
        if not self.has_word(word):
            raise ValueError('{} not found in trie'.format(word))
        
        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]
        
        return current_node.data

if __name__ == '__main__':
    """ Example use """
    trie = Trie()
    words = 'hello goodbye help gerald gold tea ted team to too tom stan standard money'
    for word in words.split():
        trie.add(word)
    print "'goodbye' in trie: ", trie.has_word('goodbye')
    print trie.start_with_prefix('g')
    print trie.start_with_prefix('to')
    print trie.start_with_prefix('t')
    print trie.start_with_prefix('t')[0:3]
    
    PrintedOutput = ''
    trie = Trie()
    segmentlist = []
    for line in sys.stdin:
        segmentlist.append(line.strip())

    for item in segmentlist[:-2]:
        trie.add(item)

    resultfound = sorted((trie.start_with_prefix(segmentlist[-1])))[0:3]
    if resultfound:
        if len(resultfound) < 3:
            start = segmentlist[:-2].index(resultfound[0])
            PrintedOutput = "\n".join(segmentlist[start:-2])
        else:
                PrintedOutput = "\n".join(resultfound)
    else:
                    PrintedOutput = '<NONE>'

    print(PrintedOutput)