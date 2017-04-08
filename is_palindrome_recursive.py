# check if is palindrome using a recursive way 
# and nonrecersive way

def is_palindrome(s):
    if s == '':
        return True
    else:
        if s[0] == s[-1]:
            return is_palindrome(s[1:-1])
        else:
            return False
        
        
def iter_palindrome(s):
    for i in range( 0, len(s) / 2 ):
        if s[ i ] != s[ - ( i + 1 ) ]:
            return False
        return True
    
def fibonacci(n):
    current = 0
    after = 1
    for i in range(0,n):
        current, after = after, current + after
    return current