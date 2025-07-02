def ____main_____(func, *args, **kwargs):
    '''Write a function to write Fibonacci numbers'''
    print(func(*args, **kwargs))

def fib(n):
    '''Write a function to compute Fibonacci numbers'''
    if n <= 1:
        return n

    # Write your code here
    return(fib(n-1)+fib(n-2))

if __name__ == '__main__':
    print(fib(100))
