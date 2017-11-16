# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:22:50 2017
Stack and String
- Valid Parentheses

- 

@author: Chens
"""


"""
Valid Parentheses
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid.
The brackets must close in the correct order, "()" and "()[]{}" are all valid 
but "(]" and "([)]" are not.

读到左括号压栈，读到右括号判断栈顶是否匹配
匹配则出栈，不匹配则return False
"""
def ValidParentheses(string):
    """
    @param : {string} string
    
    @return: {Boolean} whether the string is valid
    """    
    stack = []
    for ch in string:
        # 左括号入栈
        if ch in "([{":
            stack.append(ch)
        # 右括号检测：
        if ch in ")]}":
            # 如果当前栈内没有左括号匹配 肯定False
            if not stack:
                return False
            else:
                # 出栈 match， match 不上就是False
                top = stack.pop()
                if ch == ']' and top != '[' or ch == ')' and top != '(' or ch == '}' and top != '{':
                    return False          
    # 全loop了一遍，没有问题 此时栈内应该为空
    return not stack

s = "(asda){fas}[as(fa)fas]"
print ValidParentheses(s)